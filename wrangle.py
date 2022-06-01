import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer

from env import get_db_url

def get_zillow_data(query_db=False):
    '''Acquires the zillow data from the database or the .csv file if if is present

    Args:
        query_db = False (Bool) :  Forces a databse query and a resave of the data into a csv.
    '''
    filename = 'zillow.csv'
    if os.path.isfile(filename) and not query_db:
        print('Returning saved csv file.')
        return pd.read_csv(filename)
    else:
        print('Querying database ... ')
        query = '''SELECT parcelid, bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, yearbuilt, fips, taxvaluedollarcnt, taxamount, propertylandusetypeid, propertylandusedesc 
        FROM properties_2017
		JOIN propertylandusetype USING (propertylandusetypeid)
        WHERE propertylandusedesc = 'Single Family Residential';
        '''
        df = pd.read_sql(query, get_db_url('zillow'))
        print('Got data from the SQL database')
        df.to_csv(filename)
        print('Saved dataframe as a .csv!')
        return df

def prepare_zillow_data(df):
    '''Prepares the zillow data by dropping nulls and all rows with bedroomcnt > 0, bathroomcnt > 0
    and calculatedfinishedsquarefeet > 14'''
    #drop the nulls
    df = df.dropna()
    #apply the boolean conditions
    df = df[(df.bedroomcnt > 0) & (df.bathroomcnt > 0) & (df.calculatedfinishedsquarefeet > 149)]
    return df

def wrangle_zillow_data():
    '''gets and prepares the zillow data from the SQL db or the .csv files'''
    df = get_zillow_data()
    df = prepare_zillow_data(df)
    return df
