# structured-text-clone-detection
This tool finds code clones in structured text files.
You can either use the online version available [here](https://internal.xemedo.com/code-compare/) or you can install it by yourself. Installation instructions are provided below.

## Installation
1. Install docker and docker-compose.
2. cd into the directory where the docker-compose file is located.
3. For neural network training, you need to create a `data` directory in the root directory and fill it with structured text code files.
4. `docker-compose up -d --build`

## Usage
1. Open a browser and type `localhost:5000/upload`.
2. The webmask should open.
3. Upload a structured text file which you want to compare.
4. Upload multiple structured text files which you want to compare with the base file.
5. After some seconds, the result table should appear.
