#/bin/bash

destination="tmp2"
sourcepath="tmp"

mkdir -p $destination/script

javac -classpath "$destination" -d "$destination" -sourcepath "$sourcepath" -g -deprecation "$1"

