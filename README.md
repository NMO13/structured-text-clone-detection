# Structured Text Code Clone Detection
This tool finds code clones in structured text source code files. Different algorithms have been implemented which leverage supervised and unsupervised machine learning techniques. The different algorithms will be explained in subsequent sections.

It is an implementation of the paper .
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

## Architecural Overview

The following image depicts the workflow of our approach.

![image](https://user-images.githubusercontent.com/3988444/150003726-fdd087d9-055e-4879-a310-e2d5f0c5e457.png)

Step 1. **Function blocks are extracted from the structured text code files.** The extraction was implemented for files with single function blocks. This means that structured text code files with multiple function definitions cannot be analysed yet.

Step 2. **Parsing and abstract syntax tree (AST) creation.** The extracted functions are parsed for syntactical correctness and subsequently transformed into an AST. We employed [pyparsing](https://github.com/pyparsing/pyparsing) for the AST creation as it is simple to use and easy to debug grammatical errors.

Step 3: **Transformation of extracted symbols into token vectors.** This step takes the AST as input and counts the occurrence of individual AST tokens. The result is saved into a Python dictionary whereas the token names are used as keys.

Step 4. **Creating similarity vectors.** In this step, we create a similarity vector between a pair of token vectors and calculate the similarity with respect to each token. This algorithm is similar to the one described in [1]. The similarity vectors are persisted as numpy binary files using pickle. 

Step 5. **Performing training and Inference**. The similarity vectors are the input to all machine learning algorithms. The unsupervised methods (PCA and t-SNE) perform inference directly on these vectors. The neural network uses the vectors as training data.

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


## References
[1] **CCLearner: A Deep Learning-Based Clone Detection Approach, Liuqing Li et. al**
