#-*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from .models import EtcdCluster

import etcd 
from reprlib import recursive_repr


def home(request):

    r = es.read('/', recursive=True, sorted=True) 
    
    for child in r.children:
        print(child.key, child.value)
        
    return render_to_response(
        'home.tpl', {
            "rs": r.children
        },
        context_instance=RequestContext(request)
    )


def get_dir(request, key=None):
    
    r = es.read(str(key))
    return render_to_response(
        'getdir.tpl', {
            "rs": r
        },
        context_instance=RequestContext(request)
    )
    

#def update_key(request, key, value=None):
#    key_str = str(key)
#    es.write(key_str, value)
#    es.update(result)
#    return render_to_response(
#        'updatekey.tpl',
#        context_instance=RequestContext(request)
#    )

   
#def set_key(request, key, value=None):
#    key_str = str(key)
#    es.write(key_str, value)
#    return render_to_response(
#        'setkey.tpl',
#        context_instance=RequestContext(request)
#    )
#


