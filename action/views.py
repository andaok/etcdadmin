#-*- coding: utf-8 -*-

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from etcdadmin.settings import ETCDCLUSTER_PREFIX, ETCDCLUSTER_STATE
from .models import EtcdCluster
from .forms import EtcdClusterForm
from utils.parse_tools import parseURL

import etcd
import json
import requests

#from operator import itemgetter

#eClient = etcd.Client(host="192.168.56.2", port=4001, protocol="http", allow_reconnect=True)

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

def add_etcd_cluster(request):

    form = EtcdClusterForm()
    if request.method == "POST":
        form = EtcdClusterForm(request.POST)
        if form.is_valid():
            ec = form.save(commit=False)
            print(request.POST['ec_name'])
            ec.name = request.POST['ec_name']
            ec.prefix = request.POST['ec_prefix']
            ec.endpoint = request.POST['ec_endpoint']
            print(ec)
            parseURL(ec.endpoint)
            ec.save()
            return HttpResponseRedirect('/')
    else:
        print("something is wrong.")
        form = EtcdClusterForm()

    return render(request, 'add_ec.html', locals())

def get_dir(request, ecsn=None):

    dirs = None
    try:
        ec = EtcdCluster.objects.get(serial_number=ecsn)
        ec_endpoint = parseURL(ec.cluster_endpoint)
        eClient = etcd.Client(host=ec_endpoint['host'], port=ec_endpoint['port'], protocol=ec_endpoint['scheme'], allow_reconnect=True)
        dirs = eClient.read(str(ETCDCLUSTER_PREFIX), recursive=True, sorted=True)
#           for child in r.children:
#           print(child.key, child.value)
    except EtcdCluster.DoesNotExist:
        print("etcd cluster is not found.")

    return render(request, 'get_dir.html', locals())


def set_key(request, key=None, value=None):

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
        ec = EtcdCluster.objects.get(cluster_endpoint=ecsn)
        ec_endpoint = parseURL(ec.cluster_endpoint)
        eClient = etcd.Client(host=ec_endpoint['host'], port=ec_endpoint['port'], protocol=ec_endpoint['scheme'], allow_reconnect=True)
        key = request.GET.get('key')
        try:
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
        print("etcd cluster is not found.")

    return HttpResponseRedirect(reverse('action:getdir'))
