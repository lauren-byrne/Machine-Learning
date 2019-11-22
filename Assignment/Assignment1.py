#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Lauren Byrne
#C16452764
import pandas as pd
import numpy as np

#read in dataset from csv file and store in dataframe 'df'
df = pd.read_csv("./data/dataset.csv", header = None, na_values=' ?')

#read in text files of feature names into 'text-file'
text_file = open("./data/feature_names.txt", "r")
#split text file into a list called new_names
new_names = text_file.read().splitlines()
text_file.close()

#set the dataframe columns to be the contents of the list
df.columns = new_names


# In[2]:


#replace all ? values with NaN
df.replace(' ?', np.NaN)


# In[3]:


#separating the dataframe into categorical and continuous data
#getting all the continuous data into a new dataframe called originalCont
originalCont = df._get_numeric_data()


# In[4]:


originalCont


# In[5]:


#getting the columns names for the continuous data
continuous = df._get_numeric_data().columns


# In[6]:


continuous


# In[7]:


cols = df.columns


# In[8]:


#getting the categorical data
categorical = list(set(cols) - set(continuous))


# In[9]:


#dropping column id
categorical.remove('id')


# In[10]:


#new dataframe storing all the categorical data
originalCat = df[categorical]


# In[11]:


categorical


# In[12]:


#creating a new empty dataframe with index set as the names in the continuous names and defining column names
contdf = pd.DataFrame(index = continuous, columns=['Count', '% Miss', 'Card', 'Min', "1st Qrt", 'Mean', 'Median', "3rd Qrt", 'Max', "Std Dev"])


# In[13]:


#defining the index name
contdf.index.name = 'FEATURENAME'


# In[14]:


contdf


# In[15]:


#loop through the data in the continuous dataframe and perform functions on each column to store
#in empty dataframe created earlier
for col in originalCont.columns:
    contdf.loc[col, 'Count'] = len(originalCont[col])
    contdf.loc[col, '% Miss'] = (originalCont[col].isnull().sum()/len(originalCont[col]))*100
    contdf.loc[col, 'Card'] = originalCont[col].nunique()
    contdf.loc[col, 'Min'] = originalCont[col].min()
    contdf.loc[col, '1st Qrt'] = originalCont[col].quantile(0.25)
    contdf.loc[col, 'Mean'] = originalCont[col].mean()
    contdf.loc[col, 'Median'] = originalCont[col].median()
    contdf.loc[col, '3rd Qrt'] = originalCont[col].quantile(0.75)
    contdf.loc[col, 'Max'] = originalCont[col].max()
    contdf.loc[col, 'Std Dev'] = originalCont[col].std()


# In[16]:


contdf


# In[17]:


#creating a new empty dataframe with index set as the names in the categorical names and defining column names
catdf = pd.DataFrame(index = categorical, columns=['Count', '% Miss', 'Card', 'Mode', "Mode Freq.", 'Mode %', '2nd Mode', "2nd Mode Freq.", '2nd Mode %'])


# In[18]:


#defining the name of the index
catdf.index.name = 'FEATURENAME'


# In[19]:


catdf


# In[20]:


#function to calculate the mode% that takes in the column and the dataframe as parameters
def modePercentage(df, col):
    total_count = df[col].count()
    max_count = df[col].value_counts().max()
    result = (max_count/total_count)*100
    return result


# In[21]:


#function to calculate the second mode
def secondMode(df, col):
    series = df[col].value_counts()
    #dropping the first mode
    series = series.drop(series.index[0])
    #find the new first mode of the series
    mode_result = series.index[0]
    return mode_result


# In[22]:


#function to calculate the second Mode frequency
def secondModeFreq(df, col):
    series = df[col].value_counts()
    #dropping the first mode
    series = series.drop(series.index[0])
    #finding the frequency of the new first mode
    max_count = series[0]
    return max_count


# In[23]:


#function to calculate the second Mode %
def secondModePercentage(df, col):
    series = df[col].value_counts()
    #drop the first mode
    series = series.drop(series.index[0])
    total_count = series.count()
    max_count = series[0]
    result = (max_count/df[col].count())*100
    return result


# In[24]:


#loop through the data in the categorical dataframe and perform functions on each column to store
#in empty dataframe created earlier
for col in originalCat.columns:
    catdf.loc[col, 'Count'] = len(originalCat[col]) 
    catdf.loc[col, '% Miss'] = (originalCat[col].isnull().sum()/len(originalCat[col]))*100
    catdf.loc[col, 'Card'] = originalCat[col].nunique()
    catdf.loc[col, 'Mode'] = originalCat.mode()[col][0]
    catdf.loc[col, 'Mode Freq.'] = originalCat[col].value_counts().max()
    #the following are function calls to calculate the values
    catdf.loc[col, 'Mode %'] = modePercentage(originalCat, col)
    catdf.loc[col, '2nd Mode'] = secondMode(originalCat, col)
    catdf.loc[col, '2nd Mode Freq.'] = secondModeFreq(originalCat, col)
    catdf.loc[col, '2nd Mode %'] = secondModePercentage(originalCat, col)


# In[25]:


df.update(catdf)


# In[26]:


#reordering the index to be the correct order
catdf = catdf.reindex(index = ['workclass', 'education','marital-status', 'occupation', 'relationship', 'race', 'sex', 'native-country', 'target'])


# In[27]:


catdf


# In[28]:


#exporting the dataframes to be csv files
catdf.to_csv('C16452764CAT.csv', sep = ',')
contdf.to_csv('C16452764CONT.csv', sep = ',')


# In[ ]:




