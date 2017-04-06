from brightway2 import *
from multiprocessing import Pool
from time import time
import itertools
import json


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def worker(keys):
    projects.set_current("LC IMPACT case study")
    results = []
    for key in keys:
        results.append((key, time_me(key)))

    return results

def time_me(act):
    start = time()
    LCA({act: 1}).lci()
    return time() - start


def main():
    projects.set_current("LC IMPACT case study")
    acts = sorted([a.key for a in Database("ecoinvent")])
    as_chunks = list(chunks(acts[:250], 35))

    with Pool(7) as pool:
        results = list(itertools.chain(*pool.map(worker, as_chunks)))

    print("Finished job")

    return results


def save_me(data, fp):
    with open(fp, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    save_me(main(), "results-1.5-umfpack.json")
