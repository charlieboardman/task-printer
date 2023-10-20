#TO DO:
#Add a dictionary to translate from @ vehicle names to readable names

import pdfkit
from datetime import date

#We need a function to identify if a word in the string is a date
def isdate(word):
    for char in word:
        if not (char.isnumeric() or char == '-' or char == '/'):
            return False
        return True
    
#We need a task object with all the todo.txt information
class task:
    def __init__(self,vehicle,desc,id_,priority=None,due=None):
        self.vehicle = vehicle
        self.desc = desc
        self.id_ = id_
        self.priority = priority
        self.due = due

#Read the todo.txt file into a structure that we can put down into html
with open('todo.txt','r') as todo:
    
    #This dictionary will hold all the tasks and group them by vehicle.
    #The vehicle name is the key, and a list of the task objects for that vehile is the value
    tasks_v = {}
    
    #We are going to go over every line of the todo file. In each line, we identify which vehicle the task pertains to and the details of the tasks
    for line in todo:
        
        #Identify the vehicle
        vehicle = next((word for word in line.split() if word.startswith('@')),None)
        
        #Initialize the list where the tasks for that vehicle will go, if needed
        if vehicle not in tasks_v.keys():
            tasks_v[vehicle] = []
            
        #Identify the task description from the normal words in the line
        desclist = [word for word in line.split() if not any([isdate(word),word.startswith(( '@', 'due:', '(', '#'))])]
        desc = ' '.join(desclist)
        
        #Identify priority because it starts with (
        priority = next((word for word in line.split() if word.startswith('(')))
        
        #Identify the due date
        due_str = next((word for word in line.split() if word.startswith('due:')))[4::]
        year,month,day = [int(x) for x in due_str.split('-')]
        due = date(year,month,day)
        
        #Identify the task ID
        id_ = next((word for word in line.split() if word.startswith('#')))
        
        #Put all that into the list of tasks for each vehicle
        tasks_v[vehicle].append(task(vehicle,desc,id_,priority,due))
        
#Now actually create the html

header = f"Tasks for week of {date.today().strftime('%B')} {date.today().day}"
html = f"<html><h1>{header}</h1>"

head = """<head>
  <style>
    [data-prefix^='h'] {
      margin-top: 10;
      margin-bottom: 10;
    }
    
    p {
      margin-top: 0;
      margin-bottom: 0;
      font-size: 24;
    }
    
    input[type='checkbox'] {
      margin-right: 10px;
    }
    
  </style>
</head>"""

html += head
html += "<body>"

#Task sections generator
h_num = 2 #Start with <h2> since we use <h1> for the main title header
for vehicle in tasks_v.keys():
    html += f"<p><h{h_num} data-prefix='h'>{vehicle}</h{h_num}>"
    tnum = 1
    for task in tasks_v[vehicle]:
        html += f"<p><input type='checkbox' id='{vehicle}{tnum}'><label for='{vehicle}{tnum}'>{task.desc} ({task.id_})</label></p>"
        tnum += 1

html_closer = "</body></html>"
html += html_closer

pdfkit.from_string(html,'rendered.pdf')

print(html)