# etcdAdmin

## Overview
A tool for managing Etcd Cluster. 

Include:

[x] dashborad

[x] etcd keys manager

[x] reset api

## Supported etcd version
* etcd >= 2.0

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