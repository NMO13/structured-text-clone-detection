from os import listdir
from os.path import isfile, join
st_path = "./st/"
onlyfiles = [join(st_path, f) for f in listdir(st_path) if isfile(join(st_path, f))]
print(onlyfiles)

from src.ast_builder import ASTBuilder
creator = ASTBuilder()
for file in onlyfiles:
    print("Parsing file {}".format(file))
    with open(file) as f:
        print(creator.parse(f.read()))

