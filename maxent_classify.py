#command line
#The format is: maxent_classify.sh test_data model_file sys_output > acc_ file

#imports
import sys

#arguments
test_data_filename = sys.argv[1]
model_filename = sys.argv[2]
sys_output_filename = sys.argv[3]

#data structures, constants
model = {}
categories = set()
e = 2.71828182845904523536028747135266249775724709369995




### script ###



#read in model file
model_file = open(model_filename,'r')
model_delineator = "FEATURES FOR CLASS "

for line in model_file.readlines():
	category = ""
	if line[0:len(model_delineator)] == model_delineator:
		category = line[len(model_delineator):len(line)].strip('\n')
		model[category] = {}
	feature,value = line.split()
	model[category][feature] = float(value)
model_file.close()
categories = set(model.keys())



#read in test file, print sys output
test_file = open(test_data_filename, 'r')
sys_output_file = open(sys_output_filename, 'a')

for instance in test_file.readlines():
	instance = instance.split()
	path = instance[0]
	instance_category = instance[1]
	features = instance[2::2]
	values = instance[3::2]

	# Z=0;
	#for each y in Y 
	#		sum = 0;	// or sum = default_weight_for_class_y; 
	#		for each feature t present in x
	# 		sum += the weight for (t, y);
	#		result[y] = exp(sum); 
	#		Z += result[y];
	#for each y in Y
	#		P(y|x) = result[y] / Z;

	result = {}
	Z=0.0
	for category in categories:
		summation = model[category]["<default>"]
		for feature in features:
			try:
				summation+=model[category][feature]
			except KeyError:
				summation+=0
		result_category = ee*summation
		result[category] = result_category
		Z+=result_category

	sys_output_file.write(path)		
	for category in sorted(results, key=results.get, reverse=True):  #do we need to distinguish the winner here?  how about its original label? is our sys file correct for hw3?  am i doing this right at all?
		prob_category_given_instance = result[category] / Z
		sys_output_file.write(" " + category + " "+ prob_category_given_instance)
	sys_output_file.write("\n")
	sys_output_file.close()
		
		
		
		
#print confusion matrix

#not sure where to go on this one yet, hoping we can talk about it -- confusion matrices still have me a bit confused, but i'll check out your previous code tomorrow and that ought to get me a head start