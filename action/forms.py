from django import forms
from action.models import EtcdCluster

class EtcdClusterForm(forms.ModelForm):
    class Meta:
        model = EtcdCluster
        fields = ('name', 'cluster_prefix', 'cluster_endpoint')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'MyECluster_001'}),
            'cluster_prefix': forms.TextInput(
                attrs={'placeholder': 'default is startwith /'}),
            'cluster_endpoint': forms.TextInput(
                attrs={'placeholder': 'http://192.168.56.2:2379 or https://192.168.56.2:2379'}),
        }
        
        
class KeyForm(forms.Form):
    key_path = forms.CharField(label='Key path')
    value = forms.CharField(label='Value to set', widget=forms.Textarea(attrs={'rows':10, 'cols':6}), required=False)
    ttl =  forms.IntegerField(initial=None)
    is_dir = forms.BooleanField(initial=False, required=False ,label='Is a directory')
    #append = forms.BooleanField(initial=True, required=False)
