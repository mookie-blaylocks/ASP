'''
This file contains helper methods for utter and prover
The methods often perform sorting, resetting of the environment,
or getting common variables

'''

import os
import subprocess
from string import Template

RULES = "rules.pl"

# Sorts through atoms or agents to return the most recent
def get_current():   # t for type (agents/atoms)
    return get_sorted_convos()[0]


# Reset rules, agents, and atoms to blank for a reboot
# rules.pl is left unchanged so that it can be modified without
# being deleted by a reset
# Agents and conversational Atoms should change with a reboot
# and between conversations
# rules.pl has several derivatives that are created at runtime,
# and then reset here.
def reset():
    listOfFiles = os.listdir("./")

    convos = list(filter(lambda x : "convo" in x, listOfFiles))
    for convo in convos:
        os.remove(convo)
    with open("convo_0.pl", "w+") as f:
        f.write(":- multifile inConversation/1.\n")
    
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
    try:
        os.remove("query.pl")
    except FileNotFoundError:
        pass


# Return agents hard-coded into belief rules
def get_diarc_agents():
    return query_var(['atoms.pl'], 'diarcAgent')


def get_pred_name_and_arity(query):
    try:
        p, a = query.split("(")
        return ["{0}/{1}".format(p, len(a.split(",")))]
    except ValueError:  # Nested predicates TODO, hack to make not work
        nest = query[4:-1]
        return ["not/1"] + get_pred_name_and_arity(nest)
    

def query_yn(context, queries):

    with open("yn_template.pl", 'r') as f:
        template = Template(f.read())

    context = clean_context(context)
    query = ""
    preds = []
    for q in queries:
        if q[-1] == '.':
            query += "\nquery({0}).".format(q[:-1])
        else:
            query += "\nquery({0}).".format(q)
        preds += get_pred_name_and_arity(q)
    preds = ",".join(list(set(preds)))
    text = template.substitute(context=context, preds=preds, query=query)
    results = query_pl(text)
    for q in results.split('\n'):
        if q.split(':')[0] == "no":
            return False

    return True


def clean_context(context):
    for i, f in enumerate(context):
        context[i] = f.split(".")[0]  # Strip the .pl file ending
    return ','.join(context)

    
def query_var(context, query, var):

    with open("var_template.pl", 'r') as f:
        template = Template(f.read())

    context = clean_context(context)
    text = template.substitute(context=context, query=query, var=var)
    results = query_pl(text)
    if results == '':
        return []
    else:
        return results.split('\n')


def query_pl(query_pl):
    
    with open("query.pl", 'w+') as f:
        f.write(query_pl)

    with open("temp.txt", 'w') as f:
        subprocess.run(["swipl", "query.pl"], stdout=f)

    with open("temp.txt", 'r') as f:
        return f.read().strip()



# Return the index of the given convo string as an int
# E.g. "agents_10.pl" -> 10
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
# of type t
def get_sorted_convos():

    listOfFiles = os.listdir("./")
    convos = list(filter(lambda x : "convo_" in x, listOfFiles))
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
    return "{0}_{1}.pl".format(t, i)


# Return the prover form of a predicate
def semantics_to_prover(semantics):
    return semantics + "."


# Return a prover form of negation
# Handles double negation
def negate_semantics(semantics):
    if semantics.split('(')[0] == "not":
        return semantics[4:-1]
    else:
        return "not({0})".format(semantics)


# Return true if the conversation was common among all agents
def is_common(convo, agents):

    local_agents = query([convo], "inConversation(X)", "X")
    for agent in agents:
        if not (agent in local_agents):
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
    
