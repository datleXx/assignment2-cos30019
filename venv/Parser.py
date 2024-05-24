import sympy
from sympy import symbols
from sympy.logic.boolalg import to_cnf

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
    
    def postfix_to_infix(self, postfix_expr):
        stack = []

        for symbol in postfix_expr:
            # If the symbol is a propositional variable, push it to the stack
            if symbol.isalpha():
                stack.append(symbol)
            # If the symbol is a unary operator (~), pop the last element from the stack, combine it with the operator
            # and push the result back to the stack
            elif symbol == "~":
                operand = stack.pop()
                new_expr = f"{symbol}({operand})"
                stack.append(new_expr)
            # If the symbol is a binary operator (&, |, =>), pop the last two elements from the stack,
            # combine them with the operator and push the result back to the stack
            elif symbol in ["&", "||", "=>"]:
                operand2 = stack.pop()
                operand1 = stack.pop()
                new_expr = f"({operand1} {symbol} {operand2})"
                stack.append(new_expr)
            # If the symbol is a biconditional operator (<=>), replace it with a combination of & and | operators
            elif symbol == "<=>":
                operand2 = stack.pop()
                operand1 = stack.pop()
                new_expr = f"(({operand1} & {operand2}) || (~{operand1} & ~{operand2}))"
                stack.append(new_expr)

        # The last element in the stack is the infix expression
        return stack[-1]
    
    def cnf_parser(self, postfix_expr): 
        string = self.postfix_to_infix(postfix_expr)
        string = string.replace("=>", ">>")
        string = string.replace("||", "|")
        cnf_expr = str(to_cnf(string))
        cnf_expr = cnf_expr.replace("|", "||")
        cnf_expr = cnf_expr.replace(">>", "=>")
        return cnf_expr
    

