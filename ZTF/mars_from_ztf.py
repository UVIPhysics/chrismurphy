'''
Christopher Murphy
3rd Year Physics major
'''


import requests
from datetime import date, datetime, timedelta
import argparse


# (user friendly) command line interfaces
parser = argparse.ArgumentParser(description='Download transient candidates from MARS',
								 epilog='Use -h for help')
#Start Date, default = Yesterday
parser.add_argument("-s", 
                    "--startdate", 
                    help="The Start Date - format YYYY-MM-DD ", 
                    required=False)


#End Date, Default = Today's date
parser.add_argument("-e", 
                    "--enddate", 
                    help="The End Date - format YYYY-MM-DD ", 
                    required=False)


#RB value, Default = .9
parser.add_argument("-rb", 
                    "--realbogus", 
                    help="The real bogus threshold - format: .NN ", 
                    required=False)

start_end_rb = vars(parser.parse_args()) # Pupose of the vars is to change a Namespace object to a dictionary object
print(start_end_rb)



# We will be observing the most interesting transients discovered by ZTF that occured over the last 24 hours
# For that we need to input todays and yesterdays date into MARS API
today = datetime.utcnow()
print(today)
timeOffSet = timedelta(hours = 4) #Differnce between UTC and AST
today = today - timeOffSet #I did this so today will still be today even if u run the code after 8pm
day_change = timedelta(days = 1)
yesterday = today - day_change

today = str(today)

#Time_lt default value = Today (relative to day you run the code)
startdate = today.split(' ')[0]

#today minus one day
yesterday = str(yesterday)

#Time_gt default value = Yesterday (relative to day you run the code)
enddate = yesterday.split(' ')[0]


#Real-bogus default threshold
rb = .90




#If the optional argparse commands WERE NOT implemented, use the default API inputs
#If the optional arparse commands WERE implemented, change the values of the API inputs
if start_end_rb['startdate'] is not None:
	startdate = start_end_rb['startdate']

if start_end_rb['enddate'] is not None:
	enddate = start_end_rb['enddate']

if start_end_rb['realbogus'] is not None:
	rb = start_end_rb['realbogus']




print(startdate, enddate)




#Parameters to input into API request
params = (
    ('sort_value', 'jd'), 
    ('sort_order', 'desc'), #Sort the jd in descending order (most recent comes first)
    ('time__gt', startdate), 
    ('time__lt', enddate),
    ('rb__gte', rb), #0 rb = bogus, 1 rb = real 
    ('format', 'json'), 
)



response = requests.get('https://mars.lco.global/', params=params)


#print(response.content)


#Naming convention of file
json_downloaded_file = today + '_ztf_interesting_candidates.txt'

#write the results of our query to a filename
file = open(json_downloaded_file, 'w+') 
file.write(response.content) 
file.close















