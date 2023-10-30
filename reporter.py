#Read the todo.txt list and see which vehicles have tasks

import pandas as pd
from datetime import date, timedelta

#Need to switch this to schedule.csv to track jobs
schedule = pd.read_csv('schedule.csv')

#Date reporter is run
completed_date = date.today().strftime('%d-%b-%Y')

with open('todo.txt','r+') as todo:
    
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
            
    completed = [] #Init completed tasks
    
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
            completed.append((vehicle,ans))
            
        #Write the completed tasks to their history files
        with open(f'./vehicles_tracking/{vehicle[1::]}/history.txt','a') as history:
            todo.seek(0)
            for line in todo:
                if line == '\n' or line == '':
                    continue
                _id = int(next(word.strip('#') for word in line.split() if word.startswith('#')))
                if (vehicle,_id) in completed:
                    history.write(line.strip('\n') + f' completed:{completed_date}\n')
                
     
    todo.truncate(0)
    todo.seek(0)
    
    #Rewrite the remaining lines onto todo.txt, leaving out the completed tasks
    for line in lines:
        vehicle = next(word for word in line.split() if word.startswith('@'))
        _id = int(next(word.strip('#') for word in line.split() if word.startswith('#')))
        if (vehicle,_id) not in completed:
            todo.write(line)
            