from bench import *
from graphs import *
import os

if __name__ == "__main__":
    # measurement accuracy graphs
    data = read_bench(os.path.abspath("../data/general_no_overlap.json"))
    data = cut_bench(data, 10)
    timing_acc(data, os.path.abspath("../data/plots/timing_accuracy.pdf"))
    memory_acc(data, os.path.abspath("../data/plots/memory_accuracy.pdf"))