import requests
from datetime import date, datetime, timedelta

# We will be observing the most interesting transients discovered by ZTF that occured over the last 24 hours
# For that we need to input todays and yesterdays date into MARS API
today = datetime.utcnow()
day_change = timedelta(days = 1)
yesterday = today - day_change

today = str(today)
today = today.split(' ')[0]
yesterday = str(yesterday)
yesterday = yesterday.split(' ')[0]




params = (
    ('sort_value', 'jd'), 
    ('sort_order', 'desc'), #Sort the jd in descending order (most recent comes first)
    ('time__gt', yesterday), 
    ('time__lt', today),
    ('rb__gte', '.95'), #0 rb = bogus, 1 rb = real 
    ('format', 'json'), 
)


response = requests.get('https://mars.lco.global/', params=params)




#Naming convention of file
json_downloaded_file = today + '_ztf_interesting_candidates.txt'

#write the results of our query to a filename
file = open(json_downloaded_file, 'w+') 
file.write(response.content) 
file.close















