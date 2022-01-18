# Structured Text Code Clone Detection
This tool finds code clones in structured text source code files. Different algorithms have been implemented which leverage supervised and unsupervised machine learning techniques. The different algorithms will be explained in subsequent sections.

It is an implementation of the paper **CCLearner: A Deep Learning-Based Clone
Detection Approach, Liuqing Li et. al**.
You can either use the online version available [here](https://internal.xemedo.com/code-compare/) or you can install it by yourself. Installation instructions are provided below.

## Installation and Execution
Installation can be performed via docker-compose or via direct execution of the Python files.

### Installation via docker-compose
1. Install docker and docker-compose.
2. cd into the directory where the docker-compose file is located.
3. For neural network training, you need to create a `data` directory in the root directory and fill it with structured text code files.
4. `docker-compose up -d --build`

### Installation via Python
1. Install Python 3.8.
2. Install conda.
3. Create a new conda environment via `conda create -n clone_detection python=3.8`
4. Run `pip install -r requirements.txt`
5. Activate the environment `conda activate clone_detection`
6. Run `python main.py`

### Data Path
An environment variable `DATA_PATH` must be set. This variable must point to a data folder which contains the structured text files. The generation of the neural network input data requires the data folder to be in a specific format. This format will be explained in the *Neural Network* section.

### Execution
If everything was done correctly, a selection menu with the implemented algorithms appears. The user can select the desired algorithm from this menu.

## Implemented algorithms

### Neural Network

### Principal Component Analysis

### 


## Usage
1. Open a browser and type `localhost:5000/upload`.
2. The webmask should open.
3. Upload a structured text file which you want to compare.
4. Upload multiple structured text files which you want to compare with the base file.
5. After some seconds, the result table should appear.
