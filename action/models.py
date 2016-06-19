#-*- coding: utf-8 -*-


from django.db import models
from django.utils.translation import ugettext as _
from datetime import datetime


STATUS = (('0', 'READY'), ('1', 'UP'),('2', 'DOWN'))


class EtcdCluster(models.Model):
    name = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=100, unique=True)
    cluster_endpoint = models.CharField(max_length=300)
    cluster_prefix = models.CharField(max_length=100)
    status = models.CharField(max_length=1, choices=STATUS, default=0)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'etcdcluster'
        verbose_name = _(u'etcdcluster')
        unique_together = ("name", "cluster_endpoint")

    def __unicode__(self):
        return "%s - %s  %s / %s" % (self.name, self.cluster_address, self.status, self.created_at)

#     @staticmethod
#     def get_serial_number(eid):
#         ecid = EtcdCluster.objects.get(id=eid).id
#         serial_number = ecid.rjust(4, '0')
#         return serial_number
    
    def save(self):
        super(EtcdCluster, self).save()