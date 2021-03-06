#from api import create_app
import os

#os.environ["DATA_PATH"] = "C:/Users/AK123847/Documents/GitHub/STCloneDetection/inputtraining"
def check_path():
    import os
    data_path = os.environ.get("DATA_PATH")
    if not data_path:
        raise Exception("The environment variable DATA_PATH was not set. Please set it first to point to your structured text directory.")
    else:
        print("DATA_PATH points to {}".format(data_path))

def yes_no(msg):
    res = input(msg + "[Y/n]")
    if res == "Y" or res == "":
        return True
    elif res == "n":
        return False
    raise Exception("Abort.")

def show_options():
    print("0. Neural Network")
    print("1. Principal Component Analysis")
    print("2. t-distributed stochastic neighbor embedding")
    print("3: Quit")
    return [0, 1, 2, 3]

def choose_selection(available_selections):
    while True:
        sel = int(input("Choose value: "))
        if sel not in available_selections:
            print("Invalid value. Value must be one of {}".format(available_selections))
        else:
            break

    return sel

def boot_flask_server():
    from api import create_app
    print("Booting Flask server....")
    os.environ["FLASK_ENV"] = "production"
    application = create_app()
    application.debug = False
    application.run()

def process_selection(selection):
    from src.create_data import are_similarity_vectors_available
    # neural network
    if selection == 0:
        print("### Neural Network ###")
        print("Checking for available training data...")
        vectors_available = are_similarity_vectors_available()
        if not vectors_available:
            print("Training data not found.")
            res = yes_no("Do you want to create it now?")
            if res:
                from src.create_data import create_training_data
                create_training_data()
            else:
                raise Exception("Abort.")
        else:
            print("Training data found.")
        boot_flask_server()

    # PCA
    elif selection == 1:
        from src.create_data import get_paths, get_files
        from projection.pca import perform
        print("### Principal Component Analysis ###")
        _, original_path, _ = get_paths()
        perform(get_files(original_path))
    # t-SNE
    elif selection == 2:
        from src.create_data import get_paths, get_files
        from projection.tsne import perform
        print("### t-SNE Analysis ###")
        _, original_path, _ = get_paths()
        perform(get_files(original_path))
    elif selection == 3:
        raise Exception("Quit.")



if __name__ == "__main__":
    import os

    try:
        check_path()
        available_selections = show_options()
        selection = choose_selection(available_selections)
        process_selection(selection)
    except Exception as e:
        print(e)