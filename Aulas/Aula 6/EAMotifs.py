from EvolAlgorithm import EvolAlgorithm
from Popul import PopulInt, PopulReal
from MotifFinding import MotifFinding
from MyMotifs import MyMotifs

def createMatZeros(nl, nc):
    res = []
    for _ in range(0, nl):
        res.append([0]*nc)
    return res

def printMat(mat):
    for i in range(0, len(mat)):
        for j in range(len(mat[i])):
            print(f"{mat[i][j]:.3f}", end=' ')
        print()

class EAMotifsInt (EvolAlgorithm):

    def __init__(self, popsize, numits, noffspring, filename):
        self.motifs = MotifFinding()
        self.motifs.readFile(filename, "dna")
        indsize = len(self.motifs)
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)

    def initPopul(self, indsize):
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize
        self.popul = PopulInt(self.popsize, indsize,
                              maxvalue, [])

    def evaluate(self, indivs):
        for i in range(len(indivs)):
            ind = indivs[i]
            sol = ind.getGenes()
            fit = self.motifs.score(sol)
            ind.setFitness(fit)

class EAMotifsReal (EvolAlgorithm):

    def __init__(self, popsize, numits, noffspring, filename):
        self.motifs = MotifFinding()
        self.motifs.readFile(filename, "dna")
        indsize = self.motifs.motifSize * len(self.motifs.alphabet)
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)

    def initPopul(self, indsize):
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize
        self.popul = PopulReal(self.popsize, indsize,
                              maxvalue, [])

    def vector_to_PWM(self, v): #v -> vetor de números reais 
        self.pwm = createMatZeros(len(self.mtoifs.alphabet), self.motifs.motifSize)
        for i in range(0, len(v), self.motifs.alphabet):
            col_idx = i / len(self.motifs.alphabet)
            col = v[i : i + len(self.motifs.alphabet)]
            soma = sum(col)
            for j in range(len(self.motifs.alphabet)):
                self.pwm[j][col_idx] = col[j] / soma
        return pwm
        
    def evaluate(self, indivs):
        for i in range(len(indivs)):
            ind = indivs[i]
            sol = ind.getGenes()
            self.motifs.pwm = self.vector_to_PWM(sol)
            s = []
            for seq in self.motifs.seqs:
                p = self.motifs.mostProbableSeq(seq)
                s.append(p)
            ## TPC - ussar score multiplicativo sem atualizar a PWM ##
            fit = self.motifs.score(sol)
            ind.setFitness(fit)

def test1():
    ea = EAMotifsInt(100, 1000, 50, "exemploMotifs.txt")
    ea.run()
    ea.printBestSolution()

def test2():
    ea = EAMotifsReal(100, 2000, 50, "exemploMotifs.txt")
    ea.run()
    ea.printBestSolution()

#test1()
test2()