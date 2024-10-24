from benches import *

if __name__ == "__main__":
    run(GENERAL_NO_OVERLAP)
    run(GENERAL_OVERLAP)
    run(INCREASING_BORREL_SIZE)
    run(INCREASING_BORRELS)
    run(INCREASING_OBLIGATIONS)
    run(INCREASING_STUDENTS)
    run(INCREASING_TIMESLOTS)
    run(INCREASING_OBLIGATIONS, cust_name="simplification_" + INCREASING_OBLIGATIONS, simpl=True)