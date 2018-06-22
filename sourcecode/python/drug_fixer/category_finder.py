import os
import os.path
import re
import pandas as pd
import sqlite3
import ndc_codes as nc

class category_finder(object):

    def __init__(self, data_file='products.txt', verbose=True):

        self.data_path = '../../../data'
        self.data_file = os.path.join(self.data_path, data_file)
        self.verbose = verbose
        self.db_name = os.path.join(self.data_path, 'products.db')
        self.category_subtypes = ['','MoA', 'EPC', 'PE', 'CI']

    #--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
    def _get_db_conn(self):
        """Dump data to sqlite database. """

        if 'db_conn' not in self.__dict__.keys():

            try:
                self.db_conn = sqlite3.connect(self.db_name)

            except Exception as why:
                print(why, '\nError loading db. Ensure database is in \n {}'.format(self.db_name))


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

        if typename in self.category_subtypes:
            self.get_category(drugname)

            for thisdrug in self.pharmaclasses.keys():
                self.pharmaclasses[thisdrug] = [xx for xx in self.pharmaclasses[thisdrug] if xx.endswith(typename+']')]
        else:
            raise ValueError('Invalid subtype. Must be in list: '+self.category_subtypes)


    #--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
    def get_MoA(self, drugname):
        """Return only Method of Action (MoA) classes associated with drugname"""
        self._get_filtered_categories(drugname, typename='MoA')


    #--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
    def get_EPC(self, drugname):
        """Return only Established Pharmalogic Class (EPC) classes associated with drugname."""

        self._get_filtered_categories(drugname, typename='EPC')


    #--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
    def get_PE(self, drugname):
        """Return only Physiologic Effect (PE) classes associated with drugname"""

        self._get_filtered_categories(drugname, typename='PE')


    #--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
    def get_CI(self, drugname):
        """Return only Chemical/Ingredient (CI) classes associated with drugname."""

        self._get_filtered_categories(drugname,typename='CI')


    #--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
    def get_category(self, drugname):

        # This is a bit faster than get_category_pandasql.
        # The db uses the table name "product"

        self.cat_query = '''
                SELECT *
                FROM product
                WHERE (LOWER(PROPRIETARYNAME) LIKE '%{}%'
                    OR LOWER(NONPROPRIETARYNAME) LIKE '%{}%'
                    OR LOWER(SUBSTANCENAME) LIKE '%{}%'
                       )
                    AND PHARM_CLASSES != 'None'

                '''.format(drugname.lower(), drugname.lower(),drugname.lower())

        pharmaclasses = {}
        self._get_db_conn()

        try:
            with self.db_conn:
                query_results = pd.read_sql_query(self.cat_query, self.db_conn)

        except Exception as why:
            print("Exception: ",why)
            return False


        # Store all classes with a matching name
        pharmaclasses['ALL'] = list(set(','.join(list(query_results.PHARM_CLASSES)).split(',')))

        # Break out different products' classes
        for thisdrug in query_results.iterrows():
            pharmaclasses[thisdrug[1].PROPRIETARYNAME] = list(set(thisdrug[1].PHARM_CLASSES.split(',')))

        self.pharmaclasses = pharmaclasses

        return self.pharmaclasses


    #--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#
    def get_category_pandasql(self, drugname):

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
    def get_category_wikilinks(self, drugname):

        self.get_EPC(drugname)
        self.wikilinks = {}
        for thisdrugkey in self.pharmaclasses.keys():
            thislist = []
            for thiscat in self.pharmaclasses[thisdrugkey]:
                thiswikilink = 'http://www.wikipedia.com/wiki/index.php?search='
                thiswikilink += thiscat.split('[')[0].strip()
                thislist.append(thiswikilink.replace(' ','_').lower())
            self.wikilinks[thisdrugkey] = thislist



#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#

