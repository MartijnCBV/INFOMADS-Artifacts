from secrets import GLPK_PATH
from model import *
import os
import sys
import subprocess

MODEL_PATH = os.path.abspath("./gmpl/model.mod")
DATA_PATH = os.path.abspath("./temp/temp.dat")
REPORT_PATH = os.path.abspath("./temp/report.txt")

def write_to_temp(path: str):
    s = open(path, "r").read()
    i = parse(s)
    proc = print_i(i)
    temp_dir = "./temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    with open(os.path.join(temp_dir, "temp.dat"), "w") as f:
        f.write(proc)

def read_res() -> str:
    return

def run_glpk():
    res = subprocess.run([GLPK_PATH, "-m", MODEL_PATH, "-d", DATA_PATH, "-y", REPORT_PATH], capture_output=True).decode(sys.stdout.encoding)