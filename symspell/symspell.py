import symspellpy
from symspellpy import SymSpell

def load_symspell(unigram_dict: str, bigram_dict: str) -> symspellpy.symspellpy.SymSpell:
    sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
    sym_spell.load_dictionary(unigram_dict, term_index=0, count_index=1)
    sym_spell.load_bigram_dictionary(bigram_dict, term_index=0, count_index=2)
    return sym_spell


def spell_correct(msg: str, sym_spell: symspellpy.symspellpy.SymSpell) -> str:
    input_term = (
        msg.lower()
    )
    suggestions = sym_spell.lookup_compound(
        input_term, max_edit_distance=2, transfer_casing=True,
    )
    return suggestions[0]
