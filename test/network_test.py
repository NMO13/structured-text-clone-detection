import torch
from src.ast_builder import ASTBuilder
from src.vector_generation import create_similarity_vector, create_occurrence_list
from src.nn.network_functions import train_net, predict
from src.network_trainer import train
from numpy import dot
from numpy.linalg import norm

def cosine_similarity(tokensA, tokensB):
    from src.vector_generation import get_shared_keys, get_unshared_keys
    vectorA = []
    vectorB = []
    for category, v in tokensA.items():
        categoryA = tokensA[category]
        categoryB = tokensB[category]
        # get all shared keys
        shared_keys = get_shared_keys(categoryA, categoryB)

        # get all keys exclusively in A
        exclusive_keysA = get_unshared_keys(categoryA, categoryB)

        # get all keys exclusively in B
        exclusive_keysB = get_unshared_keys(categoryB, categoryA)

        for shared_key in shared_keys:
            vectorA.append(categoryA[shared_key])
            vectorB.append(categoryB[shared_key])

        for exclusiveA in exclusive_keysA:
            vectorA.append(categoryA[exclusiveA])
            vectorB.append(0)

        for exclusiveB in exclusive_keysB:
            vectorA.append(0)
            vectorB.append(categoryB[exclusiveB])

        cos_sim = dot(vectorA, vectorB) / (norm(vectorA) * norm(vectorB))
        return cos_sim


creator = ASTBuilder()
manualclones_path = "/home/martin/Martin/Uni/Artificial Intelligence/Practical_Work/data/synthetic data/manualclones/" # add path here
with open('{}Original.ST'.format(manualclones_path)) as f:
    tokens_original = creator.parse(f.read())

with open('{}Clone1.ST'.format(manualclones_path)) as f:
    tokens_clone1 = creator.parse(f.read())

with open('{}Clone2.ST'.format(manualclones_path)) as f:
    tokens_clone2 = creator.parse(f.read())

with open('{}Clone3.ST'.format(manualclones_path)) as f:
    tokens_clone3 = creator.parse(f.read())

with open('{}NonClone1.ST'.format(manualclones_path)) as f:
    tokens_nonclone1 = creator.parse(f.read())

with open('{}NonClone2.ST'.format(manualclones_path)) as f:
    tokens_nonclone2 = creator.parse(f.read())

with open('{}NonClone3.ST'.format(manualclones_path)) as f:
    tokens_nonclone3 = creator.parse(f.read())

sim_vector1 = create_similarity_vector(create_occurrence_list(tokens_original), create_occurrence_list(tokens_original))
sim_vector2 = create_similarity_vector(create_occurrence_list(tokens_original), create_occurrence_list(tokens_clone1))
sim_vector3 = create_similarity_vector(create_occurrence_list(tokens_original), create_occurrence_list(tokens_clone2))
sim_vector4 = create_similarity_vector(create_occurrence_list(tokens_original), create_occurrence_list(tokens_clone3))
sim_vector5 = create_similarity_vector(create_occurrence_list(tokens_clone1), create_occurrence_list(tokens_clone2))
sim_vector6 = create_similarity_vector(create_occurrence_list(tokens_clone2), create_occurrence_list(tokens_clone3))
sim_vector7 = create_similarity_vector(create_occurrence_list(tokens_clone1), create_occurrence_list(tokens_clone3))

sim_vector8 = create_similarity_vector(create_occurrence_list(tokens_original), create_occurrence_list(tokens_nonclone1))
sim_vector9 = create_similarity_vector(create_occurrence_list(tokens_original), create_occurrence_list(tokens_nonclone2))
sim_vector10 = create_similarity_vector(create_occurrence_list(tokens_original), create_occurrence_list(tokens_nonclone3))
sim_vector11 = create_similarity_vector(create_occurrence_list(tokens_nonclone1), create_occurrence_list(tokens_nonclone3))
sim_vector12 = create_similarity_vector(create_occurrence_list(tokens_nonclone2), create_occurrence_list(tokens_nonclone3))

net = train()
logit, probability = predict(net, [sim_vector1, sim_vector2, sim_vector3, sim_vector4, sim_vector5, sim_vector6, sim_vector7, sim_vector8, sim_vector9, sim_vector10, sim_vector11, sim_vector12])
print(torch.round(probability))

######## cosine similarity

print("Cosine Similarity:")
print(cosine_similarity(create_occurrence_list(tokens_original), create_occurrence_list(tokens_original)))
print(cosine_similarity(create_occurrence_list(tokens_original), create_occurrence_list(tokens_clone1)))
print(cosine_similarity(create_occurrence_list(tokens_original), create_occurrence_list(tokens_clone2)))
print(cosine_similarity(create_occurrence_list(tokens_original), create_occurrence_list(tokens_clone3)))
print(cosine_similarity(create_occurrence_list(tokens_clone1), create_occurrence_list(tokens_clone2)))
print(cosine_similarity(create_occurrence_list(tokens_clone2), create_occurrence_list(tokens_clone3)))
print(cosine_similarity(create_occurrence_list(tokens_clone1), create_occurrence_list(tokens_clone3)))

print(cosine_similarity(create_occurrence_list(tokens_original), create_occurrence_list(tokens_nonclone1)))
print(cosine_similarity(create_occurrence_list(tokens_original), create_occurrence_list(tokens_nonclone2)))
print(cosine_similarity(create_occurrence_list(tokens_original), create_occurrence_list(tokens_nonclone3)))
print(cosine_similarity(create_occurrence_list(tokens_nonclone1), create_occurrence_list(tokens_nonclone3)))
print(cosine_similarity(create_occurrence_list(tokens_nonclone2), create_occurrence_list(tokens_nonclone3)))
