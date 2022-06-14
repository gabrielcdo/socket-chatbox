from symspell.symspell import load_symspell


class Resources():
    def __inittxt__(self):
        self.unigram_dict = 'unigram_path'
        self.bigram_dict = 'bigram_path'
        self.spell_model = load_symspell(self.unigram_dict,self.bigram_dict)
