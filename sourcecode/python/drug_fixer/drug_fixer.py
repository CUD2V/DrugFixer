
from ndc_codes import ndc_codes
from norvig_spell_correct import norvig_spell_correct
from category_finder import category_finder
import os
import os.path
import sys
from docopt import docopt

#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#

def main():

    usg="""

        Usage:
            drugfix [-u, -vd] fetch_wordlist
            drugfix [-v, -d, -s] cat <word> ...
            drugfix [-c, -vd] fix <word> ...

        Options:
            -c, --candidates   Return all candidates for a word's correct spelling
            -v, --verbose      Blather more than normal
            -u, --fetch_url    Give a url from which to grab the FDA data
            -d, --debug        Even more gratuitous blathering
            -s, --sep_match    For category serches, separate results by drugname
    """


    clargs = docopt(usg)

    #  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
    if clargs['--debug']:
        print('\nInput Arguments:\n',clargs, '\n\n')

    vb = clargs['--verbose']

    #  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
    if clargs['--fetch_url'] is not 'None':
        url = clargs['--fetch_url']

    #  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
    if clargs['fetch_wordlist']:
        if vb:
            print('Fetching the wordlist.')

        nc = ndc_codes(data_location_url=url, verbose=vb, debug=clargs['--debug'])

        nc.go_fish()

        return

    #  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
    if clargs['fix'] and len(clargs['<word>']) >= 1:

        nsc = norvig_spell_correct()

        if clargs['--candidates']:
            [sys.stdout.write(str(nsc.candidates(word))+' ') for word in clargs['<word>']]
        else:
            [sys.stdout.write(nsc.correction(word)+' ') for word in clargs['<word>']]
        sys.stdout.write('\n')

    #  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
    if clargs['cat'] and len(clargs['<word>']) >= 1:

        cf = category_finder()
        for thisword in clargs['<word>']:
            thiscat = cf.get_category(thisword)
            if clargs['--sep_match']:
                print(cf.pharmaclasses)
            else:
                print(cf.pharmaclasses['ALL'])

#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
if __name__=="__main__":
    main()
