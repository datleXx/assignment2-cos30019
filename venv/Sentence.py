import re 
from Parser import Parser
from PropositionalSymbol import PropositionalSymbol

class Sentence: 
    def __init__(self, string): 
        self.parser = Parser()
        self.lst, self.symbols = self.parse_sentence(string)
        self.count = self.setCount(self.lst.copy())


    
    def hasSymbol(self, symbol): ## check if the sentence has a symbol
        s = PropositionalSymbol(symbol)
        for x in self.symbols: 
            if x == s: 
                return True
        return False
    
    def getPropSymbol(self, symbol): 
        s = PropositionalSymbol(symbol)
        for x in self.symbols: 
            if x == s: 
                return x
        return None 
    
    def setValue(self,model): 
        pass 

    def result(self): 
        return self.calculate_sentence(self.lst)

    def setValue(self,model): 
        for k,v in model.items(): 
            temp = self.getPropSymbol(k)
            if temp: 
                temp.setValue(v)
        
    def setCount(self, lst): #count for horn clause the number of symbols before the imply operator
        count = 0
        if not lst: 
            return 0
        else:
            if len(lst) < 3: 
                if len(lst) == 1: 
                    return 1
                return 0 
            else: 
            
                for symbol in range(len(lst)-2):
                    if re.search("[a-zA-Z0-9]+", lst[symbol]) != None:
                        count += 1
        
        return count
            
            
    
    def getCount(self): 
        return self.count
            
    
    def parse_sentence(self, string): 
        lst = re.findall(
            "[a-zA-Z0-9]+|[&]|[~]|[|]+|\w*(?<!<)=>|<=>|[(]|[)]", 
            string) 
        symbols_lst = []
        #separate the sentence into a list of symbols and operator
        formatted_lst = self.parser.postfix_parser(lst=lst) #transform sentence into a postfix form
        symbols = re.findall("[a-zA-Z0-9]+", string)
        set_symbols = set(symbols)
        for x in set_symbols: #create a set of symbols for the sentence
            temp = PropositionalSymbol(x)
            symbols_lst.append(temp)
        
        return formatted_lst, symbols_lst 
    
    def isHornForm(self): 
        lst = self.lst.copy()
        if not lst: 
            return False
        
        if len(lst) == 1: 
            if lst[0].isalpha(): 
                return True
            return False
        else: 
            if "=>" not in lst: 
            ## if len > 1 but not including implication symbol --> False
                return False 
            if lst[-1] != "=>": 
                return False
            if ("||" in lst or 
                "<=>" in lst): 
            ## Sentence contains || or <=> --> False
                return False
            if ("&" not in lst): 
                count_implication = lst.count("=>")
                if count_implication > 1: 
                ## Not containing &,||,<=> but has many => ---> False 
                    return False
                left = lst[:-1]
                if len(left > 2): 
                    return False
                return True
            else: 
                joined_lst = "".join(lst.copy())
                split_lst = joined_lst.split("&")
                for symbol in split_lst: 
                    if symbol == "": 
                        return False
                    if symbol == "=>" or symbol[0] == "=>": 
                        return False
                return True

                
    def getSymbolValue(self, symbol): # get the value of the symbol: T/F
        result = self.getPropSymbol(symbol)
        if result: 
            return result.getValue()
        return None
    
    def calculate_sentence(self, lst): 
        output_queue = [] 
        for token in lst:
            if token not in ["~", "&", "||", "=>", "<=>"]: #if token is a symbol then get its value
                output_queue.append(self.getSymbolValue(token))
            else:
                output_queue.append(token)
        return self.calculate(output_queue)
    
    def calculate(self,expression): #evaluate the sentence based on already processed expression
        stack = []
        for token in expression:
            if token in ["~", "&", "||", "=>", "<=>"]:
                right_operand = stack.pop()
                if token != "~":
                    left_operand = stack.pop()
                if token == "~":
                    result = not right_operand
                elif token == "&":
                    result = left_operand and right_operand
                elif token == "||":
                    result = left_operand or right_operand
                elif token == "=>":
                    result = (not left_operand) or right_operand
                elif token == "<=>":
                    result = left_operand == right_operand

                stack.append(result)
            else:
                stack.append(token)

        return stack[0]
            
       
        
