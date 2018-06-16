
from docopt import docopt
from ndc_codes import ndc_codes

#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#

def main():

    usg="""

        Usage:
            drugfix [-u, -v, -d] fetch_wordlist
            drugfix [-c, -v, -d] <word> ...

        Options:
            -c, --candidates                    Return all candidates for a word's correct spelling
            -v, --verbose                       Blather more than normal
            -u, --fetch_url [default: None]     Give a url from which to grab the FDA data
            -d, --debug                         Give extra debugging info
    """


    argsdict = docopt(usg)

    if argsdict['--debug']:
        print('\nInput Arguments:\n',argsdict, '\n\n')

    vb = argsdict['--verbose']
    url = None
    if argsdict['--fetch_url'] is not 'None':
        url = argsdict['--fetch_url']

    if argsdict['fetch_wordlist']:
        if vb:
            print('Fetching the wordlist.')

        nc = ndc_codes(data_location_url=url, verbose=vb, debug=argsdict['--debug'])
        nc.go_fish()
        return

    if len(argsdict['<word>']) >= 1:

        nsc = norvig_spell_correct()

        if argsdict['--candidates']:
            return [nsc.candidates(word) for word in argsdict['<word>']]
        else:
            return [nsc.correction(word) for word in argsdict['<word>']]


#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#

if __name__=="__main__":
   main()


