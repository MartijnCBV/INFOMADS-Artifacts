/* parameters */
param n;                                # number of students
param m;                                # number of borrels
param t;                                # number of timeslots
param ell{i in 1..n};                   # number of obligations belonging to student i
param r{i in 1..n, j in 1..ell[i]};     # start time for obligation j of student i
param d{i in 1..n, j in 1..ell[i]};     # end time for obligation j of student i
param p{i in 1..n, j in 1..ell[i]};     # number of timeslots needed for obligation j of student i
param b{h in 1..m};                     # number of timeslots borrel h takes

# decision variables
var x{h in 1..m, i in 1..n, j in 1..ell[i]}, binary;    # conflict between borrel h and obligation j of student i

# auxiliary variables
var y{i in 1..n, j in 1..ell[i], k in 1..t}, binary;    # if student i assigns timeslot k to obligation j
var z{h in 1..m, k in 1..t}, binary;                    # if borrel h starts at timeslot k

# constraints

# 1. every obligation must be scheduled exactly p_{i,j} times within its time window
s.t. obligation_timeslot{i in 1..n, j in 1..ell[i]}:
    sum{k in r[i,j]..d[i,j]-1} y[i,j,k] = p[i,j];

# 2. obligations of the same student should not overlap
s.t. no_overlap{i in 1..n, k in 1..t}:
    sum{j in 1..ell[i]} y[i,j,k] <= 1;

# 3. obligations can only be scheduled in the interval (r_{i,j},d_{i,j}]
s.t. obligation_bounds{i in 1..n, j in 1..ell[i], k in 1..t}:
    y[i,j,k] <= (if k >= r[i,j] && k < d[i,j] then 1 else 0);

# 4. each borrel must be scheduled exactly once
s.t. schedule_borrel{h in 1..m}:
    sum{k in 1..t-b[h]+1} z[h,k] = 1;

# 5. borrel cannot be scheduled beyond the last available time slot
s.t. borrel_bound{h in 1..m, k in 1..t}:
    (k + b[h] - 1) * z[h,k] <= t;

# 6. borrels should not overlap
s.t. no_borrel_overlap{k in 1..t}:
    sum{h in 1..m, k2 in max(1,k-b[h])..k} z[h,k2] <= 1;

# 6. conflict between borrel and obligation
s.t. conflict{h in 1..m, i in 1..n, j in 1..ell[i], k in 1..t, k2 in k..min(t, k+b[h]-1)}:
    x[h,i,j] >= y[i,j,k2] + z[h,k] - 1;

# objective function: minimize conflicts
minimize total_conflicts:
    sum{h in 1..m, i in 1..n, j in 1..ell[i]} x[h,i,j];


solve;


# report
printf "Cost: %d\n", sum{h in 1..m, i in 1..n, j in 1..ell[i]} x[h,i,j];
printf "Borrels:\n";
printf {h in 1..m, k in 1..t: z[h,k] = 1} "Borrel %d starts at time slot %d\n", h, k;
printf "Student obligations:\n";
printf {i in 1..n, j in 1..ell[i], k in 1..t: y[i,j,k] = 1} "Student %d obligation %d assigned time slot %d\n", i, j, k;
printf {h in 1..m, i in 1..n, j in 1..ell[i]: x[h,i,j] = 1} "Conflict between borrel %d and obligation %d of student %d\n", h,i,j;

end;