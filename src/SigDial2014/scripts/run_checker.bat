set root=../data
set ontology=config/ontology_dstc2.json
set outdir=res/


python check_track.py --dataset=dstc2_test --dataroot=%root% --trackfile=submissions/2waymodel_goals_topASR_dstc2_test_track.json --ontology=%ontology%
python check_track.py --dataset=dstc2_test --dataroot=%root% --trackfile=submissions/nbest_goals_hwu_dstc2_test_track_traindev.json --ontology=%ontology%
python check_track.py --dataset=dstc2_test --dataroot=%root% --trackfile=submissions/nbest_goals_dstc2_test_track_train.json --ontology=%ontology%
python check_track.py --dataset=dstc2_test --dataroot=%root% --trackfile=submissions/nbest_goals_hwu_food_dstc2_test_track_train.json --ontology=%ontology%
python check_track.py --dataset=dstc2_test --dataroot=%root% --trackfile=submissions/nbest_goals_hwu_food_dstc2_test_track_traindev.json --ontology=%ontology%

@pause
