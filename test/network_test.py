import numpy as np
import torch
from src.ast_builder import ASTBuilder
from src.vector_generation import create_similarity_vector, create_occurrence_list
from src.nn.train import train_net, predict

creator = ASTBuilder()
with open('./st/SDD_NH3.ST') as f:
    tokens = creator.parse(f.read())
    sim_vector1 = create_similarity_vector(create_occurrence_list(tokens), create_occurrence_list(tokens))
    print(sim_vector1)

with open('./st/ACTUATOR_3P.ST') as f:
    tokens = creator.parse(f.read())
    sim_vector2 = create_similarity_vector(create_occurrence_list(tokens), create_occurrence_list(tokens))
    print(sim_vector2)

    sim_vectors = np.array([sim_vector1, sim_vector2])

    X = np.tile(sim_vectors,(4,1))
    y = np.tile(np.array([[1], [0]]), (4, 1))
    net = train_net(X, y)
    print(torch.round(predict(net, [sim_vector1])))

