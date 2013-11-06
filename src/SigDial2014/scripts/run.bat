set root=../data
set ontology=config/ontology_dstc2.json
set outdir=res/
set CRFDir=D:/NLP/CRF++-0.58/

rem goto after_2waymodel_act
rem set m=2waymodel_actngram_topline
set m=2waymodel_actngram
for %%t in (dstc2_train dstc2_dev) do (
rem for %%t in (dstc2_train) do (
	python 2wayModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_actngram.label
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)
:after_2waymodel_act

goto after_2waymodel_error
set m=2waymodel_error
set m2=2waymodel_actngram_topline
for %%t in (dstc2_train dstc2_dev) do (
rem for %%t in (dstc2_train) do (
	python get2wayError.py --trackfile=%outdir%%m2%_%%t_track.json --summaryfile=%outdir%%%t_summary.txt --logfile=%outdir%%m2%_%%t_error.txt
)
:after_2waymodel_error

goto after_2waymodel_topline
set m=2waymodel_topline
for %%t in (dstc2_train dstc2_dev) do (
	for %%k in (0 1 2 3 4 5 6 7 8 9 10) do (
		python 2wayModelTopLine.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track_%%k.json --labelfile=%outdir%%%t_summary.txt --topK=%%k
		python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track_%%k.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score_%%k.csv
		python report.py --scorefile=%outdir%%m%_%%t_score_%%k.csv > %outdir%%m%_%%t_score_%%k.txt
	)
)
:after_2waymodel_topline

goto after_baselineTop1
set m=baselineTop1
for %%t in (dstc2_train dstc2_dev) do (
	python baselineTop1.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)
:after_baselineTop1

goto after_summary
set m=summary
for %%t in (dstc2_train dstc2_dev) do (
	python getSummary.py --dataset=%%t --dataroot=%root% --logfile=%outdir%%%t_%m%.txt
)
:after_summary

goto after_HWUbaseline
set m=HWUbaseline
for %%t in (dstc2_train dstc2_dev) do (
	python baseline_HWU.py --dataset=%%t --dataroot=%root% --ontology=%ontology% --trackfile=%outdir%%m%_%%t_track.json
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)
:after_HWUbaseline

goto after_baseline
set m=baseline
for %%t in (dstc2_train dstc2_dev) do (
	python baseline.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)
:after_baseline

goto after_baseline_focus
set m=baseline_focus
for %%t in (dstc2_train dstc2_dev) do (
	python baseline.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --focus=True
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)
:after_baseline_focus
