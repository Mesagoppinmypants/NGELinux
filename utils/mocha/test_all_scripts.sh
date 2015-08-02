#!/bin/bash

for filename in $(find /home/apathy/projects/swgnge/dsrc/sku.0/sys.server/compiled/game/script -type f \( -name '*.script' -o -name '*.scriptlib' \) -not -path "*/.deps/*"); do
    OUTPUT=$(./test_script.py $filename)
    if [[ ! -z "$OUTPUT" ]]; then
        echo "

$OUTPUT
        " >&2
    else
        echo -n .
    fi
done

echo "Finished"
