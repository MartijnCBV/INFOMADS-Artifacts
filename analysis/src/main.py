from bench import *
from graphs import *
import os

if __name__ == "__main__":
    # measurement accuracy graphs
    data = read_bench(os.path.abspath("../data/general_no_overlap.json"))
    data = cut_bench(data, 10)
    timing_acc(data, os.path.abspath("../data/plots/timing_accuracy.pdf"))
    memory_acc(data, os.path.abspath("../data/plots/memory_accuracy.pdf"))
    # overlap
    data_a = read_bench(os.path.abspath("../data/general_no_overlap.json"))
    data_a = cut_bench(data_a, 40)
    data_b = read_bench(os.path.abspath("../data/general_overlap.json"))
    data_b = cut_bench(data_b, 40)
    timing_double(data_a, data_b, "No Overlap", "Overlap", "Instance", os.path.abspath("../data/plots/overlap_time.pdf"))
    # no. borrels
    data = read_bench(os.path.abspath("../data/increasing_borrels.json"))
    timing(data, "No. Borrels", os.path.abspath("../data/plots/no_borrels_time.pdf"), dashcycle=True)
    memory(data, "No. Borrels", os.path.abspath("../data/plots/no_borrels_mem.pdf"), dashcycle=True)