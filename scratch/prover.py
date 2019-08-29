'''
This file contains methods for checking belief states
between agents. Currently, checking shared knowledge, conflicting
knowledge, and common knowledge is supported.

Shared knowledge is a fact that both agents have witnessed

Common knowledge is a fact that both agents were present for

Conflicting knowledge is two conversations where agents were told opposite facts


Search trees for each are elementary, but could be extended with inference rules
in the prover.
'''

RULES = "rules.lp"

from util import *
import subprocess

# Check for shared knowledge between a list of agents where
# agents is the list
# fact is the semantic form of the knowledge
def check_shared_knowledge(agents, fact):

    convos = get_sorted_convos()

    diarc_agents = get_diarc_agents()
    fact = semantics_to_prover(fact)
    for convo in convos:
        local_agents = get_local_agents(convo, diarc_agents, agents)

        atom_file = get_matching_file(convo, "atoms")

        with open(atom_file, 'r') as f:
            s = f.read()

            neg_fact = negate_prover_semantics(fact)
            for a in s.split('\n'):
                # Remove agents if we have proven that they believe the fact
                if a == fact:
                    agents = list(filter(lambda x : not(x in local_agents), agents))

                # Handle the case where a conversation shows that
                # an agent believes the opposite of the fact
                elif a == neg_fact:
                    a = list(filter(lambda x : not(x in local_agents), agents))
                    if a != []:
                        print("Found false belief for {0} in {1}".format(a, convo))
                        return False

        # All agents show evidence of believing the fact
        if agents == []:
            return True

    # All convos were search, and evidence was not found for at least one agent
    return False


def check_conflicting_belief(agents, fact):

    convos = get_sorted_convos()

    diarc_agents = get_diarc_agents()
    found_negated = False
    found_unnegated = False

    for convo in convos:
        local_agents = get_local_agents(convo, diarc_agents, agents)

        atom_file = get_matching_file(convo, "atoms")
        with open(atom_file, 'r') as atoms:
            contents = atoms.read()
            facts = contents.split('\n')
            if fact in contents:
                for f in facts:
                    if fact in f:
                        is_negated = check_fact_negated(f)
                        if is_negated:
                            found_negated = True
                        else:
                            found_unnegated = True

                for agent in local_agents:
                    agents = list(filter(lambda x : x != agent, agents))
                    
        if agents == []:
            break

    if found_negated and found_unnegated:
        return True
    else:
        return False

def check_common_knowledge(agents, fact):

    convos = get_sorted_convos()

    common_convos = list(filter(lambda x : is_common(x, agents), convos))

    # Search common conversations for the queried fact
    results = []
    for convo in common_convos:

        # Get atoms from convo in question
        atoms = get_matching_file(convo, "atoms")

        # Check atoms for fact
        facts = ""
        with open(atoms, 'r') as atoms:
            facts = atoms.read()

        fact = semantics_to_prover(fact)
        for f in facts.split('\n'):
            if f == fact:
                results.append(convo)

    return results
