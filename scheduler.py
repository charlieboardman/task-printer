#Monthly intervals are calculated by calendar week to account for year changes and month length differences
#2 month: 52/6 = 8.667 ~~ 9 weeks
#4 month: 52/3 = 17.333 ~~ 17 weeks
#12 month: 52/1 = 52 weeks

import os
from datetime import date, timedelta
import pandas as pd
import csv

#Establish the values for columns (0-indexed)
_2mo_lastwk_col = 2
_4mo_lastwk_col = 5
_12mo_lastwk_col = 8
_4mo_shop_lastwk_col = 11

#Establish today
today = date.today()

#Create a function to calculate the weeks since a job was performed
def weekssince(wk,yr,today):
    if yr == today.year:
        return today.isocalendar().week - wk
    if yr == today.year - 1:
        return (52-wk) + today.isocalendar().week

vehicles_tracking = os.path.join(os.getcwd(),'vehicles_tracking')

for d in os.listdir(vehicles_tracking):
    
    #Open the tracker by vehicle
    #header=1 means 2nd row (0 indexing) is header, so data starts on third row
    tracker_df = pd.read_csv(os.path.join(vehicles_tracking,d,'tracker.csv'),header=1)
    
    for row in range(len(tracker_df)):
        
        #check 2month
        lastwk = tracker_df.iloc[row,_2mo_lastwk_col]