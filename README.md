# Docker Networking

## Useful commands

```
$ docker network ls

NETWORK ID     NAME      DRIVER    SCOPE
4571d729eea8   bridge    bridge    local
06be6f658fa3   host      host      local
9a583e6c5087   none      null      local

$ docker network inspect bridge

$ docker container prune
$ docker image prune
```

## Bridge network

The bridge network is the default network for docker containers running on a host. If you are running two containers, this configuration is typical:

Posssible addresses: 172.17.0.0/16
Gateway: 172.17.0.1
Container: 172.17.0.2
Container: 172.17.0.3

Containers can ping each other, but cannot use hostnames, only IP Addresses. In this example, these two containers can communicate between each other.

* [./server.src.server.py](./server.src.server.py)
* [./client.src.client.py](./client.src.client.py)
```
$ docker run -e LISTEN_PORT=5555 --name server server
$ docker run -e SERVER_PORT=5555 -e SERVER_IP=172.17.0.2 --name client client

```