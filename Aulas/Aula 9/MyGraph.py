## Graph represented as adjacency list using a dictionary
## keys are vertices
## values of the dictionary represent the list of adjacent vertices of the key node

class MyGraph:
    
    def __init__(self, g = {}):
        ''' Constructor - takes dictionary to fill the graph as input; default is empty dictionary '''
        self.graph = g #Dicionário

    def print_graph(self):
        ''' Prints the content of the graph as adjacency list '''
        for v in self.graph.keys(): #Para cada key no dicionário (vértice)
            print (v, " -> ", self.graph[v]) #Print do vértice

    ## Get basic info

    def get_nodes(self):
        ''' Returns list of nodes in the graph '''
        return list(self.graph.keys()) #Retorna uma lista com os vértices
        
    def get_edges(self):
        ''' Returns edges in the graph as a list of tuples (origin, destination) '''
        edges = []
        for v in self.graph.keys():
            for d in self.graph[v]:
                edges.append((v,d))
        return edges  #Dá return das arcos (pares de vértices ligados)
      
    def size(self): #Tamanho do grafo
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges()) #Indica quantos nós e quantos arcos tem o grafo 
      
    ## Add nodes and edges    
    
    def add_vertex(self, v): #Adiciona vértices (nós)
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
        if v not in self.graph.keys():
            self.graph[v] = [] #Adiciona uma key ao dicionário
        
    def add_edge(self, o, d): #Adiciona arcos
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph ''' 
        if o not in self.graph.keys():
            self.add_vertex(o)
        if d not in self.graph.keys():
            self.add_vertex(d)  
        if d not in self.graph[o]:
            self.graph[o].append(d)

    ## Successors, predecessors, adjacent nodes
        
    def get_successors(self, v):
        return list(self.graph[v]) #Needed to avoid list being overwritten of result of the function is used           
             
    def get_predecessors(self, v):
        res = [] #Lista de antecessores vazia - onde vão ser adicionados os vértices já percorridos
        for k in self.graph.keys(): #Percorre as keys do dicionário
            if v in self.graph[k]: #OU if self.graph[i] == v: -> verifica se o v é um value de i
                res.append(k) #Adiciona a key com value v à lista
        return res #Retorna uma lista com os antecessores 
    
    def get_adjacents(self, v):
        suc = self.get_successors(v) #Lista de sucessores
        pred = self.get_predecessors(v) #Lista de antecessores
        res = pred #O resultado é igual aos antecessores (apenas para ser mais cómodo); podia ser ao contrário
        for p in suc: #Percorre a lista de sucessores 
            if p not in res: #Se p não estiver na lista de resultados
                res.append(p) #Adiciona p à lista de resultados
        return res #Retorna uma lista com todos os antecessores e todos os sucessores
        
    ## Degrees    
    
    def out_degree(self, v): #Grau de saída do nó
        return len(self.graph[v])
    
    def in_degree(self, v): #Grau de entrada do nó
        return len(self.get_predecessors(v))
        
    def degree(self, v): #Grau do vértice - número de arestas que são incidentes a um determinado nó
        return len(self.get_adjacents(v))
        
    def all_degrees(self, deg_type = "inout"): #Graus de entrada + graus de saída
        ''' Computes the degree (of a given type) for all nodes.
        deg_type can be "in", "out", or "inout" '''
        degs = {}
        for v in self.graph.keys(): #Para cada key no grafo
            if deg_type == "out" or deg_type == "inout": 
                degs[v] = len(self.graph[v]) #Inicializar com o número de saídas
            else: 
                degs[v] = 0
        if deg_type == "in" or deg_type == "inout":
            for v in self.graph.keys(): #Para cada v (metabolito ou reação) nas listas
                for d in self.graph[v]: #Para cada d na lista de sucessores
                    if deg_type == "in" or v not in self.graph[d]: #Se for in ou v OU não for um value de d no grafo
                        degs[d] = degs[d] + 1 #Adiciona + 1 ao value de d no dicionário degs
        return degs
    
    def highest_degrees(self, all_deg= None, deg_type = "inout", top= 10): #Vai dar o top 10
        '''Vai buscar o top 10 de nos com maior grau'''
        if all_deg is None: #Percorre todos os graus
            all_deg = self.all_degrees(deg_type) #Vai buscar o dicionário a all_degrees
        ord_deg = sorted(list(all_deg.items()), key=lambda x : x[1], reverse = True) #Coloca o dicionário por ordem decrescente (do maior para o menor)
        #Neste caso transforma um lista .items para colocar em tuplos (keys, values) e só assim é que consegue colocar por ordem decrescente
        return list(map(lambda x:x[0], ord_deg[:top])) #Retorna uma lista dos melhores 10 nós

    ## Topological metrics over degrees

    def mean_degree(self, deg_type = "inout"): #Média dos graus
        degs = self.all_degrees(deg_type) #Calcula os graus de entrada ou de saída ou ambos para todos os nós da rede
        return sum(degs.values()) / float(len(degs)) #Soma de todos os valores do dicionário e média dos nós do grafo 
    
    #Chave - k; Valor - p(k)
    def prob_degree(self, deg_type = "inout"): #Probabilidade de um determinado grau existir no grafo
        degs = self.all_degrees(deg_type) #Calcula os graus de entrada ou de saída ou ambos para todos os nós da rede
        res = {} #Dicionário vazio
        for k in degs.keys(): #Percorre todas as keys de degs
            if degs[k] in res.keys(): #Verifica se um determinado k existe nas keys de res
                res[degs[k]] += 1 #Adiciona esse k + 1 ao dicionário res
            else: #Caso contrário
                res[degs[k]] = 1 #Adiciona ao dicionário esse k (grau) = 1
        for k in res.keys():
            res[k] /= float(len(degs)) #Probabilidade dos graus 
        return res #Retorna um dicionário com os resultados (probabilidade)
    
    ## BFS and DFS searches    
    
    def reachable_bfs(self, v):
        '''Procura de cima para baixo'''
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v: 
                res.append(node)
            for elem in self.graph[node]:
                if elem not in res and elem not in l and elem != node:
                    l.append(elem)
        return res
        
    def reachable_dfs(self, v):
        '''Procura da esquerda para a direita'''
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v: 
                res.append(node)
            s = 0
            for elem in self.graph[node]:
                if elem not in res and elem not in l:
                    l.insert(s, elem)
                    s += 1
        return res    
    
    def distance(self, s, d):
        if s == d: return 0
        l = [(s,0)]
        visited = [s]
        while len(l) > 0:
            node, dist = l.pop(0)
            for elem in self.graph[node]:
                if elem == d: 
                    return dist + 1
                elif elem not in visited: 
                    l.append((elem,dist+1))
                    visited.append(elem)
        return None
        
    def shortest_path(self, s, d):
        if s == d: return 0
        l = [(s,[])]
        visited = [s]
        while len(l) > 0:
            node, preds = l.pop(0)
            for elem in self.graph[node]:
                if elem == d: 
                    return preds+[node,elem]
                elif elem not in visited: 
                    l.append((elem,preds+[node]))
                    visited.append(elem)
        return None
        
    def reachable_with_dist(self, s):
        res = [] #Lista de resultados (vai guardar os nós que já foram visitados)
        l = [(s,0)] #Lista de tuplos com s - distância - e a distância percorrida (inicialmente é 0)
        while len(l) > 0: 
            node, dist = l.pop(0) 
            if node != s: 
                res.append((node,dist)) #Dá apenas append ao node
            for elem in self.graph[node]: #Vê onde é que o node está ligado
                if not is_in_tuple_list(l,elem) and not is_in_tuple_list(res,elem): #Vê se o p se encontra dentro de l ou em res
                    l.append((elem,dist+1)) #Adiciona o vértice a que se liga e adiciona + 1 à distância
        return res
 
    ## Mean distances ignoring unreachable nodes
 
    def mean_distances(self):
        tot = 0 #Total
        num_reachable = 0 #Número de vetores ligados entre si
        for k in self.graph.keys(): 
            distsk = self.reachable_with_dist(k)
            for _, dist in distsk:
                tot += dist
            num_reachable += len(distsk) #Contagem de todas as ligações existentes entre todos os nós
        meandist = float(tot) / num_reachable #Média da distância da ligação 
        n = len(self.get_nodes()) #Contagem de todos os nós
        return meandist, float(num_reachable)/((n-1)*n) #num_reachable -> número de ligações que existem; (n - 1) * n -> número de ligações esperadas
    
    def closeness_centrality(self, node):
        '''Baseado nos nós que estão mais próximos dos restantes'''
        dist = self.reachable_with_dist(node) #Lista que devolve os nós e as distâncias associadas a esses nós
        if len(dist)==0: 
            return 0.0 #Centralidade mais próxima é 0
        s = 0.0 #Distãncia
        for d in dist: #d = ( , )
            s += d[1] #Tuplo (t, 6)
        return len(dist) / s #Nós / distância total 
        #Centralidade mais próxima = todos os tuplos (vértice com ligação a esse vértice) / distância total
           
    def highest_closeness(self, top = 10): 
        '''Centralidade mais alta -> top 10'''
        cc = {} #Dicionário com as keys do grafo e com a centralidade mais próxima
        for k in self.graph.keys(): #Para todas as keys do grafo
            cc[k] = self.closeness_centrality(k) #O value de k é = à centralidade mais próxima da key do grafo
        print(cc)
        ord_cl = sorted(list(cc.items()), key=lambda x : x[1], reverse = True) #Ordena o dicionário em ordem à centralidadde mais próxima; transforma em lista posteriormente
        return list(map(lambda x:x[0], ord_cl[:top])) #Retorna os vértices com o top 10
            
    def betweenness_centrality(self, node):
        '''Soma de todas as distâncias possíveis '''
        total_sp = 0 #Caminhos curtos que existem
        sps_with_node = 0 #Caminhos curtos que passam pelo node 
        for s in self.graph.keys(): 
            for t in self.graph.keys(): 
                if s != t and s != node and t != node:
                    sp = self.shortest_path(s, t) #Retorna os caminhos dos nós de s a t
                    if sp is not None: #Isto é, se existir um caminho 
                        total_sp += 1 #Soma + 1 aos caminhos todos que existem
                        if node in sp: #Se o node se encontrar no sp 
                            sps_with_node += 1 #Adicionar + 1
        return sps_with_node / total_sp #Divisão entre os caminhos curtos que possam pelo node pelos caminhos mais curtos totais
    
    def highest_betweenness(self, top = 10):
        '''Centralidade mais alta -> top 10'''
        cc = {} #Dicionário com todas as keys do grafo e a betweenness_centrality
        for k in self.graph.keys():#Para todas as keys no grafo
            cc[k] = self.betweenness_centrality(k)#O value de k é igual a cbetweenness_centrality da key do grafo
        print(cc)
        ord_cl = sorted(list(cc.items()), key=lambda x : x[1], reverse = True) #Ordena o dicionário em ordem da betweenness_centrality (transformar em lista)
        return list(map(lambda x:x[0], ord_cl[:top])) #Retorna os vértices com o top 10
    
    def centralidade_de_grau_vertice(self,v):
        '''A centralidade de grau de um verétice é dada pelo seu grau'''
        alldegree = self.all_degrees()
        return(alldegree[v]) #Vai buscar o grau do vértice v
                    
    ## cycles    
    
    def node_has_cycle (self, v):
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

    ## clustering
        
    def clustering_coef(self, v):
        adjs = self.get_adjacents(v)
        if len(adjs) <=1: 
            return 0.0
        ligs = 0
        for i in adjs:
            for j in adjs:
                if i != j:
                    if j in self.graph[i] or i in self.graph[j]: 
                        ligs = ligs + 1
        return float(ligs)/(len(adjs)*(len(adjs)-1))
        
    def all_clustering_coefs(self):
        ccs = {}
        for k in self.graph.keys():
            ccs[k] = self.clustering_coef(k)
        return ccs
        
    def mean_clustering_coef(self):
        ccs = self.all_clustering_coefs()
        return sum(ccs.values()) / float(len(ccs))
            
    def mean_clustering_perdegree(self, deg_type = "inout"):
        degs = self.all_degrees(deg_type)
        ccs = self.all_clustering_coefs()
        degs_k = {}
        for k in degs.keys():
            if degs[k] in degs_k.keys(): 
                degs_k[degs[k]].append(k)
            else: 
                degs_k[degs[k]] = [k]
        ck = {}
        for k in degs_k.keys():
            tot = 0
            for v in degs_k[k]: 
                tot += ccs[v]
            ck[k] = float(tot) / len(degs_k[k])
        return ck

def is_in_tuple_list(tl, val):
    res = False
    for (x,y) in tl:
        if val == x: 
            return True
    return res

if __name__ == "__main__":
    gr = MyGraph()
    gr.add_vertex(1)
    gr.add_vertex(2)
    gr.add_vertex(3)
    gr.add_vertex(4)
    gr.add_edge(1,2)
    gr.add_edge(2,3)
    gr.add_edge(3,2)
    gr.add_edge(3,4)
    gr.add_edge(4,2)
    gr.print_graph()
    print(gr.size())
    
    print (gr.get_successors(2))
    print (gr.get_predecessors(2))
    print (gr.get_adjacents(2))
    
    print (gr.in_degree(2))
    print (gr.out_degree(2))
    print (gr.degree(2))
    
    print(gr.all_degrees("inout"))
    print(gr.all_degrees("in"))
    print(gr.all_degrees("out"))
    
    gr2 = MyGraph({1:[2,3,4], 2:[5,6],3:[6,8],4:[8],5:[7],6:[],7:[],8:[]})
    print(gr2.reachable_bfs(1))
    print(gr2.reachable_dfs(1))
    
    print(gr2.distance(1,7))
    print(gr2.shortest_path(1,7))
    print(gr2.distance(1,8))
    print(gr2.shortest_path(1,8))
    print(gr2.distance(6,1))
    print(gr2.shortest_path(6,1))
    
    print(gr2.reachable_with_dist(1))
    
    print(gr.has_cycle())
    print(gr2.has_cycle())
    
    print(gr.mean_degree())
    print(gr.prob_degree())
    print(gr.mean_distances())
    print (gr.clustering_coef(1))
    print (gr.clustering_coef(2))
