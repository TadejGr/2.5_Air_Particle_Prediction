from Plot_AQI import avg_data
import requests
import sys
import pandas as pd
from bs4 import BeautifulSoup
import os
import csv

def data_combine(year, cs):
    for a in pd.read_csv("Data/Real-Data/real_"+str(year)+".csv", chunksize=cs, skip_blank_lines=True):
        df=pd.DataFrame(data=a)        
        mylist=df.values.tolist()
    return mylist
        

def meta_data(month, year):
    file_html=open("Data/Html_Data/{}/{}.html".format(year, month), 'rb')
    plain_text=file_html.read()
    
    tempD=[]
    finalD=[]
    
    soup=BeautifulSoup(plain_text, "lxml")
    for table in soup.find_all('table', {'class':'medias mensuales numspan'}):
        for tbody in table:
            for tr in tbody:
                a=tr.get_text()
                tempD.append(a)
    #we have 15 columns of different data, therefore we divide by 15
    rows=len(tempD)/15
    
    for times in range(round(rows)):
        newtempD=[]
        for i in range(15):
            newtempD.append(tempD[0])
            tempD.pop(0)
        finalD.append(newtempD)
    
    length=len(finalD)
    
    #remove the last and the first line, because it has non-relevant data
    finalD.pop(length-1)
    finalD.pop(0)
    
    #remove columns which contain non-releavnt data (ie. no data)
    for a in range(len(finalD)):
        finalD[a].pop(6)
        finalD[a].pop(13)
        finalD[a].pop(12)
        finalD[a].pop(11)
        finalD[a].pop(10)
        finalD[a].pop(9)
        finalD[a].pop(0)
        finalD[a].pop(3)
    
    return finalD

if __name__ == '__main__':
    if not os.path.exists("Data/Real-Data"):
        os.makedirs("Data/Real-Data")
    for year in range(2013, 2018):
        final_data=[]
        with open("Data/Real-Data/real_"+str(year)+".csv", 'w', newline='') as csvfile:
            wr=csv.writer(csvfile, dialect="excel")
            wr.writerow(['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM2.5'])
        for month in range(1,13):
            temp=meta_data(month,year)
            final_data=final_data+temp
        
        #pm=getattr(sys.modules[__name__], "avg_data({})".format("2013"))()
        pm=avg_data(year)
        
        if len(pm)==364:
            pm.insert(364,'-')
        
        for i in range(len(final_data)):
            final_data[i].insert(7,pm[i])
            
        with open("Data/Real-Data/real_"+str(year)+".csv", "a", newline='') as csvfile:
            wr=csv.writer(csvfile, dialect="excel")
            for row in final_data:
                flag=0
                for elem in row:
                    if elem=="" or elem=="-":
                        flag=1
                if flag != 1:
                    wr.writerow(row)
                    
    total=[]
    for year in range(2013, 2019):
        total=total+data_combine(year, 600)
        
    with open("Data/Real-Data/Real_Combine.csv", "w", newline='') as csvfile:
        wr=csv.writer(csvfile, dialect="excel")
        wr.writerow(['T', 'TM', 'Tm', 'H', 'VV', 'V', 'VM', 'PM2.5', 'nan'])
        wr.writerows(total)

df=pd.read_csv("Data/Real-Data/Real_Combine.csv")
df=df[df.columns[:-1]]
print(df)
            