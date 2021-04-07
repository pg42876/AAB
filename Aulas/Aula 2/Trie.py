# -*- coding: utf-8 -*-

class Trie:
    
    def __init__(self):
        self.nodes = { 0:{} } # dicionário 
        self.num = 0 #nó zero que não está ligado a nada
    
    def print_trie(self): #imprime a árvore e, consequentemente, o dicionário e as respetivas keys
        for k in self.nodes.keys():
            print (k, "->" , self.nodes[k]) 
    
    def add_node(self, origin, symbol): #adicona um nó à árvore; orgin -> nó atual
        self.num += 1
        self.nodes[origin][symbol] = self.num 
        self.nodes[self.num] = {} #criação de um novo nó
    
    def add_pattern(self, p): #p -> padrão
        position = 0 #posição no padrão
        no = 0 #posição na árvore (é o que nos permite percorrer a árvore)
        while position < len(p): #enquanto a posição < tamanho do padrão (serve para criar o novo nó caso ele não exista)
            if p[position] not in self.nodes[no].keys(): #se posição do padrão não estiver nas chaves do dicionário dos nós no nó correspondente
                self.add_node(no, p[position]) #adicionar o nó ao dicionário com a respetiva letra e posição no padrão
            no = self.nodes[no][p[position]] #o nó atual é o resultado que acabamos de adicionar ao dicionário
            position += 1 #repetir o ciclo caso não exista o nó no dicionário
        
        #OU#

        #no = 0
        #for position in range(len(p)):
            #if p[position] not in self.nodes[no].keys():
                #self.add_node(no, p[position])
            #no = self.nodes[no][p[position]]


    def trie_from_patterns(self, pats):
        for p in pats:
            self.add_pattern(p)
            
    def prefix_trie_match(self, text): #text -> sequência de maior comprimento
        pos = 0 #posição no padrão
        match = "" 
        node = 0 #posição na árvore
        while pos < len(text): #enquanto 
            if text[pos] in self.nodes[node].keys() :
                node = self.nodes[node][text[pos]] #buscar o nó atual 
                match += text[pos] #adicionar ao match o padrão atual
                if self.nodes[node] == {}: #se o nó tiver um dicionário vazio
                    return match #dá return no match
                else: #se ainda não chegamos a uma folha
                    pos += 1 #voltamos a repetir o ciclo, adicionando 1 ao pos
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
            if m is not None: #se m não for None
                res.append((i, m)) #guardamos o i (posição da sequência) e o m (padrão)
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
