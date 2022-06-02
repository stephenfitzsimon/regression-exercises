import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, QuantileTransformer


from env import get_db_url

RAND_SEED = 4321

def get_zillow_data(query_db=False):
    '''Acquires the zillow data from the database or the .csv file if if is present

    Args:
        query_db = False (Bool) :  Forces a databse query and a resave of the data into a csv.
    Return:
        df (DataFrame) : a dataframe containing the data from the SQL database or the .csv file
    '''
    filename = 'zillow.csv'
    if os.path.isfile(filename) and not query_db:
        print('Returning saved csv file.')
        return pd.read_csv(filename).drop(columns = ['Unnamed: 0'])
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
    and calculatedfinishedsquarefeet > 14
    
    Args:
        df (DataFrame) : dataframe to prepare
    Return:
        df (DataFrame) : prepared dataframe
    '''
    #drop the nulls
    df = df.dropna()
    #apply the boolean conditions
    #exclude very small houses
    ddf = df[(df.bedroomcnt > 0) & (df.bathroomcnt > 0) & (df.calculatedfinishedsquarefeet > 149)]
    #exclude very large houses
    df = df[(df.bedroomcnt < 7) & (df.bathroomcnt < 7)]
    #exclude very expensive houses
    df = df[df.taxvaluedollarcnt <= 2000000]
    return df

def wrangle_zillow_data():
    '''gets and prepares the zillow data from the SQL db or the .csv files'''
    df = get_zillow_data()
    df = prepare_zillow_data(df)
    return df

def split_zillow_data(df):
    '''splits the zillow dataframe into train, test and validate subsets
    
    Args:
        df (DataFrame) : dataframe to split
    Return:
        train, test, validate (DataFrame) :  dataframes split from the original dataframe
    '''
    train, test = train_test_split(df, train_size = 0.8, random_state=RAND_SEED)
    train, validate = train_test_split(train, train_size = 0.7, random_state=RAND_SEED)
    return train, test, validate

def zillow_scale(df,
                columns = ['calculatedfinishedsquarefeet', 'taxvaluedollarcnt', 'taxamount'],
                scaler_in=RobustScaler(),
                return_scalers=False):
    '''
    Returns a dataframe of the scaled columns
    
    Args:
        df (DataFrame) : The dataframe with the columns to scale
        columns (list) : The columns to scale, 
            default = ['calculatedfinishedsquarefeet', 'taxvaluedollarcnt', 'taxamount']
        scaler_in (sklearn.preprocessing) : scaler to use, default = RobustScaler()
        return_scalers (bool) : boolean to return a dictionary of the scalers used for 
            the columns, default = False
    Returns:
        df_scaled (DataFrame) : A dataframe containing the scaled columns
        scalers (dictionary) : a dictionary containing 'column' for the column name, 
            and 'scaler' for the scaler object used on that column
    '''
    #variables to hold the returns
    scalers = []
    df_scaled = df[columns]
    for column in columns:
        #determine the scaler
        scaler = scaler_in
        #fit the scaler
        scaler.fit(df[[column]])
        #transform the data
        scaled_col = scaler.transform(df[[column]])
        #store the column name and scaler
        scaler = {
            'column':column,
            'scaler':scaler
        }
        scalers.append(scaler)
        #store the transformed data
        df_scaled[f"{column}_scaled"] = scaled_col
    #determine the correct varibales to return
    if return_scalers:
        return df_scaled.drop(columns = columns), scalers
    else:
        return df_scaled.drop(columns = columns)