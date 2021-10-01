import os
import csv
import numpy as np
from src.ast_builder import ASTBuilder
from src.vector_generation import create_similarity_vector, create_occurrence_list

data_path = os.path.join(os.environ.get("DATA_PATH"))
registry_path = os.path.join(data_path, "registry")
non_parsable_counter = 0

def read_registry(data_path):
    csv_file = os.path.join(registry_path, "registry.csv")
    file_dict = {}
    with open(csv_file) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            file_dict[row["#ID"]] = row
    return file_dict

registry = read_registry(data_path)

def get_st_file(filenumber):
    path_to_file = os.path.join(data_path, "originalandclones", "clones", registry[filenumber]["Filename"].strip())
    with open(path_to_file) as f:
        return f.read()

def add_datapoint(filenumber, creator, tokens_first, label, X, y):
    global non_parsable_counter
    print("Parsing second file: {} ({})".format(registry[filenumber]["Filename"].strip(), registry[filenumber]["#ID"].strip()))
    second_file = get_st_file(filenumber)
    try:
        tokens_second = creator.parse(second_file)
    except Exception as e:
        print("Could not be parsed.")
        non_parsable_counter += 1
        return
    sim_vector = create_similarity_vector(create_occurrence_list(tokens_first), create_occurrence_list(tokens_second))
    X.append(sim_vector)
    y.append(np.array([label]))

def main():
    # read all files from registry.csv
  #  registry = read_registry(data_path)
    onlyfiles = [os.path.join(registry_path, f) for f in os.listdir(registry_path) if os.path.isfile(os.path.join(registry_path, f)) and ".csv" not in f]

    creator = ASTBuilder()
    X = []
    y = []

    for file in onlyfiles:
        with open(file) as file:
            content = file.readlines()
            file_number_first = content[0].split(" ")[3][1:]

            clones = content[1].replace("Clones:", "").split(",")
            if len(clones) == 1:
                clones = []

            non_clones = content[2].replace("Non Clones:", "").split(",")
            if len(non_clones) == 1:
                non_clones = []

            first_file = get_st_file(file_number_first)
            tokens_first = creator.parse(first_file)

            for clone in clones:
                clone_nr = clone.strip()
                if file_number_first == clone_nr:
                    continue
                add_datapoint(clone.strip(), creator, tokens_first, 1, X, y)

            for non_clone in non_clones:
                non_clone_nr = non_clone.strip()
                if file_number_first == non_clone_nr:
                    continue
                add_datapoint(non_clone_nr, creator, tokens_first, 0, X, y)

if __name__ == "__main__":
    main()