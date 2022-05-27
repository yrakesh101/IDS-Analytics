import os
import pandas as pd
import numpy as np
from sklearn import preprocessing
from scipy import stats
from datetime import date
import random
from datetime import datetime,timedelta
from matplotlib import pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from pandas.tseries.offsets import DateOffset
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from pmdarima import auto_arima
import warnings

warnings.filterwarnings("ignore")  
cwd = os.getcwd()
parent = os.path.dirname(cwd)

def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)# create a list of file and sub directories 
    allFiles = list()# names in the given directory 
    for entry in listOfFile:# Iterate over all the entries
        fullPath = os.path.join(dirName, entry)# Create full path
        if os.path.isdir(fullPath):# If entry is a directory then get the list of files in this directory
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)      
    return allFiles
agg=getListOfFiles(parent+"\web\\data\\aggregated")
masterdata=[]
for file in agg:
    masterdata.append(pd.read_csv(file))
masterdata=pd.concat(masterdata)


def predict_package():
    df=masterdata.copy()
    df["hour"] = df["hour"].astype(str)
    df["DateTime"]=df["DATE"]+" "+df["hour"]+":"+"00"
    df.drop(["DATE",'hour'],inplace=True,axis=1)
    df['DateTime'] = pd.to_datetime(df['DateTime'],format='%d-%m-%Y %H:%M')  
    Timestmp=df['DateTime']
    x_total = df.drop(['frequency',"ModeS_IP","ModeD_IP","ModeS_Port","ModeD_Port","DateTime"],axis=1)
    # Separating out the target
    y = df['frequency']
    # Standardizing the features
    x_total = StandardScaler().fit_transform(x_total)
    pca = PCA(n_components=5)
    principalComponents = pca.fit_transform(x_total)
    Df_total = pd.DataFrame(data = principalComponents
                , columns = ['PC1', 'PC2','PC3','PC4','PC5'])
    Df_total['frequency'] = y.values
    Df_total['DateTime'] = Timestmp.values
    df_t=Df_total.copy()
    df_t.DateTime= pd.to_datetime(df_t.DateTime,format='%d-%m-%Y %H:%M')
    df_t.DateTime=df_t.DateTime.dt.strftime('%d-%m-%Y %H:%M')
    lastdate = datetime.strptime(df_t.DateTime.values[-1], '%d-%m-%Y %H:%M')
    df_t.DateTime= pd.to_datetime(df_t.DateTime,format='%d-%m-%Y %H:%M')
    df_t.DateTime=df_t.DateTime.dt.strftime('%d-%m-%Y %H:%M')
    df_t.set_index(df_t.DateTime,inplace=True)
    autoorder=auto_arima(df_t['frequency'],suppress_warning=True).get_params()
    model=ARIMA(df_t['frequency'],order=autoorder['order'])
    model_fit=model.fit()
    delta=timedelta(hours=1)
    delday=timedelta(days=1)
    futuredate=[]
    for time in range(5):
        futuredate.append(lastdate+delday-delta*time)
    futuredate.reverse()
    plt.figure(figsize=(20,15)) 
    plt.plot(df_t['frequency'],label='Actual')
    plt.plot(model_fit.forecast(steps=5),label='Forecast')
    plt.legend(loc='best')
    plt.xticks(rotation=90,fontsize=6)
    plt.xlabel('Time')
    plt.ylabel('packets')
    plt.savefig(f"{parent}\web\\data\\AI\\packets.png")
    

def predict_violation():
    df=masterdata.copy()
    df["hour"] = df["hour"].astype(str)
    df["DateTime"]=df["DATE"]+" "+df["hour"]+":"+"00"
    df.drop(["DATE",'hour'],inplace=True,axis=1)
    df['DateTime'] = pd.to_datetime(df['DateTime'],format='%d-%m-%Y %H:%M')  
    df['violation'] = df['frequency']-df['SAFE']
    Timestmp=df['DateTime']
    x_total = df.drop(['violation',"ModeS_IP","ModeD_IP","ModeS_Port","ModeD_Port","DateTime"],axis=1)
    # Separating out the target
    y = df['violation']
    # Standardizing the features
    x_total = StandardScaler().fit_transform(x_total)
    pca = PCA(n_components=4)
    principalComponents = pca.fit_transform(x_total)
    Df_total = pd.DataFrame(data = principalComponents
                , columns = ['PC1', 'PC2','PC3','PC4'])
    Df_total['violation'] = y.values
    Df_total['DateTime'] = Timestmp.values
    df_t=Df_total.copy()
    df_t.DateTime= pd.to_datetime(df_t.DateTime,format='%d-%m-%Y %H:%M')
    df_t.DateTime=df_t.DateTime.dt.strftime('%d-%m-%Y %H:%M')
    lastdate = datetime.strptime(df_t.DateTime.values[-1], '%d-%m-%Y %H:%M')
    df_t.DateTime= pd.to_datetime(df_t.DateTime,format='%d-%m-%Y %H:%M')
    df_t.DateTime=df_t.DateTime.dt.strftime('%d-%m-%Y %H:%M')
    df_t.set_index(df_t.DateTime,inplace=True)
    autoorder=auto_arima(df_t['violation'],suppress_warning=True).get_params()
    model=ARIMA(df_t['violation'],order=autoorder['order'])
    model_fit=model.fit()
    delta=timedelta(hours=1)
    delday=timedelta(days=1)
    futuredate=[]
    for time in range(5):
        futuredate.append(lastdate+delday-delta*time)
    futuredate.reverse()
    plt.figure(figsize=(20,15)) 
    plt.plot(df_t['violation'],label='Actual')
    plt.plot(model_fit.forecast(steps=5),label='Forecast')
    plt.legend(loc='best')
    plt.xticks(rotation=90,fontsize=6)
    plt.xlabel('Time')
    plt.ylabel('Violation')
    plt.savefig(f"{parent}\web\\data\\AI\\violation.png")
    
predict_violation()
predict_package()
