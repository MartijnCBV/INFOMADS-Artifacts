from typing import TypedDict, Dict
import json, re


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

def read_bench(path: str) -> Dict[str, Bench]:
    with open(path, "r") as f:
        data = json.load(f)
    return data

def cut_bench(bench: Dict[str, Bench], size: int):
    ks = list(bench.keys())
    cut = dict()
    for k in bench:
        i = re.sub(r"\D", "", k)
        if int(i) <= size:
            cut[k] = bench[k]
    return cut