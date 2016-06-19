#-*- coding: utf-8 -*-


from django.contrib import admin
from action.models import EtcdCluster

class EtcdClusterAdmin(admin.ModelAdmin):
    list_display_links = ('name',)
    list_filter = ('created_at',)
    list_display = [
        'name',
        'serial_number',
        'cluster_endpoint',
        'status',
        'created_at',
        'updated_at',
    ]
    ordering = ['-updated_at']
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'serial_number',
                'cluster_endpoint',
                'status',
            ),
        }),
    )

admin.site.register(EtcdCluster, EtcdClusterAdmin)


def make_etcd_cluster_online(modeladmin, request, queryset):
    queryset.update(status='1')
    make_etcd_cluster_online.short_description = "Mark selected etcd cluster online."