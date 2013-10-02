package dstc;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;

import weka.core.Instances;
import nlp.WekaWrapper;

public class DSTCClassifier {
	
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

	/**
	 * @param args
	 * @throws Exception 
	 */
	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub
		String train = "../SigDial2013/bin/res/train1a";
		String test1 = "../SigDial2013/bin/res/test1";
		String test2 = "../SigDial2013/bin/res/test2";
		String test3 = "../SigDial2013/bin/res/test3";
		String test4 = "../SigDial2013/bin/res/test4";
		
		DSTCClassifier classifier = new DSTCClassifier();
		classifier.Classifier(train, test1);
		//classifier.Classifier(train, test2);
		//classifier.Classifier(train, test3);
		//classifier.Classifier(train, test4);
		
		System.out.println("Finish!");
		
	}

}
