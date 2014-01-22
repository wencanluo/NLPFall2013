set root=../data
set ontology=config/ontology_dstc2.json
set outdir=res/
set CRFDir=D:/NLP/CRF++-0.58/

rem goto after_summary
set m=summary
for %%t in (dstc2_test) do (
	python getSummary.py --dataset=%%t --dataroot=%root% --logfile=%outdir%%%t_%m%.txt
)
:after_summary

goto after_HWUbaseline
set m=HWUbaseline
for %%t in (dstc2_test) do (
	python baseline_HWU.py --dataset=%%t --dataroot=%root% --ontology=%ontology% --trackfile=%outdir%%m%_%%t_track.json
	rem python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	rem python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
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
for %%t in (dstc2_test) do (
	python baseline.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --focus=True
	rem python score.py --dataset=%%t --dataroot=%root% --trackfile=%outdir%%m%_%%t_track.json --ontology=%ontology% --scorefile=%outdir%%m%_%%t_score.csv
	rem python report.py --scorefile=%outdir%%m%_%%t_score.csv > %outdir%%m%_%%t_score.txt
)
:after_baseline_focus