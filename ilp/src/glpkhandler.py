from secrets import GLPK_PATH
from simplifier import simplify
from model import *
from typing import TypedDict, Dict
from statistics import fmean
import os, time, psutil, time, subprocess, json

MODEL_PATH = os.path.abspath("./gmpl/model.mod")
DATA_PATH = os.path.abspath("./temp/temp.dat")
REPORT_PATH = os.path.abspath("./temp/report.txt")
LOG_PATH = os.path.abspath("./temp/log.log")

def write_to_temp(path: str, simpl: bool):
    s = open(path, "r").read()
    i = parse(s)
    if simpl:
        simplify(i)
    proc = print_i(i)
    temp_dir = "./temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    with open(os.path.join(temp_dir, "temp.dat"), "w") as f:
        f.write(proc)


class RunReport(TypedDict):
    tim: float
    mem: int

class Run(TypedDict):
    solverr: RunReport
    psutilr: RunReport
    pytimer: float

class BenchReport(TypedDict):
    besttim: float
    bestmem: float
    avgtim: float
    avgmem: float
    tim: list[float]
    mem: list[float]

class ReducedBenchReport(TypedDict):
    besttim: float
    avgtim: float
    tim: list[float]

class Bench(TypedDict):
    solverr: BenchReport
    psutilr: BenchReport
    pytimer: ReducedBenchReport

def to_bench(rs: list[Run]) -> Bench:
    stim, ptim, ttim = [], [], []
    smem, pmem = [], []
    for r in rs:
        stim.append(r["solverr"]["tim"])
        ptim.append(r["psutilr"]["tim"])
        ttim.append(r["pytimer"])
        smem.append(r["solverr"]["mem"])
        pmem.append(r["psutilr"]["mem"])
    return {
        "solverr": {
            "besttim": min(stim),
            "bestmem": min(smem),
            "avgtim": round(fmean(stim), 1),
            "avgmem": round(fmean(smem), 1),
            "tim": stim,
            "mem": smem
        },
        "psutilr": {
            "besttim": min(ptim),
            "bestmem": min(pmem),
            "avgtim": round(fmean(ptim), 6),
            "avgmem": round(fmean(pmem), 6),
            "tim": ptim,
            "mem": pmem
        },
        "pytimer": {
            "besttim": min(ttim),
            "avgtim": round(fmean(ttim), 6),
            "tim": ttim
        }
    }

def dump_bench(path: str, name: str, bench: Bench):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, name), "w") as f:
        f.write(json.dumps(bench, indent=4))

def read_res() -> RunReport:
    s = open(LOG_PATH, "r").read()
    matches = re.findall(r"(?:used:\s*)\d+\.\d", s)
    return {
        "tim": float(re.sub(r"used:\s*", "", matches[-2])),
        "mem": float(re.sub(r"used:\s*", "", matches[-1]))
    }

def run_glpk() -> Run:
    start = time.time()
    proc = subprocess.Popen([GLPK_PATH, "-m", MODEL_PATH, "-d", DATA_PATH, "-y", REPORT_PATH, "--log", LOG_PATH])
    psproc = psutil.Process(proc.pid)
    ts = psproc.cpu_times()
    peak_m = 0
    while proc.poll() is None:
        lts = ts
        try:
            ts = psproc.cpu_times()
            ms = psproc.memory_info()
            peak_m = max(peak_m, ms.rss)
        except psutil.NoSuchProcess:
            ts = lts
            break
        time.sleep(0.001)
    end = time.time()
    return {
        "solverr": read_res(),
        "psutilr": {
            "tim": round(ts.user + ts.system, 6),
            "mem": round(peak_m / 1048567, 6)
        },
        "pytimer": round(end - start, 6)
    }

def run_dir(path: str, times: int, simpl: bool) -> Dict[str, Bench]:
    fs = next(os.walk(path), (None, None, []))[2]
    bs = dict()
    for f in fs:
        write_to_temp(os.path.join(path, f), simpl)
        rs = []
        for i in range(times):
            print(f"FILE::{f}::RUN::{i}")
            rs.append(run_glpk())
        bs[f] = to_bench(rs)
    return bs
