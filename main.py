import scheduler
import renderer
import cups
from datetime import date, timedelta

today = date.today()
today_str = today.strftime('%d-%b-%Y')

#Read todo.txt to list active bundles
active_bundles = scheduler.find_active_bundles()

#Update the todo.txt list with jobs that are due
scheduler.schedule_tasks(active_bundles,today)

#Write active bundles to active.txt
scheduler.write_active_bundles(active_bundles)

#Render the list
html = renderer.render_list(today,'english')

#Print the rendered list
conn = cups.Connection()
printers = conn.getPrinters()
printer_name = list(printers.keys())[0]
#conn.printFile(printer_name, 'rendered.pdf', f'Tasks list: {today_str}', {})
