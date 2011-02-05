#!/usr/bin/python2.6
import sys
import math

######### functions

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

# given a dictionary of vectors, find the empirical expectation
# for each feature function
def get_expectations(vectors):
    exps = {}
    N=float(len(vectors))
    
    for vector in vectors:
        label = vectors[vector]["_label_"]
        for f in vectors[vector]:
            if f == "_label_":
                continue
            
            if f in exps and label in exps[f]:
                exps[f][label] += 1/N
            elif f in exps:
                exps[f][label] = 1/N
            else:
                exps[f] = {}
                exps[f][label] = 1/N
    return exps

def write_exps(exps, output_filename):
    output = open(output_filename, 'w')

    for feature in exps:
        for label in exps[feature]:
            output.write(label + " ")
            output.write(feature + " ")
            output.write(str(exps[feature][label]) + "\n")

######### main
if len(sys.argv) < 3:
    print "Format is: calc_emp_exp.sh training_data output_file"
    sys.exit()

vectors_labels = get_vectors(sys.argv[1])
vectors = vectors_labels[0]
labels = vectors_labels[1]

exps = get_expectations(vectors)
write_exps(exps, sys.argv[2])
