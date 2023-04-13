#!/bin/bash
while $(ps aux | grep taosd | grep -v grep | awk '{print $2}' | xargs kill 2>/dev/null); do sleep 1; done
