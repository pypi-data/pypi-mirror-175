def mainfunc(stringval):
    global charlist
    chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvxyz1234567890!”#$%&’()*+,-./:;<=>?@[\]^_`{|}~'
    def listsplitChars(word):
        return [char for char in word]
    charlistunsorted=listsplitChars(chars)
    charlist = sorted(charlistunsorted, key=lambda sub: ord(max(sub)))

    stringvalList = stringval.split()
    global stringrotations
    stringrotations=[]
    

    match=[]
    for st in stringval :
        if st in charlist:
            match.append(charlist.index(st))
    charstring=''.join(charlist)

    def Rotate(string): 
        b = len(string)
        for i in range (b):
            c = string[i:]+string[:i]
            stringrotations.append(c)
        
    if len(stringval)>64:
        nlen=64
        strinput_sep=[stringval[idx:idx + nlen] for idx in range(0, len(stringval), nlen )]
        for word in strinput_sep:
            Rotate(word)
    else:
        for word in stringvalList:
            Rotate(word)


    firstcharletters=[]
    firstcharindex=[]
    for ss in stringvalList:
            firstcharletters.append(ss[0])
    for ss1 in firstcharletters:
            if ss1 in charlist:
                firstcharindex.append(charlist.index(ss1))   

    k=sum(firstcharindex)
    w=k%len(stringrotations)
    stringvalchosen=stringrotations[w]
    
    stringlist=[]
    difflist=[]
    encryptlist=[]
    encryptstr=''

    for b in stringvalchosen :
        stringlist.append(charstring.find(b))

    for f in range(1,len(stringlist)):
        x = stringlist[f] - stringlist[f-1]
        difflist.append(x-1)
    if len(stringlist)>1:
        firstchar=stringlist[0]-stringlist[-1]         
        difflist.insert(0, firstchar)
    else:
        firstchar=stringlist[0]
        difflist.insert(0, firstchar)
    for l in difflist:
        encryptlist.append(charlist[l])
    for i in encryptlist:
        encryptstr += i 
    return encryptstr

def frequencySorting(stringval):
    stringval_wowhitespaces = stringval.strip()
    stringval_wowhitespaces = stringval_wowhitespaces.replace(" ","")
   
    count = {}
    for ch in stringval_wowhitespaces:
        if ch in count:
            count[ch] += 1
        else:
            count[ch] = 1

    frequency_sorted_string = ""

    for key, val in sorted(count.items(),key=lambda item: item[1],reverse=True): 
        frequency_sorted_string += key
    return frequency_sorted_string

def index_list_normalizer(string_list):

    index=0
    string_list_updated=string_list
    for i in string_list:
        if (i>len(charlist)-1):
            new_i=i%len(charlist)
            string_list_updated[index]=new_i
        index+=1

    return string_list_updated  

def mod_vig(plaintext, key):
    key_length = len(key)
    #print("2. GPEncString as key: "+key)
    key_as_int = [ord(i) for i in key]
    key_as_int = index_list_normalizer(key_as_int)
    #print(f'GPEnc as key (in int): {key_as_int}')
    plaintext_int = [ord(i) for i in plaintext]
    plaintext_int = index_list_normalizer(plaintext_int)
    #print(f'Plaintext_int list generated:{plaintext_int}')
    ciphertext = ''
    for i in range(len(plaintext_int)):
        value = (plaintext_int[i] + key_as_int[i % key_length])
        ciphertext += charlist[(value + len(key_as_int))%len(charlist)]
    return ciphertext

def hash(strinput):
    str1=mainfunc(strinput)
    freqencr=mainfunc(frequencySorting(strinput))
    finalenc=freqencr+str1

    gplist=[]
    gpenclist=[]
    fin_sum=[]   
    for p in finalenc:
        fin_sum.append(ord(p))
    #print(f'List of all unicode values of all characters in final encrypted string: {fin_sum}')
    #print unicode values of each character in the string input
    #TN = a1 * r(n-1)    Geometric Progression Formula
    crsumlist=[]
    for w in strinput:
        crsumlist.append(ord(w))
    start_number = sum(fin_sum) # starting number (a)
    common_ratio = sum(crsumlist)  # Common ratio (r)
    nth_term = len(finalenc) # N th term to be found (n)

    for i in range(0, nth_term):
        curr_term = start_number * pow(common_ratio, i)%len(charlist)
        gplist.append(curr_term)
    #print(f"GP List: {gplist}")

    for m in gplist:
        gpenclist.append(charlist[m])
    gpencstring=''.join(gpenclist)
    #print(f'GP Encrypted String: {gpencstring}')

    fgpstring=mod_vig(finalenc,gpencstring)
    return fgpstring

