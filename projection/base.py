from collections import defaultdict

def flatten(all_keys, files):
    transformed_files = []
    for file in files:
        flat = defaultdict(lambda: 0)
        for k, v in file.items():
            for k1, v1 in v.items():
                key = "{}_{}".format(k, k1)
                all_keys.append(key)
                flat[key] += v1
        transformed_files.append(flat)
    return transformed_files

def annotate_missing_keys(flattened_files, all_keys):
    for file in flattened_files:
        for k in all_keys:
            if k not in file:
                file[k] = 0

def to_list(flattened_files):
    all = []
    for file in flattened_files:
        sortedKeys = sorted(file)
        all.append([file[k] for k in sortedKeys])
    return all