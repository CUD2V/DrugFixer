
import os
import os.path
import re


class norvig_spell_correct(object):
    """Adapted from Peter Norvig's blog entry:  https://norvig.com/spell-correct.html"""

    def __init__(self, wordlist='rxnorm_words.txt'):
        from collections import Counter
        self.data_path = '../../../data/wordlists/'
        self.wordlist= os.path.join(self.data_path, wordlist)
        self.WORDS = Counter(self.words(open(self.wordlist).read()))


    def words(self, text):
        return re.findall(r'\w+', text.lower())


    def P(self, word):
        "Probability of `word`."
        word = word.lower()
        N = sum(self.WORDS.values())
        return self.WORDS[word] / N


    def correction(self, word):
        "Most probable spelling correction for word."
        word = word.lower()
        return max(self.candidates(word), key=self.P)


    def candidates(self, word):
        "Generate possible spelling corrections for word."
        word = word.lower()
        return (self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word])


    def known(self, words):
        "The subset of `words` that appear in the dictionary of self.WORDS."
        return set(w for w in words if w in self.WORDS)


    def edits1(self, word):
        "All edits that are one edit away from `word`."
        word = word.lower()
        letters    = 'abcdefghijklmnopqrstuvwxyz'
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
        inserts    = [L + c + R               for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)


    def edits2(self, word):
        "All edits that are two edits away from `word`."
        word = word.lower()
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))





