s = [-1,0,1,2,-1,-4]
l = []
l1 = []
for a in range(0,len(s)):
    for b in range(a+1,len(s)):
        for c in range(b+1 ,len(s)):
            print(a,b,c)
            
            if s[a]+s[b]+s[c] == 0 :
                
                l.append([s[a],s[b],s[c]])
for v in l:
    v.sort() 
    if v not in l1:
        l1.append(v)  
l1.sort()  

print(l1)

           

       
        
            

           
        
           #print(s[b][0:a])
  

