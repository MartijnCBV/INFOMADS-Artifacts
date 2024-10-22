from bench import *
from typing import Dict
import re
import numpy as np
import matplotlib.pyplot as plt

def lin_graph(data, xl: str, yl: str, path: str, xs: list[int]=[], dashcycle=False):
    plt.rcParams.update({'font.size': 14})
    ks = list(data[0].keys())
    if xs == []:
        xs = list(range(1, len(data)+1))
    ys = {k: [e[k] for e in data] for k in ks}
    cyc = True
    for k in ks:
        if dashcycle:
            if cyc:
                plt.plot(xs, ys[k], label=k, linestyle=(0, (3, 3)))
            else:
                plt.plot(xs, ys[k], label=k, linestyle=(3, (3, 3)))
            cyc = not cyc
        else:
            plt.plot(xs, ys[k], label=k)
    plt.xlabel(xl)
    plt.ylabel(yl)
    plt.legend(bbox_to_anchor=(0.5, -0.2), loc='upper center', ncol=3, borderaxespad=0., frameon=False)
    plt.tight_layout()
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

def timing(data: Dict[str, Bench], xl: str, path: str, xs: list[int]=[], dashcycle=False):
    proc = np.empty(len(data.keys()), object)
    for key in data:
        i = re.sub(r"\D", "", key)
        dat = {
            "time(avg)": data[key]["pytimer"]["avgtim"],
            "time(best)": data[key]["pytimer"]["besttim"]
        }
        proc.put(int(i)-1, dat)
    lin_graph(proc, xl, "Time(sec)", path, xs=xs, dashcycle=dashcycle)

def memory(data: Dict[str, Bench], xl: str, path: str, xs: list[int]=[], dashcycle=False):
    proc = np.empty(len(data.keys()), object)
    for key in data:
        i = re.sub(r"\D", "", key)
        dat = {
            "glpsol(avg)": data[key]["solverr"]["avgmem"],
            "glpsol(best)": data[key]["solverr"]["bestmem"]
        }
        proc.put(int(i)-1, dat)
    lin_graph(proc, xl, "Memory(MB)", path, xs=xs, dashcycle=dashcycle)

def timing_double(a: Dict[str, Bench], b: Dict[str, Bench], al, bl, xl: str, path: str, xs: list[int]=[], dashcycle=False):
    proc = np.empty(len(a.keys()), object)
    for key in a:
        i = re.sub(r"\D", "", key)
        dat = {
            f"{al}(avg)": a[key]["pytimer"]["avgtim"],
            f"{al}(best)": a[key]["pytimer"]["besttim"]
        }
        proc.put(int(i)-1, dat)
    for key in b:
        i = re.sub(r"\D", "", key)
        dat = proc.item(int(i)-1)
        dat[f"{bl}(avg)"] = b[key]["pytimer"]["avgtim"]
        dat[f"{bl}(best)"] = b[key]["pytimer"]["besttim"]
        proc.put(int(i)-1, dat)
    lin_graph(proc, xl, "Memory(MB)", path, xs=xs, dashcycle=dashcycle)