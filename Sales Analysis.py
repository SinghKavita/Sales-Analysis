#!/usr/bin/env python
# coding: utf-8

# # Import necessary libraries

# In[ ]:


import pandas as pd


# In[3]:


import os #os module is used for file handling


# In[4]:


dt=pd.read_csv("C:\\Users\HP\Downloads\Sales_Data\Sales_August_2019.csv")
dt.head()


# # Merge data from each month into one CSV

# In[5]:


path = "C:\\Users\HP\Downloads\Sales_Data"
files = [file for file in os.listdir(path)]#it gives list of all files
print(files)
all_data = pd.DataFrame()#creating empty dataframe

for file in files:#files me loop chala rhe h file k liye
    current_data = pd.read_csv(path+"/"+file)#sara data read ho rha h is path me
    all_data = pd.concat([all_data, current_data])#ab empty dataframeme concatenate kr diye
all_data


# In[6]:


all_data.shape


# In[7]:


#all_data.reset_index(drop=True, inplace=True)#dropiung index,inplace=data has updated at that place itself
#all_data1=all_data.reset_index()#ye bhi kam ni kiya
#all_data=all_data.style.hide_index()
#all_data.to_csv("all_data_copy.csv", index=False)
#
all_data


# In[8]:


#for file in files[0:13:1]:
    #current_data = pd.read_csv(path+"/"+file)
#
#current_data
#sara data merge ho gya h but csv format me h
    #all_months_data = pd.concat([all_months_data, current_data])#ab empty dataframeme concatenate kr diye
#all_months_data.to_csv("all_data_copy.csv", index=False)


# # Read in updated dataframe

# In[9]:


all_data.head()
#all_months_data(index=False)


# # Clean up the data:
# The first step in this is figuring out what we need to clean. I have found in practice, that you find things you need to clean as you perform operations and get errors. Based on the error, you decide how you should go about cleaning the data

# # Drop rows of NAN
# 

# In[10]:


all_data.isnull().sum()


# In[11]:


nan_df = all_data[all_data.isna().any(axis=1)]#it shows null values along colums
nan_df.head()


# In[12]:


nan_df = all_data[all_data.isna().any(axis=1)]#it shows null values along colums
print(nan_df.head())#krne pr empty dataframe deta h with column names
nan_df.head()#sirf ye krne pr iska output ni de rha h, display krna pdega

all_data = all_data.dropna(how='all')#will dro all the null values
all_data.head()


# ## Get rid of text in order date column

# In[13]:


all_data.shape


# In[14]:


all_data.dtypes


# In[15]:


#doubtt
all_data = all_data[all_data['Order Date'].str[0:2]!='Or']


# # Make columns correct type

# In[16]:


all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])


# # Augment data with additional columns

# Add month column

# In[19]:


#doubt
all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = pd.to_numeric(all_data['Month'])
#all_data['Month'] = all_data['Month'].astype('int32')
all_data.head()


# Add month column (alternative method)

# In[87]:


all_data.dtypes


# In[88]:


#ni work kiya
#all_data['Month 2'] = pd.to_datetime(all_data['Order Date']).dt.month
#all_data.head()


# # Add city column

# In[89]:


#doubt
def get_city(a):
    return a.split(",")[1]

def get_state(a):
    return a.split(",")[2].split(" ")[1]

all_data['City'] = all_data['Purchase Address'].apply(lambda x: get_city(x) + ' ' + get_state(x))
all_data.head()


# # Data Exploration

# Question 1: What was the best month for sales? How much was earned that month?

# In[90]:


all_data['Sales'] = all_data['Quantity Ordered']* all_data['Price Each']
all_data.head()


# In[91]:


all_data.groupby(['Month'])


# In[92]:


all_data.groupby(['Month']).sum()


# In[93]:


import matplotlib.pyplot as plt

months = range(1,13)
print(months)
#doubt niche
plt.bar(months,all_data.groupby(['Month']).sum()['Sales'])
plt.xticks(months)
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month number')
plt.show()


# Question 2: What city sold the most product?

# In[94]:


all_data.groupby(['City']).sum()


# In[95]:


import matplotlib.pyplot as plt

keys = [city for city, df in all_data.groupby(['City'])]#doubt

plt.bar(keys,all_data.groupby(['City']).sum()['Sales'])#doubt
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month number')
plt.xticks(keys, rotation='vertical', size=8)
plt.show()


# Question 3: What time should we display advertisements to maximize probability of customer's buying product?

# In[96]:


# Add hour column
all_data['Hour'] = pd.to_datetime(all_data['Order Date']).dt.hour
all_data['Minute'] = pd.to_datetime(all_data['Order Date']).dt.minute
all_data.head()


# In[97]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[100]:


b=all_data.groupby(['Hour']).count()
b


# In[1]:


hours = [hour for hour, df in all_data.groupby(['Hour'])]
plt.plot(hours, all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.xlabel('Hour')
plt.ylabel('No. of Orders')
plt.grid()
plt.show()

# My recommendation is slightly before 12am or 7pm


# Question 4: What products are most often sold together?

# In[29]:


# https://stackoverflow.com/questions/43348194/pandas-select-rows-if-id-appear-several-time
df = all_data[all_data['Order ID'].duplicated(keep=False)]#it sbhows all duplicates

# Referenced: https://stackoverflow.com/questions/27298178/concatenate-strings-from-several-rows-using-pandas-groupby
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))#groupling the product by order id
df2 = df[['Order ID', 'Grouped']].drop_duplicates()#sare duplicate delete krke orderid and grouped ka dataframe bna rhe h
df2.head()


# In[30]:


# Referenced: https://stackoverflow.com/questions/52195887/counting-unique-pairs-of-numbers-into-a-python-dictionary
from itertools import combinations
from collections import Counter

count = Counter()

for row in df2['Grouped']:#grouped ka list le rhe h
    row_list = row.split(',')#isting the elements in list which are seperated by comma
    count.update(Counter(combinations(row_list, 2)))#two-two k combination me elements ko update kr rhe h but same id ka with freq
for key,value in count.most_common(10):#top 10 element is determined by most common
    print(key, value)#key ho gye 2 products and frequency ho gyi value
#this ans. helps in business decisions


# What product sold the most? Why do you think it sold the most?

# In[31]:


product_group = all_data.groupby('Product')#split the product in a group
quantity_ordered = product_group.sum()['Quantity Ordered']#group me jitne product h unki kitni quantity

products = [product for product, df in product_group]
plt.bar(products, quantity_ordered)
plt.ylabel("Quantity Ordered")
plt.xlabel("Product")
plt.bar(products, quantity_ordered)
plt.xticks(products, rotation='vertical', size=10)
plt.show()


# In[32]:


# Referenced: https://stackoverflow.com/questions/14762181/adding-a-y-axis-label-to-secondary-y-axis-in-matplotlib

prices = all_data.groupby('Product').mean()['Price Each']

fig, ax1 = plt.subplots()#mutilpe plots on a sigle figure
#fig returns figure, ax return axes
ax2 = ax1.twinx()#twins the asxes
ax1.bar(products, quantity_ordered, color='g')
ax2.plot(products, prices, color='b')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color='g')
ax2.set_ylabel('Price ($)', color='b')
ax1.set_xticklabels(products, rotation='vertical', size=8)

fig.show()


# In[ ]:




