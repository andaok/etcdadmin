# etcdAdmin

## Overview
A tool for managing Etcd Cluster. 
![etcdadmin Logo](logos/etcdadmin.png)

Include:

[x] dashborad

[x] etcd keys manager

[x] reset api

## Supported etcd version
* etcd >= 2.0, 3.0

## Installation
**Prerequisites**

* Django >= 1.9
* Python >= 3.3
* djangorestframework
* requests
* python-etcd

**Installation**

```
$ git clone git@github.com:k8scn/etcdAdmin.git
$ cd etcdAdmin
$ virtualenv3 ~/dj19-34
$ source ~/dj19-34/bin/activate
(dj19-34)$ pip3 install -r requirements.pip3
(dj19-34)$ python manage.py makemigrations
(dj19-34)$ python manage.py migrate
(dj19-34)$ python manage.py runserver
```

## License
etcdAdmin is licensed under the Apache License, Version 2.0.
See [LICENSE](LICENSE) for full license text.

```
Copyright 2016 K8SCN Open Group.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```