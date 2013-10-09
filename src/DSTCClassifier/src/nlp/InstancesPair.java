package nlp;

import weka.core.Instances;

public class InstancesPair {
	public Instances a;
	public Instances b;
	
	public InstancesPair(Instances a, Instances b){
		this.a = a;
		this.b = b;
	}
}
