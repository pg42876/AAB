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
                edges.append((v,d))
        return edges #Retorna uma lista com os pares de arcos (tuplos)
      
    def size(self):
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())
      
    ## Add nodes and edges    
    
    def add_vertex(self, v): #Adiciona o nó v ao grafo 
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
        if v not in self.graph.keys():
            self.graph[v] = []
        
    def add_edge(self, o, d): #Adiciona o arco ao grafo 
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph ''' 
        if o not in self.graph.keys():
            self.add_vertex(o) #Adiciona o nó o ao grafo
        if d not in self.graph.keys():
            self.add_vertex(d)
        if d not in self.graph[o]: #Se o nó d não estiver no grafo 
            self.graph[o].append(d) #Vai adicionar o nó d ao nó o, formando o arco (o, d)

    ## Successors, predecessors, adjacent nodes
        
    def get_successors(self, v): 
        return list(self.graph[v]) #Retorna uma lista de nós sucessores do nó v
             
    def get_predecessors(self, v): #Ir ao grafo e procurar o nó v quando é value e guardamos a key
        res = []
        for k in self.graph.keys():
            if v in self.graph[k]:
                res.append(k)
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
            if node != v: #Se o node for diferente do nó origem
                res.append(node) #Acrescenta o node ao resultado
            for elem in self.graph[node]: #Para cada elem no grafo na posição node
                if elem not in res and elem not in l and elem != node: #Faz a verificação se já existe ou não para não haver repetições
                    l.append(elem) #Os elementos são adicionados na ordem em que são percorridos
        return res #Retorna a ordem dos nós atingíveis que percorrem o grafo
        
    def reachable_dfs(self, v): #Em profundidade
        l = [v] #Nó de origem - lista de nós que têm de ser processados
        res = [] #Nós já atingidos
        while len(l) > 0: #Enquanto o tamanho da lista l for > que 0
            node = l.pop(0) #Vai ser removido o primeiro elemento da lista l, guardando este elemento no node
            if node != v: #Se o node for diferente do nó origem
                res.append(node) #Acrescenta o node ao resultado
            s = 0 #
            for elem in self.graph[node]: #Para cada elem nos valores associados aos nodes que vêm do grafo
                if elem not in res and elem not in l:
                    l.insert(s, elem) #Insert - dá a posição que queremos inserir e qual é o elemento associado a essa posição 
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
                    if elem == d: #Se o elemento for igual ao destino 
                        return dist + 1 #Dá return da distância + 1
                    elif elem not in visited: #Se o elem (nó em análise) não estiver nos visitados
                        l.append((elem,dist+1)) #Adiciona à lista tuplo (elemento (nó), distância + 1)
                        visited.append(elem) #Adiciona o elemento aos visitados
            return None #Retorna None se não for atingível
            
    def shortest_path(self, s, d): #Caminho mais curto
        if s == d: #Se o nó origem for = ao nó destino
            return [s,d] #Retorna uma lista com o nó origem e nó destino
        else:
            l = [(s,[])] #s - nó de origem; [] - lista vazia (path): representa o caminho
            visited = [s] #Lista de nós visitados - serve apenas para perceber se um nó já foi ou não visitado
            while len(l) > 0:
                node, path = l.pop(0) #Remove o o nó e o caminho e guarda o nó no node e o caminho no path
                for elem in self.graph[node]: 
                    if elem == d: #Se o elemento é = ao nó destino
                        return path + [node, elem] #Retorna o caminho + o antecessor e o seu sucessor
                    elif elem not in visited: #se o elemento não está nos nós visitados - adicionar à queue
                        l.append((elem, path + [node])) #Adiciona o elemento (nó a analisar), o caminho percorrido + o nó analisado
                        visited.append(elem) #Adiciona o elemento aos visitados
            return None
            
    def reachable_with_dist(self, s):
        res = [] 
        l = [(s,0)] #s - nó de origem; 0 - representa a distância do nó 
        while len(l) > 0:
            node, dist = l.pop(0) #Remove o o nó e a distância e guarda o nó no node e a distância no dist
            if node != s: #Se o node é diferente da origem 
                res.append((node,dist)) #Adiciona à lista res o nó e a respetiva distância
            for elem in self.graph[node]:
                if not is_in_tuple_list(l, elem) and not is_in_tuple_list(res,elem): 
                    l.append((elem, dist + 1)) #Adicona à lista l o elemento (nó analisado) e a distância do antecessor + 1
        return res 

    ## Cycles

    def node_has_cycle (self, v): #Serve para ver se um determinado nó apresenta ou não um ciclo
        l = [v]
        res = False
        visited = [v]
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                if elem == v: 
                    return True
                elif elem not in visited:
                    l.append(elem)
                    visited.append(elem)
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
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    gr.print_graph()
    print (gr.get_nodes())
    print (gr.get_edges())
    

def test2():
    gr2 = MyGraph()
    gr2.add_vertex(1)
    gr2.add_vertex(2)
    gr2.add_vertex(3)
    gr2.add_vertex(4)
    
    gr2.add_edge(1,2)
    gr2.add_edge(2,3)
    gr2.add_edge(3,2)
    gr2.add_edge(3,4)
    gr2.add_edge(4,2)
    
    gr2.print_graph()
  
def test3():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    gr.print_graph()

    print (gr.get_successors(2))
    print (gr.get_predecessors(2))
    print (gr.get_adjacents(2))
    print (gr.in_degree(2))
    print (gr.out_degree(2))
    print (gr.degree(2))

def test4():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    
    print (gr.distance(1,4))
    print (gr.distance(4,3))

    print (gr.shortest_path(1,4))
    print (gr.shortest_path(4,3))

    print (gr.reachable_with_dist(1))
    print (gr.reachable_with_dist(3))

    gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
    
    print (gr2.distance(2,1))
    print (gr2.distance(1,5))
    
    print (gr2.shortest_path(1,5))
    print (gr2.shortest_path(2,1))

    print (gr2.reachable_with_dist(1))
    print (gr2.reachable_with_dist(5))

def test5():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    print (gr.node_has_cycle(2))
    print (gr. node_has_cycle(1))
    print (gr.has_cycle())

    gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
    print (gr2. node_has_cycle(1))
    print (gr2.has_cycle())


if __name__ == "__main__":
    #test1()
    #test2()
    #test3()
    test4()
    #test5()
