from util import *


def hello(agent):

    old_convo = get_current()
    
    old_agents = query_var([old_convo], "inConversation(X)", "X")
    text = ":- multifile inConversation/1.\n"
    text += "inConversation({0}).".format(agent)
    for a in old_agents:
        text += "\ninConversation({0}).".format(a)
    
    new_convo = "convo_{0}.pl".format(get_convo_index(old_convo) + 1)
    with open(new_convo, "w") as f:
        f.write(text)
    

def goodbye(agent):
    old_convo = get_current()
    old_agents = query_var([old_convo], "inConversation(X)", "X")
    text = ":- multifile inConversation/1."
    for a in old_agents:
        if a != agent:
            text += "\ninConversation({0}).".format(a)
    
    count = get_convo_index(old_convo) + 1
    new_convo = "convo_{0}.pl".format(get_convo_index(old_convo) + 1)
    with open(new_convo, "w") as f:
        f.write(text)

        
def want_bel(semantics):
    current_convo = get_current()
    semantics = semantics_to_prover(semantics)
    semantics = "\n{0}".format(semantics)
    with open(current_convo, "a") as f:
        f.write(semantics)

