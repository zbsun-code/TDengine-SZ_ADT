#!/bin/bash

nohup ../debug/build/bin/taosd -c ./taosd.cfg > /dev/null 2>&1 &
echo 'waiting taosd to start... 30s'
sleep 30

../debug/build/bin/taosBenchmark -f ./insert_syn.json
echo 'insert test complete!'
echo 'waiting taosd to stop... 30s'
sudo ./taos_kill.sh
