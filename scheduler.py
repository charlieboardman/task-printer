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

_2mo_ID_col = 1
_4mo_ID_col = 4
_12mo_ID_col = 7
_4mo_shop_ID_col = 10

_2mo_job_col = 0
_4mo_job_col = 3
_12mo_job_col = 6
_4mo_shop_job_col = 9

#Establish today
today = date.today()

#Calculate the weeks since a job was performed
def weekssince(wk,yr,today):
    if yr == today.year:
        return today.isocalendar().week - wk
    if yr == today.year - 1:
        return (52-wk) + today.isocalendar().week
    else:
        return (52-wk) + 52*(today.year - yr)


#Check if a task already exists in todo.txt for a specific vehicle
def task_exists(ID,vehicle):
    with open('todo.txt','r') as todo:
        for row in todo:
            if f'@{vehicle}' and f'#{ID}' in row.split():
                return True
        return False
    

#Add a task to todo.txt
#Need to complete this function. tracker.csv change lets me use dot notation
def add_task(ID,vehicle,tracker_df):
    
    for 
    
    with open('todo.txt','a') as todo:
        todo.write(f"{job} @black4runner due:2016-07-30 #3")       
    

vehicles_tracking = os.path.join(os.getcwd(),'vehicles_tracking')

for d in os.listdir(vehicles_tracking):
    
    #Open the tracker by vehicle
    #header=1 means 2nd row (0 indexing) is header, so data starts on third row
    tracker_df = pd.read_csv(os.path.join(vehicles_tracking,d,'tracker.csv'),header=1)
    
    for row in range(len(tracker_df)):
        
        #check 2month
        wk,yr = tracker_df.iloc[row,_2mo_lastwk_col].split('-')
        if weekssince(int(wk),int(yr),today) >= 9 and not task_exists(ID):
            add_task(ID) #Need to create this function