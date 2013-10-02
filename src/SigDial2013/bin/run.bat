set root=../../data
set m=topline
set outdir=res/

goto after_summary
rem for %%t in (train1a train2 train3) do (
for %%t in (test1 test2 test3 test4 train1a train2 train3) do (
python getSummary.py --dataset=%%t --dataroot=%root% --logfile=%outdir%%%t_summary.txt
rem python scoreTopK.py --dataset=%%t --dataroot=%root% --trackfile=%m%_%%t_track.json --scorefile=%m%_%%t_score_%%k.csv --topK=%%k
rem python report.py --scorefile=%m%_%t%_score_%k%.csv > %m%_%t%_score_%k%.txt
)
:after_summary

rem goto after_topline
set root=../../data
set m=topline
for %%t in (test1 test2 test3 test4) do (
	for %%k in (-1 0 1 2 3 4 5 6 7 8 9 10) do (
		python topLineTopK.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track_%%k.json --topK=%%k
		python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track_%%k.json --scorefile=%outdir%%m%_%%t_score_%%k.csv
		python report.py --scorefile=%outdir%%m%_%%t_score_%%k.csv > %outdir%%m%_%%t_score_%%k.txt
	)
)
:after_topline

goto after_majoritybaseline
set root=../../data
set m=majoritybaseline
for %%t in (test1 test2 test3 test4) do (
	python baseline.py --dataset=%%t --dataroot=%root% --trackfile=%m%_%%t_track.json --null
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%m%_%%t_track.json --scorefile=%m%_%%t_score.csv
	python report.py --scorefile=%m%_%%t_score.csv > %m%_%%t_score.txt
)
:after_majoritybaseline

goto after_baseline
set root=../../data
set m=baseline_allmetrics
for %%t in (test1 test2 test3 test4) do (
	python baseline.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)
:after_baseline

goto after_nohistory
set root=../../data
set m=nohistory_allmetrics
for %%t in (test1 test2 test3 test4) do (
	python baselineNohistroy.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)

:after_nohistory
