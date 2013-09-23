#!/bin/sh

for t in test1 test2 test3 test4
do
	./bin/baseline --dataset=$t --dataroot=../data --trackfile=$t\_track.json
	./bin/score --dataset=$t --dataroot=../data --trackfile=$t\_track.json --scorefile=$t\_score.csv
	./bin/report --scorefile=$t\_score.csv > $t\_score.txt
done
	