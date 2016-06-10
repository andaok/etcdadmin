#-*- coding: utf-8 -*-

import etcd
from action.models import EtcdCluster

def getEtcdHosts(cluster, cid):
    #s="192.168.56.20:4001,192.168.56.21:4001,192.168.56.22:4001";
    etcd_ins = EtcdCluster.objects.filter(int(cid))
    
    if ',' in etcd_ins.address:
        print(etcd_ins.address)
        host = tuple([tuple(r.split(":")) for r in etcd_ins.address.split(",")])
    else:
        host = tuple(etcd_ins.address)

    return host

def EtcdConnect(host):
    etcdClient = etcd.Client(host=host, protocol='http', allow_reconnect=True)
    return etcdClient
