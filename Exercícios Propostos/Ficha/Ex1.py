class SuffixTree:
    
    def __init__(self):
        self.nodes = { 0:(-1,{}) }
        self.num = 0
        self.seq = "" #Guarda a sequência original
    
    def print_tree(self):
        for k in self.nodes.keys():
            if self.nodes[k][0] < 0:
                print (k, "->", self.nodes[k][1]) 
            else:
                print (k, ":", self.nodes[k][0])
                
    def add_node(self, origin, symbol, leafnum = -1): #Posição de origem: símbolo; caso a posição não seja uma folha: -1
        self.num += 1
        self.nodes[origin][1][symbol] = self.num
        self.nodes[self.num] = (leafnum,{})
        
    def add_suffix(self, p, sufnum):
        position = 0
        no = 0
        while position < len(p):
            if p[position] not in self.nodes[no][1].keys(): #Se a posição não se encontrar na root
                if position == len(p) - 1: #Se a posição for = à última posição da sequência
                    self.add_node(no, p[position], sufnum) #Adiciona o nó, a posição do nó e e o número da sequência 
                    #NOTA: só usamos o sufnum quando for o última posição da seq 
                else: #Se for o primeiro
                    self.add_node(no, p[position]) #Adiciona o nó e a posição do nó
            no = self.nodes[no][1][p[position]] 
            position += 1
    
    def suffix_tree_from_seq(self, text):
        self.seq = text
        t = text + "$"
        for i in range(len(t)): #Divide o texto
            self.add_suffix(t[i:], i) #Número de sequências que são adicionadas à árvore
            
    def find_pattern(self, pattern): #Vai buscar um padrão e vai dizer em que posições nas seqs vai começar por esse padrão
        position = 0
        no = 0
        for position in range(len(pattern)): 
            if pattern[position] in self.nodes[no][1].keys():
                 no = self.nodes[no][1][pattern[position]]
                 position += 1
            else:
                return None
        return self.get_leafes_below(no)
        
    def get_leafes_below(self, node):
        res = [] #Resultado são nós
        if self.nodes[node][0] >=0: 
            res.append(self.nodes[node][0])            
        else:
            for k in self.nodes[node][1].keys():
                newnode = self.nodes[node][1][k]
                leafes = self.get_leafes_below(newnode)
                res.extend(leafes)
        return res

    #Ex1a
    def nodes_below (self, node): #Todos os nós que estão por baixo do que queremos
        if node >= len(self.nodes): 
            return None
        else:
            nodesID = list(self.nodes[node][1].values()) #Adicionar a uma lista com todos os valores do dicionário
            for a in nodesID:
                nodesID.extend(list(self.nodes[a][1].values())) #Vai adicionando os nós e os valores à lista
            return nodesID
    
    #Ex1b
    def matches_prefix (self, prefix):
        NS = SuffixTree.find_pattern(self, prefix)
        if NS == None or NS == []:
            return None
        else: 
            match = []
            for a in NS:
                match.append(self.seq[a:])
            match = sorted(match, key = len, reverse = True)
            matchfinal = []
            for b in range(len(match)):
                c = len(match[b])
                d = 1
                while c > len(prefix):
                    matchfinal.append(match[b][:-d])
                    c = c - 1
                    d = d + 1
            return (list(dict.fromkeys(matchfinal)))

def test():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    st.print_tree()
    print (st.find_pattern("TA"))
    print (st.find_pattern("ACG"))

def test2():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    print (st.find_pattern("TA"))
    #print(st.repeats(2,2))

test()
print()
test2()
