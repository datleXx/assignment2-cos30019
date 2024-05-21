import re
import sys
from algorithms.Algorithm import Algorithm

sys.setrecursionlimit(10000)
class BC(Algorithm):
    def __init__(self)-> None:
        super.__init__()
        self.output = "NO"
        self.outputSymbols = []
    
    def infer(self, kb, query):
        if self.TruthValue(kb, query.lst[0],[]):
            self.output = "YES: "
            for symbol in self.outputSymbols:
                if symbol != query.lst[0]:
                    self.output += symbol + ", "
            self.output += query.lst[0]
        
    def TruthValue(self, kb, query,explored):
        if query in kb.symbols.keys() and kb.symbols[query]:
            if query not in self.outputSymbols:
                self.outputSymbols.append(query)
            return True
        for sentence in kb.sentences:
            # Check if the right hand side of the sentence contain the symbol in the query
            if sentence.lst[len(sentence.lst) - 2] == query:
                # Get all the symbols on the left hand side of the setence
                leftHandSymbols = []
                for i in range (len(sentence.lst) - 2):
                    if re.search("[a-zA-Z0-9]+", sentence.lst[i]) != None:
                        leftHandSymbols.append(sentence.lst[i])

                # Check if the left hand side symbols of the sentence is true in KB
                trueSymbolCount = 0
                for symbol in leftHandSymbols:
                    if symbol == query: break
                    
                    if symbol in explored: 
                        if kb.symbols[symbol] == False:
                            break 
                    else:
                        explored.append(symbol); 
                
                    kb.symbols[symbol] = self.TruthValue(kb, symbol,explored.copy())

                    if (kb.symbols[symbol] == False): break
                    trueSymbolCount += 1

                # Check if all the symbols in the left hand side is true
                if trueSymbolCount == len(leftHandSymbols):
                    if query not in self.outputSymbols:
                        self.outputSymbols.append(query)
                    return True
        return False


    
  
                