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
from urllib.request import urlopen
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
            etcd_ping = 0

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

    return render(request, 'addetcdcluster.html', locals())

def get_dir(request, ecsn=None):

    dirs = None
    try:
        ec = EtcdCluster.objects.get(serial_number=ecsn)
        print(ec.name)
        ec_endpoint = parseURL(ec.cluster_endpoint)
        eClient = etcd.Client(host=ec_endpoint['host'], port=4001, protocol="http", allow_reconnect=True)
        dirs = eClient.read(str(ETCDCLUSTER_PREFIX), recursive=True, sorted=True)
#           for child in r.children:
#           print(child.key, child.value)
    except EtcdCluster.DoesNotExist:
        print("etcd cluster is not found.")

    return render_to_response(
        'getdir.html', {
            "dirs": dirs
        },
        context_instance=RequestContext(request)
    )


def set_key(request, key=None, value=None):

    # try:
    #     eClient.write(str(key), str(value))
    # except etcd.EtcdKeyNotFound:
    #     print("key or value could not be none.")

    return render_to_response(
        'setkey.html',
        context_instance=RequestContext(request)
    )


def update_key(request, key, value=None):
    try:
        eClient.update(key, value)
    except etcd.EtcdException:
        print("etcd key update error.")
    return render_to_response(
        'updatekey.html',
        context_instance=RequestContext(request)
    )


def delete_key(request, key=None):

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

    return HttpResponseRedirect(reverse('action:getdir'))
