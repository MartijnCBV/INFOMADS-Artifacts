from model import *

def simplify(instance: Instance):
    for _ in range(n(instance)):
        merge_obligations(instance)

def obl_len(obl: Obligation) -> int:
    return obl["end"] - obl["start"] + 1

def merge_obligations(instance: Instance):
    for i, obls in enumerate(instance["students"]):
        obls.sort(key=lambda o: o["start"])
        merged = []
        c = obls[0]
        for j in range(1, len(obls)):
            n = obls[j]
            r1, d1, p1 = c["start"], c["end"], c["duration"]
            r2, d2, p2 = n["start"], n["end"], n["duration"]
            if r2 <= d1:
                # n contained in c
                if d2 <= d1:
                    if obl_len(c) - obl_len(n) <= p1:
                        c["duration"] = p1 + p2
                    else:
                        merged.append(c)
                        c = n
                # n partially overlaps with c
                else:
                    o = d1 - r2 + 1
                    if obl_len(c) - o <= p1 and obl_len(n) - o <= p2:
                        c["duration"] = p1 + p2
                        c["end"] = d2
            # consecutive full obligations
            elif obl_len(c) == p1 and obl_len(n) == p2:
                c["duration"] = p1 + p2
                c["end"] = d2
            else:
                merged.append(c)
                c = n
        merged.append(c)
        instance["students"][i] = merged