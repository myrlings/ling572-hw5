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
all_features = set()
e = 2.71828182845904523536028747135266249775724709369995
instances = {}



### script ###

#read in model file
model_file = open(model_filename,'r')
model_delineator = "FEATURES FOR CLASS "

category = ""
for line in model_file.readlines():
	if line[0:len(model_delineator)] == model_delineator:
		category = line[len(model_delineator):len(line)].strip('\n')
		model[category] = {}
	else:
		feature,value = line.split()
		model[category][feature] = float(value)
model_file.close()
categories = set(model.keys())



#read in test file, print sys output
test_file = open(test_data_filename, 'r')
sys_output_file = open(sys_output_filename, 'w')
for instance in test_file.readlines():
	instance = instance.split()
	path = instance[0]
	instance_category = instance[1]
	features = instance[2::2]
	
	#this is only relevant in the case that there are duplicate features in the single test file we read in
	all_features = set(features)
	
	values = instance[3::2]
	instances[path] = {}
	instances[path]['true'] = instance_category

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
	
	sorted_categories = sorted(result, key=result.get, reverse=True)	
	instances[path]['expected'] = sorted_categories[0]

	sys_output_file.write(path)		
	sys_output_file.write(" "+ instance_category +" ")
	for category in sorted_categories:
		prob_category_given_instance = result[category] / Z
		sys_output_file.write(" " + category + " "+ str(prob_category_given_instance))
	sys_output_file.write("\n")
sys_output_file.close()
		

#print confusion matrix
print "\nConfusion matrix:"
print "row is the truth, column is the system output\n"
print "class_num=", len(categories), ", feat_num=", len(all_features)
print("\n")
counts = {}
num_right = 0
for true_category in categories:
	sys.stdout.write("\t\t" + true_category)
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
	
	#a hacktastic way of formatting the table
	formatter_index = 0
	sys.stdout.write(true_category)
	for expected_category in categories:
		formatter_index+=1
		if formatter_index ==3:
			sys.stdout.write("\t\t")
		sys.stdout.write("\t\t" + str(counts[true_category][expected_category]))
	sys.stdout.write("\n")
accuracy = float(num_right) / len(instances)
print("\n")
print "Accuracy:",accuracy
print("\n")
