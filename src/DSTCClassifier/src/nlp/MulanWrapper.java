package nlp;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Random;

import java.util.regex.*;

import weka.classifiers.functions.SMO;
import weka.core.Instance;
import weka.core.Instances;

import mulan.classifier.MultiLabelOutput;
import mulan.classifier.lazy.MLkNN;
import mulan.classifier.meta.RAkEL;
import mulan.classifier.transformation.BinaryRelevance;
import mulan.classifier.transformation.LabelPowerset;
import mulan.data.MultiLabelInstances;
import mulan.evaluation.Evaluation;
import mulan.evaluation.Evaluator;
import mulan.evaluation.MultipleEvaluation;

public class MulanWrapper {
	public static MultiLabelInstances LoadData(String xml, String arff) throws Exception{
		MultiLabelInstances dataset = new MultiLabelInstances(arff, xml);
		
		return dataset;
	}
	
	public static Instances LoadData(String data) throws Exception{
		BufferedReader reader = new BufferedReader(new FileReader(data));
		Instances dataset = new Instances(reader);
		reader.close();
		
		return dataset;
	}
	
	public static void PrintResult(Evaluation eval) throws Exception{
		System.out.println(eval);
	}
	
	public static void TrianTest(MultiLabelInstances trainset, MultiLabelInstances testset, String test_arff) throws Exception{
		BinaryRelevance classifier = new BinaryRelevance(new SMO());
		//RAkEL classifier = new RAkEL(new LabelPowerset(new SMO()));
		//MLkNN classifier = new MLkNN();
		
		classifier.build(trainset);
		System.out.println("Classifier is done!");
		
		Evaluator eval = new Evaluator();
		
		//Evaluation result = eval.evaluate(classifier, testset);
		//PrintResult(result);
		
		//GetPridiction(classifier, testset, test + ".label");
		//GetPridictionDistribution(classifier, testset, test + ".dis.label");
		//output the labels
		FileReader reader = new FileReader(test_arff);
		Instances unlabeledData = new Instances(reader);
		
		int numInstances = unlabeledData.numInstances();

		BufferedWriter writer = new BufferedWriter(new FileWriter(test_arff + ".label"));
		//write header
		//writer.newLine();
		
		for (int instanceIndex=0; instanceIndex < numInstances; instanceIndex++) {
		    Instance instance = unlabeledData.instance(instanceIndex);
		    MultiLabelOutput output = classifier.makePrediction(instance);
		    // do necessary operations with provided prediction output, here just print it out
		    //System.out.println(output);
		    writer.write(output.toString());
		    writer.newLine();
		}
		
		writer.flush();
		writer.close();
	}
	
	public static void TrianTest(String train_xml, String train_arff, String test_xml, String test_arff) throws Exception{
		System.out.print(train_arff + "\t");
		MultiLabelInstances trainset = LoadData(train_xml, train_arff);
		System.out.println(trainset.getNumInstances());
		
		System.out.print(test_arff + "\t");
		
		MultiLabelInstances testset = LoadData(test_xml, test_arff);
		System.out.println(testset.getNumInstances());
		
		TrianTest(trainset, testset, test_arff);
	}
	
	public static void main(String[] args) {
		
		String logfile = "log.txt";
		try{
		
			PrintStream out = new PrintStream(new FileOutputStream(logfile));
			PrintStream orgStream = System.out;
			
			System.setOut(out);

			System.setOut(orgStream);
			
			System.out.println("Finsh!");
		}
		catch(Exception e)
		{
			System.out.println(e.toString());
		}
	}
}
