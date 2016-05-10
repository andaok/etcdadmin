from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from .models import EtcdCluster

import etcd 

dir0 = True

def getEtcdHosts(s):
    #s="192.168.56.20:4001,192.168.56.21:4001,192.168.56.22:4001";
    ehost = EctdCluster.object.get()
    if ',' in s:
        print(s)
        host = tuple([tuple(r.split(":")) for r in s.split(",")])
    else:
        host = tuple(s)

    return host

def EtcdConnect(host):
    etcdClient = etcd.Client(host=host, protocol='http', allow_reconnect=True)
    return etcdClient

def home(request):
        
    #r = es.read('/', recursive=True, sorted=True)
    r = es.read('/', sorted=True) 
    
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


