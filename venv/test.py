from Sentence import Sentence

string = "a&b&c&d&(a&n=>m)=>e"
sentence = Sentence(string)
a = "a"
print(sentence.calculate_sentence(sentence.lst))