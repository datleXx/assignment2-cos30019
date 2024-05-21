from KnowledgeBase import *
from algorithms.FC import *
from algorithms.BC import *
from algorithms.TT import *

import sys
from FileReader import FileReader
from KnowledgeBase import KnowledgeBase
# from Sentence import Sentence
# from TruthTable import TruthTable
# from HornForm import HornForm
# from ForwardChaining import ForwardChaining
# from BackwardChaining import BackwardChaining

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Enter command in following format: python iengine.py <filename> <method>")
        print("Methods: TT, FC and BC")
        exit(0)

    # get tell and ask from file of given name
    try:
        tell, ask = FileReader.read(sys.argv[1])
    except:
        print("File not found.")
        sys.exit(0)

    if len(tell) == 0:
        print("No tell found.")
        sys.exit(0)
    if not ask:
        print("No ask found.")
        sys.exit(0)
    ask = Sentence(ask)
    method = sys.argv[2]
    # set up knowledge base and method based on chosen method
    # print solution using method and query (ask)
    if method == 'TT':
        kb = KnowledgeBase(tell) # setup knowledge base with general sentences
        tt = TT()
        tt.infer(kb, ask)
        print(tt.getOutput())
    elif method == 'FC':
        kb = KnowledgeBase(tell) # setup knowledge base with horn form
        fc = FC()
        fc.infer(kb,ask)
        print(fc.getOutput())
        # print(fc.solve(ask))
    elif method == 'BC':
        kb = KnowledgeBase(tell)
        bc = BC()
        bc.infer(kb,ask)
        print(bc.getOutput())
    else:
        print("Unknown method entered.")