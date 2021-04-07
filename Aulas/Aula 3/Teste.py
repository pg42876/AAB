#Funçaõ build_bwt
text = 'AGCGGT'
ls = []
for a in range(len(text)):
    ls.append(text[a:] + text[:a]) 
    print (ls)
ls.sort() 
print (ls)
res = ''
for b in range(len(text)):
    res += ls[b][len(text) - 1]
    print (res)
print (res) 

