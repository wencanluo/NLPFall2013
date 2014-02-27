set root=../data
set ontology=config/ontology_dstc2.json
set outdir=res/
set CRFDir=D:/NLP/CRF++-0.58/

rem goto after_2waymodel_method
set m=2waymodel_method
for %%t in (dstc2_test) do (
	rem python 2wayModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --methodfile=%outdir%%%t_method_recovery.label --requestfile=%outdir%%%t_request_actngram_slot_ngram.arff.label --goal_area=%outdir%%%t_nbest_goals_asr_Larea.label --goal_food=%outdir%%%t_nbest_goals_asr_Lfood.label --goal_name=%outdir%%%t_nbest_goals_asr_Lname.label --goal_pricerange=%outdir%%%t_nbest_goals_asr_Lpricerange.label
	
	rem python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)

:after_2waymodel_method

goto after_topline
set m=topline3
for %%t in (dstc2_test) do (
	rem for %%k in (0 1 2 3 4 5 6 7 8 9 10) do (
	for %%k in (10) do (
	rem for %%k in (0) do (
		python TopLine.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track_%%k.json --topK=%%k
		python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track_%%k.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score_%%k.csv
		python report.py --scorefile=%outdir%%m%_%%t_score_%%k.csv > %outdir%%m%_%%t_score_%%k.txt
	)
)
:after_topline

goto after_2waymodel_ff
set m=decompose_topline
for %%t in (dstc2_test) do (
	rem for %%f in (asr_act_score rawscore noasr noid noscore nosystem noslu) do (
	rem for %%f in (asr_act_score) do (
		python 2wayModelSlotFinder.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --methodfile=%outdir%%%t_method_trans.label --requestfile=%outdir%%%t_request_trans_ngram.arff.label --goal_area=%outdir%%%t_trans_Larea.label --goal_food=%outdir%%%t_trans_Lfood.label --goal_name=%outdir%%%t_trans_Lname.label --goal_pricerange=%outdir%%%t_trans_Lpricerange.label
		python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
		python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
		rem )
	)
)
:after_2waymodel_ff

goto after_2waymodel_error
set m=2waymodel_error
set m2=decompose_topline
rem for %%t in (dstc2_train dstc2_dev dstc2_traindev dstc2_test) do (
for %%t in (dstc2_test) do (
	python get2wayError.py --trackfile=%outdir%%m2%_%%t_track.json --summaryfile=%outdir%%%t_summary.txt --logfile=%outdir%%m2%_%%t_error.txt
)
:after_2waymodel_error

goto after_convert_track_prediction
for %%m in (baseline_focus HWUbaseline nbest_goals) do (
rem for %%m in (nbest_goals) do (
	for %%t in (dstc2_dev dstc2_test) do (
		python GetTrackFood.py --summaryfile=%outdir%%%t_summary.txt --trackfile=%outdir%%%m_%%t_track.json
		rem python ConvertTrack.py --summaryfile=%outdir%%%t_summary.txt --trackfile=%outdir%%%m_%%t_track.json
	)
)
:after_convert_track_prediction

goto after_summary
set m=summary
for %%t in (dstc2_train dstc2_dev dstc2_traindev dstc2_test) do (
rem for %%t in (dstc2_traindev) do (
	python getSummary.py --dataset=%%t --dataroot=%root% --logfile=%outdir%%%t_%m%.txt
)
:after_summary

goto after_3waymodel
set m=3waymodel
for %%t in (dstc2_train dstc2_dev) do (
	python 3wayModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --methodfile=%outdir%%%t_method_actwithNamengram_mindchange.label --requestfile=%outdir%%%t_request_actngram_slot_ngram.arff.label --labelfile=%outdir%%%t_H1_actngram_3way_top1.label
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
	)
)
:after_3waymodel

goto after_CombineNBest
set m=CombineNBest
for %%t in (dstc2_train dstc2_dev) do (
	for %%k in (0 1 2 3 4 5 6 7 8 9 10) do (
	python CombineNBest.py --dataset=%%t --dataroot=%root% --goal_area=%outdir%%%t_nbest_goals_asrs_Larea.label --goal_food=%outdir%%%t_nbest_goals_asrs_Lfood.label --goal_name=%outdir%%%t_nbest_goals_asrs_Lname.label --goal_pricerange=%outdir%%%t_nbest_goals_asrs_Lpricerange.label --topK=%%k
	rem python CombineNBest.py --dataset=%%t --dataroot=%root% --goal_food=%outdir%%%t_nbest_goals_enrich_asrs_class_Lfood.label
	)
)
:after_CombineNBest

goto after_CombineNBest_Method
set m=CombineNBest_Method
for %%t in (dstc2_train dstc2_dev dstc2_test) do (
	for %%k in (0 1 2 3 4 5 6 7 8 9 10) do (
	python CombineNBest.py --dataset=%%t --dataroot=%root% --goal_area=%outdir%%%t_request_asr_act_score_all_ngram.arff.label.matrix --topK=%%k
	python CombineNBest.py --dataset=%%t --dataroot=%root% --goal_area=%outdir%%%t_method_asr_act_score_mindchange_all.label --topK=%%k
	)
)
:after_CombineNBest_Method

goto after_firstCorrect
set m=firstcorrect_top1
for %%t in (dstc2_train dstc2_dev) do (
	for %%k in (1) do (
		python FirstCorrectModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_H1_actngram_binaryswitch.label --topK=%%k --methodfile=%outdir%%%t_method_actwithNamengram_mindchange.label --requestfile=%outdir%%%t_request_actngram_slot_ngram.arff.label
		rem python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
		rem python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
	)
)

for %%t in (dstc2_test) do (
	for %%k in (1) do (
		python FirstCorrectModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_H1_actngram_binaryswitch.label --topK=%%k --methodfile=%outdir%%%t_method_actwithNamengram_mindchange.label --requestfile=%outdir%%%t_request_actngram_slot_ngram.arff.label
	)
)
:after_firstCorrect

goto after_binaryswitch
set m=binaryswitch
for %%t in (dstc2_train dstc2_dev) do (
	for %%k in (0 1 2 3 4 5 6 7 8 9 10) do (
	rem for %%k in (0) do (
	python BinarySwitchModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_H1_actngram_binaryswitchwithName.label --methodfile=%outdir%%%t_method_actwithNamengram_mindchange.label --requestfile=%outdir%%%t_request_actngram_slot_ngram.arff.label --topK=%%k
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.%%k.txt
	)
)
:after_binaryswitch

goto after_asr_act_score
set m=nbest_goals_all
for %%t in (dstc2_train dstc2_dev dstc2_test) do (
	for %%k in (0 1 2 3 4 5 6 7 8 9 10) do (
	python NbestModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --methodfile=%outdir%%%t_method_asr_act_score_mindchange_all.label.%%k.combine --requestfile=%outdir%%%t_request_asr_act_score_all_ngram.arff.label.matrix.%%k.combine --goal_area=%outdir%%%t_asr_act_score_Larea_all.label --goal_food=%outdir%%%t_asr_act_score_Lfood_all.label --goal_name=%outdir%%%t_asr_act_score_Lname_all.label --goal_pricerange=%outdir%%%t_asr_act_score_Lpricerange_all.label --topK=%%k
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.%%k.txt
	)
)

:after_asr_act_score

goto after_nbestmodel_goals
set m=nbest_goals
for %%t in (dstc2_train dstc2_dev) do (
	rem for %%k in (0 1 2 3 4 5 6 7 8 9 10) do (
	for %%k in (4) do (
	rem python NbestModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --methodfile=%outdir%%%t_method_actwithNamengram_mindchange.label --requestfile=%outdir%%%t_request_actngram_slot_ngram.arff.label --goal_area=%outdir%%%t_nbest_goals_asrs_Larea.label --goal_food=%outdir%%%t_nbest_goals_asrs_Lfood.label --goal_name=%outdir%%%t_nbest_goals_asrs_Lname.label --goal_pricerange=%outdir%%%t_nbest_goals_asrs_Lpricerange.label --topK=%%k
	rem python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	rem python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.%%k.txt
	)
)
for %%t in (dstc2_test) do (
	rem for %%k in (0 1 2 3 4 5 6 7 8 9 10) do (
	for %%k in (4) do (
	rem python NbestModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --methodfile=%outdir%%%t_method_actwithNamengram_mindchange.label --requestfile=%outdir%%%t_request_actngram_slot_ngram.arff.label --goal_area=%outdir%%%t_nbest_goals_asrs_Larea.label --goal_food=%outdir%%%t_nbest_goals_asrs_Lfood.label --goal_name=%outdir%%%t_nbest_goals_asrs_Lname.label --goal_pricerange=%outdir%%%t_nbest_goals_asrs_Lpricerange.label --topK=%%k
	)
)

:after_nbestmodel_goals

goto after_2waymodel_error
set m=2waymodel_error
set m2=nbest_goals_hwu_food
rem for %%t in (dstc2_train dstc2_dev dstc2_traindev dstc2_test) do (
for %%t in (dstc2_traindev) do (
	python get2wayError.py --trackfile=%outdir%%m2%_%%t_track.json --summaryfile=%outdir%%%t_summary.txt --logfile=%outdir%%m2%_%%t_error.txt
)
:after_2waymodel_error

goto after_nbestmodel_goals_hwu_food
set m=nbest_goals_focus_food
for %%t in (dstc2_train dstc2_dev) do (
	for %%k in (0 1 2 3 4 5 6 7 8 9 10) do (
	rem for %%k in (4) do (
	python NbestModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --methodfile=%outdir%%%t_method_actwithNamengram_mindchange.label --requestfile=%outdir%%%t_request_actngram_slot_ngram.arff.label --goal_area=%outdir%%%t_nbest_goals_asrs_Larea.label --goal_food=%outdir%%%t_nbest_goals_asrs_Lfood.label --goal_name=%outdir%%%t_nbest_goals_asrs_Lname.label --goal_pricerange=%outdir%%%t_nbest_goals_asrs_Lpricerange.label --topK=%%k --goal_food_prediction=%outdir%baseline_focus_%%t_track.json.food.prediction 
	rem --goal_name_prediction=%outdir%HWUbaseline_%%t_track.json.name.prediction 
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score_%%k.txt
	)
)
for %%t in (dstc2_test) do (
	for %%k in (0 1 2 3 4 5 6 7 8 9 10) do (
	rem for %%k in (4) do (
	python NbestModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --methodfile=%outdir%%%t_method_actwithNamengram_mindchange.label --requestfile=%outdir%%%t_request_actngram_slot_ngram.arff.label --goal_area=%outdir%%%t_nbest_goals_asrs_Larea.label --goal_food=%outdir%%%t_nbest_goals_asrs_Lfood.label --goal_name=%outdir%%%t_nbest_goals_asrs_Lname.label --goal_pricerange=%outdir%%%t_nbest_goals_asrs_Lpricerange.label --topK=%%k --goal_food_prediction=%outdir%baseline_focus_%%t_track.json.food.prediction 
	rem --goal_name_prediction=%outdir%HWUbaseline_%%t_track.json.name.prediction 
	rem --goal_food_prediction=%outdir%HWUbaseline_%%t_track.json.food.prediction
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score_%%k.txt
	)
)
:after_nbestmodel_goals_hwu_food

goto after_nbestmodel_goals_hwu_food_self
set m=nbest_goals_hwu_self
for %%t in (dstc2_dev) do (
	for %%k in (0 1 2 3 4 5 6 7 8 9 10) do (
	rem for %%k in (4) do (
	python NbestModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --methodfile=%outdir%%%t_method_actwithNamengram_mindchange.label --requestfile=%outdir%%%t_request_actngram_slot_ngram.arff.label --goal_area=%outdir%%%t_nbest_goals_asrs_Larea.label --goal_food=%outdir%%%t_nbest_goals_asrs_Lfood.label --goal_name=%outdir%%%t_nbest_goals_asrs_Lname.label --goal_pricerange=%outdir%%%t_nbest_goals_asrs_Lpricerange.label --topK=%%k --goal_food_prediction=%outdir%HWUbaseline_%%t_track.json.food.prediction 
	rem --goal_name_prediction=%outdir%HWUbaseline_%%t_track.json.name.prediction 
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.%%k.txt
	)
)
for %%t in (dstc2_test) do (
	rem for %%k in (0 1 2 3 4 5 6 7 8 9 10) do (
	for %%k in (4) do (
	rem python NbestModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --methodfile=%outdir%%%t_method_actwithNamengram_mindchange.label --requestfile=%outdir%%%t_request_actngram_slot_ngram.arff.label --goal_area=%outdir%%%t_nbest_goals_asrs_Larea.label --goal_food=%outdir%%%t_nbest_goals_asrs_Lfood.label --goal_name=%outdir%%%t_nbest_goals_asrs_Lname.label --goal_pricerange=%outdir%%%t_nbest_goals_asrs_Lpricerange.label --topK=%%k 
	rem --goal_food_prediction=%outdir%HWUbaseline_%%t_track.json.food.prediction
	)
)
:after_nbestmodel_goals_hwu_food_self

goto after_2waymodel_goals_nbest
set m=2waymodel_goals_nbest
for %%t in (dstc2_train dstc2_dev) do (
	for %%k in (0 1 2 3 4 5 6 7 8 9 10) do (
	rem for %%k in (0) do (
	python 2wayModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --methodfile=%outdir%%%t_method_actwithNamengram_mindchange.label --requestfile=%outdir%%%t_request_actngram_slot_ngram.arff.label --goal_area=%outdir%%%t_nbest_goals_asrs_Larea.label.%%k.combine --goal_food=%outdir%%%t_nbest_goals_asrs_Lfood.label.%%k.combine --goal_name=%outdir%%%t_nbest_goals_asrs_Lname.label.%%k.combine --goal_pricerange=%outdir%%%t_nbest_goals_asrs_Lpricerange.label.%%k.combine 
	rem --goal_food_prediction=%outdir%HWUbaseline_%%t_track.json.food.prediction --goal_name_prediction=%outdir%HWUbaseline_%%t_track.json.name.prediction 
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.%%k.txt
	)
)
for %%t in (dstc2_test) do (
	rem for %%k in (0 1 2 3 4 5 6 7 8 9 10) do (
	for %%k in (0) do (
	rem python 2wayModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.%%k.json --methodfile=%outdir%%%t_method_actwithNamengram_mindchange.label --requestfile=%outdir%%%t_request_actngram_slot_ngram.arff.label --goal_area=%outdir%%%t_nbest_goals_asrs_Larea.label.%%k.combine --goal_food=%outdir%%%t_nbest_goals_asrs_Lfood.label.%%k.combine --goal_name=%outdir%%%t_nbest_goals_asrs_Lname.label.%%k.combine --goal_pricerange=%outdir%%%t_nbest_goals_asrs_Lpricerange.label.%%k.combine
	)
)

:after_2waymodel_goals_nbest

goto after_2waymodel_goals_nbest_hwufood
set m=2waymodel_goals_nbest_hwu_food
for %%t in (dstc2_train dstc2_dev) do (
	rem for %%k in (0 1 2 3 4 5 6 7 8 9 10) do (
	for %%k in (0) do (
	python 2wayModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --methodfile=%outdir%%%t_method_actwithNamengram_mindchange.label --requestfile=%outdir%%%t_request_actngram_slot_ngram.arff.label --goal_area=%outdir%%%t_nbest_goals_asrs_Larea.label.%%k.combine --goal_food=%outdir%%%t_nbest_goals_asrs_Lfood.label.%%k.combine --goal_name=%outdir%%%t_nbest_goals_asrs_Lname.label.%%k.combine --goal_pricerange=%outdir%%%t_nbest_goals_asrs_Lpricerange.label.%%k.combine --goal_food_prediction=%outdir%HWUbaseline_%%t_track.json.food.prediction --goal_name_prediction=%outdir%HWUbaseline_%%t_track.json.name.prediction 
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.%%k.txt
	)
)
for %%t in (dstc2_test) do (
	for %%k in (0 1 2 3 4 5 6 7 8 9 10) do (
	rem for %%k in (0) do (
	rem python 2wayModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.%%k.json --methodfile=%outdir%%%t_method_actwithNamengram_mindchange.label --requestfile=%outdir%%%t_request_actngram_slot_ngram.arff.label --goal_area=%outdir%%%t_nbest_goals_asrs_Larea.label.%%k.combine --goal_food=%outdir%%%t_nbest_goals_asrs_Lfood.label.%%k.combine --goal_name=%outdir%%%t_nbest_goals_asrs_Lname.label.%%k.combine --goal_pricerange=%outdir%%%t_nbest_goals_asrs_Lpricerange.label.%%k.combine
	)
)

:after_2waymodel_goals_nbest_hwufood

goto after_2waymodel_hybrid
set m=2waymodel_hybrid
for %%t in (dstc2_train dstc2_dev) do (
	python 2wayModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --methodfile=%outdir%%%t_method_actwithNamengram_mindchange.label --requestfile=%outdir%%%t_request_actngram_slot_ngram.arff.label --goal_area=%outdir%%%t_goals_enrich_logasr_hybrid_Larea.label --goal_food=%outdir%%%t_goals_enrich_logasr_hybrid_Lfood.label --goal_name=%outdir%%%t_goals_enrich_logasr_hybrid_Lname.label --goal_pricerange=%outdir%%%t_goals_enrich_logasr_hybrid_Lpricerange.label
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)
for %%t in (dstc2_test) do (
	python 2wayModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --methodfile=%outdir%%%t_method_actwithNamengram_mindchange.label --requestfile=%outdir%%%t_request_actngram_slot_ngram.arff.label --goal_area=%outdir%%%t_nbest_goals_asr_Larea.label --goal_food=%outdir%%%t_nbest_goals_asr_Lfood.label --goal_name=%outdir%%%t_nbest_goals_asr_Lname.label --goal_pricerange=%outdir%%%t_nbest_goals_asr_Lpricerange.label
	)
)

:after_2waymodel_hybrid

goto after_2waymodel_goals_topASR
set m=2waymodel_goals_topASR
for %%t in (dstc2_train dstc2_dev) do (
	python 2wayModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --methodfile=%outdir%%%t_method_actwithNamengram_mindchange.label --requestfile=%outdir%%%t_request_actngram_slot_ngram.arff.label --goal_area=%outdir%%%t_nbest_goals_asr_Larea.label --goal_food=%outdir%%%t_nbest_goals_asr_Lfood.label --goal_name=%outdir%%%t_nbest_goals_asr_Lname.label --goal_pricerange=%outdir%%%t_nbest_goals_asr_Lpricerange.label
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)
for %%t in (dstc2_test) do (
	python 2wayModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --methodfile=%outdir%%%t_method_actwithNamengram_mindchange.label --requestfile=%outdir%%%t_request_actngram_slot_ngram.arff.label --goal_area=%outdir%%%t_nbest_goals_asr_Larea.label --goal_food=%outdir%%%t_nbest_goals_asr_Lfood.label --goal_name=%outdir%%%t_nbest_goals_asr_Lname.label --goal_pricerange=%outdir%%%t_nbest_goals_asr_Lpricerange.label
	)
)

:after_2waymodel_goals_topASR

goto after_HWUbaseline
set m=HWUbaseline
for %%t in (dstc2_train dstc2_dev dstc2_test) do (
	python baseline_HWU.py --dataset=%%t --dataroot=%root% --ontology=%ontology% --trackfile=%outdir%%m%_%%t_track.json
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)
:after_HWUbaseline

goto after_baseline
set m=baseline
for %%t in (dstc2_test) do (
	python baseline.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json
	rem python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	rem python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)
:after_baseline

goto after_baseline_focus
set m=baseline_focus
for %%t in (dstc2_train dstc2_dev dstc2_test) do (
	python baseline.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --focus=True
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)
:after_baseline_focus
