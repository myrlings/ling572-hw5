import sys
import math

########## Functions

# read in the data from the file
# return a dictionary of vectors 
def get_vectors(training_data_filename):
    data_file = open(training_data_filename, 'r')

    vectors = {}
    labels = set()
    for line in data_file:
        line_array = line.split()
        instance_name = line_array[0]
        label = line_array[1]
        features = line_array[2::2] 
        values = line_array[3::2]

        vectors[instance_name] = {}
        vectors[instance_name]["_label_"] = label
        
        labels.add(label)

        for (f, v) in zip(features, values):
            vectors[instance_name][f] = v

    return [vectors, labels]

# read in the model from the file
def get_model(model_filename):
    model_file = open(model_filename, 'r')

    cur_class = ""
    model = {}
    for line in model_file:
        line_array = line.split()

        # check that we're not on a new class
        if line_array[0] == "FEATURES":
            cur_class = line_array[-1]
            model[cur_class] = {}
            continue

        if len(line_array) < 2:
            continue
        model[cur_class][line_array[0]] = line_array[1]
    return model    

# find the model expectations for each feature function
def get_expectations(labels, vectors, model):
    exps = {}
    N = float(len(vectors))
    for vector in vectors:
        result = get_py_x(vectors[vector], model, labels)
        for f in vectors[vector]:
            if f == "_label_":
                continue
            for label in labels:
                py_x = result[label]
                if f in exps and label in exps[f]:
                    exps[f][label] += 1/N * py_x
                elif f in exps:
                    exps[f][label] = 1/N * py_x
                else:
                    exps[f] = {}
                    exps[f][label] = 1/N * py_x
    return exps

def get_py_x(vector, model, labels):
    Z = 0.0
    result = {}
    for label in labels:
        summation = 0.0
        lambda_0 = 0.0
        if "_const_" in model:
            lambda_0 = float(model["_const_"])
        else:
            lambda_0 = float(model[label]["<default>"])
        for feature in vector:
            if feature == "_label_":
                continue
            if "_const_" in model:
                    summation+=float(model["_const_"])
            elif feature in model[label]:
    		    summation+=float(model[label][feature])
        result[label] = math.e**summation
        Z += result[label]

    for label in labels:
        result[label] = result[label]/Z

    return result

        

def write_exps(exps, output_filename):
    output = open(output_filename, 'w')

    for feature in exps:
        for label in exps[feature]:
            output.write(label + " ")
            output.write(feature + " ")
            output.write(str(exps[feature][label]) + "\n")

#def process_model(model, vectors, labels):
#    py_x_model = {}
#    for vector in vectors:
#        Z = 0.0
#        for label in labels:
#            summation = model[label]["<default>"]
#            for feature in vectors[vector]:
#                if feature == "_label_":
#                    continue
#	    		try:
#		    		summation+=model[label][feature]
#			    except KeyError:
#				    summation+=0
#                

########## Main

# read in args
if len(sys.argv) < 3:
    print "Need at least: training_data and output_file"
    sys.exit()

model_filename = ""
if len(sys.argv) > 3:
    model_filename = sys.argv[3]

# read in training_data
vectors_labels = get_vectors(sys.argv[1])
vectors = vectors_labels[0]
labels = vectors_labels[1]

model = {}
if model_filename == "":
    # calculate default values for P(y|x)
    model["_const_"] = 1.0/len(labels)
else:
    # read in model
    model = get_model(model_filename)

#model = process_model(model, vectors, labels)

exps = get_expectations(labels, vectors, model)
write_exps(exps, sys.argv[2])
