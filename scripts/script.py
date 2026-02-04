## for  setting  up the environment 
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio


import warnings 
warnings.filterwarnings("ignore")



sns.set_style("whitegrid")
pio.renderers.default = 'svg'
%matplotlib inline


!pip install -U kaleido
!pip install --upgrade plotly

!sudo apt update 
!sudo apt-get install -y libnss3 libatk-bridge2.0-0 libcups2 libxcomposite libxdamage1 libxfixes3 libcrandr2 libgbm1
!plotly_get_chrome

## For reading excel file
!pip install xlrd


## Basic analysis and Transformation
df1 = pd.read_csv('/content/hotel_bookings 2.xls')

df1.head()

df.info()

df1['reservation_status_date'] = pd.to_datetime(df1['reservation_status_date'],dayfirst=True)

df1.describe(include="object")

for col in df1.describe(include="object"):
    print(col)
    print(df[col].unique())
    print('-'*50)

df1.isnull().sum()

df1.drop(['company','agent'], axis = 1 , inplace = True)

df1.dropna(inplace = True)

## For visualisation

plt.figure(figsize=(5,5))
plt.title('Reservation Status Count')
plt.bar(['Not_Cancelled', 'Cancelled'],df1['is_canceled'].value_counts(), edgecolor = 'k', width = 0.7, color = 'teal')
plt.show()

---------------------------------------------------------------------------------

plt.figure(figsize = (8,5))
ax1 = sns.countplot(x ='hotel', hue = 'is_canceled', data = df1, palette = 'Blues')
legend_labels_ = ax1. get_legend_handles_labels()
plt.title('Reservation status of different Hotels', size = 20)
plt.xlabel('hotel')
plt.ylabel('number of reservations')
plt.legend(['not_cancelled', 'cancelled'])
plt.show()

---------------------------------------------------------------------------------

plt.figure(figsize = (22,8))
plt.title('AvG Daily Rate In City and Resort Hotel', fontsize = 30)
plt.plot(Resort_Hotel.index, Resort_Hotel['adr'], label = 'Resort_Hotel')
plt.plot(City_Hotel.index, City_Hotel['adr'], label = 'City_Hotel')
plt.legend(fontsize = 20 )
plt.show()

-------------------------------------------------------------------------------

df1['month'] = df1['reservation_status_date'].dt.month
plt.figure(figsize = (20,10))
ax1 = sns.countplot(x = 'month', hue = 'is_canceled' , data = df1, palette = 'viridis')
legend_labels_ = ax1. get_legend_handles_labels()
plt.title('Reservation Status per Month', size = 20)
plt.xlabel('month')
plt.ylabel('No. of Reservations')
plt.legend(['Not Cancelled', 'cancelled'])
plt.show()


--------------------------------------------------------------------------------

monthly_data = df1.groupby('month')['is_canceled'].value_counts().unstack().fillna(0)

if 0 not in monthly_data.columns:
    monthly_data[0] = 0
if 1 not in monthly_data.columns:
    monthly_data[1] = 0
monthly_data = monthly_data.sort_index()
monthly_data['total'] = monthly_data[0] + monthly_data[1]
x = np.arange(len(monthly_data.index))
width = 0.25
plt.figure(figsize=(20,10))
plt.bar(x - width, monthly_data[0], width=width, label='Not Cancelled')
plt.bar(x, monthly_data[1], width=width, label='Cancelled')
plt.bar(x + width, monthly_data['total'], width=width, label='Total')
plt.xticks(x, monthly_data.index)
plt.title('Reservation Status per Month', size=20)
plt.xlabel('Month', fontsize = 15)
plt.ylabel('No. of Reservations', fontsize = 15)
plt.legend()

plt.show()


## for heat map

df1['price_range'] = pd.qcut(df1['adr'], 4, labels=['Low','Medium','High','Very High'])

heat_data = df1.groupby(['month','price_range'])['is_canceled'].mean().unstack()

plt.figure(figsize=(12,6))
sns.heatmap(heat_data, annot=True, fmt=".2f", cmap="YlGnBu")

plt.title('Cancellation Rate by Month and Price Range')
plt.ylabel('Month')
plt.xlabel('Price Range')
plt.show()



## for pie chart

cancelled_df = df1[df1['is_canceled'] == 1]
country_cancel = cancelled_df['country'].value_counts().head(5)

plt.figure(figsize=(8,10))
plt.pie(country_cancel, 
        labels=country_cancel.index, 
        autopct='%1.1f%%',
        startangle=140)

plt.title('Top 5 Countries by Cancellations')
plt.show()


## some transformations and ADR visualisation

filtered_df = df1[
    (df1['reservation_status_date'] >= '2016-01-01') &
    (df1['reservation_status_date'] <= '2017-09-30')
].copy()


filtered_df['year_month'] = filtered_df['reservation_status_date'].dt.to_period('M')


--------------------------------------------------------------------------

adr_not_cancelled = (
    filtered_df[filtered_df['is_canceled'] == 0]
    .groupby('year_month')['adr']
    .mean()
)

adr_cancelled = (
    filtered_df[filtered_df['is_canceled'] == 1]
    .groupby('year_month')['adr']
    .mean()
)


---------------------------------------------------------------------------

adr_not_cancelled.index = adr_not_cancelled.index.to_timestamp()
adr_cancelled.index = adr_cancelled.index.to_timestamp()

combined = pd.concat([adr_not_cancelled, adr_cancelled], axis=1)
combined.columns = ['Not Cancelled', 'Cancelled']
combined = combined.sort_index()


---------------------------------------------------------------------------

plt.figure(figsize=(14,6))

plt.plot(combined.index, combined['Not Cancelled'], marker='o', label='Not Cancelled')
plt.plot(combined.index, combined['Cancelled'], marker='o', label='Cancelled')

plt.xlabel('Year-Month', fontsize = 15)
plt.ylabel('Average ADR', fontsize = 13)
plt.title('ADR Trend (Jan 2016 - Sept 2017)', fontsize = 20)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()




