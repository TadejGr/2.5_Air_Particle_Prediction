import pandas as pd
import matplotlib.pyplot as plt

#obtain average daily PM2.5 values for each day in a specific year in the form of a list
def avg_data(year):
    temp_i=0
    average=[]
    #because measurements are taken hourly, we can take a chunk of 24 measurements to get the data for one day
    for rows in pd.read_csv("Data/AQI/aqi{}.csv".format(year), chunksize=24): 
        add_var=0
        avg=0.0
        data=[]
        count=0
        df=pd.DataFrame(data=rows)
        for index, row in df.iterrows():
            data.append(row['PM2.5'])
        for i in data:
            if type(i) is float or type(i) is int:
                add_var=add_var+i
                count=count+1
            elif type(i) is str:
                if i!='NoData' and i !='PwrFail' and i!='---' and i!='InVld':
                    temp=float(i)
                    add_var=add_var+temp
                    count=count+1
        if count==0:
            avg=0
        else:
            avg=add_var/count
        temp_i=temp_i+1
        
        average.append(avg)
    
    return average
           
if __name__ == '__main__':
    lst2013=avg_data("2013")
    lst2014=avg_data("2014")
    lst2015=avg_data("2015")
    lst2016=avg_data("2016")
    lst2017=avg_data("2017")
    lst2018=avg_data("2018")
    plt.plot(range(0,365), lst2013, label="2013 data")
    plt.plot(range(0,364), lst2014, label="2014 data")
    plt.plot(range(0,365), lst2015, label="2015 data")
    plt.show()
            