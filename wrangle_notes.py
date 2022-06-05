import os

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from env import get_db_url

def get_big_zillow_data(query_db=False):
    '''Acquires the zillow data from the database or the .csv file if if is present

    Args:
        query_db = False (Bool) :  Forces a databse query and a resave of the data into a csv.
    Return:
        df (DataFrame) : a dataframe containing the data from the SQL database or the .csv file
    '''
    filename = 'big_zillow.csv'
    if os.path.isfile(filename) and not query_db:
        print('Returning saved csv file.')
        return pd.read_csv(filename).drop(columns = ['Unnamed: 0'])
    else:
        print('Querying database ... ')
        query = '''
        SELECT properties_2017.*, propertylandusedesc FROM properties_2017 JOIN propertylandusetype USING (propertylandusetypeid) WHERE propertylandusedesc = 'Single Family Residential';
        '''
        df = pd.read_sql(query, get_db_url('zillow'))
        print('Got data from the SQL database')
        df.to_csv(filename)
        print('Saved dataframe as a .csv!')
        return df

df = get_big_zillow_data(query_db=True)
df