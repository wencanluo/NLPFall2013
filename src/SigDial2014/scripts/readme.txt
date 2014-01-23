Method_Classifier (MindChange Model)
	Step0: Get Summary
		python getSummary.py
	Step0: Get Act List
		python getWekaArff.getActList() > dstc2_train_name.dict
	Step1: Get ARFF file
		python getWekaMethodArff.getWekaARFF_ActwithNameNgramRecovery()
			* Top ASR
			* Acts (51)
			> dstc_train_method_actwithNamengram_mindchange.arff
			> dstc_test_method_actwithNamengram_mindchange.arff
	Step2: Do the method Classifier
		java SigDial2014MethodClassifier
			> dstc_train_method_actwithNamengram_mindchange.label
			> dstc_test_method_actwithNamengram_mindchange.label
	Step3: Run the 2waymodel
		python 2wayModel.py
		
Request_Classifier
	Step1: Get ARFF file
		python getMulanRequestArff.getMulanARFF_ActNgram()
			> dstc_train_request_actngram_slot.arff dstc_train_request_actngram_slot.xml
			> dstc_test_request_actngram_slot.arff dstc_train_request_actngram_slot.xml
	Step2: Do the method Classifier
		java SigDial2014RequestClassifier
			> 
	Step3: Run the 2waymodel
		python 2wayModel.py
		
First-correct model
	Step1: Get NBest Training
		python getWekaArff.getWekaARFFBinarySwitch_ActNgramWithName()
			* Trans_System
			* Trans_SLU
			* Acts (51)
			* Label (H1)
			> dstc2_train_H1_actngram_binaryswitchwithName.arff
			> dstc2_dev_H1_actngram_binaryswitchwithName.arff
		#python getWekaArff.getWekaARFFBinarySwitch_ActWithName
	Step2: Classifier on Dev and Test
		java SigDial2014Classifier
			> dstc2_train_H1_actngram_binaryswitchwithName.label
			> dstc2_dev_H1_actngram_binaryswitchwithName.label
	Step3: Run the BinarySwitch Model
		python FirstCorrectModel.py --topk=2
		
BinarySwitch Model
	Step1: Get NBest Training
		python getWekaArff.getWekaARFFBinarySwitch_ActNgramWithName()
			* Trans_System
			* Trans_SLU
			* Acts (51)
			* Label (H1)
			> dstc2_train_H1_actngram_binaryswitchwithName.arff
			> dstc2_dev_H1_actngram_binaryswitchwithName.arff
		#python getWekaArff.getWekaARFFBinarySwitch_ActWithName
	Step2: Classifier on Dev and Test
		java SigDial2014Classifier > 
	Step3: Run the BinarySwitch Model
		python FirstCorrectModel.py --topk=2
		
NBest model
	Step1: Get NBest Training ARFF for goals
		python getWekaGoalsArff.getWekaARFFBinarySwitch_ASRs()
			* SR ID
			* ASRs (10)
			* Acts (51)
			> dstc2_train_nbest_goals_asrs_L*.arff  #* \in [area, food, name, pricerange]
			> dstc2_dev_nbest_goals_asrs_L*.arff  #* \in [area, food, name, pricerange]
	Step2: Classifier on Dev and Test
		java SigDial2014GoalClassifier.java
	Step3: Combine NBest
		java CombineNBest.py
	Step4: Run the BinarySwitch Model
		python 2wayModel.py
		
Voting Model
	Step1: Get the NBest model
	Step2: Get the baseline_focus, HWUBaseline models
	Step3: Convert the tracker output to the label prediction format
	Step4: Combine them
	
Nbest + HWUBasline
	Step
