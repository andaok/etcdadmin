#-*- coding: utf-8 -*-

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from etcdadmin.settings import ETCDCLUSTER_PREFIX, ETCDCLUSTER_STATE
from .models import EtcdCluster
from .forms import EtcdClusterForm
from utils.parse_tools import parseURL

import etcd
import json
import requests
import logging


logger = logging.getLogger(__name__)


def log_event(app, msg, level=logging.INFO):
    # controller needs to know which app this log comes from
    logger.log(level, "{}: {}".format(app.id, msg))
    app.log(msg, level)
    

def home(request):

    try:
        ecs = EtcdCluster.objects.all()
    except EtcdCluster.DoesNotExist:
        ecs = None

    return render_to_response(
        'home.html', {
            "ecs": ecs
        },
        context_instance=RequestContext(request)
    )


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
            print(ec)
            parseURL(ec.endpoint)
            ec.save()
            return HttpResponseRedirect('/')
    else:
        print("something is wrong.")
        form = EtcdClusterForm()

    return render(request, 'add_ec.html', locals())


def del_ec(request):
    
    try:
        ecsn = request.GET.get('ecsn')
        EtcdCluster.objects.filter(serial_number=ecsn).delete()
    except EtcdCluster.DoesNotExist:
        print("etcd cluster is not found.")
    
    return HttpResponseRedirect(reverse('home'))


def get_dir(request, ecsn=None):

    dirs = None
    
    try:
        ec = EtcdCluster.objects.get(serial_number=ecsn)
        ec_endpoint = parseURL(ec.cluster_endpoint)
        eClient = etcd.Client(host=ec_endpoint['host'], port=ec_endpoint['port'], protocol=ec_endpoint['scheme'], allow_reconnect=True)
        dirs = eClient.read(str(ETCDCLUSTER_PREFIX), recursive=True, sorted=True)
#         print(objs)
#         paginator = Paginator(objs.children, 25) # Show 25 contacts per page
#         
#         page = request.GET.get('page')
#         try:
#             dirs = paginator.page(page)
#         except PageNotAnInteger:
#             dirs = paginator.page(1)
#         except EmptyPage:
#             dirs = paginator.page(paginator.num_pages)
        
    except EtcdCluster.DoesNotExist:
        print("etcd cluster is not found.")

    return render(request, 'get_dir.html', locals())


def set_key(request, ecsn=None):

    # try:
    #     eClient.write(str(key), str(value))
    # except etcd.EtcdKeyNotFound:
    #     print("key or value could not be none.")

    return render_to_response(
        'set_key.html',
        context_instance=RequestContext(request)
    )


def update_key(request, ecsn=None):
    
    try:
        ec = EtcdCluster.objects.get(cluster_endpoint=ecsn)
        ec_endpoint = parseURL(ec.cluster_endpoint)
        eClient = etcd.Client(host=ec_endpoint['host'], port=ec_endpoint['port'], protocol=ec_endpoint['scheme'], allow_reconnect=True)
        key = request.GET.get('key')
        value = request.GET.get('value')
        try:
            eClient.update(key, value)
        except etcd.EtcdException:
            print("etcd key update error.")
    
    except EtcdCluster.DoesNotExist:
        print("etcd cluster is not found.")
        
    return render_to_response(
        'update_key.html',
        context_instance=RequestContext(request)
    )


def delete_key(request, ecsn=None):

    try:
        print("ec sn is: %s " % ecsn)
        ec = EtcdCluster.objects.get(serial_number=ecsn)
        ec_endpoint = parseURL(ec.cluster_endpoint)
        eClient = etcd.Client(host=ec_endpoint['host'], port=ec_endpoint['port'], protocol=ec_endpoint['scheme'], allow_reconnect=True)
        
        try:
            key = request.GET.get('key')
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

    return HttpResponseRedirect(reverse('getdir', kwargs={'ecsn': ecsn}))
