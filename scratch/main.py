import subprocess
import os

from util import *
from prover import *
from utter import *


RULES = "rules.lp"

reset()
hello("evan")
want_bel("like(dempster,dancing)")
want_bel("not(like(andy,gambling))")
hello("ravenna")
want_bel("like(ravenna,rats)")
goodbye("evan")
want_bel("like(andy,gambling)")
want_bel("like(dempster,dancing)")

desc_map = {check_common_knowledge: "Common knowledge",
            check_shared_knowledge: "Shared knowledge",
            check_conflicting_belief: "Conflicting beliefs"}

def test(method, agents, fact):
    results = method(agents, fact)
    desc = desc_map[method]
    print("{0}: {1}\t\t{2}".format(desc, fact, results))

methods = [check_common_knowledge, check_shared_knowledge, check_conflicting_belief]
# methods = [check_shared_knowledge]
facts = ["like(dempster,dancing)", "like(ravenna,rats)", "like(andy,gambling)"]
# facts = ["like(dempster,dancing)"]
agents = ["evan", "ravenna", "dempster"]

for m in methods:
    print('\n')
    for f in facts:
        test(m, agents, f)



# TODO: shared knowledge True facts
# TODO: write test case for display of opposing fact
