import sys
from algorithms.Algorithm import Algorithm

sys.setrecursionlimit(10000)

class TT(Algorithm):
    def __init__(self) -> None:
        # super.__init__()
        self.output = ""
        self.count = 0
        self.check = None

    def infer(self,kb,query): #infer the query from the knowledgebase
        temp = [] #list to store all symbols include in the query and knowledge base
        for x in query.symbols: #get symbols from the query
            temp.append(x.getCharacter())
        lst = kb.symbols.copy() 
        for x in temp: #combine any new symbol in query with symbols in the knowledge base
            lst[x] = False
        symbols = list(lst.keys()) #just get the unique set of symbols in both query and knowledge base
        self.TTCheckAll(kb,query,symbols,{}) #check the entailment
        if  self.check == "NO": #if detect a case that does not entail then the output is NO 
            self.output = "NO"
        else:
            self.output = f"YES: {self.count}"
        
    def TTCheckAll(self,kb, query, symbols, model):
       
        if self.check == "NO": #if the query already not entailed by the kb then return 
            return
        if len(symbols) == 0: #if we get enough number of symbols then check for entailment
            if kb.PLTrue(model): #satisfy kb
                query.setValue(model)
                if query.result(): #satisfy query
                    self.count +=1
                else: #otherwise return no
                    self.check = "NO" 
        else:
            s = symbols.pop(0) #copy all the lists and objects to prevent call by reference
            s1 = symbols.copy() #every objects need to be new ones
            s2 = symbols.copy()
            t1 = model.copy()
            t2 = model.copy()
            t1[s] = True
            a = self.TTCheckAll(kb, query, s1, t1) 
            t2[s] = False
            b= self.TTCheckAll(kb, query, s2, t2)