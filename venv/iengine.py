from KnowledgeBase import *
from algorithms.FC import *
from algorithms.BC import *
from algorithms.TT import *
from algorithms.WSAT import WSAT

import sys
from FileReader import FileReader
from KnowledgeBase import KnowledgeBase

# from Sentence import Sentence
# from TruthTable import TruthTable
# from HornForm import HornForm
# from ForwardChaining import ForwardChaining
# from BackwardChaining import BackwardChaining

if __name__ == "__main__":
    if len(sys.argv) != 6 and len(sys.argv) != 3:
        print("Enter command in following format: python iengine.py <filename> <method> (<mt> <mf> <p>)")
        print("Methods: TT, FC, BC, WSAT")
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
    if len(sys.argv) == 6:
        mt = int(sys.argv[3])
        mf = int(sys.argv[4])
        p = float(sys.argv[5])
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
    elif method == 'WSAT':
        kb = KnowledgeBase(tell)
        wsat = WSAT()
        wsat.infer(kb, ask)
        print(wsat.getOutput())
    else:
        print("Unknown method entered.")