#-*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from etcdadmin.settings import (
    ETCDCLUSTER_STATE, 
    ETCDCLUSTER_HEALTH, 
    ETCDCLUSTER_VERSION_PREFIX
)
from .models import EtcdCluster
from .forms import EtcdClusterForm, KeyForm
from utils.parse import parseURL

import etcd
from etcd import EtcdKeyNotFound, EtcdException, EtcdNotFile, EtcdKeyError
import json
import requests
import logging
import uuid

logger = logging.getLogger(__name__)


def log_event(app, msg, level=logging.INFO):
    # controller needs to know which app this log comes from
    logger.log(level, "{}: {}".format(app.id, msg))
    app.log(msg, level)
     

@login_required
def ecs_list(request):

    try:
        ecs = EtcdCluster.objects.all()
        print(ecs.count())
        paginator = Paginator(ecs, 12) # Show 12 contacts per page
           
        page = request.GET.get('page')
        try:
            ecs = paginator.page(page)
        except PageNotAnInteger:
            ecs = paginator.page(1)
        except EmptyPage:
            ecs = paginator.page(paginator.num_pages)

    except EtcdCluster.DoesNotExist:
        ecs = None

    return render(request, 'ecs_list.html', {"ecs": ecs})


@login_required
def ec_status(request, ecsn=None):
    
    try:
        ec = EtcdCluster.objects.get(serial_number=ecsn)
        API_URL = ec.cluster_endpoint + ETCDCLUSTER_STATE
        
        try:
            req = requests.get(API_URL, verify=False)
            content = json.loads(req.content.decode('utf8'))
 
        except requests.exceptions.ConnectionError as ex:
            print("ERROR talking to etcd API: %s" % ex.message)

    except EtcdCluster.DoesNotExist:
        print("etcd cluster is not found.")
        
    return render(request, 'ec_status.html', locals())


@login_required
def add_ec(request):

    form = EtcdClusterForm()
    if request.method == "POST":
        form = EtcdClusterForm(request.POST)
        if form.is_valid():
            ec = form.save(commit=False)
            print(request.POST['name'])
            ec.name = request.POST['name']
            ec.prefix = request.POST['cluster_prefix']
            ec.endpoint = request.POST['cluster_endpoint']
            ec.serial_number = uuid.uuid4()
            ec.save()
            return HttpResponseRedirect(reverse('ecs_list'))
    else:
        print("something is wrong.")
        form = EtcdClusterForm()

    return render(request, 'add_ec.html', locals())


@login_required
def update_ec(request):
    ecsn = request.GET.get('ecsn')
    ec = get_object_or_404(EtcdCluster, serial_number=ecsn)
    print(ec.id)
    if request.method == "POST":
        form = EtcdClusterForm(request.POST.copy(), instance=ec)
        if form.is_valid():
            ec = form.save(commit=False)
            print(request.POST['name'])
            ec.name = request.POST['name']
            ec.prefix = request.POST['cluster_prefix']
            ec.endpoint = request.POST['cluster_endpoint']
            ec.save()
            return HttpResponseRedirect(reverse('ecs_list'))
    else:
        print("something is wrong.")
        form = EtcdClusterForm(instance=ec)

    return render(request, 'update_ec.html', locals())


@login_required
def delete_ec(request):
    
    try:
        ecsn = request.GET.get('ecsn')
        EtcdCluster.objects.filter(serial_number=ecsn).delete()
    except EtcdCluster.DoesNotExist:
        print("etcd cluster is not found.")
    
    return HttpResponseRedirect(reverse('ecs_list'))


@login_required
def check_ec(request):
    
    try:
        ecsn = request.GET.get('ecsn')
        ec = EtcdCluster.objects.get(serial_number=ecsn)
        API_URL = ec.cluster_endpoint + ETCDCLUSTER_HEALTH
        API_URL2 = ec.cluster_endpoint + ETCDCLUSTER_HEALTH
        try:
            req = requests.get(API_URL, verify=False, allow_redirects=True, timeout=5)
            content = json.loads(req.content.decode('utf8'))
            print(content['health'])
            
            if content['health'] == "true":
                EtcdCluster.objects.filter(serial_number=ecsn).update(status=1)
            else:
                print("error...")
        except requests.exceptions.ConnectionError as e:
            print(ecsn)
            EtcdCluster.objects.filter(serial_number=ecsn).update(status=2)
            print("ERROR: %s" % e)
            return HttpResponseRedirect(reverse('ecs_list'))
            
    except EtcdCluster.DoesNotExist:
        print("etcd cluster is not found.")
    
    return HttpResponseRedirect(reverse('ecs_list'))

@login_required
def get_dir(request, ecsn=None):

    dirs = None
    
    try:
        ec = EtcdCluster.objects.get(serial_number=ecsn)
        ec_endpoint = parseURL(ec.cluster_endpoint)
        try:
            eClient = etcd.Client(
                host=ec_endpoint['host'], 
                port=ec_endpoint['port'], 
                protocol=ec_endpoint['scheme'], 
                allow_reconnect=True
            )
            dirs = eClient.read(str(ec.cluster_prefix), recursive=True, sorted=True)
        except EtcdException as e:
            messages.add_message(
                request, 
                messages.ERROR, 
                "Could not get the list of servers, maybe you provided the wrong endpoint(%s) to connect to?" % ec.cluster_endpoint
            )
            return HttpResponseRedirect(reverse('ecs_list'))
    except EtcdCluster.DoesNotExist:
        print("etcd cluster is not found.")

    return render(request, 'get_dir.html', locals())


@login_required
def set_key(request, ecsn=None):

    try:
        ec = get_object_or_404(EtcdCluster, serial_number=ecsn)
        ec_endpoint = parseURL(ec.cluster_endpoint)
        eClient = etcd.Client(
            host=ec_endpoint['host'], 
            port=ec_endpoint['port'], 
            protocol=ec_endpoint['scheme'], 
            allow_reconnect=True
        )
        form = KeyForm()
        if request.method == "POST":
            form = KeyForm(request.POST)
            if form.is_valid():
                form.key_path = request.POST['key_path']
                form.value = request.POST['value']
                form.ttl = request.POST['ttl']
                form.is_dir = request.POST.get('is_dir', False)
                
                try:
                    if form.is_dir:
                        print(form.key_path)
                        eClient.write(str(form.key_path), None, ttl=form.ttl, dir=True)
                    elif form.ttl:
                        print(form.ttl)
                        eClient.write(str(form.key_path), str(form.value), ttl=form.ttl)
                    else:
                        print(form.key_path)
                        eClient.write(str(form.key_path), str(form.value))
                except EtcdException as e:
                    print("key or value could not be none.")
                return HttpResponseRedirect(reverse('get_dir', kwargs={'ecsn': ecsn}))
        else:
            print("something is wrong.")
            form = KeyForm()
            
    except EtcdCluster.DoesNotExist:
        print("etcd cluster is not found.")
        form = KeyForm()

    return render(request, 'set_key.html', locals())


@login_required
def update_key(request, ecsn=None):

    try:
        print(ecsn)
        ec = EtcdCluster.objects.get(serial_number=ecsn)
        ec_endpoint = parseURL(ec.cluster_endpoint)
        print(ec_endpoint)
        eClient = etcd.Client(
            host=ec_endpoint['host'], 
            port=ec_endpoint['port'], 
            protocol=ec_endpoint['scheme'], 
            allow_reconnect=True
        )
        key = request.GET.get('key')
        value = request.GET.get('value')
        try:
            eClient.update(key, value)
        except etcd.EtcdException:
            print("etcd key update error.")
    
    except EtcdCluster.DoesNotExist:
        print("etcd cluster is not found.")
        
    return render(request, 'update_key.html', locals())


@login_required
def delete_key(request, ecsn=None):

    try:
        print("ec sn is: %s " % ecsn)
        ec = EtcdCluster.objects.get(serial_number=ecsn)
        ec_endpoint = parseURL(ec.cluster_endpoint)
        eClient = etcd.Client(
            host=ec_endpoint['host'], 
            port=ec_endpoint['port'], 
            protocol=ec_endpoint['scheme'], 
            allow_reconnect=True
        )
        
        try:
            key = request.GET.get('key')
            print(key)
            eClient.delete(key, dir=True)
            print("dir(%s) has deleted" % key)
            messages.add_message(request, messages.INFO, ("dir(%s) has deleted" % key))
        except etcd.EtcdKeyNotFound:
            if eClient.read(key).dir:
                print("dir(%s) is not empty" % key)
                messages.add_message(request, messages.ERROR, ("dir(%s) is not empty" % key))
            else:
                print("dir(%s) not found" % key)

    except EtcdCluster.DoesNotExist:
        print("etcd cluster is not online.")

    return HttpResponseRedirect(reverse('get_dir', kwargs={'ecsn': ecsn}))


@login_required
def lock_key(request, ecsn=None):
    return  HttpResponseRedirect(reverse('get_dir', kwargs={'ecsn': ecsn}))