import torch
from src.ast_builder import ASTBuilder

ALLOWED_EXTENSIONS = {"st"}

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, make_response
)
bp = Blueprint('upload', __name__, url_prefix='/upload')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/', methods=("POST", "GET"))
def upload():
    if request.method == "GET":
        return render_template("upload/fileupload.html", error=False)
    if request.method == 'POST':
        try:
            if request.values["submit"] == "Upload Files":
                basefile = request.files["file"]
                check_file(basefile)
                compare_files = request.files.getlist("file[]")
                [check_file(x) for x in compare_files]
        except:
            return render_template("upload/fileupload.html", error=True)

        # file is valid
        from src.nn.network_functions import predict
        from . import net
        sim_vectors = create_similarity_vectors(basefile, compare_files)
        logit, probability = predict(net, sim_vectors)



        return render_template("upload/fileupload.html", error=False, upload_success=True, result=torch.round(probability).cpu().data.numpy())

def check_file(file):
    if not (file and allowed_file(file.filename)):
        raise Exception("Illegal file.")

def create_similarity_vectors(basefile, compare_files):
    from src.vector_generation import create_similarity_vector, create_occurrence_list
    creator = ASTBuilder()
    tokens_base = creator.parse(basefile.read().decode("utf-8"))
    sim_vectors = []

    for compare_file in compare_files:
        print("comparison file: " + compare_file.filename)
        vector = create_similarity_vector(create_occurrence_list(tokens_base),
                                 create_occurrence_list(creator.parse(compare_file.read().decode("utf-8"))))
        sim_vectors.append(vector)

    return sim_vectors