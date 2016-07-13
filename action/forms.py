from django import forms
from action.models import EtcdCluster

class EtcdClusterForm(forms.ModelForm):
    class Meta:
        model = EtcdCluster
        fields = ('name', 'cluster_endpoint', 'cluster_prefix')
        
        
class KeyForm(forms.Form):
    value = forms.CharField(label='Your name')