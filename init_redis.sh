#!/bin/bash
sysctl -w vm.overcommit_memory=1
exec redis-server /usr/local/etc/redis/redis.conf