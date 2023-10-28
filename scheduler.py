#Monthly intervals are calculated by calendar week to account for year changes and month length differences
#2 month: 52/6 = 8.667 ~~ 9 weeks
#4 month: 52/3 = 17.333 ~~ 17 weeks
#12 month: 52/1 = 52 weeks

import os
from datetime import date, timedelta
import pandas as pd

#Establish today
today = date.today() #This runs on a monday
friday = date.today() + timedelta(days=4) #So friday is 4 days ahead
friday_str = friday.strftime("%m-%d-%Y")

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
def add_bundle(bundle,vehicle):
    
    with open('todo.txt','a') as todo:
        
        schedule = pd.read_csv('schedule.csv')
        
        for row in range(len(schedule)):
            if schedule.bundle[row] == bundle and not task_exists(schedule._id[row],vehicle):        
                job = schedule.job[row]
                _id = schedule._id[row]
                todo.write("\n")
                todo.write(f"{job} @{vehicle} due:{friday_str} #{_id}")       
        
vehicles_tracking = os.path.join(os.getcwd(),'vehicles_tracking')

for _dir in os.listdir(vehicles_tracking):
    
    #Open the tracker by vehicle
    tracker = pd.read_csv(os.path.join(vehicles_tracking,_dir,'tracker.csv'),header=0)
    
    for row in range(len(tracker)):
        
        if tracker.bundle[row] == '_2month':
            wk,yr = tracker.lastwk[row].split('-')
            if weekssince(int(wk),int(yr),today) >= 9:
                add_bundle('_2month',_dir)
                
        if tracker.bundle[row] == '_4month':
            wk,yr = tracker.lastwk[row].split('-')
            if weekssince(int(wk),int(yr),today) >= 17:
                add_bundle('_4month',_dir)
                
        if tracker.bundle[row] == '_12month':
            wk,yr = tracker.lastwk[row].split('-')
            if weekssince(int(wk),int(yr),today) >= 52:
                add_bundle('_12month',_dir)
                
        if tracker.bundle[row] == '_shop4month':
            wk,yr = tracker.lastwk[row].split('-')
            if weekssince(int(wk),int(yr),today) >= 17:
                add_bundle('_shop4month',_dir)
        