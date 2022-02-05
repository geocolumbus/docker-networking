# Docker Networking

## Useful commands

    $ docker network ls

    NETWORK ID     NAME      DRIVER    SCOPE
    4571d729eea8   bridge    bridge    local
    06be6f658fa3   host      host      local
    9a583e6c5087   none      null      local

    $ docker network inspect bridge

    $ docker container prune
    $ docker image prune

## Bridge Network (bridge driver)

The bridge network is the default network for docker containers running on a host. If you are running two containers, this configuration is typical:

Posssible addresses: 172.17.0.0/16
Gateway: 172.17.0.1
Container: 172.17.0.2
Container: 172.17.0.3

Here is a simple socket example of two docker containers talking to each other:

* [./server.src.server.py](./server.src.server.py)
* [./client.src.client.py](./client.src.client.py)
```
$ docker build -t server ./server
$ docker build -t client ./client
$ docker run -e LISTEN_PORT=5555 --name server server
$ docker run -e SERVER_PORT=5555 -e SERVER_IP=172.17.0.2 --name client client
```
Note that we did not use the ```--expose [container port]:[host port]``` option, but the server and client were still able to communicate with each other over the bridge network. Exposing ports makes them available to the localhost of the machine running the docker containers, but is not requirement for them to talk to each other.

The bridge network has limitations:
* You cannot do name resolution.
* You cannot isolate containers from each other.
* IP Addresses can be different every time you start the containers

## Custom Bridge Network (bridge driver)

    $ docker network create my_bridge
    $ docker network ls

    NETWORK ID     NAME        DRIVER    SCOPE
    4571d729eea8   bridge      bridge    local
    06be6f658fa3   host        host      local
    97bd989cc2fb   my_bridge   bridge    local
    9a583e6c5087   none        null      local

So we can use the same containers, but they can reference each other with names instead of IP addresses. The name assigned to the container is also the hostname of the instance. Instead of referring to ```SERVER_IP=172.17.0.2``` for the client, we can refer to ```SERVER_IP=server```. This way these will always work no matter which IP they are assigned to. Of course, we avoided the defauly bridge network by specifyng the ```--network my_bridge``` option.

    $ docker run --network my_bridge -e LISTEN_PORT=5555 --name server server
    $ docker run --network my_bridge -e SERVER_PORT=5555 -e SERVER_IP=server --name client client

The custom bridge network these features
* It cannot access containers on other networks.
* It can use name resolution
* It can ping the host IP address
* It can ping external servers, like google.com

## Host Network (host driver)

If you are hosting an nginx server inside a docker container on a default bridge network, you do it like this:

    docker run --rm -d --name nginx -p 80:80 nginx

If you want that container to be directly hosted by your local machine, you do it like this. No need to bridge port 80, and you specify the network is host.

    docker run --rm -d --name nginx --network host nginx

Now every port that nginx works with is connected to your localhost

## MACVlan Network

The docker container has a unique MAC address that can be used to create a unique IP Address on your local network.

    docker network create -d macvlan --subnet 192.168.0.0/24 --gateway 192.168.0.1

Sadly, it does not get a new IP address fromt eh DHCP server. Instead, it assigns the first one that it knows is available, which is 192.168.0.1. This immediately causes and IP address conflict with the local gateway.

So you need to add another parameter to set the range that the docker host can assign

    --ip-range 192.168.0.233/32  <--- limited to just one IP address not used by any other device on the network

Also add these parameters and the name

    -o parent=ens18 custom_mac_vlan

You can run against that network by specifying ```--network custom_mac_vlan```

## IPVlan Network

When you use docker run, specify the ip address:

    --ip 192.168.0.233 ----network custom_ip_vlan

* MACVlan networks have a separate MAC address for each container.
* IPVLan networks have the same MAC address for all containers.

IPVlan is useful when a switch does not like that separate ports are running different MAC addresses. With IPVlans, all the ports will have the same MAC address.

IPVlan's can also operate in layer 2 and 3 mode.

## Overlay Network

For multiple docker hosts in a swarm cluster - connect with one network spread across those different hosts. But if you need a cluster to run containers, just go with Kubernetes.



## References

* [NetShoot](https://github.com/nicolaka/netshoot)
* [Docker Networking Tutorial](https://www.youtube.com/watch?v=5grbXvV_DSk)
* [Docker Cheatsheet w/NetShoot](https://github.com/xcad2k/cheat-sheets/blob/main/infrastructure/docker.md)