import os
import pandas as pd
import numpy as np
from sklearn import preprocessing
from scipy import stats
from datetime import date
import random
import warnings

warnings.filterwarnings("ignore")
Encoder1=preprocessing.LabelEncoder()
Encoder2=preprocessing.LabelEncoder()
Encoder3=preprocessing.LabelEncoder()
Encoder4=preprocessing.LabelEncoder()
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

def cleandata(data):
    data.columns = ['Sourceip','Destinationip','Sourceport','Destinationport',
                  'OS','Flags','Protocol','TTL','Length','Date','Time','Comments']
    data = data[data.Sourceip.str.contains('Sourceip') == False]
    data.dropna(subset=['Sourceip','Sourceport'], inplace=True)
    data["DateTime"]=data.Date+ " "+data.Time
    if(data['DateTime'].iloc[0].find('/')!=-1):
        data['DateTime'] = pd.to_datetime(data['DateTime'], format='%Y/%m/%d %H:%M:%S')
        data['DateTime'] = data['DateTime'].dt.strftime('%d-%m-%Y %H:%M:%S')
    elif(len(data['DateTime'].iloc[0].split('-')[0])==4):
        data['DateTime'] = pd.to_datetime(data['DateTime'], format='%Y-%m-%d %H:%M:%S')
        data['DateTime'] = data['DateTime'].dt.strftime('%d-%m-%Y %H:%M:%S')
    else:
        data['DateTime'] = pd.to_datetime(data['DateTime'], format='%d-%m-%Y %H:%M:%S')
    data.drop(["Date","Time"],axis=1,inplace=True)
    values = {"Comments": "[SAFE]", "Flags": "N"}
    data.fillna(value=values,inplace=True)
    data = data.reindex(columns=['DateTime','Sourceip','Destinationip','Sourceport','Destinationport','OS','Flags','Protocol','TTL','Length','Comments'])
    for feature in ["Sourceport","Destinationport","TTL","Length"]:
        data[feature]=pd.to_numeric(data[feature], downcast='unsigned')
    return data

def fragment(data):
    data[['Source1','Source2','Source3','Source4']]=data.Sourceip.str.split('.', expand=True)
    data[['dest1','dest2','dest3','dest4']]=data.Destinationip.str.split('.', expand=True)
    data.drop(['Sourceip','Destinationip'],axis=1,inplace=True)
    if("Total" not in data.columns.tolist()):
        cols=['DateTime','Source1','Source2','Source3','Source4','dest1','dest2','dest3','dest4','Sourceport','Destinationport','OS','Flags','Protocol','TTL','Length','Comments']
        data = data.reindex(columns=cols)
    for item in ["1","2","3","4"]:
        feature="Source"+item
        data[feature]=pd.to_numeric(data[feature], downcast='unsigned')
    for item in ["1","2","3","4"]:
        feature="dest"+item
        data[feature]=pd.to_numeric(data[feature], downcast='unsigned')
    return data

def unfragment(data):
    for item in ["1","2","3","4"]:
        feature="dest"+item
        data[feature] = data[feature].astype(str)
    for item in ["1","2","3","4"]:
        feature="Source"+item
        data[feature] = data[feature].astype(str)
    data["Source1"]=data["Source1"]+"."+data["Source2"]+"."+data["Source3"]+"."+data["Source4"]
    data["dest1"]=data["dest1"]+"."+data["dest2"]+"."+data["dest3"]+"."+data["dest4"]
    data.drop(['Source2','Source3','Source4','dest2','dest3','dest4'],axis=1,inplace=True)
    data.rename(columns={'Source1': 'Sourceip', 'dest1': 'Destinationip'}, inplace=True)
    if("Total" not in data.columns.tolist()):
        cols=['DateTime','Sourceip','Destinationip','Sourceport','Destinationport','OS','Flags','Protocol','TTL','Length','Comments']
        data = data.reindex(columns=cols)
    return data

def labelize(data):
    data["Comments"]=Encoder1.fit_transform(data["Comments"])
    data["Protocol"]=Encoder2.fit_transform(data["Protocol"])
    data["Flags"]=Encoder3.fit_transform(data["Flags"])
    data["OS"]=Encoder4.fit_transform(data["OS"])
    return data

def unlabelize(data):
    data["Comments"]=Encoder1.inverse_transform(data["Comments"])
    data["Potocol"]=Encoder2.inverse_transform(data["Protocol"])
    data["Flags"]=Encoder3.inverse_transform(data["Flags"])
    data["OS"]=Encoder4.inverse_transform(data["OS"])
    return data

def dataextrF(dic):
    key=list(dic.keys())
    internal_keys= list(dic[key[0]].keys())
    hour=[]
    for tup in internal_keys:
        hour.append(tup[0])
    hour=list(set(hour))
    act=dict()
    for time in hour:
        val=dict()
        for value in ["F","A","P","R","S","U","N"]:
            if ((time,f"{value}") in internal_keys):
                val[f"Flag_{value}"]=dic[key[0]][(time,f"{value}")]
                del dic[key[0]][(time,f"{value}")]
            else: val[f"Flag_{value}"]=0
        temp=[]
        if (len(dic[key[0]])>0):
            val["Flag_Multi"]=0
        for multi in internal_keys:
            temp.append(multi[1])
        temp=list(set(temp))
        for hold in internal_keys:
            if(time==hold[0] and hold[1] in temp and hold[1] not in ["F","A","P","R","S","U","N"]):
                val["Flag_Multi"]=val["Flag_Multi"]+dic[key[0]][(time,hold[1])]
            else:val["Flag_Multi"]=0
        act[time]=val
        del val
    data=pd.DataFrame.from_dict(act).T
    return data

def dataextrP(dic):
    key=list(dic.keys())
    internal_keys= list(dic[key[0]].keys())
    hour=[]
    for tup in internal_keys:
        hour.append(tup[0])
    hour=list(set(hour))
    act=dict()
    for time in hour:
        val=dict()
        for value in ["TCP","UDP"]:
            if ((time,f"{value}") in internal_keys):
                val[f"Proto_{value}"]=dic[key[0]][(time,f"{value}")]
                del dic[key[0]][(time,f"{value}")]
            else: val[f"Proto_{value}"]=0
        act[time]=val
        del val
    data=pd.DataFrame.from_dict(act).T
    return data

def dataextrC(dic):
    key=list(dic.keys())
    internal_keys= list(dic[key[0]].keys())
    hour=[]
    for tup in internal_keys:
        hour.append(tup[0])
    hour=list(set(hour))
    act=dict()
    for time in hour:
        val=dict()
        for value in ["SAFE","PORT","IP","FLAG"]:
            if ((time,f"[{value}]") in internal_keys):
                val[f"{value}"]=dic[key[0]][(time,f"[{value}]")]
                del dic[key[0]][(time,f"[{value}]")]
            else: val[f"{value}"]=0
        temp=[]
        if (len(dic[key[0]])>0):
            val["MULTIPLE_Com"]=0
        for multi in internal_keys:
            temp.append(multi[1])
        temp=list(set(temp))
        for hold in internal_keys:
            if(time==hold[0] and hold[1] in temp and hold[1] not in ["[FLAG]","[IP]","[SAFE]","[PORT]"]):
                val["MULTIPLE_Com"]=val["MULTIPLE_Com"]+dic[key[0]][(time,hold[1])]
            else:val["MULTIPLE_Com"]=0
        act[time]=val
        del val
    data=pd.DataFrame.from_dict(act).T
    return data

def dataextrO(dic):
    key=list(dic.keys())
    internal_keys= list(dic[key[0]].keys())
    hour=[]
    for tup in internal_keys:
        hour.append(tup[0])
    hour=list(set(hour))
    act=dict()
    for time in hour:
        val=dict()
        for value in ["O","W","L","M"]:
            if ((time,f"{value}") in internal_keys):
                val[f"OS_{value}"]=dic[key[0]][(time,f"{value}")]
                del dic[key[0]][(time,f"{value}")]
            else: val[f"OS_{value}"]=0
        act[time]=val
        del val
    data=pd.DataFrame.from_dict(act).T
    return data

def aggr(data):
    data.columns = ['DateTime','Sourceip','Destinationip','Sourceport','Destinationport',
                  'OS','Flags','Protocol','TTL','Length','Comments']
    if(data['DateTime'].iloc[0].find('/')!=-1):
        data['DateTime'] = pd.to_datetime(data['DateTime'], format='%Y/%m/%d %H:%M:%S')
        data['DateTime'] = data['DateTime'].dt.strftime('%d-%m-%Y %H:%M:%S')
    elif(len(data['DateTime'].iloc[0].split('-')[0])==4):
        data['DateTime'] = pd.to_datetime(data['DateTime'], format='%Y-%m-%d %H:%M:%S')
        data['DateTime'] = data['DateTime'].dt.strftime('%d-%m-%Y %H:%M:%S')
    else:
        data['DateTime'] = pd.to_datetime(data['DateTime'], format='%d-%m-%Y %H:%M:%S')
    data['DateTime'] = pd.to_datetime(data['DateTime'])
    data['DateTime'] = data['DateTime'].dt.strftime('%d-%m-%Y %H:%M:%S')
    data['DateTime'] = pd.to_datetime(data['DateTime'])
    data["hour"] = data["DateTime"].dt.hour
    grouped = data.groupby('hour').agg(
        frequency=('Comments', 'count'),
        ModeS_IP=('Sourceip',lambda x: stats.mode(x)[0]),
        ModeD_IP=('Destinationip',lambda x: stats.mode(x)[0]),
        ModeS_Port=('Sourceport',lambda x: stats.mode(x)[0]),
        ModeD_Port=('Destinationport',lambda x: stats.mode(x)[0]),
        Mode_TTL=('TTL',lambda x: stats.mode(x)[0]),
        length=('Length',lambda x: stats.mode(x)[0])
        )
    grouped1=data.groupby(['hour','Comments'])[['Sourceip']].count()
    grouped1.columns = ['Packet']
    grpComm=dataextrC(grouped1.to_dict())
    grouped2=data.groupby(['hour','Flags'])[['Sourceip']].count()
    grouped2.columns = ['Packet']
    grpFlag=dataextrF(grouped2.to_dict())
    join_df_1= pd.merge(grpComm, grpFlag,right_index=True, left_index=True, how='inner')
    grouped3=data.groupby(['hour','Protocol'])[['Sourceip']].count()
    grouped3.columns = ['Packet']
    grpPro=dataextrP(grouped3.to_dict())
    grouped4=data.groupby(['hour','OS'])[['Sourceip']].count()
    grouped4.columns = ['Packet']
    grpOS=dataextrO(grouped4.to_dict())
    join_df_2= pd.merge(grpPro, grpOS,right_index=True, left_index=True, how='inner')
    join_df_inter= pd.merge(join_df_1, join_df_2,right_index=True, left_index=True, how='inner')
    join_df_final=pd.merge(join_df_inter,grouped,right_index=True, left_index=True, how='inner')
    join_df_final.reset_index(inplace=True)
    join_df_final["DATE"]=pd.to_datetime(data['DateTime'],format='%d-%m-%Y %H:%M:%S')
    join_df_final["DATE"]=data['DateTime'].dt.strftime('%d-%m-%Y')
    join_df_final['WEEKDAY']=data['DateTime'].dt.dayofweek
    #join_df_final.set_index('date', inplace=True)
    join_df_final.rename(columns={'index': 'hour'}, inplace=True)
    cols=['DATE','hour','WEEKDAY', 'SAFE', 'PORT', 'IP', 'FLAG', 'MULTIPLE_Com', 'Flag_F',
            'Flag_A', 'Flag_P', 'Flag_R', 'Flag_S', 'Flag_U', 'Flag_N', 'Flag_Multi',
            'Proto_TCP', 'Proto_UDP', 'OS_O', 'OS_W', 'OS_L', 'OS_M', 'ModeS_IP', 'ModeD_IP',
            'ModeS_Port', 'ModeD_Port', 'Mode_TTL', 'length', 'frequency' ]
    join_df_final = join_df_final.reindex(columns=cols)
    join_df_final.ffill(inplace=True)
    join_df_final.bfill(inplace=True)
    for feature in ['hour', 'SAFE', 'PORT', 'IP', 'FLAG', 'MULTIPLE_Com', 'Flag_F',
            'Flag_A', 'Flag_P', 'Flag_R', 'Flag_S', 'Flag_U', 'Flag_N', 'Flag_Multi',
            'Proto_TCP', 'Proto_UDP', 'OS_O', 'OS_W', 'OS_L', 'OS_M','frequency']:
        join_df_final[feature]=pd.to_numeric(join_df_final[feature], downcast='unsigned')
    return join_df_final

def cleanfldr():
    dirRaw=parent+"\web\\data\\raw"
    today = date.today()
    check=today.strftime("%Y-%m-%d")
    checkfile=dirRaw+"\\"+check+".csv"
    listOfFilesRaw = getListOfFiles(dirRaw)
    if(checkfile in listOfFilesRaw):
        listOfFilesRaw.remove(checkfile)
    if not os.path.exists(parent+"\web\\data\\cleaned"):
        os.makedirs(parent+"\web\\data\\cleaned")
    if (len(listOfFilesRaw)>0):
        for file in listOfFilesRaw:
            data=pd.read_csv(file)
            data=cleandata(data)
            data.to_csv(parent+"\web\\data\\cleaned\\"+file.split("\\")[-1],index=False)
        for file in listOfFilesRaw:
            os.remove(file)
        
        
def agrfldr():
    cleanfldr()
    dirClean=parent+"\web\\data\\cleaned"
    listOfFilesClean = getListOfFiles(dirClean)
    if not os.path.exists(parent+"\web\\data\\aggregated"):
        os.makedirs(parent+"\we\\data\\aggregated")
    for file in listOfFilesClean:
        data=pd.read_csv(file)
        ag=aggr(data)
        ag.to_csv(parent+"\web\\data\\aggregated\\"+file.split("\\")[-1],index=False)
        
agrfldr()
