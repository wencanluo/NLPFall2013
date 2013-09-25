rem goto after_topline
set root=../../data
set m=topline
for %%t in (test1 test2 test3 test4) do (
	python baselineTopK.py --dataset=%%t --dataroot=%root% --trackfile=%m%_%%t_track.json
	
	for %%k in (1 2 3 4 5) do ( 
		python scoreTopK.py --dataset=%%t --dataroot=%root% --trackfile=%m%_%%t_track.json --scorefile=%m%_%%t_score_%%k.csv --topK=%%k
		python report.py --scorefile=%m%_%%t_score_%%k.csv > %m%_%%t_score_%%k.txt
	)
)
:after_topline

goto after_baseline
set root=../../data
set m=baseline
for %%t in (test1 test2 test3 test4) do (
	python baseline.py --dataset=%%t --dataroot=%root% --trackfile=%m%_%%t_track.json
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%m%_%%t_track.json --scorefile=%m%_%%t_score.csv
	python report.py --scorefile=%m%_%%t_score.csv > %m%_%%t_score.txt
)
:after_baseline

goto comment_no_history
rem run no_history
set root=../../data
set m=nohistory
for %%t in (test1 test2 test3 test4) do (
	python baselineNohistroy.py --dataset=%%t --dataroot=%root% --trackfile=%m%_%%t_track.json
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%m%_%%t_track.json --scorefile=%m%_%%t_score.csv
	python report.py --scorefile=%m%_%%t_score.csv > %m%_%%t_score.txt
)

:comment_no_history

pause