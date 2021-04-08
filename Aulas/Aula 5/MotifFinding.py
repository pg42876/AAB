# -*- coding: utf-8 -*-

from MySeq import MySeq
from MyMotifs import MyMotifs

class MotifFinding:
    
    def __init__(self, size = 8, seqs = None):
        self.motifSize = size 
        if (seqs != None): #Vai ver qual é o tamanho dos motifs 
            self.seqs = seqs
            self.alphabet = seqs[0].alfabeto()
        else:
            self.seqs = []
                    
    def __len__ (self):
        return len(self.seqs)
    
    def __getitem__(self, n):
        return self.seqs[n]
    
    def seqSize (self, i):
        return len(self.seqs[i])
    
    def readFile(self, fic, t): #Lê um ficheiro que vai 
        for s in open(fic, "r"):
            self.seqs.append(MySeq(s.strip().upper(),t))
        self.alphabet = self.seqs[0].alfabeto()
        
        
    def createMotifFromIndexes(self, indexes): #Recebe uma lista de números composta pelos números das posições inciais dos motifs
        pseqs = []
        for i,ind in enumerate(indexes): #Faz uma contagem de elementos
            pseqs.append( MySeq(self.seqs[i][ind:(ind+self.motifSize)], self.seqs[i].tipo) ) #
        return MyMotifs(pseqs)
        
        
    # SCORES
        
    def score(self, s): 
        score = 0
        motif = self.createMotifFromIndexes(s)
        motif.doCounts() #Cria a matriz de contagem
        mat = motif.counts 
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for  i in range(1, len(mat)):
                if mat[i][j] > maxcol: 
                    maxcol = mat[i][j]
            score += maxcol
        return score #Dá return ao score máximo
   
    def scoreMult(self, s):
        score = 1.0
        motif = self.createMotifFromIndexes(s)
        motif.createPWM()
        mat = motif.pwm
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for  i in range(1, len(mat)):
                if mat[i][j] > maxcol: 
                    maxcol = mat[i][j]
            score *= maxcol
        return score     
       
    # EXHAUSTIVE SEARCH - vai comparar tudo com tudo
       
    def nextSol (self, s): 
        nextS = [0]*len(s) #Lista que contém as posições das sequências onde começa a formação dos motifs
        pos = len(s) - 1 #Posição é o comprimento da lista - 1
        while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if (pos < 0): 
            nextS = None #Vai finalizar e temos como resultado as posições dos motifs nas sequências
        else:
            for i in range(pos): 
                nextS[i] = s[i]
            nextS[pos] = s[pos] + 1 #Próxima posição do motif
            for i in range(pos + 1, len(s)):
                nextS[i] = 0
        return nextS
        
    def exhaustiveSearch(self):
        melhorScore = -1
        res = []
        s = [0]* len(self.seqs) #Posição inicial das sequências onde começam os motifs
        while (s!= None):
            sc = self.score(s) #Vai calcular o score dos motifs na posição inicial com o size escolhido
            if (sc > melhorScore):
                melhorScore = sc
                res = s #Lista com as posições iniciais onde vai começar o motif
            s = self.nextSol(s)
        return res #O resultado são as posições inicais que vão maximizar o score
     
    # BRANCH AND BOUND     
     
    def nextVertex (self, s):
        res =  []
        if len(s) < len(self.seqs): # internal node -> down one level
            for i in range(len(s)): 
                res.append(s[i])
            res.append(0) #Adiciona um 0 para começar na primeira
        else: # bypass
            pos = len(s)-1 #Número de sequências existentes
            while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize: #Enquanto a posição
                pos -= 1 #Verifica se a posição é menor que 0
            if pos < 0: 
                res = None # last solution
            else:
                for i in range(pos): 
                    res.append(s[i]) #
                res.append(s[pos]+1) #
        return res #
    
    
    def bypass (self, s): #Verifica se já chegou ou não ao final de uma sequência 
        res =  []
        pos = len(s) -1
        while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if pos < 0: 
            res = None 
        else:
            for i in range(pos): 
                res.append(s[i])
            res.append(s[pos] + 1)
        return res
        
    def branchAndBound (self): #Só verifica quando chegamos ao final de uma das sequências
        melhorScore = -1
        melhorMotif = None
        size = len(self.seqs)
        s = [0]*size
        while s != None:
            if len(s) < size: #Significa que já chegou à última posição de uma das sequências
                optimScore = self.score(s) + (size-len(s)) * self.motifSize 
                if optimScore < melhorScore: #Se o score ótimo for menor que o melhor score anteriormente descoberto
                    s = self.bypass(s) #Passa-se a análise à frente
                else: 
                    s = self.nextVertex(s) 
            else:
                sc = self.score(s) #Calcular o score dos motifs
                if sc > melhorScore:
                    melhorScore = sc
                    melhorMotif  = s
                s = self.nextVertex(s)
        return melhorMotif

    # Consensus (heuristic)
  
    def heuristicConsensus(self): #É mais rápido mas não é o ideal porque as duas primeiras sequências não garantem a conservação das sequências
        """ Procura as posições para o motif nas duas primeiras sequências """ 
        mf = MotifFinding(self.motifSize, self.seqs[:2]) #Procura exaustiva das duas primeiras sequências 
        s = mf.exhaustiveSearch() #Exemplo: (1, 3) -> 1 corresponde à primeira posição do motif na sequência e o 3 a segunda posição
        for a in range(2, len(self.seqs)): #Avalia a melhor posição para cada uma das sequências, guardando-a (maximiza o score)
            s.append(0)
            melhorScore = -1 
            melhorPosition = 0
            for b in range(self.seqSize(a) - self.motifSize + 1):
                s[a] = b 
                scoreatual = self.score(s)
                if scoreatual > melhorScore:
                    melhorScore = scoreatual
                    melhorPosition = b
                s[a] = melhorPosition
        return s

    # Consensus (heuristic)

    def heuristicStochastic (self):
        from random import randint
        s = [0] * len(self.seqs) #Gerar um vetor aleatória com o mesmo tamnho do número de sequências
        #Passo 1: inicia todas as posições com valores aleatórios 
        for i in range(len(self.seqs)):
            s[i] = randint(0, self.seqSize(i) - self.motifSize) #Randint (A, B) retorna um valor x que é: A <= x <= B; escolhe um valor aleatório onde começa o motif
        #Passo 2
        melhorscore = self.score(s)
        improve = True
        while improve:
            motif = self.createMotifFromIndexes(s) #Constrói o perfil com base nas posições iniciais s
            motif.createPWM() #Cria a matriz PWM
            #Passo 3
            for i in range(len(self.seqs)): #Avalia a melhor posição inicial para cada sequência com base no perfil
                s[i] = motif.mostProbableSeq(self.seqs[i]) #Vai ver em cada sequência qual é a subsequência que é mais provável acontecer na PWD
            #Passo 4
            #Verifica se houve alguma melhoria
            scr = self.score(s) #Vai calcular o score
            if scr > melhorscore: #Se o score for melhorado, o ciclo volta-se a repetir
                melhorscore = scr
            else: 
                improve = False
        return s

    # Gibbs sampling 

    def gibbs (self, interations = 100):
        from random import randint
        s = []
        #Passo 1
        for i in range(len(self.seqs)):
            s.append(randint(0, len(self.seqs[i]) - self.motifSize -1)) #[i] porque as sequências têm de ter todas o mesmo tamanho
        melhors = list(s)
        melhorscore = self.score(s) #Calcular o score de s
        for a in range(interations):
            #Passo 2: selecionar uma das sequência aleatoriamente
            seq_idx = randint(0, len(self.seqs) - 1) #Posição
            #Passo 3: criar um perfil que não contenha a sequência aleatória
            seq = self.seqs[seq_idx] #Indica qual é a sequência que vai ser removida
            s.pop(seq_idx) #Remove a posição inicial correspondente à sequência escolhida que foi removida
            removed = self.seqs.pop(seq_idx) #Mostra qual é a sequência que foi removida
            motif = self.createMotifFromIndexes(s) #Criar o perfil sem a sequência removida
            motif.createPWM() #Cria a matriz de PWD
            self.seqs.insert(seq_idx, removed) #Vai adicionar a sequência que foi removida anteriormente
            r = motif.probAllPositions(seq) #Calcular a probabilidade de todas as subsequências possíveis na sequência removida
            position = self.roulette(r) #Fazer o roulette da lista e escolhe um valor dos valores maiores do que 0, devolvendo a posição se iniciou o motif
            s.insert(seq_idx, position) #Adiciona o valor da posição do motif na posição da seq_idx
            scr = self.score(s) #Cálculo do novo score de s 
            if scr > melhorscore: #Se o score é maior que o melhorscore, este passa a ser o score e a bests passa a ser s
                melhorscore = scr
                bests = list(s)
        return bests

    def roulette(self, f): 
        from random import random
        tot = 0.0
        for x in f: 
            tot += (0.01 + x)
        val = random() * tot #Vai multiplicar o total por um valor random - dá um número entre 0 e 1 (não incluído)
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] + 0.01)
            ind += 1
        return ind-1

#------------------------------------------------------------------------------------------------------------------------------------------------#
    
    #Exercícios aulas 
    def ex_score(self, m): #Responsável por calcular a contagem com as pseudocontagens
        score = 0
        motif = self.createMotifFromIndexes(m)
        motif.doCounts()
        mat = []
        for i in range(len(motif.counts)):
            linha = []
            for j in range(len(motif.counts[i])):
                linha.append(motif.counts[i][j] + 1)
            mat.append(linha)
        for k in range(len(mat[0])):
            maxcol = mat[0][k] 
            for  f in range(1, len(mat)): 
                if mat[f][k] > maxcol: 
                    maxcol = mat[f][k]
            score += maxcol 
        return score
    
    def ex_probabSeq(self, seq, PWM): #Calcula a probabilidade da sequência fazer parte ou não da PWM (nenhum dos valores é negativo)
        res = 1.0
        for i in range(self.motifSize):
            lin = self.alphabet.index(seq[i])
            res *= PWM[lin][i]
        return res

    def ex_mostProbableSeq(self, seq, PWM): #Vai ser qual é a posição inicial da subsequência de uma sequência de comprimento indefinido que encaixa melhor no quadro dos motifs das sequências
        maximo = -1.0
        maxind = -1
        for k in range(len(seq)-self.motifSize):
            p = self.ex_probabSeq(seq[k:k+ self.motifSize], PWM)
            if(p > maximo):
                maximo = p
                maxind = k
        return maxind
    
    def ex_probAllPositions(self, seq, PWM): #Devolve uma lista com as probabilidades de ocorrer em cada letra da sequência
        res = []
        for k in range(len(seq)-self.motifSize+1):
            res.append(self.ex_probabSeq(seq, PWM))
        return res
    
    def ex_heuristicStochastic(self): 
        from random import randint
        s = [0] * len(self.seqs)
        for i in range(len(self.seqs)):
            s[i] = randint(0, self.seqSize(i) - self.motifSize)
        melhorscore = self.ex_score(s) #Faz o score consoante o novo score (não vai conter valores iguais a 0 com as pseudocontagens)
        improve = True
        while improve:
            motif = self.createMotifFromIndexes(s)
            motif.createPWM()
            newPWM = [] #Contruir a matriz PWM sem nenhum valor negativo
            for k in range(len(motif.PWM)):
                linhas = []
                for t in range(len(motif.PWM[0])):
                    linhas.append(motif.PWM[k][t] + 0.1)
                newPWM.append(linhas)
            for i in range(len(self.seqs)):
                s[i] = self.ex_mostProbableSeq(self.seqs[i], newPWM)
            scr = self.ex_score(s)
            if scr > melhorscore:
                melhorscore = scr
            else: 
                improve = False
        return s
    
    def ex_gibbs(self, interations = 100):
        from random import randint
        s = [] 
        for i in range(len(self.seqs)):
             s.append(randint(0, len(self.seqs[i]) - self.motifSize -1))
        melhorscore = self.scoreEX(s)
        bests = list(s)
        for it in range(iterations):
            seq_idx = randint(0, len(self.seqs) - 1)
            seq = self.seqs[seq_idx]
            s.pop(seq_idx)
            removed = self.seqs.pop(seq_idx)
            motif = self.createMotifFromIndexes(s)
            motif.createPWM()
            newPWM = [] 
            for k in range(len(motif.PWM)):
                linhas = []
                for t in range(len(motif.PWM[0])):
                    linhas.append(motif.PWM[k][t] + 0.1)
                newPWM.append(linhas)
            self.seqs.insert(seq_idx, removed) #Volta a adicionar a sequência removida à lista de sequências na posição seq_idx
            r = self.ex_probAllPositions(seq, newPWM) #Calcula a probabilidade de todas as subsequências possíveis na sequência removida
            pos = self.roulette(r) #Faz o roulette da lista e escolhe um dos valores maiores que 0 e devolve a posição onde se iniciou o motif
            s.insert(seq_idx, pos) #Adiciona o valor da posição do motif à lista s na posição seq_idx
            score = self.ex_score(s) #Calcula o novo score de s
            if score > melhorscore: #Se o score for maior que o melhor score, o melhor score passa a ser o score e a bests passa a ser a lista s
                melhorscore = score
                bests = list(s)
        return bests

# tests

def test1():  
    sm = MotifFinding()
    sm.readFile("C:/Users/maria/Desktop/UNI/1º Ano/2º Semestre/Algoritmos Avançados de Bioinformática/Prática/Aula 5/exemploMotifs.txt","dna")
    sol = [25,20,2,55,59]
    sa = sm.score(sol)
    print(sa)
    scm = sm.scoreMult(sol)
    print(scm)

def test2():
    print ("Test exhaustive:")
    seq1 = MySeq("ATAGAGCTGA","dna")
    seq2 = MySeq("ACGTAGATGA","dna")
    seq3 = MySeq("AAGATAGGGG","dna")
    mf = MotifFinding(3, [seq1,seq2,seq3])
    sol = mf.exhaustiveSearch()
    print ("Solution", sol)
    print ("Score: ", mf.score(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())

    print ("Branch and Bound:")
    sol2 = mf.branchAndBound()
    print ("Solution: " , sol2)
    print ("Score:" , mf.score(sol2))
    print("Consensus:", mf.createMotifFromIndexes(sol2).consensus())
    
    print ("Heuristic consensus: ")
    sol1 = mf.heuristicConsensus()
    print ("Solution: " , sol1)
    print ("Score:" , mf.score(sol1))

def test3():
    mf = MotifFinding()
    mf.readFile("C:/Users/maria/Desktop/UNI/1º Ano/2º Semestre/Algoritmos Avançados de Bioinformática/Prática/Aula 5/exemploMotifs.txt","dna")
    print ("Branch and Bound:")
    sol = mf.branchAndBound()
    print ("Solution: " , sol)
    print ("Score:" , mf.score(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())

def test4():
    mf = MotifFinding()
    mf.readFile("C:/Users/maria/Desktop/UNI/1º Ano/2º Semestre/Algoritmos Avançados de Bioinformática/Prática/Aula 5/exemploMotifs.txt","dna")
    print("Heuristic stochastic")
    sol = mf.heuristicStochastic()
    print ("Solution: " , sol)
    print ("Score:" , mf.score(sol))
    print ("Score mult:" , mf.scoreMult(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())
    sol2 = mf.gibbs()
    print ("Score:" , mf.score(sol2))
    print ("Score mult:" , mf.scoreMult(sol2))

def ex_test():
    mf = MotifFinding()
    mf.readFile("C:/Users/maria/Desktop/UNI/1º Ano/2º Semestre/Algoritmos Avançados de Bioinformática/Prática/Aula 5/exemploMotifs.txt","dna")
    print("Heuristic stochastic:")
    sol = mf.ex_heuristicStochastic()
    print ("Solution:" , sol)
    print ("Score:" , mf.ex_score(sol))
    print("ConsensusEX:", mf.createMotifFromIndexes(sol).consensus())
    sol2 = mf.ex_gibbs()
    print ("Score:" , mf.ex_score(sol2))

test4()