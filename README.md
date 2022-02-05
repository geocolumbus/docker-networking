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

## References

* [NetShoot](https://github.com/nicolaka/netshoot)
* [Docker Networking Tutorial](https://www.youtube.com/watch?v=5grbXvV_DSk)
* [Docker Cheatsheet w/NetShoot](https://github.com/xcad2k/cheat-sheets/blob/main/infrastructure/docker.md)