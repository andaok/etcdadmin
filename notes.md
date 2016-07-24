1. Start etcd standalone server.
	```
	$ export HostIP="192.168.56.2"
	
	$ docker run -d -v /usr/share/ca-certificates/:/etc/ssl/certs -p 4001:4001 -p 2380:2380 -p 2379:2379 \
	 --name etcd quay.io/coreos/etcd:v2.3.3 \
	 -name etcd0 \
	 -advertise-client-urls http://${HostIP}:2379,http://${HostIP}:4001 \
	 -listen-client-urls http://0.0.0.0:2379,http://0.0.0.0:4001 \
	 -initial-advertise-peer-urls http://${HostIP}:2380 \
	 -listen-peer-urls http://0.0.0.0:2380 \
	 -initial-cluster-token etcd-cluster-1 \
	 -initial-cluster etcd0=http://${HostIP}:2380 \
	 -initial-cluster-state new
	
	$ etcdctl -C http://192.168.56.2:2379 member list
	$ etcdctl -C http://192.168.56.2:4001 member list
	$ for n in {1..9};do etcdctl -C http://192.168.56.2:4001 set /worker/dev/r$n;done
	$ etcdctl -C 192.168.56.2:4001 ls /worker/dev/
	$ etcdctl set /foo "Expiring Soon" --ttl 20
	```
2. Get started with Django.

	$ git clone git@github.com:k8scn/etcdAdmin.git

3. Etcd cluster client connect formate:

    * m1 ---> http://192.168.56.2:2379

    * m2 ---> http://192.168.56.2:2379,http://192.168.56.3:2379,http://192.168.56.4:2379

4. etcdadmin todo
	
    * etcd cluster sn

    * request with etcd cluster sn

5. Others
	
    * etcd TCP ports

    * The [official etcd ports](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml?search=etcd) are 2379 for client requests, and 2380 for peer communication.

    * https://github.com/yun-an/deis/blob/de27c11475bb7ca24816f288aa115699a1c37e26/controller/api/utils.py
	