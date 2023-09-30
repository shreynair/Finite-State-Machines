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
  raise Exception("Not Implemented")

def concat(r1,r2):
  raise Exception("Not Implemented")

def union(r1,r2):
  raise Exception("Not Implemented")

def star(r1):
  raise Exception("Not Implemented")
  
def e_closure(s,nfa):
  raise Exception("Not Implemented")
  
def move(c,s,nfa):
  raise Exception("Not Implemented")

def nfa_to_dfa(nfa): 
  raise Exception("Not Implemented")

def accept(nfa,string):
  raise Exception("Not Implemented")
