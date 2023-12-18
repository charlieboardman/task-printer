#TO DO:
#Add a dictionary to translate from @ vehicle names to readable names

import pandas as pd
import pdfkit
from datetime import date

#We need a function to identify if a word in the string is a date
def isdate(word):
    for char in word:
        if not (char.isnumeric() or char == '-' or char == '/'):
            return False
        return True


def render_list(today,*languages):

    #We need a task object with all the todo.txt information
    class task:
        def __init__(self,vehicle,job_eng,job_spa,_id,priority=None,due=None):
            self.vehicle = vehicle
            self.job_eng = job_eng
            self.job_spa = job_spa
            self._id = _id
            self.priority = priority
            self.due = due


#Read the todo.txt file into a structure that we can put down into html
    with open('todo.txt','r') as todo:
        
        #We will read the job descriptions off of schedule.csv
        schedule = pd.read_csv('schedule.csv',header=0)
        
        #This dictionary will hold all the tasks and group them by vehicle.
        #The vehicle name is the key, and a list of the task objects for that vehile is the value
        tasks_v = {}
        
        #We are going to go over every line of the todo file. In each line, we identify which vehicle the task pertains to and the details of the tasks
        for line in todo:
            
            #Pass over empty lines
            if line == '' or line == '\n':
                continue
            
            #Identify the vehicle
            vehicle = next((word.strip('@') for word in line.split() if word.startswith('@')),None)
            
            #Initialize the list where the tasks for that vehicle will go, if needed
            if vehicle not in tasks_v.keys():
                tasks_v[vehicle] = []
            
            #Identify the task ID
            _id = int(next((word.strip('#') for word in line.split() if word.startswith('#'))))
            
            #Get the job description from schedule.csv, based on ID (which is also row index)
            if 'english' in languages:
                job_eng = schedule.job_eng[_id]
            else:
                job_eng = ''
            if 'spanish' in languages:
                job_spa = schedule.job_spa[_id]
            else:
                job_spa = ''
            
            #Identify the task description from the normal words in the line
            #desclist = [word for word in line.split() if not any([isdate(word),word.startswith(( '@', 'due:', '(', '#', '%'))])]
            #desc = ' '.join(desclist)
            
            #Identify priority because it starts with (
            #priority = next((word for word in line.split() if word.startswith('(')))
            
            #Identify the due date
            due_str = next((word for word in line.split() if word.startswith('due:')))[4::]
            year,month,day = [int(x) for x in due_str.split('-')]
            due = date(year,month,day)
            due_fmt = due.strftime('%d-%b-%Y')
            
            
            
            #Put all that into the list of tasks for each vehicle
            tasks_v[vehicle].append(task(vehicle,job_eng,job_spa,_id,due_fmt))
            
    #Now actually create the html

    header = f"Tasks for week of {today.strftime('%B')} {today.day}"
    html = f"<html><h1>{header}</h1>"

    head = """<head>
      <style>
        [data-prefix^='h'] {
          margin-top: 10;
          margin-bottom: 10;
        }
        
        p {
          margin-top: 5px;
          margin-bottom: 5px;
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
        task_number = 1
        for task in tasks_v[vehicle]:
            html += f"""
                    <p style="display: flex; align-items: center;">
                    <input type='checkbox' id='{vehicle}{task_number}' style="margin-right: 10px;">
                    <label for='{vehicle}{task_number}'>"""
                    
            for language in languages:
                if language == 'english':
                    html += f'{task.job_eng}<br>'
                if language == 'spanish':
                    html += f'{task.job_spa}<br>'
                
            html += f"</label><span style='margin-left: 10px;'>(#{task._id})</span></p>"
            task_number += 1

    html_closer = "</body></html>"
    html += html_closer

    pdfkit.from_string(html,'rendered.pdf')
    return(html)

#print(html)
