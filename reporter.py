#Read the todo.txt list and see which vehicles have tasks

import pandas as pd
from datetime import date, timedelta

#Need to switch this to schedule.csv to track jobs
schedule = pd.read_csv('schedule.csv')

#Date reporter is run
completed_date = date.today().strftime('%d-%b-%Y')

with open('todo.txt','r+') as todo:

    #Identify which bundles are active before beginning
    #This will be used later to compare against active bundles once tasks are reported
    active_bundles_before = []
    for row in todo:
        vehicle = next((word.strip('@') for word in row.split() if word.startswith('@')),None)
        bundle = next((word.strip('%') for word in row.split() if word.startswith('%')),None)
        active_bundles_before.append((vehicle,bundle))
        
    active_bundles_before = list(set(active_bundles_before))
        
    todo.seek(0)

    lines = [line for line in todo.readlines() if line != '\n']
    
    todo.seek(0)
    
    vehicles = []
    
    for line in todo:
        
        if line == '' or line == '\n':
            continue
        
        #Identify the vehicle
        vehicle = next((word for word in line.split() if word.startswith('@')),None)
        
        #Initialize the list where the tasks for that vehicle will go, if needed
        if vehicle not in vehicles:
            vehicles.append(vehicle)
            
    completed_tasks = [] #Init completed tasks
    
    for vehicle in vehicles:
        print(f"Reporting {vehicle} task completion:\n")
        
        todo.seek(0) #Reset the pointer

        #This loop needs to be rewritten to deal with the new tracker.csv and schedule.csv
        for line in todo:
            if f"{vehicle}" in line:
                _id = next(x[1:] for x in line.split() if x.startswith("#"))
                print(f"{schedule.job[int(_id)]}: {schedule._id[int(_id)]}")
        print('\n')
        
        ans = 0
        print('Enter completed task IDs. When finished, input x.')
        
        while ans != 'x':
            ans = input('Input ID and press enter: ')
            if ans == 'x':
                break
            ans = int(ans)
            completed_tasks.append((vehicle,ans))
            
        #Write the completed tasks to their history files
        with open(f'./vehicles_tracking/{vehicle[1::]}/history.txt','a') as history:
            todo.seek(0)
            for line in todo:
                if line == '\n' or line == '':
                    continue
                _id = int(next(word.strip('#') for word in line.split() if word.startswith('#')))
                if (vehicle,_id) in completed_tasks:
                    history.write(line.strip('\n') + f' completed:{completed_date}\n')
                
     
    todo.truncate(0)
    todo.seek(0)
    
    #Rewrite the remaining lines onto todo.txt, leaving out the completed tasks
    for line in lines:
        vehicle = next(word for word in line.split() if word.startswith('@'))
        _id = int(next(word.strip('#') for word in line.split() if word.startswith('#')))
        if (vehicle,_id) not in completed_tasks:
            todo.write(line)
            
    #Compare remaining tasks on todo.txt with active.txt to see which bundles have completed
    todo.seek(0)
    active_bundles_after = []
    for row in todo:
        vehicle = next((word.strip('@') for word in row.split() if word.startswith('@')),None)
        bundle = next((word.strip('%') for word in row.split() if word.startswith('%')),None)
        active_bundles_after.append((vehicle,bundle))
    
    active_bundles_after = list(set(active_bundles_after))
    
    completed_bundles = [bundle for bundle in active_bundles_before if bundle not in active_bundles_after]
    
#Update the tracker
for vehicle,bundle in completed_bundles:
    with open(f'./vehicles_tracking/{vehicle}/tracker.csv','r+') as tracker:
        rows = tracker.readlines()
        for n,row in enumerate(rows):
            if bundle in row.split(','):
                rows[n] = f'{bundle},{date.today().isocalendar().week}-{date.today().year}\n'
        tracker.truncate(0)
        tracker.seek(0)
        for row in rows:
            tracker.write(row)

#Update active.txt
with open('active.txt','r+') as active:
    
    lines = active.readlines()
    for n,line in enumerate(lines):
        if line == '\n' or line == '':
            continue
        vehicle = line.split(',')[0]
        bundle = line.split(',')[1].strip('\n')
        
        if (vehicle,bundle) in completed_bundles:
            lines.pop(n)
    
    active.truncate(0)
    active.seek(0)
    
    for line in lines:
        active.write(line)

