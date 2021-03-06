set root=../../data
set m=topline
set outdir=res/score/
set CRFDir=D:/NLP/CRF++-0.58/

goto after_3waymodel_train23
set root=../../data
set m=3way_enrich_train23
for %%t in (test1 test2 test3 test4) do (
	python 3wayDistModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_train23_enrich.dis.label
	python scoreAll.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_allmetrics_%%t_score.txt
)
:after_3waymodel_train23

goto after_3waymodel_train3
set root=../../data
set m=3way_enrich_train3
for %%t in (test1 test2 test3 test4) do (
	python 3wayDistModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_train3_enrich.dis.label
	python scoreAll.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_allmetrics_%%t_score.txt
)
:after_3waymodel_train3

goto after_3waymodel_train2
set root=../../data
set m=3way_enrich_train2
for %%t in (test1 test2 test3 test4) do (
	python 3wayDistModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_train2_enrich.dis.label
	python scoreAll.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_allmetrics_%%t_score.txt
)
:after_3waymodel_train2

goto after_3way_actngram_dis
set m=3way_actngram_dis
for %%t in (test1 test2 test4) do (
	python 3wayDistModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_actngram.dis.label
	rem python 3wayModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_actngram.label
	python scoreAll.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_allmetrics_%%t_score.txt
)

for %%t in (test3) do (
 	python 3wayDistModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_actngram_train3.dis.label
 	python scoreAll.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --scorefile=%outdir%%m%_%%t_score.csv
 	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_allmetrics_%%t_score.txt
 )
:after_3way_actngram_dis

goto after_SummaryError
set m=actngram
for %%t in (test1 test2 test3 test4) do (
	python get3wayError.py --summaryfile=res/%%t_summary.txt --labelfile=res/%%t_%m%.label --logfile=res/%%t_%m%_summary_label.txt
)
:after_SummaryError

goto after_CRF_ActNgram
set root=../../data
set m=3way_crf_actngram
for %%t in (test1 test2 test3 test4) do (
	python 3wayModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_actngram_crf.label
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)
:after_CRF_ActNgram

goto after_CRF_Train_ActNGram
set train=train2
%CRFDir%crf_learn -c 4.0 %outdir%template.unigram %outdir%%train%_actngram.crf %outdir%model_%train%_actngram

for %%t in (test1 test2 test3 test4) do (
	%CRFDir%crf_test -m %outdir%model_%train%_actngram %outdir%%%t_actngram.crf > %outdir%%%t_actngram.out
)
:after_CRF_Train_ActNGram

goto after_CRF_Act
set root=../../data
set m=3way_crf_act
for %%t in (test1 test2 test3 test4) do (
	python 3wayModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_crf.label
	python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)
:after_CRF_Act

goto after_CRF
set root=../../data
set m=3way_crf_act_scoreall
for %%t in (test1 test2 test3 test4) do (
	python 3wayModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_crf.label
	python scoreAll.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --scorefile=%outdir%%m%_%%t_score.csv
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)
:after_CRF

goto after_CRF_Train
set CRFDir=D:/NLP/CRF++-0.58/
set train=train2
%CRFDir%crf_learn -c 4.0 %outdir%template.default %outdir%%train%.crf %outdir%model_%train%

for %%t in (test1 test2 test3 test4) do (
	%CRFDir%crf_test -m %outdir%model_%train% %outdir%%%t.crf > %outdir%%%t.out
)
:after_CRF_Train

rem goto after_3waymodel1
set root=../../data
set m=3way_enrich_voting
rem for %%t in (test1 test2 test3 test4) do (
for %%t in (test1) do (
	for %%a in (0.2 0.4 0.6 0.8 1.0) do (
		for %%b in (0 0.2 0.4 0.6 0.8 1.0) do (
			for %%c in (0 0.2 0.4 0.6 0.8 1.0) do (
				python 3wayModel1.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_enrich_voting.label --w1=%%a --w2=%%b --w3=%%c
				python scoreAll.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --scorefile=%outdir%%m%_%%t_score.csv  --rocbins=100
				python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_allmetrics_%%t_%%a_%%b_%%c_score.txt
			)
		)
	)
)

:after_3waymodel1

goto after_3waymodel
set root=../../data
set m=3way_enrich_voting
rem for %%t in (test1 test2 test3 test4) do (
for %%t in (test1) do (
	python 3wayModel.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --labelfile=%outdir%%%t_enrich_voting.label
	python scoreAll.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --scorefile=%outdir%%m%_%%t_score.csv  --rocbins=200
	python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_allmetrics_%%t_score.txt
)

:after_3waymodel

goto after_summary
rem for %%t in (train1a train2 train3) do (
for %%t in (test1 test2 test3 test4 train1a train2 train3) do (
python getSummary.py --dataset=%%t --dataroot=%root% --logfile=%outdir%%%t_summary.txt
rem python scoreTopK.py --dataset=%%t --dataroot=%root% --trackfile=%m%_%%t_track.json --scorefile=%m%_%%t_score_%%k.csv --topK=%%k
rem python report.py --scorefile=%m%_%t%_score_%k%.csv > %m%_%t%_score_%k%.txt
)
:after_summary

goto after_topline
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
rem for %%t in (test1 test2 test3 test4) do (
for %%t in (test1) do (
	python baseline.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ignorescores
	python scoreAll.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --scorefile=%outdir%%m%_%%t_score.csv
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
