import pprint
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
            drug_fixer.py [-duv]   fetch
            drug_fixer.py [-dpsvw] cat <word> ...
            drug_fixer.py [-cdv]   fix <word> ...

        Options:
            -p, --pretty       Print results beautifilly
            -c, --candidates   Return all candidates for a word's correct spelling
            -v, --verbose      Blather more than normal
            -d, --debug        Even more gratuitous blathering

            -u, --fetch_url    For fetches, Give a url from which to grab the FDA data
            -s, --sep_match    For category serches, separate results by drugname
            -w, --wikipedia    For category searches, include Wikipedia URL in results
    """


    clargs = docopt(usg)

    if clargs['--debug']:
        print('\nInput Arguments:\n',clargs, '\n\n')


    if clargs['--fetch_url'] is not 'None':
        url = clargs['--fetch_url']


    if clargs['fetch']:
        if clargs['--verbose']:
            print('Fetching FDA drug data.')
        nc = ndc_codes(data_location_url=url,
                        verbose=clargs['--verbose'],
                        debug=clargs['--debug'])

        nc.manage_data()
        return


    if clargs['fix'] and len(clargs['<word>']) >= 1:

        nsc = norvig_spell_correct()

        if clargs['--candidates']:
            [sys.stdout.write(str(nsc.candidates(word))+' ') for word in clargs['<word>']]
        else:
            [sys.stdout.write(nsc.correction(word)+' ') for word in clargs['<word>']]
        sys.stdout.write('\n')
        return


    if clargs['cat'] and len(clargs['<word>']) >= 1:
        cf = category_finder()

        for thisword in clargs['<word>']:
            if clargs['--wikipedia']:
                thiscat = cf.get_category_wikilinks(thisword)
                if clargs['--sep_match']:
                    pprint.pprint(cf.wikilinks)
                else:
                    pprint.pprint(cf.wikilinks['ALL'])


            else:
                thiscat = cf.get_category(thisword)
                if clargs['--sep_match']:
                    pprint.pprint(cf.pharmaclasses)
                else:
                    pprint.pprint(cf.pharmaclasses['ALL'])

        cf.db_conn.close()

        return


#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
if __name__=="__main__":
    main()
