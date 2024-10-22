from glpkhandler import *
import os

if __name__ == "__main__":
    res = run_dir(os.path.abspath("../benchmarks/increasing_borrels"), 10)
    dump_bench("../data", "increasing_borrels.json", res)