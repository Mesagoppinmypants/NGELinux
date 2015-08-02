#/bin/bash

destination="tmp2"
sourcepath="tmp"

mkdir -p $destination/script

for filename in $(find $sourcepath -name '*.java'); do
    ok=1

    javac -classpath "$destination" -d "$destination" -sourcepath "$sourcepath" -g -deprecation "$filename" || ok=0

    if [ $ok -eq 1 ]; then
        echo -n .
    else
        echo "$filename"
    fi
done
