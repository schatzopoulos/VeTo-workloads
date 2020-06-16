import sys
import csv
import json
import os  
    
with open(sys.argv[2]) as config_file:
    config = json.load(config_file)
    metapath = config["query"]["metapath"]
    nodes_dir = config["indir"]
    outfile = config["final_out"] 
    select_field = config["select_field"]
    first_entity = metapath[:1]
    operation = config["operation"]

    input_pr = config["analysis_out"]

    # change intermediate file according to analysis type
    if os.path.isdir(config["analysis_out"]): 
        if operation == "community_detection":
            input_pr = config["analysis_out"] + "/level_0_vertices/part-00000" 
        else:
            input_pr = config["analysis_out"] + "/part-00000" 

entity_file = nodes_dir + first_entity + ".csv"

with open(entity_file) as fp:
    
    # read header file
    line = fp.readline()

    fields = line.rstrip().split('\t')
    for i in range(len(fields)):

        if select_field in fields[i]: 
            break

    select_field_idx = i

    # assign names to ids 
    names = {}
    while line:
        line = line.rstrip()
        parts = line.strip().split("\t")
        names[parts[0]] = parts[select_field_idx]
        line = fp.readline()


# read analysis resuls and append names
with open(outfile, 'w', newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    with open(input_pr) as fd:
        
        for line in fd:
        # for line in sys.stdin:

            line = line.rstrip()
            parts = line.split("\t")

            row_data = []

            # convert only first column for community detection output
            cols = 1 if operation == "community_detection" else len(parts)-1

            # loop in all columns except last one
            for col in range(cols):
                # print(parts[col])
                value = 'Unknown'
                if parts[col] in names:
                    parts[col] = parts[col] + "|" + names[parts[col]]

                # row_data.append(parts[col] + "|" + value)

            # append last column that is the score of the analysis
            # row_data.append(parts[len(parts)-1])
            filewriter.writerow(parts)
