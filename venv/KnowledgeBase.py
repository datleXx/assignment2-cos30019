from HornForm import HornForm
from Sentence import Sentence
import re 

class KnowledgeBase:
    """Used to store propositional statements and symbols."""
    def __init__(self, sentences):
        ## fields ##
        self.sentences = []        # sentences contained in knowledge base
        self.symbols = {}         # all found unique symbols in sentences
        for sentence in sentences: # add sentences
            self.tell(sentence)

    # tell knowledge base a sentence
    def tell(self, sentence):
        new = Sentence(sentence)
        self.sentences.append(new)
        lst = [sym.getCharacter() for sym in new.symbols]
        # print(lst)
        # add new symbols to knowledge base if found
        if len(lst) == 1: 
            if lst[0] in self.symbols: 
                self.symbols.pop(lst[0])
            self.symbols[lst[0]] = True
        else: 
            for symbol in lst:
                if symbol in self.symbols:
                    self.symbols.pop(symbol)
                self.symbols[symbol] = False
                

    def setValue(self, dict): 
        for k,v in dict.items(): 
            if k in self.symbols.keys(): 
                self.symbols[k] = v 

    def PLTrue(self,model): 
        for s in self.sentences: 
            s.setValue(model)
            if s.result() == False: 
                return False 
        return True 