
import pandas as pd
import os
import os.path
import zipfile
import requests
import sqlite3

#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
class ndc_codes(object):


    def __init__(self, data_location_url=None, drugs_only=True, verbose=True, debug=False):
        # drugs_only =True gives a word list excluding non-drugs, i.e. Homeopathic stuff

        if data_location_url:
            self.data_location_url = data_location_url

        else:
            self.data_location_url='https://www.accessdata.fda.gov/cder/ndctext.zip'

        self.drugs_only = drugs_only
        self.verbose = verbose
        self.debug = debug
        self.data_path = '../../../data/'
        self.data_file_name = self.data_location_url.split('/')[-1]
        self.data_full_path = os.path.join(self.data_path, self.data_file_name)
        self.db_name = os.path.join(self.data_path, 'products.db')


#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
    def download_raw_file(self):

        # Stolen from https://stackoverflow.com/questions/17285464/whats-the-best-way-to-download-file-using-urllib3
        #  ?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

        if self.verbose:
            print('Fetching NDC Database from FDA Website.')

        r = requests.get(self.data_location_url, allow_redirects=True)
        open(self.data_full_path, 'wb').write(r.content)

#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
    def unzip_file(self):

        if self.verbose:
            print('Unzipping NDC Database archive.')

        myzip = zipfile.ZipFile(self.data_full_path, 'r')
        self.zipfile_namelist = myzip.namelist()
        if self.verbose:
            print('Archive contents:\r\t',self.zipfile_namelist)

        myzip.extractall(self.data_path)


#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
    def _to_data_frame(self):

        # 'ISO-8859-1' is encoding for German--many companies making drugs have
        # umlauts, etc in the names

        if 'product.txt' in os.listdir(self.data_path):
            if self.debug:
                print('Converting to data frame.')

            self.product_df = pd.read_table(os.path.join(self.data_path, 'product.txt'),  encoding='ISO-8859-1')

            return self.product_df

        else:
            print("product.txt doesn't appear to be in the archive :( ")

#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
    def _to_sqlite3(self):
        """Dump data to sqlite database. """
        if self.verbose:
            print('Dumping data to sqlite3 db.')

        self._to_data_frame()

        self.db_conn = sqlite3.connect(self.db_name)
        self.product_df.to_sql('product', self.db_conn, if_exists='replace', index=False)


#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
    def execute(self,query):
        self._to_sqlite3()

        try:
            with self.db_conn:
                cur = self.db_conn.cursor()
                cur.execute(query)
                results = cur.fetchall()

                if self.verbose:
                    print(results)
                return results

        except Exception as why:
            print("Exception: ",why)
            return False




#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
    def filter_data_frame(self):

        filtered_df = self.product_df['DRUG' in self.product_df['PRODUCTTYPENAME']]
        self.product_df = filtered_df


#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
    def manage_data(self, overwrite=True):
        """Get source file from FDA, unzip, etc, and dump to sqlite3 db."""
        if overwrite:
            if self.verbose:
                print("Fetching data from FDA website.")

            self.download_raw_file()
            self.unzip_file()

        self._to_sqlite3()

        self.get_drug_names()
        self.write_drug_list()



#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
    def get_drug_names(self):
        self._to_data_frame()

        #self.name_columns = ['PRODUCTTYPENAME', 'PROPRIETARYNAME', 'NONPROPRIETARYNAME', 'SUBSTANCENAME']
        self.name_columns = ['PROPRIETARYNAME', 'NONPROPRIETARYNAME', 'SUBSTANCENAME']
        self.all_names = []
        for column in self.name_columns:
            self.all_names += list(self.product_df[column])

        self.drugnames = []
        # Some entries have multiple entries, comma or semicolon delimited
        for entry in self.all_names:
            if type(entry) == type(""):
                entry = entry.replace(' - ', ';' ) # catch hyphens when they separate compounds
                entry = entry.replace(' / ', ';')  # catch slashes when they separate compounds
                entry = entry.replace(',', ';')
                entry = entry.replace(' and ', ';')
                entry_list = entry.split(';')   # some products list multiple ingredients--separate them.

                if self.debug:
                    if len(entry_list) > 1:
                        print(entry_list)

                for thisword in entry_list:
                    self.drugnames.append(thisword.strip().lower())


        # De-duplicate
        self.drugnames = [str(xx) for xx in set(self.drugnames)]
        self.drugnames.sort()


#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
    def write_drug_list(self, filename='drugnames.txt'):
        outfile = os.path.join(self.data_path, filename)
        with open(outfile,'w') as ff:
            for word in enumerate(self.drugnames):

                if type(word[1]) == type(""):
                    try:
                        if self.debug:
                            print('Word: ', word[0],'=', word[1])

                        ff.write(word[1].strip().replace(',','\n').replace(';','\n').lower().strip()+'\n')

                    except Exception as e:
                        if self.verbose:
                            print('\tProblem with word', word, '.  Skipping.')

                        if self.debug:
                            print('Exception: ', e)


#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#

if __name__=="__main__":
   main()


