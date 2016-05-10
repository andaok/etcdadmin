#-*- coding: utf-8 -*-

import etcd


def getEtcdHosts(cluster, cid):
    #s="192.168.56.20:4001,192.168.56.21:4001,192.168.56.22:4001";
    ehost.address = cluster.objects.filter(int(cid))
    if ',' in :
        print(s)
        host = tuple([tuple(r.split(":")) for r in s.split(",")])
    else:
        host = tuple(s)

    return host

def EtcdConnect(host):
    etcdClient = etcd.Client(host=host, protocol='http', allow_reconnect=True)
    return etcdClient