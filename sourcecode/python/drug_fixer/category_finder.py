import os
import os.path
import re
import pandas as pd

class category_finder(object):

    def __init__(self, data_file='products.txt', verbose=True):

        self.data_path = '../../../data'
        self.data_file = os.path.join(self.data_path, data_file)
        self.verbose = verbose

    #--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
    def to_data_frame(self):

        # 'ISO-8859-1' is encoding for German--many companies making drugs have
        # umlauts, etc in the names

        if 'product.txt' in os.listdir(self.data_path):
            if self.verbose:
                print('Converting to data frame.')

            self.product_df = pd.read_table(os.path.join(self.data_path, 'product.txt'),  encoding='ISO-8859-1')

            return self.product_df

        else:
            print("product.txt doesn't appear to be in the archive.  Run >> python drug_fixer.py fetch_wordlist ")


    #--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
    def _get_filtered_categories(self, drugname, typename=''):
        """Return only given types of classes associated with drugname

            Use convenience methods:  self.get_EPC, ...

            types:
                ''    -->  all types
                'MoA' --> Method of Action
                'EPC' --> Established Pharmalogic Class
                'PE'  --> Physiologic Effect
                'CI'  --> Chemical/Ingredient

        """

        self.get_category(drugname)

        for thisdrug in self.pharmaclasses.keys():
            self.pharmaclasses[thisdrug] = [xx for xx in self.pharmaclasses[thisdrug] if xx.endswith(typename+']')]

    #--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
    def get_MoA(self, drugname):
        """Return only Method of Action (MoA) classes associated with drugname"""

        return self._get_filtered_categories(self, drugname, typename='MoA')

    #--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
    def get_EPC(self, drugname):
        """Return only Established Pharmalogic Class (EPC) classes associated with drugname."""

        return self._get_filtered_categories(self, drugname, typename='EPC')

    #--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
    def get_PE(self, drugname):
        """Return only Physiologic Effect (PE) classes associated with drugname"""

        return _get_filtered_categories(self, drugname, typename='PE')

    #--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
    def get_CI(self, drugname):
        """Return only Chemical/Ingredient (CI) classes associated with drugname."""

        return self._get_filtered_categories(self, drugname, typename='Chemical/Ingredient')

    #--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
    def get_category(self, drugname):

        from pandasql import sqldf as q

        if 'product_df' not in self.__dict__.keys():
            self.to_data_frame()

        df = self.product_df # pandasql doesn't like "self."

        self.cat_query = '''
                SELECT *
                FROM df
                WHERE (LOWER(PROPRIETARYNAME) LIKE '%{}%'
                    OR LOWER(NONPROPRIETARYNAME) LIKE '%{}%'
                    OR LOWER(SUBSTANCENAME) LIKE '%{}%'
                       )
                    AND PHARM_CLASSES != 'None'

                '''.format(drugname.lower(), drugname.lower(),drugname.lower())

        pharmaclasses = {}
        query_results = q(self.cat_query)

        # Store all classes with a matching name
        pharmaclasses['ALL'] = list(set(','.join(list(query_results.PHARM_CLASSES)).split(',')))
        # Break out different products' classes
        for thisdrug in query_results.iterrows():
            pharmaclasses[thisdrug[1].PROPRIETARYNAME] = list(set(thisdrug[1].PHARM_CLASSES.split(',')))

        self.pharmaclasses = pharmaclasses
        return pharmaclasses

#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#

