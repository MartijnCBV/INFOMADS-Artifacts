from typing import TypedDict
import re

class Obligation(TypedDict):
    start: int
    end: int
    duration: int

type Student = list[Obligation]

class Instance(TypedDict):
    timeslots: int
    borrels: list[int]
    students: list[Student]

# Parameters see ILP formulation

def n(instance: Instance) -> int:
    return len(instance["students"])

def m(instance: Instance) -> int:
    return len(instance["borrels"])

def t(instance: Instance) -> int:
    return instance["timeslots"]

def ell(instance: Instance, i: int) -> int:
    return len(instance["students"][i])

def r(instance: Instance, i: int, j: int) -> int:
    return instance["students"][i][j]["start"]

def d(instance: Instance, i: int, j: int) -> int:
    return instance["students"][i][j]["end"]

def p(instance: Instance, i: int, j: int) -> int:
    return instance["students"][i][j]["duration"]

def b(instance: Instance, h: int) -> int:
    return instance["borrels"][h]

def parse(s: str) -> Instance:
    lines = s.split("\n")
    students: list[Student] = []
    
    for i in range(4, int(lines[3]) + 4):
        line = parse_line(lines[i])
        obligations: list[Obligation] = []
        for j in range(1, line[0] * 3, 3):
            obligations.append({
                'start': line[j],
                'end': line[j + 1],
                'duration': line[j + 2]
            })
        
        students.append(obligations)
    
    return {
        'timeslots': parse_line(lines[0])[0],
        'borrels': parse_line(lines[2]),
        'students': students
    }

def parse_line(s: str) -> list[int]:
    return list(map(int, re.sub(r"\s+", "", s).split(",")))

def print_i(i: Instance) -> str:
    return f"""data;

param n := {n(i)};
param m := {m(i)};
param t := {t(i)};

param ell := 
{'\n'.join([f"{j+1} {ell(i, j)}" for j in range(n(i))])};

# Time intervals [r, d] for obligations
param r :=
{'\n'.join([f"[{j+1},{k+1}] {r(i, j, k)}" for j in range(n(i)) for k in range(ell(i, j))])};

param d :=
{'\n'.join([f"[{j+1},{k+1}] {d(i, j, k)}" for j in range(n(i)) for k in range(ell(i, j))])};

# Time slots needed for each obligation
param p :=
{'\n'.join([f"[{j+1},{k+1}] {p(i, j, k)}" for j in range(n(i)) for k in range(ell(i, j))])};

# Lengths of borrels
param b := 
{'\n'.join([f"{j+1} {b(i, j)}" for j in range(m(i))])};

end;"""

# teststr = """10
#  2
#  1,3
#  4
#  2,1,4,3,5,10,6
#  1,2,5,1
#  1,4,10,3
#  4,1,3,1,1,6,5,3,9,2,8,8,1"""

# print(print_i(parse(teststr)))