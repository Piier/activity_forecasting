import csv
import pandas as pd
import numpy as np

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.preprocessing import MinMaxScaler

def chi_squared(X, y, num_feats):
    X_norm = MinMaxScaler().fit_transform(X)
    chi_selector = SelectKBest(chi2, k=num_feats)
    chi_selector.fit(X_norm, y)
    chi_support = chi_selector.get_support()
    chi_feature = X.loc[:,chi_support].columns.tolist()
    return chi_feature


case=['HH101','HH102','HH103','HH104','HH105','HH106','HH108','HH109','HH110','HH111','HH112','HH113','HH114','HH116','HH117','HH118','HH119','HH120','HH122','HH123','HH124','HH125','HH126','HH127','HH128','HH129','HH130']

for casa in case:
    df = pd.read_csv('./feature_vector'+casa+'.csv') 
    
    num_feature = len(df.columns)-1
    if num_feature>500:
        num_feature=500
    
    numcols = list(df.columns)

    df = df[numcols]
    traindf = df[numcols]
    features = traindf.columns

    traindf = traindf.dropna()
    traindf = pd.DataFrame(traindf,columns=features)
    y = traindf['TO PREDICT']
    X = traindf.copy()

    del X['TO PREDICT']


    cor_feature = chi_squared(X, y, num_feature)
    print(casa,str(len(cor_feature)))
    #print(casa,cor_feature)

    df1 = X[cor_feature]#+traindf['TO PREDICT']
    df1['TO PREDICT'] = traindf['TO PREDICT']
    df1.to_csv(r'./selected'+casa+'.csv', index = False)
