#-*- coding:utf-8 -*-

import json
import requests


def main():
    
    zs = ZaggSender()
    
    try:
        request = requests.get(API_URL, verify=False)
        content = json.loads(request.content)
        etcd_ping = 1
        
        # parse the items and add it as metrics
        zs.add_check_keys({'etcd.create.success' : content['createSuccess']})
        zs.add_check_keys({'etcd.create.fail' : content['createFail']})
        zs.add_check_keys({'etcd.delete.success' : content['deleteSuccess']})
        zs.add_check_keys({'etcd.delete.fail' : content['deleteFail']})
        zs.add_check_keys({'etcd.get.success' : content['getsSuccess']})
        zs.add_check_keys({'etcd.get.fail' : content['getsFail']})
        zs.add_check_keys({'etcd.set.success' : content['setsSuccess']})
        zs.add_check_keys({'etcd.set.fail' : content['setsFail']})
        zs.add_check_keys({'etcd.update.success' : content['updateSuccess']})
        zs.add_check_keys({'etcd.update.fail' : content['updateFail']})
        zs.add_check_keys({'etcd.watchers' : content['watchers']})
        
    except requests.exceptions.ConnectionError as ex:
        print "ERROR talking to etcd API: %s" % ex.message
        etcd_ping = 0

    zs.add_check_keys({'openshift.master.etcd.ping' : etcd_ping})
    
    # Finally, sent them to zabbix
    zs.send_metrics()
    
if __name__ == '__main__':
    main()