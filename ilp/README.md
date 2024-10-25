# Borrels ILP model

This folder houses the ILP model for the borrel scheduling problem, as well as auxiliary code for data gathering and running the glpk solver.

## Running the project
In order to run the project a gew preliminary steps have to be taken:

1. run `pip install -r requirements.txt`
2. install `glpsol`
3. add a new file to the `src` folder called `secrets.py`
4. add the path to your `glpsol` installation to `secrets.py` like follow:
`GLPK_PATH = "absolute/path/to/installation"`

After these steps the program can be executed by running: `python ./src/main.py` 

## Project organisation

The project consists of the following files:

| File                                       | Description                                                                                                 |
|--------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| [gmpl/model.mod](./gmpl/model.mod)         | The ILP model in gmpl format                                                                                |
| [src/main.py](./src/main.py)               | The entrypoint of the program                                                                               |
| [src/benches.py](./src/benches.py)         | Contains paths to different benchmarks and a function to run them                                           |
| [src/model.py](./src/model.py)             | Contains the python representation of instances and some elementary functions to handle these instances     |
| [src/glpkhandler.py](./src/glpkhandler.py) | Contains all logic having to do with glpk/glpsol and processing the instance format to the gmpl data format |
| [src/simplifier.py](./src/simplifier.py)   | Contains functions to simplify problem instances                                                            |