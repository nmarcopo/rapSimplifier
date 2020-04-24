#%%
import bisect 
import math

def e_step(s):
    s[0]=s[0].split(' ')
    s[1]=s[1].split(' ')
    m=len(s[0])
    l=len(s[1])
    for j in range(0,m):
        en_sum=0
        for i in range(0,l):
            fe=s[0][j]+'|'+s[1][i]
            if fe in t:
                en_sum+=t[fe]
        for i in range(0,l):
            fe=s[0][j]+'|'+s[1][i]
            if fe in t and fe in c:
                c[fe]+= t[fe]/(en_sum)

def m_step():
    ch_sums={}
    for key, value in c.items():
        words=key.split('|')
        if words[1] in ch_sums:
            ch_sums[words[1]]+=value
        else:
            ch_sums[words[1]]=value
    for key in t:
        words=key.split('|')
        t[key]=c[key]/ch_sums[words[1]]
    return ch_sums

def likelihood(s):
    p_sum=0
    prod=1

    s[0]=s[0].split(' ')
    s[1]=s[1].split(' ')
    l=len(s[1])

    for ch_word in range(1,len(s[0])):
        en_sum=0
        for en_word in s[1]:
            fe=s[0][ch_word]+'|'+en_word
            if fe in t:
                en_sum+=t[fe]
        prod*=(1/(l+1))*en_sum
    return prod*.01

f=open('/Users/jwenger/documents/hw5/rapSimplifier/rapSimplifier/data/rap_en.txt')
t={}
c={}
null='NULL'
#lines=[]
#lines.append('garcia y asociados\tgarcia and associates')
#lines.append('sus asociados no son fuertes\this associates are not strong')
ch_words=set([])
en_words=set([])

x=0
for line in f.readlines():
    if x<30:
        line = line.split('\t')

        ch_line = line[0].split(' ')
        en_line = line[1].split(' ')

        for ch_word in ch_line:
            ch_words.add(ch_word)
            t[ch_word+'|'+null]=1
            c[ch_word+'|'+null]=0
            for en_word in en_line:
                if en_word[-1]=='\n':
                    en_word=en_word[:-1]
                en_words.add(en_word)
                t[ch_word+'|'+en_word]=1
                c[ch_word+'|'+en_word]=0
                
        #x+=1
for key, val in t.items():
    t[key]=1/len(ch_words)

for x in range(10):
    f=open('/Users/jwenger/documents/hw5/rapSimplifier/rapSimplifier/data/rap_en.txt')
    p_sum=0
    for item in c:
        c[item]=0
    for line in f.readlines():
        if line[-1]=='\n':
            line=line[:-1]
        line += ' NULL'
        e_step(line.split('\t'))
        #p_sum+=math.log(likelihood(line.split('\t')))
    #print('log probability:',p_sum)
    m_step()
    f=open('/Users/jwenger/documents/hw5/rapSimplifier/rapSimplifier/data/rap_en.txt')

#%%
#c['Trapping|sell']
#%%
out=open('ttable.out', 'w+')
for key, value in t.items():
    words = key.split('|')
    out.write('{} {} {}\n'.format(words[1],words[0],value))

 
samples=set(['jedi', 'force', 'droid', 'sith', 'lightsabre'])
tops={}
back={}
for samp in samples:
    tops[samp]=[]
for key, value in t.items():
    words = key.split('|')
    if words[1] in samples:
        bisect.insort(tops[words[1]], value) 
        back[value]=words[0]
for samp in samples:
    for x in range(1,6):
        print('{}: translation rank {}: {}, probability: {}'.format(samp, x, back[tops[samp][-x]], tops[samp][-x]))


