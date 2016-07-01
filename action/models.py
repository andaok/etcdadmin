#-*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from datetime import datetime


STATUS = (('0', 'READY'), ('1', 'UP'),('2', 'DOWN'),('3', 'UNKOWN'))

class EtcdCluster(models.Model):
    name = models.CharField(max_length=50, unique=True)
    serial_number = models.CharField(max_length=100)
    cluster_endpoint = models.CharField(max_length=300)
    cluster_prefix = models.CharField(max_length=100)
    status = models.CharField(max_length=1, choices=STATUS, default=0)
    version = models.CharField(max_length=50, default="UNKOWN")
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'etcdcluster'
        verbose_name = _(u'etcdcluster')
        unique_together = ("cluster_endpoint",)

    def __unicode__(self):
        return "%s - %s  %s / %s" % (self.name, self.cluster_address, self.status, self.created_at)

#     @staticmethod
#     def get_serial_number(self):
#         print(self.id)
#         serial_number = self.id.rjust(4, '0')
#         return serial_number
    
    def save(self):
        super(EtcdCluster, self).save()