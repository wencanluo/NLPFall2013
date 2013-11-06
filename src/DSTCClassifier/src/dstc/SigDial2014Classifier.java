package dstc;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.PrintStream;

import nlp.InstancesPair;
import nlp.StringVectorWrapper;
import nlp.WekaWrapper;

import weka.core.Instances;

public class SigDial2014Classifier {
	
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
	
	void ClassifierwithCostMatrix(String train, String test, String cm) throws Exception{
		WekaWrapper wekaWapper = new WekaWrapper();
		
		Instances dataTrain = new Instances(new BufferedReader(new FileReader(train+".arff")));
		dataTrain.setClassIndex(dataTrain.numAttributes()-1);
		
		dataTrain = wekaWapper.applyCostMatrix(dataTrain, cm);
		
		Instances dataTest = new Instances(new BufferedReader(new FileReader(test+".arff")));
		dataTest.setClassIndex(dataTest.numAttributes()-1);
		
		int n = dataTrain.numInstances();
		System.out.println("train:" + train);
		System.out.println("test:" + test);
		System.out.println("Train: " + n);
		System.out.println("Test: " + dataTest.numInstances());
		
		wekaWapper.TrianTest(dataTrain, dataTest, test+"_cost");
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
		
		wekaWapper.SaveInstances(dataTrain, train + "_bak.arff");
		
		wekaWapper.TrianTest(dataTrain, dataTest, test);
	}
	
	/**
	 * @param args
	 * @throws Exception 
	 */
	public static void main(String[] args) throws Exception {
		PrintStream oldout = System.out;
		File f = new File("log.txt");		
		System.setOut(new PrintStream(f));
		
		SigDial2014Classifier classifier = new SigDial2014Classifier();
		
		//Act
		///*
		String train = "../SigDial2014/scripts/res/dstc2_train_act";
		String dev = "../SigDial2014/scripts/res/dstc2_dev_act";
		classifier.Classifier(train, train);
		classifier.Classifier(train, dev);
		//*/
		
		//Act + Ngram
		/*String train = "../SigDial2014/scripts/res/dstc2_train_actngram";
		String dev = "../SigDial2014/scripts/res/dstc2_dev_actngram";
		
		classifier.ClassifierNgram(train, train);
		classifier.ClassifierNgram(train, dev);*/
		
		//String test2 = "../SigDial2013/bin/res/test2_actngram";
		//String test3 = "../SigDial2013/bin/res/test3_actngram";
		//String test4 = "../SigDial2013/bin/res/test4_actngram";
		
		//Enrich
		/*
		String train = "../SigDial2013/bin/res/train2_enrich";
		String test1 = "../SigDial2013/bin/res/test1_enrich";
		String test2 = "../SigDial2013/bin/res/test2_enrich";
		String test3 = "../SigDial2013/bin/res/test3_enrich";
		String test4 = "../SigDial2013/bin/res/test4_enrich";
		String train3 = "../SigDial2013/bin/res/train3_enrich";
		*/
		
		//String train = "../SigDial2013/bin/res/train2_train2_enrich";
		//String test1 = "../SigDial2013/bin/res/test1_train2_enrich";
		//String test2 = "../SigDial2013/bin/res/test2_train2_enrich";
		//String test3 = "../SigDial2013/bin/res/test3_train2_enrich";
		//String test4 = "../SigDial2013/bin/res/test4_train2_enrich";
		
		//String train = "../SigDial2013/bin/res/train3_train3_enrich";
		//String test1 = "../SigDial2013/bin/res/test1_train3_enrich";
		//String test2 = "../SigDial2013/bin/res/test2_train3_enrich";
		//String test3 = "../SigDial2013/bin/res/test3_train3_enrich";
		//String test4 = "../SigDial2013/bin/res/test4_train3_enrich";
		
		//String train = "../SigDial2013/bin/res/train23_train23_enrich";
		//String test1 = "../SigDial2013/bin/res/test1_train23_enrich";
		//String test2 = "../SigDial2013/bin/res/test2_train23_enrich";
		//String test3 = "../SigDial2013/bin/res/test3_train23_enrich";
		//String test4 = "../SigDial2013/bin/res/test4_train23_enrich";
		
		//Train on train3
		//String train3 = "../SigDial2013/bin/res/train3_actngram_train3";
		//String test1 = "../SigDial2013/bin/res/test1_actngram_train3";
		//String test2 = "../SigDial2013/bin/res/test2_actngram_train3";
		//String test3 = "../SigDial2013/bin/res/test3_actngram_train3";
		//String test4 = "../SigDial2013/bin/res/test4_actngram_train3";
		
		//Train on train2 + train3
		//String train = "../SigDial2013/bin/res/train23_actngram_train23";
		//String test1 = "../SigDial2013/bin/res/test1_actngram_train23";
		//String test2 = "../SigDial2013/bin/res/test2_actngram_train23";
		//String test3 = "../SigDial2013/bin/res/test3_actngram_train23";
		//String test4 = "../SigDial2013/bin/res/test4_actngram_train23";
		
		//Self Training
		/*String train1 = "../SigDial2013/bin/res/test1_actngram_selftraining";
		String train2 = "../SigDial2013/bin/res/test2_actngram_selftraining";
		String train3 = "../SigDial2013/bin/res/test3_actngram_selftraining";
		String train4 = "../SigDial2013/bin/res/test4_actngram_selftraining";
		
		String test1 = "../SigDial2013/bin/res/test1_actngram";
		String test2 = "../SigDial2013/bin/res/test2_actngram";
		String test3 = "../SigDial2013/bin/res/test3_actngram";
		String test4 = "../SigDial2013/bin/res/test4_actngram";
		
		classifier.ClassifierNgram(train1, test1);
		classifier.ClassifierNgram(train2, test2);
		classifier.ClassifierNgram(train3, test3);
		classifier.ClassifierNgram(train4, test4);*/
		
		/*classifier.ClassifierNgram(train, train);
		classifier.ClassifierNgram(train, test1);
		classifier.ClassifierNgram(train, test2);
		classifier.ClassifierNgram(train3, test3);
		classifier.ClassifierNgram(train, test4);*/
		
		System.setOut(oldout);
		
		System.out.println("Finish!");
	}

}
