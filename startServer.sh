#!/bin/bash

cd exe/linux

killall LoginServer &> /dev/null
./bin/LoginServer -- @servercommon.cfg &

sleep 5

./bin/TaskManager -- @servercommon.cfg
