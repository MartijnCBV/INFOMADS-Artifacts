from glpkhandler import *
import os

GENERAL_NO_OVERLAP = "general_no_overlap"
GENERAL_OVERLAP = "general_overlap"
INCREASING_BORREL_SIZE = "increasing_borrel_size"
INCREASING_BORRELS = "increasing_borrels"
INCREASING_STUDENTS = "increasing_students"
INCREASING_TIMESLOTS = "increasing_timeslots"

def run(id: str):
    res = run_dir(os.path.abspath(f"../benchmarks/{id}"), 10)
    dump_bench("../data", f"{id}.json", res)