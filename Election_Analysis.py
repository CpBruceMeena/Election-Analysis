from __future__ import division  #this line should always be written at the top
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set_style('whitegrid')

#Use to grab the data from the web
import requests

from io import StringIO

#This is the data from the website in the form of csv
url = 'https://elections.huffingtonpost.com/pollster/2012-general-election-romney-vs-obama.csv'

source = requests.get(url).text

poll_data = StringIO(source)

poll_df = pd.read_csv(poll_data)
#print(poll_df.head())
#print(poll_df.info())

#We are using the subplot to plot two plots in one window
fig, ax = plt.subplots(1, 2)
sns.countplot('Affiliation', data = poll_df, ax = ax[0])

sns.countplot('Affiliation', data = poll_df, ax = ax[1], hue = 'Population')

fig.show()

avg = pd.DataFrame(poll_df.mean())
print(avg.head())

avg.drop('Number of Observations', axis = 0, inplace = True) 

std = pd.DataFrame(poll_df.std())
std.drop('Number of Observations', axis = 0, inplace = True) 

avg.plot(yerr = std, kind = 'bar', legend = False)

#We are concatening the list in one data frame
poll_avg = pd.concat([avg, std], axis = 1)
print(poll_avg)
poll_avg.columns = ['Average', 'STD']
print(poll_avg)

#poll_df.plot(x = 'End Date', y = ['Obama', 'Romney', 'Undecided'], linestyle = '', marker = 'o')

from datetime import datetime

poll_df['Difference'] = (poll_df.Obama - poll_df.Romney)/100

poll_df = poll_df.groupby(['Start Date'], as_index = False).mean()
print(poll_df.head())

#poll_df.plot('Start Date', 'Difference', figsize = (12, 4), marker = 'o', linestyle = '-', color = 'red')

row_in = 0
xlimit = []

#We are trying to figure the month of october in the list using the for loop and if loop
# and we are storing the index of the values at which the octoober start and when it ends
for date in poll_df['Start Date']:
    if date[0:7] == '2012-10':
        xlimit.append(row_in)
        row_in += 1
    else:
        row_in +=1

print(min(xlimit))
print(max(xlimit))
'''
#We are plotting for the month of october    
poll_df.plot('Start Date', 'Difference', figsize = (12, 4), marker = 'o', linestyle = '-', color = 'red', xlim = (329, 356))

#October 3
plt.axvline(x = 329 + 2, linewidth = 4, color = 'green')

#October 11
plt.axvline(x = 329 + 10, linewidth = 4, color = 'green')

#October 22nd
plt.axvline(x = 329 + 21, linewidth = 4, color = 'green')
'''
#NOW we are looking forward towards the donor set
donor_df = pd.read_csv('C://Users//LENOVO IDEAPAD 320//OneDrive//Desktop//Election_Donor_Data.csv')

#Counting the how much amount is donated by how much people
donor_df['contb_receipt_amt'].value_counts()
don_mean = donor_df['contb_receipt_amt'].mean()
don_std = donor_df['contb_receipt_amt'].std()

print("The averge donation was %.2f with a std %.2f" % (don_mean, don_std))

#Data frame does not allow sort, we need to use sort_values or sort_index to sort
top_donor = donor_df['contb_receipt_amt'].copy()
top_donor.sort_values()
top_donor = top_donor[top_donor > 0]
top_donor.sort_values()

print(top_donor.value_counts().head(10))

com_don = top_donor[top_donor < 2500]
#com_don.hist(bins = 100)

candidate = donor_df.cand_nm.unique()

party_map = {'Bachmann, Michelle': 'Republican',
             'Cain, Herman' : 'Republican',
             ' Gingrich, Newt': 'Republican',
             ' Huntsman, Jon' : 'Republican',
             ' Johnson, Gary Earl' : 'Republican',
             ' McCotter, Thaddeus G' : 'Republican',
             ' Obama, Barrach' : 'Democrat',
             ' Paul, Ron ' : 'Republican',
             ' Pawlenty, Timothy' : 'Republican',
             ' Perry, Rick' : 'Republican',
             "Roemer , carles E. 'Buddy' III" : 'Republican',
             ' Romney, Mitt'  : 'Republican', 
             ' Santoru, Rick' : 'Republican'}

donor_df['Party'] = donor_df.cand_nm.map(party_map)
print(donor_df.head())
donor_df = donor_df[donor_df.contb_receipt_amt > 0]
donor_df.groupby('cand_nm')['contb_receipt_amt'].count()
donor_df.groupby('cand_nm')['contb_receipt_amt'].sum()

cand_amount = donor_df.groupby('cand_nm')['contb_receipt_amt'].sum()

i = 0
for don in cand_amount:
    print('the candidate %s raise %.0f dollars ' %(cand_amount.index[i], don))
    
    print('\n')
    i+=1
    
cand_amount.plot(kind = 'bar')
donor_df.groupby('Party')['contb_receipt_amt'].sum().plot(kind = 'bar')

occupation_df = donor_df.pivot_table('contb_receipt_amt', index = 'contbr_occupation',
                                     columns = 'Party',
                                     aggfunc = 'sum')

occupation_df = occupation_df[occupation_df.sum(1) > 1000000]
occupation_df.plot(kind = 'bar')
