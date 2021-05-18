from MyGraph import MyGraph

class MetabolicNetwork (MyGraph): 
    #Sub-classe associada à classe MyGraph (herança) -> deriva de uma classe
    
    def __init__(self, network_type = "metabolite-reaction", split_rev = False):
        #split_rev-> indica se as  reações são ou não reversíveis, isto é, se nos mostra as reações reversiveis através do grafo
        #Indica se se consideram as reações reversíveis como duas reações distintas, uma para cada direção (True) ou não (False)
        #Tipo de rede-> é o que lhe passarmos
        MyGraph.__init__(self, {}) #Construtor da classe MyGraph - cria o self.graph (podia pôr-se self.graph = {})
        self.net_type = network_type #Tipo de rede
        self.node_types = {} #Tipos de nós
        if network_type == "metabolite-reaction":
            self.node_types["metabolite"] = [] #Tipo de nó - metabolitos
            self.node_types["reaction"] = [] #Tipo de nó - reações
        self.split_rev = split_rev #flag
    
    def add_vertex_type(self, v, nodetype): #Esta função serve para adicionar novos nós
        self.add_vertex(v) #Chama o add_vertex da classe mãe e cria um nó
        self.node_types[nodetype].append(v) #Atualiza a lista de nós 
    
    def get_nodes_type(self, node_type): #Vai buscar os nós de diferentes tipos
        if node_type in self.node_types: #Se o nós estiverem na lista dos tipos de nós
            return self.node_types[node_type] #Dá return dos tipos de nós que queremos
        else: 
            return None
    
    def load_from_file(self, filename): #Load do ficheiro para ter as reações e criar o grafo
        rf = open(filename)
        gmr = MetabolicNetwork("metabolite-reaction") #Metabolito-reação
        for line in rf: #Lê cada linha do ficheiro
            if ":" in line:
                tokens = line.split(":")
                reac_id = tokens[0].strip()
                gmr.add_vertex_type(reac_id, "reaction")
                rline = tokens[1]
            else: raise Exception("Invalid line:")                
            if "<=>" in rline:
                left, right = rline.split("<=>")
                mets_left = left.split("+")
                for met in mets_left:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    if self.split_rev:
                        gmr.add_vertex_type(reac_id+"_b", "reaction")
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id+"_b", met_id)
                    else:
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id, met_id)
                mets_right = right.split("+")
                for met in mets_right:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    if self.split_rev:
                        gmr.add_edge(met_id, reac_id+"_b")
                        gmr.add_edge(reac_id, met_id)
                    else:
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id, met_id)
            elif "=>" in line:
                left, right = rline.split("=>") #Irreversível
                mets_left = left.split("+")
                for met in mets_left:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    gmr.add_edge(met_id, reac_id)
                mets_right = right.split("+")
                for met in mets_right:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    gmr.add_edge(reac_id, met_id)
            else: 
                raise 
            Exception("Invalid line:")    

        if self.net_type == "metabolite-reaction": #Se for metabolito-reação
            self.graph = gmr.graph #Vai ser o grafo que está no objeto gmr em cima
            self.node_types = gmr.node_types 
        elif self.net_type == "metabolite-metabolite":
            self.convert_metabolite_net(gmr) #Converte o grafo em gmr num grafo só de metabolitos
        elif self.net_type == "reaction-reaction": 
            self.convert_reaction_graph(gmr) #Converte o grafo em gmr num grafo só de reações
        else: self.graph = {}
        
    def convert_metabolite_net(self, gmr): #Cria a rede metabolito-metabolito
        for m in gmr.node_types["metabolite"]: #Para cada metabolito em gmr
            self.add_vertex(m) #Juntar o vértice ao novo grafo - não é necessário!
            sucs = gmr.get_successors(m) #Buscar os sucessores do m
            for s in sucs: #Para cada s em sucs
                sucs_r = gmr.get_successors(s) #Buscar os sucessores de s
                for s2 in sucs_r: #Para cada s2 em sucs_r
                    if m != s2: #Se m for diferentes de s2 (ou seja, se não existir)
                        self.add_edge(m, s2) #Adiciona um arco (m, s2)
        
    def convert_reaction_graph(self, gmr): #Cria a rede reação-reação
        for r in gmr.node_types["reaction"]: #Para cada reação em gmr
            self.add_vertex(r) #Juntar o vértice ao novo grafo - não é necessário!
            sucs = gmr.get_successors(r) #Buscar os sucessores do r
            for s in sucs: #Para cada s em sucs
                sucs_r = gmr.get_successors(s) #Buscar os sucessores de s
                for s2 in sucs_r: #Para cada s2 em sucs_r
                    if r != s2: #Se r for diferentes de s2 (ou seja, se não existir)
                        self.add_edge(r, s2) #Adiciona o arco (r, s2)

def test1():
    m = MetabolicNetwork("metabolite-reaction") #Cria o tipo de rede
    m.add_vertex_type("R1","reaction") #Adiciona o nó
    m.add_vertex_type("R2","reaction")
    m.add_vertex_type("R3","reaction")
    m.add_vertex_type("M1","metabolite")
    m.add_vertex_type("M2","metabolite")
    m.add_vertex_type("M3","metabolite")
    m.add_vertex_type("M4","metabolite")
    m.add_vertex_type("M5","metabolite")
    m.add_vertex_type("M6","metabolite")
    m.add_edge("M1","R1") #Adiciona o arco entre os nós (ao nó M1 vou adicionar uma ligação R1)
    m.add_edge("M2","R1")
    m.add_edge("R1","M3")
    m.add_edge("R1","M4")
    m.add_edge("M4","R2")
    m.add_edge("M6","R2")
    m.add_edge("R2","M3")
    m.add_edge("M4","R3")
    m.add_edge("M5","R3")
    m.add_edge("R3","M6")
    m.add_edge("R3","M4")
    m.add_edge("R3","M5")
    m.add_edge("M6","R3")
    m.print_graph()
    print("Reactions: ", m.get_nodes_type("reaction") ) #Lista de reações
    print("Metabolites: ", m.get_nodes_type("metabolite") ) #Lista de metabolitos

        
def test2():
    print("metabolite-reaction network:")
    mrn = MetabolicNetwork("metabolite-reaction")
    mrn.load_from_file("example-net.txt")
    mrn.print_graph()
    print("Reactions: ", mrn.get_nodes_type("reaction") )
    print("Metabolites: ", mrn.get_nodes_type("metabolite") )
    print()
    
    print("metabolite-metabolite network:")
    mmn = MetabolicNetwork("metabolite-metabolite")
    mmn.load_from_file("example-net.txt")
    mmn.print_graph()
    print()
    
    print("reaction-reaction network:")
    rrn = MetabolicNetwork("reaction-reaction")
    rrn.load_from_file("example-net.txt")
    rrn.print_graph()
    print()
    
    print("metabolite-reaction network (splitting reversible):")
    mrsn = MetabolicNetwork("metabolite-reaction", True)
    mrsn.load_from_file("example-net.txt")
    mrsn.print_graph()
    print()
    
    print("reaction-reaction network (splitting reversible):")
    rrsn = MetabolicNetwork("reaction-reaction", True)
    rrsn.load_from_file("example-net.txt")
    rrsn.print_graph()
    print()

def test3():
    print("metabolite-reaction network:")
    mrn = MetabolicNetwork("metabolite-reaction")
    mrn.load_from_file("ecoli.txt")
    mrn.print_graph()
    print("Reactions: ", mrn.get_nodes_type("reaction") )
    print("Metabolites: ", mrn.get_nodes_type("metabolite") )
    print()
  
    print("metabolite-metabolite network:")
    mmn = MetabolicNetwork("metabolite-metabolite")
    mmn.load_from_file("ecoli.txt")
    mmn.print_graph()
    print()
    
    print("reaction-reaction network:")
    rrn = MetabolicNetwork("reaction-reaction")
    rrn.load_from_file("ecoli.txt")
    rrn.print_graph()
    print()
    
    print("metabolite-reaction network (splitting reversible):")
    mrsn = MetabolicNetwork("metabolite-reaction", True)
    mrsn.load_from_file("ecoli.txt")
    mrsn.print_graph()
    print()
    
    print("reaction-reaction network (splitting reversible):")
    rrsn = MetabolicNetwork("reaction-reaction", True)
    rrsn.load_from_file("ecoli.txt")
    rrsn.print_graph()
    print()

#test1()
#print()
#test2()
#print()
test3()
print()