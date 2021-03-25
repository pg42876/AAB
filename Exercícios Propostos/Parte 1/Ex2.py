class SuffixTree:
    
    def __init__(self):
        self.nodes = { 0:(-1,{}) }
        self.num = 0
        self.sq1 = ''
        self.sq2 = ''
    
    #Ex2
    def unpack (self, k):
        if self.nodes[k][0] == -1:
            a = self.nodes[k][0]
            b = ''
        else: 
            a = self.nodes[k][0]
            b = self.nodes[k][0]
        return a, b
    
    def print_tree(self):
        for k in self.nodes.keys():
            m = self.unpack(k) 
            n = self.unpack(k) 
            if m < 0:
                print(k, "->", self.nodes[k][1])
            else:
                print(k, ":", m, n)
                
    def add_node(self, origin, symbol, leafnum = -1): 
        self.num += 1 
        self.nodes[origin][1][symbol] = self.num  
        self.nodes[self.num] = (leafnum, {}) 
        
    def add_suffix(self, p, sufnum):
        position = 0
        no = 0
        while position < len(p):
            if p[position] not in self.nodes[no][1].keys():
                if position == len(p) - 1:
                    self.add_node(no, p[position], sufnum)
                else:
                    self.add_node(no, p[position])
            no = self.nodes[no][1][p[position]] 
            position += 1
    
    def suffix_tree_from_seq(self, sq1, sq2):
        sq1 = sq1 + '$'
        sq2 = sq2 + '#'
        self.sq1 = sq1
        self.sq2 = sq2
        for i in range(len(sq1)): 
            self.add_suffix(sq1[i:], (0, i)) #vamos adicionar as leafs o 0, ou 1 correspondente a seq e o i que é o numero da letra onde começou
        for i in range(len(sq2)):  
            self.add_suffix(sq2[i:], (1, i))
            
    def find_pattern(self, pattern):
        position = 0
        no = 0
        for position in range(len(pattern)):
            if pattern[position] is self.nodes[no][1].keys():
                 no = self.nodes[no][1][pattern[position]]
            else:
                return None
        return self.get_leafes_below(no)
        
    def get_leafes_below(self, node):
        f1 = []
        f2 = []
        m = self.unpack(node)
        n = self.unpack(node)
        if m >= 0:  
            if m == 0:
                f2.append(n)
            else:
                f1.append(n)
        else:  
            for k in self.nodes[node][1].keys(): 
                newnode = self.nodes[node][1][k]  
                l = self.get_leafes_below(newnode) 
                r = self.get_leafes_below(newnode) 
                f1.extend(r) 
                f2.extend(l)
        return(f1, f2)

    #Ex2
    def largestCommonSubstring(self):
        matchfinal = ''
        contagemfinal = 0
        for c in range(len(self.sq1)):
            contagem = 0
            match = ''
            for d in self.sq2:
                match += self.sq1[c]
                contagem += 1
                c += 1
            else:
                if contagem > contagemfinal:
                    matchfinal = match
                    contagemfinal = contagem
                match = ''
                contagem = 0
        print (matchfinal)

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