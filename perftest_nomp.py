from brightway2 import *
from multiprocessing import Pool
from time import time
import itertools
import json
import pyprind


def time_me(act):
    start = time()
    LCA({act: 1}).lci()
    return time() - start


def main():
    projects.set_current("LC IMPACT case study")
    acts = sorted([a.key for a in Database("ecoinvent")])[:250]
    results = []
    for key in pyprind.prog_bar(acts):
        results.append((key, time_me(key)))

    return results


def save_me(data, fp):
    with open(fp, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    save_me(main(), "results-1.6-pardiso.json")
