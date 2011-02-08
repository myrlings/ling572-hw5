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
categories = set() #just initializing up top so it's visible
e = 2.71828182845904523536028747135266249775724709369995
instances = {}
expected = {}




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
	
	instances[path] = {}
	instances[path]['true'] = instance_category

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
		result_category = e**summation
		result[category] = result_category
		Z+=result_category

	sys_output_file.write(path)		
	sys_output_file.write(" "+ instance_category +" ")
	
	sorted_categories = sorted(results, key=results.get, reverse=True)
	instance['expected'] = sorted_categories[0]
	
	for category in sorted_categories:
		prob_category_given_instance = result[category] / Z
		sys_output_file.write(" " + category + " "+ prob_category_given_instance)
	sys_output_file.write("\n")
	sys_output_file.close()
		
		
		
		
# #print confusion matrix

print "\nConfusion matrix for the training data:"
print "row is the truth, column is the system output\n"

print "class_num=", len(instances), ", feat_num=", # vectors_labels[2]			Should we be tallying the total number of features or unique features?

counts = {}
num_right = 0
for true_category in categories:
	sys.stdout.write("\t" + true_category)
	counts[true_category] = {}
	for expected_category in categories:
		counts[true_category][expected_category] = 0
for instance in instances:
	true_category = instances[instance]['true']
	expected_category = instances[instance]['expected']
	counts[true_category][expected_category] +=1
	if true_category == expected_category:
		num_right += 1
sys.stdout.write("\n")
for true_category in categories:
	sys.stdout.write(true_category)
	for expected_category in categories:
		sys.stdout.write("\t" + str(counts[true_category][expected_category]))
	sys.stdout.write("\n")
accuracy = float(num_right) / len(instances)

print "Accuracy:",accuracy


# def print_acc(vectors, guesses, labels):
#     counts = {}
#     num_right = 0
#     for actuallabel in labels:
#         sys.stdout.write("\t" + actuallabel)
#         counts[actuallabel] = {}
#         for expectedlabel in labels:
#             counts[actuallabel][expectedlabel] = 0
#     for instance in vectors:
#         actual_label = vectors[instance]['class_label']
#         expected_label = guesses[instance]['winner']
#         counts[actual_label][expected_label] += 1
#         if actual_label == expected_label:
#             num_right += 1
# 
#     sys.stdout.write("\n")
#     for actuallabel in labels:
#         sys.stdout.write(actuallabel)
#         for expectedlabel in labels:
#             sys.stdout.write("\t" + str(counts[actuallabel][expectedlabel]))
#         sys.stdout.write("\n")
#     accuracy = float(num_right) / len(vectors)
#     return accuracy

