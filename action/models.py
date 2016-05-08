#-*- coding: utf-8 -*-


from django.db import models
from django.utils.translation import ugettext as _

from datetime import datetime


STATUS = (('0', 'DOWN'), ('1', 'UP'),)
PROTOCOLS = (('a', 'HTTP'), ('b', 'HTTPS'))

class EtcdCluster(models.Model):
    name = models.CharField(max_length=50)
    cluster_address = models.CharField(max_length=200)
    status = models.CharField(max_length=1, choices=STATUS, default=1)
    protocol = models.CharField(max_length=1, choices=PROTOCOLS, default='a')
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'etcdcluster'
        verbose_name = _(u'etcdcluster')
        unique_together = ("name", "cluster_address")

    def __unicode__(self):
        return "%s - %s  %s / %s" % (self.name, self.cluster_address, self.status, self.created_at)

    def save(self):
        super(EtcdCluster, self).save()