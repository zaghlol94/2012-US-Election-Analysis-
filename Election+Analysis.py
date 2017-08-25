
# coding: utf-8

# In[1]:

import pandas as pd
from pandas import Series,DataFrame
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
get_ipython().magic('matplotlib inline')


# In[3]:

import requests
from io import StringIO


# In[5]:

url = "http://elections.huffingtonpost.com/pollster/2012-general-election-romney-vs-obama.csv"

source = requests.get(url).text

poll_data = StringIO(source) 


# In[7]:

df=pd.read_csv(poll_data)
df.head()


# In[8]:

df.info()


# In[10]:

sns.countplot('Affiliation',data=df)


# In[12]:

sns.countplot('Affiliation',data=df,hue='Population')


# In[14]:

avg=pd.DataFrame(df.mean())


# In[15]:

avg.head()


# In[31]:

avg.drop(['Question Text','Question Iteration'],axis=0,inplace=True)


# In[32]:

avg


# In[33]:

std=pd.DataFrame(df.std())
std.drop(['Number of Observations','Question Text','Question Iteration'],axis=0,inplace=True)


# In[34]:

std.head()


# In[35]:

avg.plot(yerr=std,kind='bar',legend=False)


# In[36]:

poll_avg = pd.concat([avg,std],axis=1)

poll_avg.columns = ['Average','STD']


poll_avg


# In[37]:

df


# In[39]:

df.plot(x='End Date',y=['Obama','Romney','Undecided'],linestyle='',marker='o')


# In[40]:

from datetime import datetime


# In[42]:

df['diffrence']=(df.Obama-df.Romney)/100


# In[43]:

df.head()


# In[44]:

df=df.groupby(['Start Date'],as_index=False).mean()


# In[46]:

df.head()


# In[50]:

fig = df.plot('Start Date','diffrence',figsize=(12,4),marker='o',linestyle='-',color='purple')


# In[53]:

row_in = 0
xlimit = []


for date in df['Start Date']:
    if date[0:7] == '2012-10':
        xlimit.append(row_in)
        row_in +=1
    else:
        row_in += 1
        
print (min(xlimit))
print (max(xlimit))


# In[67]:

fig = df.plot('Start Date','diffrence',figsize=(12,4),marker='o',linestyle='-',color='purple',xlim=(329,356))
plt.axvline(x=329+2, linewidth=4, color='grey')
plt.axvline(x=329+10, linewidth=4, color='grey')
plt.axvline(x=329+21, linewidth=4, color='grey')


# In[68]:

df1 = pd.read_csv('Election_Donor_Data.csv')


# In[69]:

df1.head()


# In[73]:

df1['contb_receipt_amt'].value_counts()


# In[76]:

don_mean = df1['contb_receipt_amt'].mean()


don_std = df1['contb_receipt_amt'].std()
print ('The average donation was %.2f with a std of %.2f' %(don_mean,don_std))


# In[78]:

top_donor = df1['contb_receipt_amt'].copy()
top_donor.sort_values()
top_donor


# In[80]:

top_donor = top_donor[top_donor >0]
top_donor.sort_values()
top_donor.value_counts().head(10)


# In[81]:

com_don = top_donor[top_donor < 2500]
com_don.hist(bins=100)


# In[83]:

candidates = df1.cand_nm.unique()
candidates


# In[84]:

party_map = {'Bachmann, Michelle': 'Republican',
           'Cain, Herman': 'Republican',
           'Gingrich, Newt': 'Republican',
           'Huntsman, Jon': 'Republican',
           'Johnson, Gary Earl': 'Republican',
           'McCotter, Thaddeus G': 'Republican',
           'Obama, Barack': 'Democrat',
           'Paul, Ron': 'Republican',
           'Pawlenty, Timothy': 'Republican',
           'Perry, Rick': 'Republican',
           "Roemer, Charles E. 'Buddy' III": 'Republican',
           'Romney, Mitt': 'Republican',
           'Santorum, Rick': 'Republican'}


# In[86]:

df1['Party'] = df1.cand_nm.map(party_map)


# In[88]:

df1=df1[df1.contb_receipt_amt >0]


# In[90]:

df1.head()


# In[92]:

df1.groupby('cand_nm')['contb_receipt_amt'].count()


# In[94]:

df1.groupby('cand_nm')['contb_receipt_amt'].sum()


# In[96]:

cand_amount = df1.groupby('cand_nm')['contb_receipt_amt'].sum()
i = 0

for don in cand_amount:
    print(" The candidate %s raised %.0f dollars " %(cand_amount.index[i],don))
    print ('\n')
    i += 1


# In[97]:

cand_amount.plot(kind='bar')


# In[99]:

df1.groupby('Party')['contb_receipt_amt'].sum()


# In[98]:

df1.groupby('Party')['contb_receipt_amt'].sum().plot(kind='bar')


# In[101]:

occupation_df = df1.pivot_table('contb_receipt_amt',
                                index='contbr_occupation',
                                columns='Party', aggfunc='sum')


# In[103]:

occupation_df.head()


# In[104]:

occupation_df.shape


# In[ ]:

occupation_df.plot(kind='bar')


# In[ ]:



