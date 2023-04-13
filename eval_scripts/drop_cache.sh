#!/bin/bash
grep file /proc/meminfo
sudo echo 3 > /proc/sys/vm/drop_caches
grep file /proc/meminfo
