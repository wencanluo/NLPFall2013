set root=../data
set ontology=config/ontology_dstc2.json
set outdir=res/
set CRFDir=D:/NLP/CRF++-0.58/



rem goto after_binaryswitch
set m=binaryswitch_decayhistory_topline
for %%t in (dstc2_train dstc2_dev) do (
	python BinarySwitchModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_H1_actngram_binaryswitch.label
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)
:after_binaryswitch

goto after_2waymodel_error
set m=2waymodel_error
set m2=binaryswitch_history_topline
for %%t in (dstc2_train dstc2_dev) do (
	python get2wayError.py --trackfile=%outdir%%m2%_%%t_track.json --summaryfile=%outdir%%%t_summary.txt --logfile=%outdir%%m2%_%%t_error.txt
)
:after_2waymodel_error

goto after_2waymodel_request
set m=2waymodel_actngram_request
for %%t in (dstc2_train dstc2_dev) do (
	python 2wayModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_actngram.label --methodfile=%outdir%%%t_method_actngram_mindchange.label --requestfile=%outdir%%%t_request_actngram_ngram.arff.label
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)
:after_2waymodel_request

goto after_2waymodel_method
set m=2waymodel_actngram_method_mindchange
for %%t in (dstc2_train dstc2_dev) do (
	python 2wayModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_actngram.label --methodfile=%outdir%%%t_method_actngram_mindchange.label
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)
:after_2waymodel_method

goto after_topline2
set m=topline3
for %%t in (dstc2_train dstc2_dev) do (
	python TopLine.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)
:after_topline2

goto after_topline
set m=topline1
for %%t in (dstc2_train dstc2_dev) do (
	for %%k in (0 1 2 3 4 5 6 7 8 9 10) do (
	rem for %%k in (0) do (
		python TopLine.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track_%%k.json --topK=%%k
		python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track_%%k.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score_%%k.csv
		python report.py --scorefile=%outdir%%m%_%%t_score_%%k.csv > %outdir%%m%_%%t_score_%%k.txt
	)
)
:after_topline

goto after_2waymodel_act
set m=2waymodel_actngram
for %%t in (dstc2_train dstc2_dev) do (
	python 2wayModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_actngram.label
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)
:after_2waymodel_act

goto after_2waymodel_topline
set m=2waymodel_topline_H3
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
