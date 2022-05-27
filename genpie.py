import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *
from datetime import *
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
def genpieC(data):
    data['DateTime'] = pd.to_datetime(data['DateTime'], infer_datetime_format=True)
    data['DateTime'] = data['DateTime'].dt.strftime('%d-%m-%Y %H:%M:%S')
    data['DateTime'] = data['DateTime'].astype(str)
    strt=data['DateTime'].values[0].split(" ")[0]
    end=data['DateTime'].values[-1].split(" ")[0]
    values=dict(data["Comments"].value_counts())
    pie_val=dict()
    for value in ['SAFE','IP','PORT','FLAG']:
        if (f"[{value}]" in  list(values.keys())):
            pie_val[f"{value}"]=values[f"[{value}]"]
            del values[f'[{value}]']
    if (len(values)>0 ):
        pie_val["MULTIPLE"]=0
        for key in values:
            pie_val["MULTIPLE"]=pie_val["MULTIPLE"]+values[key]
    exp=list()
    for x in range(len(pie_val)):
        exp.append(0.1)  
    colors = sns.color_palette('pastel')
    plt.pie(pie_val.values(), labels = pie_val.keys(), colors = colors, autopct='%.0f%%',explode = exp, shadow = True)
    plt.legend(title = "Comments",bbox_to_anchor =(0.75,0.75))
    plt.savefig(f"{parent}\web\\data\\pie\\Comments.png")
    plt.clf()
    

def genpieF(data):
    data['DateTime'] = pd.to_datetime(data['DateTime'], infer_datetime_format=True)
    data['DateTime'] = data['DateTime'].dt.strftime('%d-%m-%Y %H:%M:%S')
    data['DateTime'] = data['DateTime'].astype(str)
    strt=data['DateTime'].values[0].split(" ")[0]
    end=data['DateTime'].values[-1].split(" ")[0]
    values=dict(data["Flags"].value_counts())
    pie_val=dict()
    for value in ["F","A","P","R","S","U","N"]:
        if (f"{value}" in  list(values.keys())):
            pie_val[f"{value}"]=values[f"{value}"]
            del values[f'{value}']
    if (len(values)>0):
        pie_val["MULTIPLE"]=0
        for key in values:
            pie_val["MULTIPLE"]=pie_val["MULTIPLE"]+values[key]
    exp=list()
    for x in range(len(pie_val)):
        exp.append(0.3)  
    colors = sns.color_palette('hls')
    plt.pie(pie_val.values(), labels = pie_val.keys(), colors = colors, autopct='%.0f%%',explode = exp, shadow = True)
    plt.legend(title = "Flags",bbox_to_anchor =(0.75,0.75))
    plt.savefig(f"{parent}\web\\data\\pie\\Flags.png")
    plt.clf()

def genpieP(data):
    data['DateTime'] = pd.to_datetime(data['DateTime'], infer_datetime_format=True)
    data['DateTime'] = data['DateTime'].dt.strftime('%d-%m-%Y %H:%M:%S')
    data['DateTime'] = data['DateTime'].astype(str)
    strt=data['DateTime'].values[0].split(" ")[0]
    end=data['DateTime'].values[-1].split(" ")[0]
    values=dict(data["Protocol"].value_counts())
    pie_val=dict()
    for value in ["TCP","UDP"]:
        if (f"{value}" in  list(values.keys())):
            pie_val[f"{value}"]=values[f"{value}"]
            del values[f'{value}']
    exp=list()
    for x in range(len(pie_val)):
        exp.append(0.2)  
    colors = sns.color_palette('Paired')
    plt.pie(pie_val.values(), labels = pie_val.keys(), colors = colors, autopct='%.0f%%',explode = exp, shadow = True)
    plt.legend(title = "Protocol",bbox_to_anchor =(0.75,0.75))
    plt.savefig(f"{parent}\web\\data\\pie\\Protocol.png")
    plt.clf()


def genpieO(data):
    data['DateTime'] = pd.to_datetime(data['DateTime'], infer_datetime_format=True)
    data['DateTime'] = data['DateTime'].dt.strftime('%d-%m-%Y %H:%M:%S')
    data['DateTime'] = data['DateTime'].astype(str)
    strt=data['DateTime'].values[0].split(" ")[0]
    end=data['DateTime'].values[-1].split(" ")[0]
    values=dict(data["OS"].value_counts())
    pie_val=dict()
    for value in ["O","W","L","M"]:
        if (f"{value}" in  list(values.keys())):
            pie_val[f"{value}"]=values[f"{value}"]
            del values[f'{value}']
    exp=list()
    for x in range(len(pie_val)):
        exp.append(0.05)  
    colors = sns.color_palette('PuOr')
    plt.pie(pie_val.values(), labels = pie_val.keys(), colors = colors, autopct='%.0f%%',explode = exp, shadow = True)
    plt.legend(title = "OS",bbox_to_anchor =(0.75,0.75))
    plt.savefig(f"{parent}\web\\data\\pie\\OS.png")
    plt.clf()

def genpieT(data):
    data['DateTime'] = pd.to_datetime(data['DateTime'], infer_datetime_format=True)
    data['hour']=data['DateTime'].dt.hour
    data['DateTime'] = data['DateTime'].dt.strftime('%d-%m-%Y %H:%M:%S')
    data['DateTime'] = data['DateTime'].astype(str)
    strt=data['DateTime'].values[0].split(" ")[0]
    end=data['DateTime'].values[-1].split(" ")[0]
    values=dict(data["hour"].value_counts())
    data['hour']=pd.to_numeric(data['hour'], downcast='unsigned')
    pie_val=dict()
    for value in values.keys():
        pie_val[value]=values[value]
    exp=list()
    for x in range(len(pie_val)):
        exp.append(0.05)  
    colors = sns.color_palette("rocket")
    plt.pie(pie_val.values(), labels = pie_val.keys(), colors = colors, autopct='%.0f%%',explode = exp, shadow = True)
    plt.legend(title = "Time",bbox_to_anchor =(0.75,0.75))
    plt.savefig(f"{parent}\web\\data\\pie\\Time.png")
    plt.clf()


def genMaster(data): 
    genpieT(data)
    genpieO(data)
    genpieP(data)
    genpieC(data)
    genpieF(data)
    
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

def userin():
    clean=getListOfFiles(parent+"\web\\data\\cleaned")
    masterdata=[]
    for file in clean:
        masterdata.append(pd.read_csv(file))
    masterdata=pd.concat(masterdata)
    dirRaw=parent+"\web\\data\\raw"
    today = date.today()
    check=today.strftime("%Y-%m-%d")
    checkfile=dirRaw+"\\"+check+".csv"
    if os.path.exists(checkfile):
        today_df=pd.read_csv(checkfile)
        today_df=cleandata(today_df)
        masterdata=pd.concat([masterdata,today_df])
    masterdata['DateTime'] = pd.to_datetime(masterdata['DateTime'],format='%Y-%m-%d %H:%M:%S')
    strtdate=input("Enter Start Date (dd-mm-yyyy): ")
    enddate=input("Enter End Date (dd-mm-yyyy): ")
    
    if(strtdate=="" and enddate==""):
        genMaster(masterdata)
    elif(enddate==""):
        mask=masterdata['DateTime'] == strtdate
        masterdata=masterdata[mask]
        genMaster(masterdata)
    else:
        mask = (masterdata['DateTime'] > strtdate) & (masterdata['DateTime'] <= enddate)
        data=masterdata[mask]
        if(data.empty):
            print("No Data Found")
        else:genMaster(data)

userin()