#Read the todo.txt list and see which vehicles have tasks

import pandas as pd

#Need to switch this to schedule.csv to track jobs
tracker = pd.read_csv('tracker.csv')

with open('todo.txt','r') as todo:
    vehicles = []
    
    for line in todo:
        
        if line == '' or line == '\n':
            continue
        
        #Identify the vehicle
        vehicle = next((word for word in line.split() if word.startswith('@')),None)
        
        #Initialize the list where the tasks for that vehicle will go, if needed
        if vehicle not in vehicles:
            vehicles.append(vehicle)
            
    todo.seek(0) #Reset the pointer
    
    for vehicle in vehicles:
        print(f"Reporting {vehicle} task completion:\n")

        #This loop needs to be rewritten to deal with the new tracker.csv and schedule.csv
        for line in todo:
            if f"{vehicle}" in line:
                ID = next(x[1:] for x in line.split() if x.startswith("#"))
                print(f"{tracker.job[int(ID)]}: {tracker._id[int(ID)]}")
        print('\n')
        
        ans = 0
        print('Enter completed task IDs. When finished, input x.')
        completed = []
        while ans != 'x':
            ans = int(input('Input ID and press enter: '))
            if ans == 'x':
                break
            completed.append(ans)
            