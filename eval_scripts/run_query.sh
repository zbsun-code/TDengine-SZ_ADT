#!/bin/bash

sudo ./drop_cache.sh
nohup ../debug/build/bin/taosd -c ./taosd.cfg > /dev/null 2>&1 &
echo 'waiting taosd to start... 30s'
sleep 30

../debug/build/bin/taosBenchmark -f ./query_demo.json | tee -a result_query.txt
rm -f output.txt
echo 'waiting taosd to stop... 30s'
sudo ./taos_kill.sh
