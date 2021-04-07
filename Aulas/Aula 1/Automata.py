# -*- coding: utf-8 -*-

class Automata:
    
    def __init__(self, alphabet, pattern):
        self.numstates = len(pattern) + 1 
        self.alphabet = alphabet
        self.transitionTable = {}
        self.buildTransitionTable(pattern)        
    
    def buildTransitionTable(self, pattern): 
        for q in range(self.numstates): 
            for a in self.alphabet: 
                prefixo = pattern[:q] + a #Pattern de 0 a q + letra 
                self.transitionTable[(q, a)] = overlap(prefixo, pattern) #Para fazer as entradas no dicionário, onde q é o estado onde estamos e a o estado para onde vamos 

    def printAutomata(self):
        print ("States: " , self.numstates)
        print ("Alphabet: " , self.alphabet)
        print ("Transition table: ")
        for k in self.transitionTable.keys():
            print (k[0], ",", k[1], " -> ", self.transitionTable[k])
         
    def nextState(self, current, symbol):
        return self.transitionTable[(current, symbol)]
    
    def get_string(srlf, **kwargs): #kwargs - key words arguments
        if kwargs.get('reverse', False):
            return self.s.reverse
        if kwargs.get('maiuscula', False):
            return self.s.maiuscula

    def applySeq(self, seq):
        q = 0 #Iniciador do estado; o q varia
        res = [q] #Criação de lista com 0
        for c in seq:
            q = self.nextState(q, c)
            res.append(q)
        return res #Resulta uma lista com os valores calculados no overlap -> i
        
    def occurencesPattern(self, text):
        q = 0 
        res = []
        for i in range(len(text)):
            q = self.nextState(q, text[i])
            if q == self.numstates - 1:
                res.append(i - self.numstates + 2) #+2 porque temos de ter uma casa em branco no início (+1) e porque temos de ter o tamanho correto da sequência (+1)
        return res #Resulta uma lista com os valores das posições onde se encontram os padrões

def overlap(s1, s2): #s1: prefixo, s2: padrão
    maxov = min(len(s1), len(s2)) #Mínimo entre prefixo e padrão
    for i in range(maxov, 0, -1):
        if s1[-i:] == s2[:i]: #-i: vai buscar o último valor; Compara o início da sequência com o final desta
            return i
    return 0
               
def test():
    auto = Automata("AC", "ACA")
    auto.printAutomata()
    print (auto.applySeq("CACAACAA"))
    print (auto.occurencesPattern("CACAACAA"))

test()

#States:  4
#Alphabet:  AC
#Transition table:
#0 , A  ->  1     {(0, 'A': 1)}
#0 , C  ->  0
#1 , A  ->  1
#1 , C  ->  2
#2 , A  ->  3
#2 , C  ->  0
#3 , A  ->  1
#3 , C  ->  2
#[0, 0, 1, 2, 3, 1, 2, 3, 1]
#[1, 4]