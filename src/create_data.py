import os
from tqdm import tqdm
from random import shuffle
import csv
import numpy as np
from src.ast_builder import ASTBuilder
from src.vector_generation import create_similarity_vector, create_occurrence_list
from src.dataloading import save_data

def get_paths():
    data_path = os.path.join(os.environ.get("DATA_PATH"))
    originalpath = os.path.join(data_path, "original")
    registry_path = os.path.join(data_path, "registry")
    return data_path, originalpath, registry_path

non_parsable_counter = 0

def are_similarity_vectors_available():
    onlyfiles = get_similarity_vectors()
    return len(onlyfiles) != 0

def get_similarity_vectors():
    import pathlib
    path = pathlib.Path(__file__).parent.resolve()
    data_path = os.path.join(path, "../data")
    if not os.path.isdir(data_path):
        return []
    return [os.path.join(data_path, f) for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f))]

def read_registry():
    _, _, registry_path = get_paths()
    csv_file = os.path.join(registry_path, "registry.csv")
    file_dict = {}
    with open(csv_file) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            file_dict[row["#ID"]] = row
    return file_dict


def get_clone_file(filenumber):
    registry = read_registry()
    data_path, _, _ = get_paths()
    path_to_file = os.path.join(data_path, "originalandclones", "clones", registry[filenumber]["Filename"].strip())
    with open(path_to_file) as f:
        return f.read()

def get_registry_file(filename):
    _, _, registry_path = get_paths()
    path_to_file = os.path.join(registry_path, "TRAINED_" + filename + ".txt")
    with open(path_to_file) as f:
        return f.readlines()

def add_datapoint(filenumber, creator, tokens_first, label, X, y):
    global non_parsable_counter
    second_file = get_clone_file(filenumber)
    try:
        tokens_second = creator.parse(second_file)
    except Exception as e:
        non_parsable_counter += 1
        return
    sim_vector = create_similarity_vector(create_occurrence_list(tokens_first), create_occurrence_list(tokens_second))
    X.append(sim_vector)
    y.append(np.array([label]))


def create_training_data():
    _, originalpath, _ = get_paths()
    # get all original files
    originalfiles = [f for f in os.listdir(originalpath) if os.path.isfile(os.path.join(originalpath, f)) and ".csv" not in f]

    creator = ASTBuilder()

    for i in tqdm(range(len(originalfiles))):
        X = []
        y = []
        originalfile = originalfiles[i]
        content = get_registry_file(originalfile)
        file_number_first = content[0].split(" ")[3][1:]
        first_file = get_clone_file(file_number_first)
        tokens_first = creator.parse(first_file)

#todo extract to method
#############################
        clones = content[1].replace("Clones:", "").split(",")
        clones.remove("\n")
        if len(clones) == 1:
            clones = []

        for clone in clones:
            clone_nr = clone.strip()
            if file_number_first == clone_nr:
                continue
            add_datapoint(clone.strip(), creator, tokens_first, 1, X, y)

#############################
        non_clones = content[2].replace("Non Clones:", "").split(",")
        non_clones.remove("\n")
        if len(non_clones) == 1:
            non_clones = []

        # perform under-sampling
        shuffle(non_clones)
        len_X_clones = len(X)

        for non_clone in non_clones:
            non_clone_nr = non_clone.strip()
            if file_number_first == non_clone_nr:
                continue
            if len(X) == len_X_clones * 2:
                break
            add_datapoint(non_clone_nr, creator, tokens_first, 0, X, y)

        if len(X) == 0:
            print("No valid clonedata found.")
            continue

        print("Saving data...")
        save_data(originalfile, X, y)
        print("Finished.")
        print("{} files could not be parsed".format(non_parsable_counter))


if __name__ == "__main__":
    create_training_data()
