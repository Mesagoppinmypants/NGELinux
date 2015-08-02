#/bin/bash

destination="data/sku.0/sys.server/compiled/game"
sourcepath="dsrc/sku.0/sys.server/compiled/game"

mkdir -p $destination/script

javac -classpath "$destination" -d "$destination" -sourcepath "$sourcepath" -g -deprecation "$1"
