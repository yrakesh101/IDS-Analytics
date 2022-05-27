from turtle import color
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
import squarify
import xlsxwriter
from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *
from datetime import *
from sklearn.preprocessing import MinMaxScaler
import warnings

warnings.filterwarnings("ignore")
scaler = MinMaxScaler()
cwd = os.getcwd()
parent = os.path.dirname(cwd)
excel_file = f"{parent}\web\\data\\IP\\data.xlsx"
writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
if (not(os.path.exists(excel_file))):
    workbook = xlsxwriter.Workbook(excel_file)
    worksheet = workbook.add_worksheet()
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
def data_IP_C(dic):
  key=list(dic.keys())
  internal_keys= list(dic[key[0]].keys())
  IP=[]
  for tup in internal_keys:
    IP.append(tup[0])
  IP=list(set(IP))
  act=dict()
  for time in IP:
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

def data_IP_F(dic):
  key=list(dic.keys())
  internal_keys= list(dic[key[0]].keys())
  IP=[]
  for tup in internal_keys:
    IP.append(tup[0])
  IP=list(set(IP))
  act=dict()
  for time in IP:
    val=dict()
    for value in ["F","A","P","R","S","U"]:
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
        if(time==hold[0] and hold[1] in temp and hold[1] not in ["F","A","P","R","S","U"]):
           val["Flag_Multi"]=val["Flag_Multi"]+dic[key[0]][(time,hold[1])]
    else:val["Flag_Multi"]=0
    act[time]=val
    del val
  data=pd.DataFrame.from_dict(act).T
  return data

def data_IP_T(dic):
  key=list(dic.keys())
  internal_keys= list(dic[key[0]].keys())
  IP=[]
  hour=[]
  for tup in internal_keys:
    IP.append(tup[0])
    hour.append(tup[1])
  IP=list(set(IP))
  hour=list(set(hour))
  act=dict()
  for value in IP:
    val=dict()
    for time in hour:
      if ((f"{value}",time) in internal_keys):
        val[f"hour_{time}"]=dic[key[0]][(f"{value}",time)]
        del dic[key[0]][(f"{value}",time)]
      else: val[f"hour_{time}"]=0
    act[value]=val
    del val
  data=pd.DataFrame.from_dict(act).T
  return data

def data_IP_D(dic):
  key=list(dic.keys())
  internal_keys= list(dic[key[0]].keys())
  IP=[]
  date=[]
  for tup in internal_keys:
    IP.append(tup[0])
    date.append(tup[1])
  print(dic)
  IP=list(set(IP))
  date=list(set(date))
  act=dict()
  for value in IP:
    val=dict()
    for time in date:
      if ((f"{value}",time) in internal_keys):
        val[f"{time}"]=dic[key[0]][(f"{value}",time)]
        del dic[key[0]][(f"{value}",time)]
      else: val[f"{time}"]=0
    act[value]=val
    del val
  data=pd.DataFrame.from_dict(act).T
  return data

def aggrIP(data,tod=False):
  data['DateTime'] = pd.to_datetime(data['DateTime'], infer_datetime_format=True,format='%d-%m-%Y %H:%M:%S')
  data["hour"] = data["DateTime"].dt.hour
  data["date"] = data["DateTime"].dt.date
  grouped1=data.groupby(['Sourceip','Comments'])[['hour']].count()
  grouped1.columns = ['Packet']
  grpC=data_IP_C(grouped1.to_dict())
  if(tod==False):grpC.to_excel(writer, sheet_name="comments")
  grpC=pd.DataFrame(scaler.fit_transform(grpC),columns=grpC.columns.tolist(),index=grpC.index)
  mask_F=data['Flags']!='N'
  data_F=data[mask_F]
  grouped2=data_F.groupby(['Sourceip','Flags'])[['hour']].count()
  grouped2.columns = ['Packet']
  grpF=data_IP_F(grouped2.to_dict())
  if(tod==False):grpF.to_excel(writer, sheet_name="flags")
  grpF=pd.DataFrame(scaler.fit_transform(grpF),columns=grpF.columns.tolist(),index=grpF.index)
  mask_C=data['Comments']!='[SAFE]'
  data_C=data[mask_C]
  grouped3=data_C.groupby(['Sourceip','hour'])[['Comments']].count()
  grouped3.columns = ['Packet']
  grpT=data_IP_T(grouped3.to_dict())
  if(tod==False):grpT.to_excel(writer, sheet_name="time")
  grpT=pd.DataFrame(scaler.fit_transform(grpT),columns=grpT.columns.tolist(),index=grpT.index)
  mask_D=data['Comments']!='[SAFE]'
  data_D=data[mask_D]
  grouped4=data_D.groupby(['Sourceip','date'])[['Comments']].count()
  grouped4.columns = ['Packet']
  grpD=data_IP_D(grouped4.to_dict())
  if(tod==False):grpD.to_excel(writer, sheet_name="date")
  grpD=pd.DataFrame(scaler.fit_transform(grpD),columns=grpD.columns.tolist(),index=grpD.index)
  val={'date':[grpD.shape[0],grpD.shape[1]],'time':[grpT.shape[0],grpT.shape[1]],'comments':[grpC.shape[0],grpC.shape[1]],'flags':[grpF.shape[0],grpF.shape[1]]}
  for value in val.keys():
    workbook = writer.book
    worksheet = writer.sheets[value]
    worksheet.conditional_format(0, 0, val[value][0],val[value][1], {'type': 'data_bar','bar_color': '#63C384'})
  writer.save()
  plt.figure(figsize=(25,20)) 
  #axC=sns.heatmap(grpC.head(10), cmap="YlGnBu",linewidths=.1,annot=True, fmt='f')
  grpC['Sum']=grpC.sum(axis=1)
  squarify.plot(sizes=grpC.nlargest(50,['Sum'])['Sum'], label=grpC.nlargest(50,['Sum']).index, alpha=.8,color=sns.color_palette("YlGnBu") ,pad=True)
  plt.title("Comments",fontsize =25)
  if(tod==False):plt.savefig(f"{parent}\web\\data\\heat\\Comments.png")
  else:plt.savefig(f"{parent}\web\\data\\heat\\Comments_today.png")
  plt.clf()
  #axF=sns.heatmap(grpF.head(100), cmap="rocket_r",linewidths=.2,annot=True, fmt='.2f')
  grpF['Sum']=grpF.sum(axis=1)
  squarify.plot(sizes=grpF.nlargest(50,['Sum'])['Sum'], label=grpF.nlargest(50,['Sum']).index, alpha=.8,color=sns.color_palette("rocket_r"),pad=True )
  plt.title("Flags",fontsize =25)
  if(tod==False):plt.savefig(f"{parent}\web\\data\\heat\\Flags.png")
  else:plt.savefig(f"{parent}\web\\data\\heat\\Flags_today.png")
  plt.clf()
  #axT=sns.heatmap(grpT.head(100), cmap="mako_r",linewidths=.2,annot=True, fmt='.2f')
  grpT['Sum']=grpT.sum(axis=1)
  squarify.plot(sizes=grpT.nlargest(50,['Sum'])['Sum'], label=grpT.nlargest(50,['Sum']).index, alpha=.8,color= sns.color_palette("mako_r") ,pad=True)
  plt.title("Time",fontsize =25)
  if(tod==False):plt.savefig(f"{parent}\web\\data\\heat\\Time.png")
  else:plt.savefig(f"{parent}\web\\data\\heat\\Time_today.png")
  plt.clf()
  #axD=sns.heatmap(grpD.head(100), cmap="magma_r",linewidths=.2,annot=True, fmt='.2f')
  grpD['Sum']=grpD.sum(axis=1)
  squarify.plot(sizes=grpD.nlargest(50,['Sum'])['Sum'], label=grpD.nlargest(50,['Sum']).index, alpha=.8,color= sns.color_palette("magma_r"),pad=True )
  plt.title("Date",fontsize =25)
  if(tod==False):plt.savefig(f"{parent}\web\\data\\heat\\Date.png")
  plt.clf()
  
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
    masterdata=pd.concat(masterdata,False)
    aggrIP(masterdata)
    dirRaw=parent+"\web\\data\\raw"
    today = date.today()
    check=today.strftime("%Y-%m-%d")
    checkfile=dirRaw+"\\"+check+".csv"
    if os.path.exists(checkfile):
        today_df=pd.read_csv(checkfile)
        today_df=cleandata(today_df)
        #aggrIP(today_df,True)

userin()