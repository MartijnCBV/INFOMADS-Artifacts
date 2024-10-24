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
    timing_double(data_a, data_b, "No Overlap", "Overlap", "Instance", os.path.abspath("../data/plots/overlap_time.pdf"), dashcycle=True)
    memory_double(data_a, data_b, "No Overlap", "Overlap", "Instance", os.path.abspath("../data/plots/overlap_mem.pdf"), dashcycle=True)
    # borrel size
    data = read_bench(os.path.abspath("../data/increasing_borrel_size.json"))
    timing(data, "Borrel Size", os.path.abspath("../data/plots/size_borrels_time.pdf"), dashcycle=True)
    memory(data, "Borrel Size", os.path.abspath("../data/plots/size_borrels_mem.pdf"), dashcycle=True)    
    # no. borrels
    data = read_bench(os.path.abspath("../data/increasing_borrels.json"))
    timing(data, "No. Borrels", os.path.abspath("../data/plots/no_borrels_time.pdf"), dashcycle=True)
    memory(data, "No. Borrels", os.path.abspath("../data/plots/no_borrels_mem.pdf"), dashcycle=True)
    # obligation density
    data = read_bench(os.path.abspath("../data/increasing_obligations.json"))
    timing(data, "Obligation Density(%)", os.path.abspath("../data/plots/obligation_density_time.pdf"), xs=list(range(5, 101, 5)), dashcycle=True)
    memory(data, "Obligation Density(%)", os.path.abspath("../data/plots/obligation_density_mem.pdf"), xs=list(range(5, 101, 5)), dashcycle=True)
    # no. students
    data = read_bench(os.path.abspath("../data/increasing_students.json"))
    timing(data, "No. Students", os.path.abspath("../data/plots/no_students_time.pdf"), dashcycle=True)
    memory(data, "No. Students", os.path.abspath("../data/plots/no_students_mem.pdf"), dashcycle=True)
    # no. timeslots
    data = read_bench(os.path.abspath("../data/increasing_timeslots.json"))
    timing(data, "No. Timeslots", os.path.abspath("../data/plots/no_timeslots_time.pdf"), xs=list(range(100, 1001, 100)), dashcycle=True)
    memory(data, "No. Timeslots", os.path.abspath("../data/plots/no_timeslots_mem.pdf"), xs=list(range(100, 1001, 100)), dashcycle=True)
    # simplification (full)
    data = read_bench(os.path.abspath("../data/simplification_increasing_obligations.json"))
    timing(data, "Obligation Density(%)", os.path.abspath("../data/plots/obligation_density_time_simpl.pdf"), xs=list(range(5, 101, 5)), dashcycle=True)
    memory(data, "Obligation Density(%)", os.path.abspath("../data/plots/obligation_density_mem_simpl.pdf"), xs=list(range(5, 101, 5)), dashcycle=True)
    # simplification (cut)
    data_a = cut_bench(data, 18)
    data_b = read_bench(os.path.abspath("../data/increasing_obligations.json"))
    data_b = cut_bench(data_b, 18)
    timing_double(data_a, data_b, "Simplified", "Normal", "Obligation Density(%)", os.path.abspath("../data/plots/obligation_density_time_simpl_comp.pdf"), xs=list(range(5, 91, 5)), dashcycle=True)
    memory_double(data_a, data_b, "Simplified", "Normal", "Obligation Density(%)", os.path.abspath("../data/plots/obligation_density_mem_simpl_comp.pdf"), xs=list(range(5, 91, 5)), dashcycle=True)