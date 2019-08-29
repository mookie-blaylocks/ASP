import os

from util import *
from prover import check_common_knowledge, check_shared_knowledge, check_conflicting_belief


def converse():
    
    from utter import hello, want_bel, goodbye
    
    reset()
    hello("evan")
    want_bel("like(dempster,dancing)")
    want_bel("not(like(andy,gambling))")
    hello("ravenna")
    want_bel("like(ravenna,rats)")
    goodbye("evan")
    want_bel("like(andy,gambling)")
    want_bel("like(dempster,dancing)")


def test(method, agents, fact):

    desc_map = {check_common_knowledge: "Common knowledge",
            check_shared_knowledge: "Shared knowledge",
            check_conflicting_belief: "Conflicting beliefs"}
    
    results = method(agents, fact)
    desc = desc_map[method]
    print("{0}: {1}\t\t{2}".format(desc, fact, results))


def test2():
    #methods = [check_common_knowledge, check_shared_knowledge, check_conflicting_belief]
    methods = [check_conflicting_belief]

    fact_sets = []
    fact_sets.append(["like(andy,gambling)", "like(dempster,dancing)", "like(ravenna,rats)"])
    fact_sets.append(["like(andy,gambling)", "like(ravenna,rats)", "like(dempster,dancing)"])
    fact_sets.append(["like(ravenna,rats)", "like(andy,gambling)", "like(dempster,dancing)"])
    fact_sets.append(["like(dempster,dancing)", "like(andy,gambling)", "like(ravenna,rats)"])
    fact_sets.append(["like(ravenna,rats)", "like(dempster,dancing)", "like(andy,gambling)"])
    fact_sets.append(["like(dempster,dancing)", "like(ravenna,rats)", "like(andy,gambling)"])


    converse()

    for m in methods:
        for s in fact_sets:
            print('\n')
            for f in s:
                agents = ["evan", "ravenna", "dempster"]
                test(m, agents, f)

test2()
#reset()
