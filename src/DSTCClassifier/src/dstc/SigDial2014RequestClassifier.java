package dstc;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.PrintStream;

import nlp.InstancesPair;
import nlp.MulanWrapper;
import nlp.StringVectorWrapper;
import nlp.WekaWrapper;

import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.classifiers.functions.SMO;
import weka.core.Attribute;
import weka.core.Instance;
import weka.core.Instances;

public class SigDial2014RequestClassifier {
	
	void Classifier(String train, String test) throws Exception{
		WekaWrapper wekaWapper = new WekaWrapper();
		
		Instances dataTrain = new Instances(new BufferedReader(new FileReader(train+".arff")));
		dataTrain.setClassIndex(dataTrain.numAttributes()-1);
		
		Instances dataTest = new Instances(new BufferedReader(new FileReader(test+".arff")));
		dataTest.setClassIndex(dataTest.numAttributes()-1);
		
		int n = dataTrain.numInstances();
		System.out.println("train:" + train);
		System.out.println("test:" + test);
		System.out.println("Train: " + n);
		System.out.println("Test: " + dataTest.numInstances());
		
		wekaWapper.TrianTest(dataTrain, dataTest, test);
	}
	
	void ClassifierNgram(String train, String test) throws Exception{
		WekaWrapper wekaWapper = new WekaWrapper();
		
		Instances dataTrain = new Instances(new BufferedReader(new FileReader(train+".arff")));
		dataTrain.setClassIndex(dataTrain.numAttributes()-1);
		
		Instances dataTest = new Instances(new BufferedReader(new FileReader(test+".arff")));
		dataTest.setClassIndex(dataTest.numAttributes()-1);
		
		int n = dataTrain.numInstances();
		System.out.println("train:" + train);
		System.out.println("test:" + test);
		System.out.println("Train: " + n);
		System.out.println("Test: " + dataTest.numInstances());
		
		StringVectorWrapper ngramWrapper = new StringVectorWrapper();
		InstancesPair p = ngramWrapper.ApplyStringVectorFilter(dataTrain, "ASR", dataTest);
		dataTrain = p.a;
		dataTest = p.b;
		
		wekaWapper.SaveInstances(dataTrain, train + "_ngram.arff");
		wekaWapper.SaveInstances(dataTest, test + "_ngram.arff");
		
		MulanWrapper mulanWrapper = new MulanWrapper();
		
		mulanWrapper.TrianTest( train + ".xml", train + "_ngram.arff", test + ".xml", test + "_ngram.arff");
	}
	
	/**
	 * @param args
	 * @throws Exception 
	 */
	public static void main(String[] args) throws Exception {
		PrintStream oldout = System.out;
		File f = new File("res_request_asr_act_score_all2.txt");		
		System.setOut(new PrintStream(f));
		
		SigDial2014RequestClassifier classifier = new SigDial2014RequestClassifier();
		
		//Act + Ngram, MindChange
		String train = "../SigDial2014/scripts/res/dstc2_train_request_asr_act_score";
		String trainall = "../SigDial2014/scripts/res/dstc2_train_request_asr_act_score_all";
		String dev = "../SigDial2014/scripts/res/dstc2_dev_request_asr_act_score_all";
		String traindev = "../SigDial2014/scripts/res/dstc2_traindev_request_asr_act_score";
		String test = "../SigDial2014/scripts/res/dstc2_test_request_asr_act_score_all";
		
		//classifier.ClassifierNgram(train, trainall);
		//classifier.ClassifierNgram(train, dev);
		classifier.ClassifierNgram(traindev, test);
		
		System.setOut(oldout);
		
		System.out.println("Finish!");
	}

}
