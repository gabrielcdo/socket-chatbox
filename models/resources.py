from symspell.symspell import load_symspell


class Resources():
    def __init__(self):
        self.unigram_dict = '/home/gabriel/Documents/Letrus/agluti/redacoesC1/corrected_dict.txt'
        self.bigram_dict = '/home/gabriel/Documents/Letrus/agluti/redacoesC1/corrected_bigram_dict.txt'
        self.spell_model = load_symspell(self.unigram_dict,self.bigram_dict)
