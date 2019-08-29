'''
This file contains helper methods for utter and prover
The methods often perform sorting, resetting of the environment,
or getting common variables

'''

import os
import subprocess


RULES = "rules.lp"

# Sorts through atoms or agents to return the most recent
def get_current(t):   # t for type (agents/atoms)
    listOfFiles = os.listdir("./")
    atoms = list(filter(lambda x : t in x, listOfFiles))
    recent = 0
    for atom in atoms:
        atom_num = int(atom.split("_")[1][0])
        if atom_num > recent:
            recent = atom_num
    return "{0}_{1}.lp".format(t, recent)


# Reset rules, agents, and atoms to blank for a reboot
# rules.lp is left unchanged so that it can be modified without
# being deleted by a reset
# Agents and conversational Atoms should change with a reboot
# and between conversations
# rules.lp has several derivatives that are created at runtime,
# and then reset here.
def reset():
    listOfFiles = os.listdir("./")

    atoms = list(filter(lambda x : "atoms" in x, listOfFiles))
    for atom in atoms:
        os.remove(atom)
    with open("atoms_0.lp", "w+") as atom:
        atom.write("")

    agents = list(filter(lambda x : "agents" in x, listOfFiles))
    for agent in agents:
        os.remove(agent)
    with open("agents_0.lp", "w+") as agent:
        agent.write("")
    
    rules = list(filter(lambda x : "rules_" in x, listOfFiles))
    for rule in rules:
        try:
            os.remove(rule)
        except FileNotFoundError:
            pass
    try:
        os.remove("temp.txt")
    except FileNotFoundError:
        pass


# Return agents hard-coded into belief rules
def get_diarc_agents():

    with open("rules.lp", "r") as rules:
        r = rules.read()
    diarcAgents_rules = r + "\n#show inConversation/1."
    with open("rules_agents.lp", "w") as rules:
        rules.write(diarcAgents_rules)

    with open("temp.txt", 'w') as output:
        subprocess.run(["clingo", "--verbose=0", "rules_agents.lp"], stdout=output)
    with open("temp.txt", 'r') as output:
        o = output.read()
        return filter_agents(o)


def filter_agents(s):    # s for String from file input
    agents = []
    for i in s.split(')'):
        if '(' in i:
            agents.append(i.split('(')[1])
    return agents



# Return the index of the given convo string as an int
# E.g. "agents_10.lp" -> 10
def get_convo_index(convo):

    a = convo.split("_")[1]
    b = a.split(".")[0]
    return int(b)


# Return True if fact is negated
def check_fact_negated(fact):
    if "not" == fact.split(' ')[0]:
        return True
    else:
        return False
    

# Return convos sorted from most to least recent (reverse numerical)
def get_sorted_convos():

    listOfFiles = os.listdir("./")
    convos = list(filter(lambda x : "agents_" in x, listOfFiles))
    convos = sorted(convos, key = lambda x : get_convo_index(x))
    convos.reverse()
    return convos


# For a given convo, return the actors of interest
# return (agent of interest) intersection ((agents in convo) union (diarc agents))
def get_local_agents(convo, diarc_agents, agents_of_interest):

    local_agents = diarc_agents
    i = get_convo_index(convo)
    with open(convo, 'r') as f:
        conversants = f.read()
        for agent in agents_of_interest:   # for agents_of_interest
            if agent in conversants:       # if present
                local_agents.append(agent) # add
                
    return local_agents


# For a given file, return the matching index of the given type
def get_matching_file(convo, t):

    i = get_convo_index(convo)
    return "{0}_{1}.lp".format(t, i)


# Return the prover form of a predicate
def semantics_to_prover(semantics):
    if semantics[0:3] == "not":
        l = list(semantics)
        l[3] = " "
        l[-1] = ""
        l.append('.')
        return "".join(l)
    else:
        return semantics + "."


# Return a prover form of negation
# Handles double negation
def negate_prover_semantics(semantics):
    if semantics.split(' ')[0] == "not":
        return semantics.split(' ')[1]
    else:
        return "not " + semantics


# Return true if the conversation was common among all agents
def is_common(convo, agents):

    with open(convo, 'r') as f:
        participants = f.read()
    participants = filter_agents(participants)
    participants += get_diarc_agents()
    for agent in agents:
        if (not (agent in participants)):
            return False

    return True

# Print out the current state of conversational belief
def write_current():
    current_agents = get_current("agents")
    print("{0}:\n".format(current_agents))
    with open(current_agents, "r") as agents:
        print(agents.read())
    current_atoms = get_current("atoms")
    print("{0}:\n".format(current_atoms))
    with open(current_atoms, "r") as atoms:
        print(atoms.read())
    print("\n")
    
