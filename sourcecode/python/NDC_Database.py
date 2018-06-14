
import re
import pandas as pd
import os
import os.path
import zipfile
import requests


class ndc_codes(object):



    def __init__(self, data_location_url=None, verbose=True):

        
        if data_location_url:
            self.data_location_url = data_location_url

        else:
            self.data_location_url='https://www.accessdata.fda.gov/cder/ndctext.zip'

        self.verbose = verbose
        self.data_path = '../../data/'
        self.data_file_name = self.data_location_url.split('/')[-1]
        self.data_full_path = os.path.join(self.data_path, self.data_file_name)


    def download_raw_file(self):

        # Stolen from https://stackoverflow.com/questions/17285464/whats-the-best-way-to-download-file-using-urllib3
        #  ?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

        

        if self.verbose:
            print('Fetching NDC Database from FDA Website.')

        r = requests.get(self.data_location_url, allow_redirects=True)
        open(self.data_full_path, 'wb').write(r.content) 
               
    def unzip_file(self):

        if self.verbose:
            print('Unzipping NDC Database archive.')

        myzip = zipfile.ZipFile(self.data_full_path, 'r')
        self.zipfile_namelist = myzip.namelist()
        if self.verbose:
            print('Archive contents:\r\t',self.zipfile_namelist)

        myzip.extractall(self.data_path)


    def to_data_frame(self):

        if 'product.txt' in os.listdir(self.data_path):
            if self.verbose:
                print('Converting to data frame.')

            self.product_df = pd.read_table(os.path.join(self.data_path, 'product.txt'),  encoding='ISO-8859-1')

            return self.product_df

        else:
            print("product.txt doesn't appear to be in the archive :( ")


    def load_data(self):

        if 'product.txt' in os.listdir(self.data_path):
            if self.verbose:
                print('Loading NDC Database.')
            self.to_data_frame()

        else:
            if self.verbose:
                print("product.txt not found--fetching data from FDA website.")

            self.download_raw_file()
            self.unzip_file()
            self.to_data_frame()

    def get_drug_names(self):
        self.load_data()
        self.name_columns = ['PRODUCTTYPENAME', 'PROPRIETARYNAME', 'NONPROPRIETARYNAME', 'SUBSTANCENAME']
        self.all_names = []
        for column in self.name_columns:
            self.all_names += list(self.product_df[column])
       
        self.drugnames = list(set(self.all_names))
        # self.drugnames.sort()

 
    def write_drug_list(self, filename='drugnames.txt'):
        outfile = os.path.join(self.data_path, filename)        
        with open(outfile,'w') as ff:
            for word in drugnames:
                ff.write(word.replace(';',' ')+' ')


class norvig_spell_correct(object):
    """Adapted from Peter Norvig's blog entry:  https://norvig.com/spell-correct.html"""
    
    def __init__(self, wordlist='drugnames.txt'):
        from collections import Counter
        self.data_path = '../data'
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



