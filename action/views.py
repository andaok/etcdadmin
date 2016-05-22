#-*- coding: utf-8 -*-

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from etcdadmin.settings import ETCDCLUSTER_PREFIX

#from .models import EtcdCluster

import etcd

eClient = etcd.Client(host="192.168.56.2", port=4001, protocol="http", allow_reconnect=True)

def home(request):

    return render_to_response('home.html', context_instance=RequestContext(request))


def get_dir(request):

    dirs = eClient.read(str(ETCDCLUSTER_PREFIX), recursive=True, sorted=True)
#     for child in r.children:
#         print(child.key, child.value)

    return render_to_response(
        'getdir.html', {
            "dirs": dirs
        },
        context_instance=RequestContext(request)
    )


def set_key(request, key, value=None):

    try:
        eClient.write(str(key), str(value))
    except etcd.EtcdKeyNotFound:
        print("key or value could not be none.")

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
