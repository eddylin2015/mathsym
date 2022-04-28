#1.1  File List:  *-*.jpg
from os import listdir
import pandas as pd
mypath = "./in/"
files = listdir(mypath)
data_date=[]
data_customer=[]
data_average=[]

for f in files:
    if ".csv" in f  :
        print(f)
        df = pd.read_csv(f'{mypath}{f}', delimiter=',') #, names=('time','customer'))
        data_date.append(f.replace(".csv",""))
        data_customer.append(df["customer"].sum())
        data_average.append(0)

for idx,val in enumerate(data_customer):
    if idx==0:
        pass
    elif idx==len(data_customer)-1:
        pass
    else:
        data_average[idx]=int((data_customer[idx-1]+val+data_customer[idx+1])/3)

print(data_date)
print(data_customer)
print(data_average)

d = {'date': data_date, 'total_customer': data_customer,'Ave':data_average }
total_df = pd.DataFrame(data=d)
total_df.to_excel("out/output.xlsx")  

import matplotlib.pyplot as plt
import numpy as np

x = np.arange(len(data_date))  # the label locations
width = 0.35  # the width of the bars
fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, data_customer, width, label='customer')
rects2 = ax.bar(x + width/2, data_average, width, label='3 days average')
# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('customer')
ax.set_title('customer / pre day')
ax.set_xticks(x)
ax.set_xticklabels(data_date)
ax.legend()
plt.xticks(rotation=30)
fig.tight_layout()
plt.savefig("out/out.png")