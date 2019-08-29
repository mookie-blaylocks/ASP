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

from util import get_sorted_convos, is_common, query_yn, query_var, negate_semantics
import sys

CONTEXT = ["rules.pl", "atoms.pl"]


def check_conflicting_belief(agents, fact):

    convos = get_sorted_convos()

    believe_negated = []
    believe_unnegated = []

    negated_query = negate_semantics(fact)

    for convo in convos:

        if query_yn([convo], [fact]):
            local_agents = query_var([convo] + CONTEXT, "inConversation(X)", "X")
            for agent in agents:
                if agent in local_agents:
                    believe_unnegated.append(agent)
                    agents.remove(agent)

        if query_yn([convo], [negated_query]):
            local_agents = query_var([convo]+CONTEXT, "inConversation(X)", "X")
            for agent in agents:
                if agent in local_agents:
                    believe_negated.append(agent)
                    agents.remove(agent)

    if believe_negated == [] or believe_unnegated == []:
        return False # No conflicts
    else:
        return True
    

def check_common_knowledge(agents, fact):

    convos = get_sorted_convos()

    query = [fact]
    for agent in agents:
        query.append("inConversation({0}).".format(agent))

    results = []
    for convo in convos:
        context = [convo] + CONTEXT
        if query_yn(context, query):
            results.append(convo)

    return results
    

# Check for shared knowledge between a list of agents where
# agents is the list
# fact is the semantic form of the knowledge
def check_shared_knowledge(agents, fact):

    convos = get_sorted_convos()
    negated_query = negate_semantics(fact)

    for convo in convos:

        # If we show that the most recent belief is the opposite,
        # Return false
        if query_yn([convo], [negated_query]):
            local_agents = query_var([convo] + CONTEXT, "inConversation(X)", "X")
            for agent in agents:
                if agent in local_agents:
                    return False

        # If the conversation posits the fact, agents present believe
        # this fact
        if query_yn([convo], [fact]):
            local_agents = query_var([convo] + CONTEXT, "inConversation(X)", "X")
            for agent in local_agents:
                try:
                    agents.remove(agent)
                except ValueError:
                    pass
                
        if agents == []:
            return True

    return False
