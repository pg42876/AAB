# -*- coding: utf-8 -*-

class BoyerMoore:
    
    def __init__(self, alphabet, pattern):
        self.alphabet = alphabet
        self.pattern = pattern
        self.preprocess() 

    def preprocess(self):
        self.process_bcr()
        self.process_gsr()
        
    def process_bcr(self): 
        """ Implementação do pré-processamento do bad-character rule """
        self.occ = {} #Abre um dicionário
        for a in self.alphabet: #Adiciona ao dicionário tudo o que está no alfabeto (com valor -1)
            self.occ[a] = -1
        for b in range(len(self.pattern)): #Altera o 
            c = self.pattern[b] #Altera no dicionário a letra no  pattern para o valor b
            self.occ[c] = b #Dá a última posição onde elas estão
  
    def process_gsr(self):
        """ Implementação do pré-processamento do good suffix rule """
        self.f = [0] * (len(self.pattern) + 1) #Abre uma lista com 0 = ao comprimento do padrão
        self.s = [0] * (len(self.pattern) + 1)
        i = len(self.pattern) #Comprimento do padrão
        j = len(self.pattern) + 1 
        self.f[i] = j #Altera o último elemento da lista self.f para o valor de j
        while i > 0:
            while j <= len(self.pattern) and self.pattern[i - 1] != self.pattern [j - 1]: #Enquanto o j for menor que o tamanho do padrão e a posição do padrão de i-1 for menor que a posição do padrão de j-1
            #Define a lista s, que representa o número de casas que se podem avançar caso não haja encaixe no pattern
                if self.s[j] == 0:
                   self.s[j] = j - i
                j = self.f[j]
            i = i -1 #ou i -= 1
            j = j - 1 #ou j -= 1
            self.f[i] = j
        j = self.f[0]
        for i in range(len(self.pattern)): #Quando está definido como 0, altera-se para o valor de j mais recente, que é o mesmo que passar o resto da cadeia - passa para a frente sem comprometer a qualidade do padrão
            if self.s[i] == 0:
                self.s[i] = j
            if i == j:
                j = self.f[j]
         
    def search_pattern(self, text):
        res = []
        i = 0 #Posição inicial da sequência
        while i <= (len(text) - len(self.pattern)): #Para começar a correr a sequência
            j = len(self.pattern) - 1 #Posição no padrão
            while j >= 0 and self.pattern[j] == text[j + i]: #Continua a correr enquanto está a dar match
                j = j - 1 #Ou j -= 1
            if j < 0: #Comparação desde a última sequência do alinhamento
                res.append(i)
                i = i + self.s[0] #Avançar para i 'casas' para a frente, como j < 0 significa que deu match com um padrão  
            else:
                c = text[j + i]
                i += max(self.s[j + 1], j - self.occ[c]) #Avançar uma sequência dependendo do GSR e BCR
        return res

def test():
    bm = BoyerMoore("ACTG", "ACCA")
    print (bm.search_pattern("ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC"))

if __name__ == '__main__':
    test()
    
#result: [5, 13, 23, 37]