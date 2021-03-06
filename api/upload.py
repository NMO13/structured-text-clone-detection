import io
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

def handle_compare_files():
    import os
    from src.create_data import get_paths, get_files
    compare_files = request.files.getlist("file[]")
    # if compare files were not uploaded, use the one on the file system
    if len(compare_files) == 1 and compare_files[0].filename == "":
        _, originalpath, _ = get_paths()
        # get all original files
        compare_files = get_files(originalpath)
    else:
        [check_file(x) for x in compare_files]
        compare_files = [[x.filename, x.read().decode("utf-8")] for x in compare_files]
    return compare_files


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
                compare_files = handle_compare_files()
        except Exception as e:
            return render_template("base.html", error=True)

        # file is valid
        from src.nn.network_functions import predict
        from . import net
        try:
            basetext = basefile.read().decode("utf-8")
            sim_vectors, filenames, exec_times, filesizes = create_similarity_vectors(basetext, compare_files)
        except Exception as e:
            return render_template("base.html", error=True, message=str(e))
        start = time.time()
        logit, probabilities = predict(net, sim_vectors)
        pred_time = time.time() - start
        rounded_probs = map(lambda x: "true" if x[0] == 1 else "false", torch.round(probabilities).cpu().data.numpy())
        nn_result = list(zip(rounded_probs, probabilities.cpu().data.numpy(), filenames, exec_times, filesizes))

        # pca
        expl_ratio = []
        pca_result = [[],[]]
        if len(sim_vectors) > 1:
            df, expl_ratio = calculate_pca(sim_vectors)
            expl_ratio = expl_ratio.tolist()
            pca_result = [df["pca-one"].to_list(), df["pca-two"].to_list()]

        return render_template("upload/result.html", error=False, upload_success=True, basefile=basefile.filename, pred_time=pred_time, overall_time=sum(exec_times), basefile_size=utf8len(basetext), result=nn_result, expl_ratio_data=expl_ratio, pca_result=pca_result, probabilities=probabilities.cpu().data.tolist(), filenames=filenames)


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
        print("comparison file: " + compare_file[0])
        start = time.time()
        #comparetext = compare_file.read().decode("utf-8")
        vector = create_similarity_vector(create_occurrence_list(tokens_base),
                                 create_occurrence_list(creator.parse(compare_file[1])))
        sim_vectors.append(vector)
        filenames.append(compare_file[0])
        filesizes.append(utf8len(compare_file[1]))
        exec_times.append(time.time() - start)

    return sim_vectors, filenames, exec_times, filesizes