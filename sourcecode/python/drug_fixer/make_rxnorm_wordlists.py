def make_rxnorm_wordlists():

    import pandas as pd
    import os
    import os.path


    dataloc = '../../../data/'
    filz = os.listdir(dataloc)
    normfilz = [xx for xx in filz if xx.startswith('RxNorm_full')]
    normfilz.sort()
    most_current = normfilz[-1]

    rxfile = os.path.join(dataloc,most_current,'rrf','RXNATOMARCHIVE.RRF')
    rxf = pd.read_table(rxfile, delimiter='|', header=-1,low_memory=False)

    drugnames = ' '.join(rxf[2])

    letters_only = "".join([ dd if dd.isalnum() else " " for dd in drugnames ])

    words = list(set([xx.lower() for xx in letters_only.split() if len(xx)>3 and xx.isalpha() ]))
    words.sort()
    phrases = list(set(rxf[2]))

    word_out_file = '../../../data/wordlists/rxnorm_words.txt'
    phrase_out_file = '../../../data/wordlists/rxnorm_phrases.txt'



    with open(word_out_file,'w') as wf:
        wf.write('\n'.join(words))

    with open(phrase_out_file,'w') as pf:
        pf.write('\n'.join(phrases))


if __name__ == "__main__":
    make_rxnorm_wordlists()
