from bench import *
from typing import Dict
import re
import numpy as np
import matplotlib.pyplot as plt

def lin_graph(data, xl: str, yl: str, path: str):
    plt.rcParams.update({'font.size': 14})
    ks = list(data[0].keys())
    xs = list(range(1, len(data)+1))
    ys = {k: [e[k] for e in data] for k in ks}
    for k in ks:
        plt.plot(xs, ys[k], label=k)
    plt.xlabel(xl)
    plt.ylabel(yl)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.savefig(path, format="pdf", bbox_inches='tight')
    plt.clf()

def bar_graph(data, xl: str, yl: str, path: str):
    plt.rcParams.update({'font.size': 14})
    ks = list(data[0].keys())
    xs = np.arange(len(data)) + 1
    ys = {k: [e[k] for e in data] for k in ks}
    nb = len(ks)
    bw = 0.1
    for i, k in enumerate(ks):
        plt.bar(xs + i * bw, ys[k], bw, label=k)
    plt.xlabel(xl)
    plt.ylabel(yl)
    plt.xticks(xs + bw * (nb - 1) / 2, xs)
    plt.legend(bbox_to_anchor=(0.5, -0.2), loc='upper center', ncol=3, borderaxespad=0., frameon=False)
    plt.tight_layout()
    plt.savefig(path, format="pdf", bbox_inches='tight')
    plt.clf()

def timing_acc(data: Dict[str, Bench], path: str):
    proc = np.empty(len(data.keys()), object)
    for key in data:
        i = re.sub(r"\D", "", key)
        dat = {
            "glpsol(avg)": data[key]["solverr"]["avgtim"],
            "glpsol(best)": data[key]["solverr"]["besttim"],
            "psutil(avg)": data[key]["psutilr"]["avgtim"],
            "psutil(best)": data[key]["psutilr"]["besttim"],
            "time(avg)": data[key]["pytimer"]["avgtim"],
            "time(best)": data[key]["pytimer"]["besttim"]
        }
        proc.put(int(i)-1, dat)
    bar_graph(proc, "Index", "Time(sec)", path)

def memory_acc(data: Dict[str, Bench], path: str):
    proc = np.empty(len(data.keys()), object)
    for key in data:
        i = re.sub(r"\D", "", key)
        dat = {
            "glpsol(avg)": data[key]["solverr"]["avgmem"],
            "glpsol(best)": data[key]["solverr"]["bestmem"],
            "psutil(avg)": data[key]["psutilr"]["avgmem"],
            "psutil(best)": data[key]["psutilr"]["bestmem"]
        }
        proc.put(int(i)-1, dat)
    bar_graph(proc, "Index", "Memory(MB)", path)

