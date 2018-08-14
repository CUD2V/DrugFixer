def make_loinc_wordlists():

    import pandas as pd
    import os
    import os.path

    dataloc = '../../../data/Loinc/'
    filz = os.listdir(dataloc)

    lf = pd.read_csv(os.path.join(dataloc,'Loinc.csv'), low_memory=False)

    cmpts = ' '.join(lf.COMPONENT)
    #cmpts = cmpts.replace()

    letters_only = "".join([ c if c.isalnum() else " " for c in cmpts ])

    words = list(set([xx.lower() for xx in letters_only.split() if len(xx)>3 and xx.isalpha() ]))
    words.sort()
    phrases = list(set(lf.COMPONENT))

    word_out_file = '../../../data/wordlists/loinc_words.txt'
    phrase_out_file = '../../../data/wordlists/loinc_phrases.txt'



    with open(word_out_file,'w') as wf:
        wf.write('\n'.join(words))

    with open(phrase_out_file,'w') as pf:
        pf.write('\n'.join(phrases))


if __name__ == "__main__":
    make_loinc_wordlists()

