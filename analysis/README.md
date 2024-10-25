# Analysis

This folder contains code to generate graphs based on the [data](../data/) obtained from running the [ILP model](../ilp/) on different [benchmarks](../benchmarks/). It uses matplotlib to draw the the graphs.

## Running the project

To run the project please follow the following steps:
1. run `pip install -r requirements.txt`
2. run `python ./src/main.py`
It will place the generated plots in the [plots folder](../data/plots/)

## Project organisation

The project consists of the following files:

| File                             | Description                                                                                     |
|----------------------------------|-------------------------------------------------------------------------------------------------|
| [src/graphs.py](./src/graphs.py) | Contains functions to draw relevant graphs                                                      |
| [src/main.py](./src/main.py)     | The entrypoint of the program                                                                   |
| [src/bench.py](./src/bench.py)   | Contains types and methods to manipulate the data obtained from running the [ILP mode](../ilp/) |