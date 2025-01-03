from glpkhandler import *
import os

GENERAL_NO_OVERLAP = "general_no_overlap"
GENERAL_OVERLAP = "general_overlap"
INCREASING_BORREL_SIZE = "increasing_borrel_size"
INCREASING_BORRELS = "increasing_borrels"
INCREASING_OBLIGATIONS = "increasing_obligations"
INCREASING_STUDENTS = "increasing_students"
INCREASING_TIMESLOTS = "increasing_timeslots"

def run(id: str, cust_name="", simpl=False):
    res = run_dir(os.path.abspath(f"../benchmarks/{id}"), 10, simpl)
    if cust_name != "":
        id = cust_name
    dump_bench("../data", f"{id}.json", res)