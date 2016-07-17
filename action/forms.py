from django import forms
from action.models import EtcdCluster

class EtcdClusterForm(forms.ModelForm):
    class Meta:
        model = EtcdCluster
        fields = ('name', 'cluster_endpoint', 'cluster_prefix')
        
        
class KeyForm(forms.Form):
    key_path = forms.CharField(label='Key path')
    value = forms.CharField(label='Value to set', widget=forms.Textarea(attrs={'rows':10, 'cols':6}), required=False)
    ttl =  forms.IntegerField(min_value=0)
    is_dir = forms.BooleanField(required=False ,label='Is a directory')
    append = forms.BooleanField(required=False)
