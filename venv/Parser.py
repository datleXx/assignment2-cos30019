class Parser: 
    def __init__(self):
        pass 

    def postfix_parser(self, lst): 
        operator_stack = [] # Store operator
        sentence_stack = [] # Store sentence
        precedence = {"~": 3, 
                      "&": 2, 
                      "||": 1,  # Logic OP priority set # 
                      "=>": 0, 
                      "<=>": 0}
        for token in lst: 
            if token in ["~", "&", "||", "=>", "<=>"]:
                while (operator_stack and 
                operator_stack[-1] != "("  # if operator = (, then continue adding operator to the list
                and precedence[token] <= precedence[operator_stack[-1]]):
                    temp = operator_stack.pop()
                    sentence_stack.append(temp)
                operator_stack.append(token)
            elif token == "(":
                operator_stack.append(token)
            elif token == ")":
                while operator_stack and operator_stack[-1] != "(":
                    temp = operator_stack.pop()
                    sentence_stack.append(temp)
                operator_stack.pop()  # Remove "(" from stack
            else:
                sentence_stack.append(token)

        while operator_stack:
            temp = operator_stack.pop()
            sentence_stack.append(temp)
        
        return sentence_stack