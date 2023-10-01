import re
from functools import reduce

class Fsm:
  def __init__(self,alphabet,states,start,final,transitions):
    self.sigma = alphabet
    self.states = states
    self.start = start
    self.final = final
    self.transitions = transitions
  def __str__(self):
    sigma = "Alphabet: " + str(self.sigma) + "\n"
    states = "States: " + str(self.states) + "\n"
    start = "Start: " + str(self.start) + "\n"
    final = "Final: " + str(self.final) + "\n"
    trans_header = "Transitions: [\n"
    thlen = len(trans_header)
    translist = ""
    for t in self.transitions:
      translist += " " * thlen + str(t)+ "\n"
    translist += " " * thlen + "]"
    transitions = trans_header + translist
    ret = sigma + states + start + final + transitions 
    return ret

count = 0

def fresh(): 
  global count
  count += 1
  return count

def char(string):
  start = fresh()
  end = fresh()
  return Fsm([string], [start,end], start, [end], [(start,string,end)])

def concat(r1,r2):
  onset = r1.final
  closure = r2.start

  nfa = Fsm(r1.sigma + r2.sigma, r1.states + r2.states, r1.start, r2.final, r1.transitions + r2.transitions)

  for o in onset:
    nfa.transitions.append((o, "epsilon", closure))
  
  return nfa


def union(r1,r2):
  union_state = fresh()

  nfa = Fsm(r1.sigma + r2.sigma, r1.states + r2.states, r1.start, r1.final + r2.final, r1.transitions + r2.transitions)

  nfa.states.append(union_state)
  nfa.start = union_state

  nfa.transitions.append((nfa.start, "epsilon", r1.start))
  nfa.transitions.append((nfa.start, "epsilon", r2.start))

  return nfa

def star(r1):
  start = fresh()
  nfa = r1

  for f in nfa.final:
    nfa.transitions.append((f, "epsilon", nfa.start))
  
  nfa.states.append(start)
  nfa.transitions.append((start, "epsilon", nfa.start))

  nfa.start = start
  nfa.final.append(nfa.start)

  return nfa
  
def e_closure(s,nfa):
  e_list = list(s)
  transition_dict = sort_transitions(nfa)

  for state in e_list:
    for t in transition_dict[state]:
      if(t[1] == "epsilon" and t[2] not in e_list):
        e_list.append(t[2])

  return e_list


def move(c,s,nfa):
  move_list = []
  transition_dict = sort_transitions(nfa)
  for state in s:
    for t in transition_dict[state]:
      if(t[1] == c and t[2] not in move_list):
        move_list.append(t[2])

  return move_list


def sort_transitions(self):
  transition_dict = {}
  for s in self.states:
    transition_dict[s] = []
  for t in self.transitions:
    transition_dict[t[0]].append(t)

  return transition_dict

def nfa_to_dfa(nfa): 
  dfa_states = []
  dfa_alphabet = list(nfa.sigma)
  dfa_transitions = []
  dfa_final = []
  dfa_start = tuple(e_closure([nfa.start], nfa))
  dfa_states.append(dfa_start)

  for s in dfa_states:
    for c in dfa_alphabet:
      dest = tuple(e_closure(move(c, s, nfa), nfa))
      if(dest not in dfa_states):
        dfa_states.append(dest)
      dfa_transitions.append((s,c,dest))

    intersection = set(s) & set(nfa.final)
    if(intersection):
      dfa_final.append(s)
    
  return Fsm(dfa_alphabet, dfa_states, dfa_start, dfa_final, dfa_transitions)

    

def accept(nfa,string):
  # accept_state = False
  dfa = nfa_to_dfa(nfa)
  curr = dfa.start
  path = []

  for s in string:
    path = move(s, [curr], dfa)
    if(path):
      curr = path[0]
    else:
      break
  
  if(curr in dfa.final):
    return True

  return False
