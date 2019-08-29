from util import *
import subprocess

RULES = "rules.lp"


def hello(agent):
    current_agents = get_current("agents")
    with open(current_agents, "r") as agents:
        participants = agents.read();

    participants += "\ninConversation({0}).".format(agent)

    count = int(current_agents.split("_")[1][0]) + 1

    new_agents = "agents_{0}.lp".format(count)
    with open(new_agents, "w") as agents:
        agents.write(participants)

    new_atoms = "atoms_{0}.lp".format(count)
    with open(new_atoms, "w") as atoms:
        atoms.write("")
    

def goodbye(agent):
    current_agents = get_current("agents")
    with open(current_agents, "r") as agents:
        old_participants = agents.read().split("\n")

    new_participants = list(filter(lambda x : not (agent in x), old_participants))
    output = ""
    for participant in new_participants:
        output += "{0}\n".format(participant)
    
    count = int(current_agents.split("_")[1][0]) + 1
    new_agents = "agents_{0}.lp".format(count)

    with open(new_agents, "w") as agents:
        agents.write(output)

    new_atoms = "atoms_{0}.lp".format(count)
    with open(new_atoms, "w") as atoms:
        atoms.write("")

        
def want_bel(semantics):
    current_atoms = get_current("atoms")
    semantics = semantics_to_prover(semantics)
    semantics = "\n{0}".format(semantics)
    with open(current_atoms, "a") as atoms:
        atoms.write(semantics)

