## Graph represented as adjacency list using a dictionary
## keys are vertices
## values of the dictionary represent the list of adjacent vertices of the key node

class MyGraph:
    
    def __init__(self, g = {}):
        ''' Constructor - takes dictionary to fill the graph as input; default is empty dictionary '''
        self.graph = g 

    def print_graph(self): #Imprime o grafo - cada linha é constituída pelo nó e pelos seus vizinhos
        ''' Prints the content of the graph as adjacency list '''
        for v in self.graph.keys():
            print (v, " -> ", self.graph[v])

    ## Get basic info

    def get_nodes(self): 
        ''' Returns list of nodes in the graph '''
        return list(self.graph.keys()) #Retorna uma lista dos nós 
        
    def get_edges(self): 
        ''' Returns edges in the graph as a list of tuples (origin, destination) '''
        edges = []
        for v in self.graph.keys():
            for d in self.graph[v]:
                dest, ct = d #O d vai ter um destino e um custo
                edges.append((v,dest)) #Para dar append queremos apenas a origem e o destino
        return edges #Retorna uma lista com os pares de arcos (tuplos)
      
    def size(self):
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())
      
    ## Add nodes and edges    
    
    def add_vertex(self, v): #Adiciona o nó/vértice v ao grafo 
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
        if v not in self.graph.keys():
            self.graph[v] = []
        
    def add_edge(self, o, d, ct): #Adiciona o arco ao grafo 
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph ''' 
        if o not in self.graph.keys():
            self.add_vertex(o) #Adiciona o nó o ao grafo
        if d not in self.graph.keys():
            self.add_vertex(d)
        dt = [] #Lista com os vértices de destino - serve apenas para confirmar se já passamos ou não pelo vértice
        for i in self.graph[o]:
            dest, ct = i
            dt.append(dest)
        if d not in dt: #Verifica se existe ligação entre os dois vértices; caso contrário, adiciona o vertice d à lista dos vértices
            self.graph[o].append((d, ct)) #Vai adicionar o nó d ao nó o, formando o arco (d, custo associado a este arco)

    ## Successors, predecessors, adjacent nodes
        
    def get_successors(self, v): #Sucessores
        dt = [] #Lista de sucessores
        for i in self.graph[v]:
            dest, ct = i
            dt.append(dest) 
        return dt #Retorna uma lista de nós sucessores do nó v
             
    def get_predecessors(self, v): #Ir ao grafo e procurar o nó v quando é value e guardamos a key
        res = [] #Lista de antecessores
        for k in self.graph.keys(): #Percorre as keys do grafo
            dt = [] #Lista de sucessores
            for i in self.graph[k]: #Percorrer os valores em i
                dest, ct = i #i é um tuplo com o vértice destino e o custo
                dt.append(dest) #Adicionar o vértice destino à lista de vértices
                if v in dt: #Verifica se v se encontra na lista de sucessores de i
                    res.append(i) #Se isto se verificar o i vai ser antecessor de v entao adicionamos a lista
        return res #Retorna uma lista de nós antecessores do nó v
    
    def get_adjacents(self, v): #Antecessores + sucessores
        suc = self.get_successors(v) #Sucessores
        pred = self.get_predecessors(v) #Antecessores
        res = pred 
        for p in suc: #Para cada p na suc
            if p not in res: #Se este p não estiver em res
                res.append(p) #Vai adicionar ao res o p - isto garante que não existam repetições
        return res #Retorna uma lista de nós adjacentes do nó v (sucessores + antecessores)
        
    ## Degrees    
    
    def out_degree(self, v):
        return len(self.graph[v]) #Número de sucessores
    
    def in_degree(self, v):
        return len(self.get_predecessors(v)) #Número de antecessores
        
    def degree(self, v):
        return len(self.get_adjacents(v)) #Número de adjacentes (todos os nós adjacentes + percursores + sucessores)
        
    ## BFS and DFS searches    
    
    def reachable_bfs(self, v): #Em largura
        l = [v] #Nó de origem - lista de nós que têm de ser processados
        res = [] #Nós já atingidos
        while len(l) > 0: #Enquanto o tamanho da lista l for > que 0
            node = l.pop(0) #Vai ser removido o primeiro elemento da lista l, guardando este elemento no node
            for elem in self.graph[node]: #Para cada elem no grafo na posição node
                newnode, ct = elem
                if newnode != v: #Se o newnode for diferente do nó origem
                    res.append(newnode) #Acrescenta o node ao resultado
                if newnode not in res and newnode not in l and newnode != node: #Faz a verificação se já existe ou não para não haver repetições
                    l.append(newnode) #Os elementos são adicionados na ordem em que são percorridos
        return res #Retorna a ordem dos nós atingíveis que percorrem o grafo
        
    def reachable_dfs(self, v): #Em profundidade
        l = [v] #Nó de origem - lista de nós que têm de ser processados
        res = [] #Nós já atingidos
        while len(l) > 0: #Enquanto o tamanho da lista l for > que 0
            node = l.pop(0) #Vai ser removido o primeiro elemento da lista l, guardando este elemento no node
            for elem in self.graph[node]: #Para cada elem nos valores associados aos nodes que vêm do grafo
                newnode, ct = elem
                if newnode != v: #Se o newnode for diferente do nó origem
                    res.append(newnode) #Acrescenta o newnode ao resultado
                s = 0 #
                if newnode not in res and newnode not in l:
                    l.insert(s, newnode) #Insert - dá a posição que queremos inserir e qual é o elemento associado a essa posição 
                    s += 1
        return res    
    
    def distance(self, s, d): #Distância
        if s == d: #Se o nó de origem for = ao nó destino
            return 0
        else:
            l = [(s,0)] #s - nó de origem; 0 - representa a distância do nó 
            visited = [s]  
            while len(l) > 0:
                node, dist = l.pop(0) #Remove o o nó e a distância e guarda o nó no node e a distância no dist
                for elem in self.graph[node]: 
                    newnode, ct = elem
                    if newnode == d: #Se o newnode for igual ao destino 
                        return dist + ct #Dá return da distância + ct
                    elif newnode not in visited: #Se o elem (nó em análise) não estiver nos visitados
                        l.append((newnode, dist + ct)) #Adiciona à lista tuplo (elemento (nó), distância + ct)
                        visited.append(newnode) #Adiciona o newnode aos visitados
            return None #Retorna None se não for atingível
            
    def shortest_path(self, s, d): #Caminho mais curto
        if s == d: #Se o nó origem for = ao nó destino
            return [s,d] #Retorna uma lista com o nó origem e nó destino
        else:
            l = [(s, [], 0)] #s - nó de origem; [] - lista vazia (path): representa o caminho; 0 - custo inicial
            visited = [s] #Lista de nós visitados - serve apenas para perceber se um nó já foi ou não visitado
            while len(l) > 0:
                node, path, cost = l.pop(0) #Remove o o nó, o caminho e o custo e guarda o nó no node, o caminho no path e o custo no ct
                maiorct = 999999 #Custo arbitrário
                for elem in self.graph[node]: 
                    newnode, ct = elem
                    if newnode == d: #Se o elemento é = ao nó destino
                        return path + [node, newnode], cost + ct #Retorna o caminho + o antecessor e o seu sucessor + custo 
                    if ct < maiorct:
                        maiorct = ct
                        newnewnode = newnode #Nó a analisar
                if newnewnode not in visited: #se o elemento não está nos nós visitados - adicionar à queue
                    l.append((newnewnode, [(node, newnewnode)], ct + maiorct)) #Adiciona o elemento (nó a analisar), o caminho percorrido + custo
                    visited.append(node) #Adiciona o elemento aos visitados
            return None
            
    def reachable_with_dist(self, s): #Procura com distância estabelecida
        res = [] 
        l = [(s, 0)] #s - nó de origem; 0 - representa a distância do nó 
        while len(l) > 0:
            node, dist = l.pop(0) #Remove o o nó e a distância e guarda o nó no node e a distância no dist
            if node != s: #Se o node é diferente da origem 
                res.append((node, dist)) #Adiciona à lista res o nó e a respetiva distância
            for elem in self.graph[node]:
                newnode, ct = elem 
                if not is_in_tuple_list(l, newnode) and not is_in_tuple_list(res, newnode): 
                    l.append((newnode, dist + ct)) #Adicona à lista l o elemento (nó analisado) e a distância do antecessor + 1
        return res 

    ## Cycles

    def node_has_cycle (self, v): #Serve para ver se um determinado nó apresenta ou não um ciclo
        l = [v]
        res = False
        visited = [v]
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                newnode, ct = elem
                if newnode == v: 
                    return True
                elif newnode not in visited:
                    l.append(newnode)
                    visited.append(newnode)
        return res

    def has_cycle(self):
        res = False
        for v in self.graph.keys():
            if self.node_has_cycle(v): 
                return True
        return res

def is_in_tuple_list (tl, val): #Desempacotar um tuplo - verifica se o tuplo existe ou não
    res = False
    for (x,y) in tl:
        if val == x: 
            return True
    return res


def test1():
    gr = MyGraph({1: [(2,2)], 2: [(3,4)], 3: [(2,3), (4,2)], 4: [(2,5)]})  # criar o grafo
    gr.print_graph()
    print(gr.get_nodes())
    print(gr.get_edges())
    
def test2():
    gr2 = MyGraph()
    gr2.add_vertex(1)
    gr2.add_vertex(2)
    gr2.add_vertex(3)
    gr2.add_vertex(4)
    
    gr2.add_edge(1,2,2)
    gr2.add_edge(2,3,3)
    gr2.add_edge(3,2,4)
    gr2.add_edge(3,4,6)
    gr2.add_edge(4,2,3)
    
    gr2.print_graph()
  
def test3():
    gr = MyGraph({1: [(2,2)], 2: [(3,4)], 3: [(2,3), (4,2)], 4: [(2,5)]})
    gr.print_graph()
    print()
    print(gr.get_successors(2))
    print()
    print(gr.get_predecessors(2))
    print()
    print(gr.get_adjacents(2))
    print()
    print(gr.in_degree(2))
    print()
    print(gr.out_degree(2))
    print()
    print(gr.degree(2))

def test4():
    gr = MyGraph({1: [(2,2)], 2: [(3,4)], 3: [(2,3), (4,2)], 4: [(2,5)]})

    print(gr.distance(1, 4))
    print(gr.distance(4, 3))

    print(gr.shortest_path(1, 4))
    print(gr.shortest_path(4, 3))

    print(gr.reachable_with_dist(1))
    print(gr.reachable_with_dist(3))

    gr2 = MyGraph({1: [(2,2)], 2: [(3,4)], 3: [(2,3), (4,2)], 4: [(2,5)]})

    print(gr2.distance(2, 1))
    print(gr2.distance(1, 5))

    print(gr2.shortest_path(1, 5))
    print(gr2.shortest_path(2, 1))

    print(gr2.reachable_with_dist(1))
    print(gr2.reachable_with_dist(4))

def test5():
    gr = MyGraph({1: [(2,2)], 2: [(3,4)], 3: [(2,3), (4,2)], 4: [(2,5)]})
    print(gr.node_has_cycle(2))
    print(gr.node_has_cycle(1))
    print(gr.has_cycle())

    gr2 = MyGraph({1: [(2,2)], 2: [(3,4)], 3: [(2,3), (4,2)], 4: [(2,5)]})
    print(gr2.node_has_cycle(1))
    print(gr2.has_cycle())


if __name__ == "__main__":
    #test1()
    #test2()
    #test3()
    #test4()
    #test5()
