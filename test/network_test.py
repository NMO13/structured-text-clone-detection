import numpy as np
import torch
from src.ast_builder import ASTBuilder
from src.vector_generation import create_similarity_vector, create_occurrence_list
from src.nn.train import train_net, predict

creator = ASTBuilder()
with open('./st/SDD_NH3.ST') as f:
    tokens = creator.parse(f.read())
    sim_vector = create_similarity_vector(create_occurrence_list(tokens), create_occurrence_list(tokens))
    print(sim_vector)
    X = np.tile(sim_vector,(4,1))
    y = np.ones(4)
    net = train_net(X, y)
    print(predict(net, [sim_vector]))

