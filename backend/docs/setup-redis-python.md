# Setup

## Setting up Redis and a Python client.

### Notes

The Redis installation page suggests compiling from source.

Connections to Redis are, by default, unsecure. Redis binds to any network interface without any notion of authentication or encryption. The [quickstart page](http://redis.io/topics/quickstart#securing-redis) suggests:

- Firewalling Redis ports from external connections, if the service is meant to stay local.
- Using a Redis configuration file to limit the available network interfaces used.
- Requiring the Redis `AUTH` command or using a secure tunnel.

### Build and install Redis

```
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
sudo make install
```

### Set up Python client

Services that rely on Redis should already have the `python-redis` project specified as a dependency (e.g; `requirements.txt`). For whatever reason, you may choose to use the `redis-py` client.

```
sudo pip install redis
```

### Running the Redis server

Simply run `redis-server` to start the server. You can use the `redis-cli` program to communicate with a Redis server.
