
for %%t in (test1) do (
	echo %%t
	python bin/baseline --dataset=%%t --dataroot=../data --trackfile=%%t_track.json
	python bin/score --dataset=%%t --dataroot=../data --trackfile=%%t_track.json --scorefile=%%t_score.csv
	python bin/report --scorefile=%%t_score.csv > %%t_score.txt
)