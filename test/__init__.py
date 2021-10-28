import os
from os import listdir
from os.path import isfile, join
from src.vector_generation import create_similarity_vector, create_occurrence_list
st_path = os.path.join(os.environ.get("DATA_PATH"))
onlyfiles = [join(st_path, f) for f in listdir(st_path) if isfile(join(st_path, f))]
print(onlyfiles)

from src.ast_builder import ASTBuilder
creator = ASTBuilder()
for file in onlyfiles:
    print("Parsing file {}".format(file))
    with open(file) as f:
        tokens = creator.parse(f.read())
        print("Similarity Vector: {}".format(
            create_similarity_vector(create_occurrence_list(tokens), create_occurrence_list(tokens))))


