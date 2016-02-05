#!/bin/bash

DIR="$( dirname "${BASH_SOURCE[0]}" )"

spinstr='|/-\'
i=0

filenames=$(find $1 -type f \( -name '*.script' -o -name '*.scriptlib' \) -not -path "*/.deps/*")
current=0
total=$(ls ${filenames[@]} | wc -l)

compile () {
        OFILENAME=${filename//.scriptlib/.java}
        OFILENAME=${OFILENAME//.script/.java}

    ok=1

    if [[ -e $OFILENAME && $filename -nt $OFILENAME ]] || [ ! -e $OFILENAME ]; then
        ${DIR}/script_prep2.py -i $filename -o $OFILENAME || ok=0

        if [ ! $ok -eq 1 ]; then
            printf "$filename $OFILENAME\n\n"
        fi
    fi
}

for filename in $filenames; do
    current=$((current+1))
    i=$(( (i+1) %4 ))
    perc=$(bc -l <<< "scale=0; $current*100/$total")
    printf "\rConverting .scripts [${spinstr:$i:1}] $perc%%"
	while [ `jobs | wc -l` -ge 50 ]
	do
		sleep 5
	done
    compile $filename & done
wait

echo ""
