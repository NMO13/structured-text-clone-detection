def create_occurrence_list(tokens):
    token_occurence_dict = {
        "KEYWORD": {},
        "OPERATOR": {},
        "MARKER": {},
        "LITERAL": {},
        "METHOD_IDENTIFIER": {},
        "DATATYPE": {},
        "QUALIFIED_NAME": {},
        "VARIABLE_IDENTIFIER": {},
    }
    for t in tokens:
        if t[0] in token_occurence_dict:
            if t[1] not in token_occurence_dict[t[0]]:
                token_occurence_dict[t[0]][t[1]] = 0
            token_occurence_dict[t[0]][t[1]] += 1
    return token_occurence_dict


def get_shared_keys(categoryA, categoryB):
    common_keys = []
    for key in categoryA:
        if key in categoryB:
            common_keys.append(key)
    return common_keys


def get_unshared_keys(categoryA, categoryB):
    exclusive_keys = []
    for key in categoryA:
        if key not in categoryB:
            exclusive_keys.append(key)
    return exclusive_keys


def create_similarity_vector(tokensA, tokensB):
    sim_score = []
    for category, v in tokensA.items():
        # get all shared keys
        shared_keys = get_shared_keys(tokensA[category], tokensB[category])

        # get all keys exclusively in A
        exclusive_keysA = get_unshared_keys(tokensA[category], tokensB[category])

        # get all keys exclusively in B
        exclusive_keysB = get_unshared_keys(tokensB[category], tokensA[category])

        if not (shared_keys or exclusive_keysA or exclusive_keysB):
            sim_score.append(0.5)
            continue

        freq_diff = 0
        freq_sum = 0

        for shared_key in shared_keys:
            freq_diff += tokensA[category][shared_key] - tokensB[category][shared_key]
            freq_sum += tokensA[category][shared_key] + tokensB[category][shared_key]

        for exclusiveA in exclusive_keysA:
            freq_diff += tokensA[category][exclusiveA]
            freq_sum += tokensA[category][exclusiveA]

        for exclusiveB in exclusive_keysB:
            freq_diff += -tokensA[category][exclusiveB]
            freq_sum += tokensA[category][exclusiveB]

        sim_score.append(1 - freq_diff / freq_sum)
    return sim_score
