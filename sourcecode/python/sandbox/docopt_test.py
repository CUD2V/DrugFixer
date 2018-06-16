


from docopt import docopt

#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#

def main():

    usg="""
       
        Usage:
            drugfix [-u, -v] fetch_wordlist
            drugfix [-c, -v] <word> ...

        Options:
            -c, --candidates   Return all candidates for a word's correct spelling
            -v, --verbose      Blather more than normal
            -u, --fetch_url    Give a url from which to grab the FDA data
    """

    argsdict = docopt(usg)
    print('\n\n',argsdict, '\n\n')    
    if argsdict['fetch_wordlist']:
        print('Go fetch the wordlist')
        return

    if len(argsdict['<word>']) >=1 :
        if argsdict['--candidates']:
            print('Activated candidates switch')
        if argsdict['--verbose']:
            print('Activated verbose switch')

        for thisword in argsdict['<word>']:
            print('Processing ', thisword)
        return
    

#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#

if __name__=="__main__":
   main() 

