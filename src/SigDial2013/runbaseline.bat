
for %%t in (test1) do (
	echo %%t
	python bin/baseline.py --dataset=%%t --dataroot=../data --trackfile=%%t_track.json
	python bin/score.py --dataset=%%t --dataroot=../data --trackfile=%%t_track.json --scorefile=%%t_score.csv
	python bin/report.py --scorefile=%%t_score.csv > %%t_score.txt
)