set root=../data
set ontology=config/ontology_dstc2.json
set outdir=res/
set CRFDir=D:/NLP/CRF++-0.58/

goto after_summary
set m=summary
for %%t in (dstc2_train dstc2_dev) do (
	python getSummary.py --dataset=%%t --dataroot=%root% --logfile=%outdir%%%t_%m%.txt
)
:after_summary

rem goto after_2waymodel_goals_actwithname
set m=2waymodel_enrich_goals
for %%t in (dstc2_train dstc2_dev) do (
	python 2wayModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_actngram.label --methodfile=%outdir%%%t_method_actngram_mindchange.label --requestfile=%outdir%%%t_request_actngram_ngram.arff.label --goal_area=%outdir%%%t_goals_enrich_Larea.label --goal_food=%outdir%%%t_goals_enrich_Lfood.label --goal_name=%outdir%%%t_enrich_trans_Lname.label --goal_pricerange=%outdir%%%t_goals_enrich_Lpricerange.label
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)
:after_2waymodel_goals_actwithname

goto after_2waymodel_goals_actwithname
set m=2waymodel_actWithNamengram_goals
for %%t in (dstc2_train dstc2_dev) do (
	python 2wayModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_actngram.label --methodfile=%outdir%%%t_method_actngram_mindchange.label --requestfile=%outdir%%%t_request_actngram_ngram.arff.label --goal_area=%outdir%%%t_goals_actWithNamengram_Larea.label --goal_food=%outdir%%%t_goals_actWithNamengram_Lfood.label --goal_name=%outdir%%%t_goals_actWithNamengram_Lname.label --goal_pricerange=%outdir%%%t_goals_actWithNamengram_Lpricerange.label
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)
:after_2waymodel_goals_actwithname

goto after_2waymodel_goals
set m=2waymodel_actngram_goals
for %%t in (dstc2_train dstc2_dev) do (
	python 2wayModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_actngram.label --methodfile=%outdir%%%t_method_actngram_mindchange.label --requestfile=%outdir%%%t_request_actngram_ngram.arff.label --goal_area=%outdir%%%t_goals_actngram_Larea.label --goal_food=%outdir%%%t_goals_actngram_Lfood.label --goal_name=%outdir%%%t_goals_actngram_Lname.label --goal_pricerange=%outdir%%%t_goals_actngram_Lpricerange.label
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)
:after_2waymodel_goals

rem goto after_2waymodel_error
set m=2waymodel_error
set m2=2waymodel_enrich_goals
for %%t in (dstc2_train dstc2_dev) do (
	python get2wayError.py --trackfile=%outdir%%m2%_%%t_track.json --summaryfile=%outdir%%%t_summary.txt --logfile=%outdir%%m2%_%%t_error.txt
)
:after_2waymodel_error

goto after_firstCorrect
set m=firstcorrect_top3
for %%t in (dstc2_train dstc2_dev) do (
	for %%k in (0 1 2 3 4 5 6 7 8 9 10) do (
		python FirstCorrectModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_H1_actngram_binaryswitch_top3_10.label --topK=%%k
		python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
		python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score_%%k.txt
	)
)
:after_firstCorrect

goto after_binaryswitch
set m=binaryswitch_decay_no_history_topline
for %%t in (dstc2_train dstc2_dev) do (
	python BinarySwitchModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_H1_actngram_binaryswitch.label
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)
:after_binaryswitch

goto after_binaryswitch_full
set m=binaryswitch_fullscore_top1
for %%t in (dstc2_train dstc2_dev) do (
	for %%k in (0 1 2 3 4 5 6 7 8 9 10) do (
		python BinarySwitchModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_H1_actngram_binaryswitch_top1_10.label --topK=%%k
		python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
		python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score_%%k.txt
	)
)
:after_binaryswitch_full

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
set m=2waymodel_actWithNamengram_method_mindchange
for %%t in (dstc2_train dstc2_dev) do (
	python 2wayModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_actngram.label --methodfile=%outdir%%%t_method_actwithNamengram_mindchange.label
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
