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
    current_app.logger.info("Using {} device".format("cuda" if torch.cuda.is_available() else "cpu"))
    if request.method == "GET":
        return render_template("base.html", error=False)
    if request.method == 'POST':
        try:
            if request.values["submit"] == "Upload Files":
                basefile = request.files["file"]
                check_file(basefile)
                compare_files = request.files.getlist("file[]")
                [check_file(x) for x in compare_files]
        except:
            return render_template("base.html", error=True)

        # file is valid
        from src.nn.network_functions import predict
        from . import net
        try:
            sim_vectors, filenames = create_similarity_vectors(basefile, compare_files)
        except Exception as e:
            return render_template("base.html", error=True, message=str(e))
        logit, probabilities = predict(net, sim_vectors)
        rounded_probs = map(lambda x: "true" if x[0] == 1 else "false", torch.round(probabilities).cpu().data.numpy())
        res = zip(rounded_probs, probabilities.cpu().data.numpy(), filenames)

        return render_template("upload/result.html", error=False, upload_success=True, basefile=basefile.filename, result=res)

def check_file(file):
    if not (file and allowed_file(file.filename)):
        raise Exception("Illegal file.")

def create_similarity_vectors(basefile, compare_files):
    from src.vector_generation import create_similarity_vector, create_occurrence_list
    creator = ASTBuilder()
    tokens_base = creator.parse(basefile.read().decode("utf-8"))
    sim_vectors = []
    filenames = []

    for compare_file in compare_files:
        print("comparison file: " + compare_file.filename)
        vector = create_similarity_vector(create_occurrence_list(tokens_base),
                                 create_occurrence_list(creator.parse(compare_file.read().decode("utf-8"))))
        sim_vectors.append(vector)
        filenames.append(compare_file.filename)

    return sim_vectors, filenames