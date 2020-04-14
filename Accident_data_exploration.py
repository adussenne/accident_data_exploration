
# coding: utf-8

# In[ ]:

import pandas as pd
import matplotlib as mlp
import matplotlib.pyplot as plt


# In[ ]:

raw_data = pd.read_csv("accidents.csv")
data.head()


# # ** Methodology **
# ## ** Step 1: Describe dataset**
# - Number of rows and columns 
# - Check data type
# - Check missing data
# 
# ## ** Step 2: Clean and enrich data **
# - Handle missing data
# - Invalid data types
# - Corrupted data
# - Calculate additional fields and extract features
# - Adding data (here: number of people by city)
# 
# ## ** Step 3: Visualize data **
# - Data distribution
# - Bar charts
# - Histograms
# - Box plots
# - Correlation

# In[ ]:

## STEP 1.1
## Extract number of rows and columns to better understand the shape of the dataset (small >< large dataset)
print "Number of observations:",raw_data.shape[0]
print "Number of features:",raw_data.shape[1]


# There are almost 3 millions of observations, so this is a large dataset. This number might slightly decrease when we clean the data (eg: observations with missing data). Moreover, the number of features may decrease depending on the quality of the information / number of missing observations for a specific feature. 

# In[ ]:

## STEP 1.2
## Check the data type of all
## raw_data.dtypes


# In[ ]:

## STEP 1.3
## Check missing values
raw_data.isnull().sum()


# Many observations are missing for some columns (eg: Wind Chill). In the "STEP 2", I will use a two-steps approach to handle missing data.
# 1. Remove columns with a significant number of missing observations (eg: Wind Chill)
# 2. Remove additional data points with missing data (eg: remove the 93 data points with missing data for "Sunrise Sunset"

# In[ ]:

## Remove columns with high number of missing obersations
data = raw_data.drop(['TMC','End_Lat', 'End_Lng','Number','Wind_Chill(F)','Weather_Timestamp',
                 'Airport_Code','Temperature(F)','Humidity(%)', 'Pressure(in)',
                 'Visibility(mi)','Wind_Direction','Wind_Speed(mph)',
                  'Precipitation(in)','Weather_Condition','Turning_Loop'], axis = 1)
## Remove additional data points with missing data
data = data.dropna()


# In[ ]:

## Rank states by number of accidents
## Merge with number of people by state
## Create new variable: number of incidents / population
## Note: I am using the population for 2020, there are some small variations for 
population = pd.read_csv("state_population.csv")
abbreviation = pd.read_csv('state_abbreviation.csv')
combined_data = abbreviation.merge(population, left_on='State', right_on='State')[['Code','Pop']]
enriched_data = combined_data.merge(data, left_on='Code', right_on='State')

## Check that the number of rows in the dataset "Data" and "Enriched_Data" is the same
print data.shape
print enriched_data.shape

## Calculate number of accidents per 1000 population
ratio =(enriched_data.groupby(['State'])['ID'].count()/enriched_data.groupby(['State'])['Pop'].mean())*1000
average_ratio = ratio.mean()
print 'average ratio is',average_ratio, 'accidents per 1000'


# In[ ]:

ratio.sort_values(ascending=False)


# In[ ]:

## Extract the day of the week to analyze weekdays >< weekends
import datetime
data['Start_Time'] = pd.to_datetime(data['Start_Time'])
data['day_of_week'] = data['Start_Time'].dt.dayofweek
data['day_of_week_text'] = data['day_of_week'].map({0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',
                                                   4:'Friday',5:'Saturday',6:'Sunday'})
data['day_of_week_text'].value_counts()


# In[ ]:

## Analyze correlation
## Select a subset of the dataset. Excluded features providing less information. 
## Eg: "Traffic_Calming" with less than 0.05% of value "True"
correlation_dataset = data[['Start_Time','Distance(mi)','State','County','Amenity','Sunrise_Sunset',
                       'day_of_week','Bump','Crossing','Junction','Traffic_Signal']]

corr = correlation_dataset.corr()
corr.style.background_gradient(cmap='coolwarm').set_precision(2)


# Correlation are extremely low. The only features that seem to generate correlation are traffic signal, crossing, amenity

# In[ ]:

data.plot(kind='scatter',x='Start_Lng',y='Start_Lat',alpha=0.01)
plt.show()


# In[ ]:

fig, ax = plt.subplots(figsize=(12,8))
#fig.set_facecolor('lightgrey') #changes color around the plot area
#fig.set_axis_bgcolor('lightgrey')
data.groupby('State').size().plot(kind = 'bar', 
                                 colormap='Spectral')
plt.show()


# In[ ]:




# In[ ]:



