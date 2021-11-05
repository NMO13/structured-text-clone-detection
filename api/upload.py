import torch
import time
from src.ast_builder import ASTBuilder
from src.nn.projections.pca import calculate_pca

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
        import json
        try:
            basetext = basefile.read().decode("utf-8")
            sim_vectors, filenames, exec_times, filesizes = create_similarity_vectors(basetext, compare_files)
        except Exception as e:
            return render_template("base.html", error=True, message=str(e))
        start = time.time()
        logit, probabilities = predict(net, sim_vectors)
        pred_time = time.time() - start
        rounded_probs = map(lambda x: "true" if x[0] == 1 else "false", torch.round(probabilities).cpu().data.numpy())
        res = zip(rounded_probs, probabilities.cpu().data.numpy(), filenames, exec_times, filesizes)
        df, expl_ratio = calculate_pca()


        return render_template("upload/result.html", error=False, upload_success=True, basefile=basefile.filename, pred_time=pred_time, overall_time=sum(exec_times), basefile_size=utf8len(basetext), result=res, expl_ratio_data=expl_ratio.tolist())


def utf8len(s):
    return len(s.encode('utf-8'))

def check_file(file):
    if not (file and allowed_file(file.filename)):
        raise Exception("Illegal file.")

def create_similarity_vectors(basetext, compare_files):
    from src.vector_generation import create_similarity_vector, create_occurrence_list
    creator = ASTBuilder()
    tokens_base = creator.parse(basetext)
    sim_vectors = []
    filenames = []
    exec_times = []
    filesizes = []

    for compare_file in compare_files:
        print("comparison file: " + compare_file.filename)
        start = time.time()
        comparetext = compare_file.read().decode("utf-8")
        vector = create_similarity_vector(create_occurrence_list(tokens_base),
                                 create_occurrence_list(creator.parse(comparetext)))
        sim_vectors.append(vector)
        filenames.append(compare_file.filename)
        filesizes.append(utf8len(comparetext))
        exec_times.append(time.time() - start)

    return sim_vectors, filenames, exec_times, filesizes