#Monthly intervals are calculated by calendar week to account for year changes and month length differences
#2 month: 52/6 = 8.667 ~~ 9 weeks
#4 month: 52/3 = 17.333 ~~ 17 weeks
#12 month: 52/1 = 52 weeks

import os
from datetime import date, timedelta
import pandas as pd
from typing import List, Tuple

#def establish_dates():
#Establish today and end of week, Friday
today = date.today() #This runs on a monday
friday = date.today() + timedelta(days=4) #So friday is 4 days ahead
friday_str = friday.strftime("%Y-%m-%d")

#Calculate the weeks since a job was performed
def weeks_since(wk,yr,today):
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
            if (f'@{vehicle}' in row.split()) and (f'#{ID}' in row.split()):
                return True
        return False
    

#Add a task to todo.txt
#Need to complete this function. tracker.csv change lets me use dot notation
def add_bundle(vehicle,bundle):
    
    with open('todo.txt','a') as todo:
        
        todo.seek(0,2) #Move to the new empty line at the end of the file
        
        friday_str = friday.strftime("%Y-%m-%d")
        
        schedule = pd.read_csv('schedule.csv')
        
        for row in range(len(schedule)):
            if schedule.bundle[row] == bundle and not task_exists(schedule._id[row],vehicle):        
                job = schedule.job_eng[row]
                _id = schedule._id[row]
                bundle = schedule.bundle[row]
                todo.write(f"{job} @{vehicle} due:{friday_str} #{_id} %{bundle}")
                todo.write("\n")

def find_active_bundles():
    #Identify which vehicles already have bundles under work
    with open('todo.txt') as todo:
        active_bundles = []
        for row in todo:
            vehicle = next((word.strip('@') for word in row.split() if word.startswith('@')),None)
            bundle = next((word.strip('%') for word in row.split() if word.startswith('%')),None)
            active_bundles.append((vehicle,bundle))
        #Eliminate duplicates from active_bundles
        active_bundles = list(set(active_bundles))
        return(active_bundles)
    

def schedule_tasks(active_bundles: List) -> List[Tuple[str, str]]:

#Inputs
#today: A datetime.date object with the date the script is run
#active_bundles: A list of tuples for all bundles active for each vehicle. For example:
    #[('f250','_2month'),('whitetacoma','_12month'),('whitetacoma,'_4month')]

#Output: An updated list of active bundles. This function also writes to todo.txt

    tracker = pd.read_csv('tracker.csv')
    
    vehicles = [x for x in list(tracker.columns) if x != 'bundle']
    
    #Main loop--check what is due and add to todo.txt
    for vehicle in vehicles:
        
        for row in range(len(tracker)):
            
            if tracker.bundle[row] == '_2month':
                lastwk = tracker[vehicle][row]
                if pd.isna(lastwk):
                    continue
                wk,yr = lastwk.split('-')
                if weeks_since(int(wk),int(yr),today) >= 9 and (vehicle,'_2month') not in active_bundles:
                    add_bundle(vehicle,'_2month')
                    active_bundles.append((vehicle,'_2month'))
                    
            if tracker.bundle[row] == '_4month':
                lastwk = tracker[vehicle][row]
                if pd.isna(lastwk):
                    continue
                wk,yr = lastwk.split('-')
                if weeks_since(int(wk),int(yr),today) >= 17 and (vehicle,'_4month') not in active_bundles:
                    add_bundle(vehicle,'_4month')
                    active_bundles.append((vehicle,'_4month'))
                    
            if tracker.bundle[row] == '_12month':
                lastwk = tracker[vehicle][row]
                if pd.isna(lastwk):
                    continue
                wk,yr = lastwk.split('-')
                if weeks_since(int(wk),int(yr),today) >= 52 and (vehicle,'_12month') not in active_bundles:
                    add_bundle(vehicle,'_12month')
                    active_bundles.append((vehicle,'_12month'))
                    
            if tracker.bundle[row] == '_shop4month':
                lastwk = tracker[vehicle][row]
                if pd.isna(lastwk):
                    continue
                wk,yr = lastwk.split('-')
                if weeks_since(int(wk),int(yr),today) >= 17 and (vehicle,'_shop4month') not in active_bundles:
                    add_bundle(vehicle,'_shop4month')
                    active_bundles.append((vehicle,'_shop4month'))
                    
    return(active_bundles)

def write_active_bundles(active_bundles: List[Tuple[str,str]]):
    #Write active bundles to active.txt
    with open('active.txt','w') as active:
        active.truncate(0)
        for vehicle, bundle in active_bundles:
            active.write(f"{vehicle},{bundle}")
            active.write('\n')