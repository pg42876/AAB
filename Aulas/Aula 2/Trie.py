# -*- coding: utf-8 -*-

class Trie:
    
    def __init__(self):
        self.nodes = { 0:{} }
        self.num = 0
    
    def print_trie(self):
        for k in self.nodes.keys():
            print (k, "->" , self.nodes[k]) 
    
    def add_node(self, origin, symbol):
        self.num += 1
        self.nodes[origin][symbol] = self.num 
        self.nodes[self.num] = {}
    
    def add_pattern(self, p):
        position = 0 
        no = 0 
        while position < len(p):
            if p[position] not in self.nodes[no].keys():
                self.add_node(no, p[position]) 
            no = self.nodes[no][p[position]] 
            position += 1 
        
        #OU#

        #no = 0
        #for position in range(len(p)):
            #if p[position] not in self.nodes[no].keys():
                #self.add_node(no, p[position])
            #no = self.nodes[no][p[position]]


    def trie_from_patterns(self, pats):
        for p in pats:
            self.add_pattern(p)
            
    def prefix_trie_match(self, text): 
        pos = 0 
        match = "" 
        node = 0 
        while pos < len(text):
            if text[pos] in self.nodes[node].keys() :
                node = self.nodes[node][text[pos]]
                match += text[pos] 
                if self.nodes[node] == {}: 
                    return match 
                else:
                    pos += 1
            else: 
                return None
        return None 
        
        #OU#

        #pos = 0
        #match = ""
        #node = 0
        #for i in range(len(text)):
            #if text[i] in self.nodes[node].keys():
                #node = self.nodes[node][text[i]]
                #match += text[i]
                #if self.nodes[node] == {}:
                    #return match
            #else:
                #return None
        #return None
        
    def trie_matches(self, text):
        res = []
        for i in range(len(text)):
            m = self.prefix_trie_match(text[i:])
            if m is not None: 
                res.append((i, m))
        return res
        
          
def test():
    patterns = ["GAT", "CCT", "GAG"]
    t = Trie()
    t.trie_from_patterns(patterns)
    t.print_trie()

def test2():
    patterns = ["AGAGAT", "AGC", "AGTCC", "CAGAT", "CCTA", "GAGAT", "GAT", "TC"]
    t = Trie()
    t.trie_from_patterns(patterns)
    print (t.prefix_trie_match("GAGATCCTA"))
    print (t.trie_matches("GAGATCCTA"))
    
test()
print()
test2()
