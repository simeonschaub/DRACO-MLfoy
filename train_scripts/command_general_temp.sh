#!/bin/bash

set=HandSelec_S01
echo $set
for i in 1 2 3 
do
	for cat in ge4j_3t ge4j_ge4t #4j_ge3t 5j_ge3t ge6j_ge3t ge4j_3t ge4j_ge4t 
	do
    	python ttZ_train.py -v ${set} -o ${set}/sp_v${i} -i DNN_Input_splitTTToSemiLeptonic -c $cat -n ttZAnalysis -e 300 -p -s -1 -P -R  -S ttZ  #2> /storage/8/lbosch/S04_bin_$cat.err
	done
done 