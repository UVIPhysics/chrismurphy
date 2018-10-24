'''
Christopher Murphy
A. Cucchiara 
Download transient candidates given an upper and lower date, and a real bogus threshold
From downloaded transients, find which ones can be observed with VIRT, and which time is best to
observe the candidate
'''


import requests
from datetime import date, datetime, timedelta
import argparse
import json


# (user friendly) command line interfaces
parser = argparse.ArgumentParser(description='Download transient candidates from MARS',
                                 epilog='Use -h for help')

#Lower Date, default = Yesterday
parser.add_argument("-l", 
                    "--lower", 
                    help="Lower bound for date - format: YYYY-MM-DD - Default = Yesterday", 
                    required=False)


#Upper Date, Default = Today's date
parser.add_argument("-u", 
                    "--upper", 
                    help="Upper bound for date - format: YYYY-MM-DD - Default = Today", 
                    required=False)


#RB value, Default = .9
parser.add_argument("-rb", 
                    "--realbogus", 
                    help="The real bogus threshold (0 = bogus, 1 = real) - format: .NN ", 
                    required=False)


#Observing start time, Default = tonight 7pm AST 
parser.add_argument("-o", 
                    "--observingTime", 
                    help="The day and hour you will begin observing - format: YYYY-MM-DD-HH:MM:SS.sss - Default = Today 7pm", 
                    required=False)

start_end_rb = vars(parser.parse_args()) # Pupose of the vars is to change a Namespace object to a dictionary object
print(start_end_rb)





# We will be observing the most interesting transients discovered by ZTF that occured over the last 24 hours
# For that we need to input todays and yesterdays date into MARS API
today = datetime.utcnow()
print(today)
timeOffSet = timedelta(hours = 4) #Differnce between UTC and AST
today = today - timeOffSet #today will still be today even if u run the code after 8pm
day_change = timedelta(days = 1)
yesterday = today - day_change

today = str(today)

#Time_lt default value = Today (relative to day you run the code)
upper_date = today.split(' ')[0]

#today minus one day
yesterday = str(yesterday)

#Time_gt default value = Yesterday (relative to day you run the code)
lower_date = yesterday.split(' ')[0]


#Real-bogus default threshold
rb = .90

'''
Observing time default = Tonight 7pm
Today at 7 pm (ast) = 11pm UTC
Current strategy at Etelman is to observe from ~7-11 pm
'''
from astropy.time import Time
#print upper_date
today_7 = upper_date + 'T23:00:00'
#print today_7
observing_time = Time(today_7, format = 'isot', scale = 'utc') 
#print observing_time


'''
If the optional argparse commands WERE NOT implemented, use the default API inputs. Defaults
    Upper = today
    Lower = yesterday
    RB = .9
If the optional arparse commands WERE implemented, change the values of the API inputs to be the inputs

'''

if start_end_rb['lower'] is not None:
    lower_date = start_end_rb['lower']

if start_end_rb['upper'] is not None:
    upper_date = start_end_rb['upper']

if start_end_rb['realbogus'] is not None:
    rb = start_end_rb['realbogus']

if start_end_rb['observingTime'] is not None:
    observing_time = start_end_rb['observingTime']
    observing_time = Time(observing_time, format = 'isot', scale = 'utc') 

print("Observations begin: " + str(observing_time) + " UTC") 
print('\n')


print(upper_date, lower_date)

print observing_time


#Parameters to input into API request
params = (
    ('sort_value', 'jd'), 
    ('sort_order', 'desc'), #Sort the jd in descending order (most recent comes first)
    ('time__gt', lower_date), #Lower
    ('time__lt', upper_date), #Upper
    ('rb__gte', rb), #0 rb = bogus, 1 rb = real 
    ('format', 'json'), 
)



response = requests.get('https://mars.lco.global/', params=params)
#print(response.content)


#Naming convention of file
json_downloaded_file = lower_date + '-' + upper_date + '_ztf_interesting_candidates.txt'

#write the results of our query to a filename
file = open(json_downloaded_file, 'w+') 
file.write(response.content) 
file.close


'''
Pt 2:
Extract the RA, DEC, magnitude of every source in the json file
Find the RA 
'''

import pandas as pd
from astropy.coordinates import EarthLocation,SkyCoord
from astropy import units as u
from astropy.coordinates import AltAz
import matplotlib.pyplot as plt


#Set observing location to Etelman
observing_location = EarthLocation(lat='18.3381', lon='-64.8941', height=450*u.m) 

#Take in time, ra, dec-- convert to az and alt during given time
def az_alt(time, ra, dec):
    observing_time = Time(time)  
    aa = AltAz(location=observing_location, obstime=observing_time)
    coord = SkyCoord(ra*u.deg, dec*u.deg)
    aa = coord.transform_to(aa)
    az = "{0.az}".format(aa) 
    az_deg = az.split(' ')[0]
    alt = "{0.alt}".format(aa)
    alt_deg = alt.split(' ')[0]
    return az_deg, alt_deg






#Load the downloaded json content
file = json_downloaded_file
with open(file, 'r') as f:
    data = json.load(f)
results = data['results']

#Extract candidate information
candidates = {}
for i in results:
    candidates[i['objectId']] = i['candidate']


df = pd.DataFrame(candidates) #Columns and rows seem to be flipped in opposite way we want

#Transpose the table to make the table more readable
df_transposed = df.T

#Get these columns in case we need them later, NOTE: Much more columns are available than what we have rn
df1 = df_transposed[['filter','ra','dec','candid','magap','magpsf','distnr','classtar', 'rb']]


ra = df1['ra'].tolist()
dec = df1['dec'].tolist()
candid = df1['candid'].tolist()
#print ra, dec, candid
# print len(ra), len(dec), len(candid)
print(str(len(ra)) + " transient candidates above given real/bogus threshold")
print('\n')




four_hours = [0, 1, 2, 3, 4] #Create list of 0-4
time_change = four_hours*u.hour # let astropy know that every number represents an hour

candidate_az_alt = {}

for i, r, d in zip(candid, ra, dec):
    az = []
    alt = []
    az_alt_dict = {} # For each candidate, find the alt and az for four hours starting at observing time
    for x in time_change:
        time = observing_time + x # add one minute
        azimuth , altitude = az_alt(time, r, d)
        az.append(float(azimuth))
        alt.append(float(altitude))
        az_alt_dict['azimuth'] = az 
        az_alt_dict['altitude'] = alt
    count = 0
    
    for al in az_alt_dict['altitude']:
        if al > 30:
            count += 1
        #If a candidate is above 30 deg alt for more than 3 hours, add that candidate to the candidate_az_alt dictionary     
        if count >= 3:
            candidate_az_alt[i] =  az_alt_dict 

print str(len(candidate_az_alt.items())) + " candidates available to view with VIRT at " + str(observing_time)
print '\n'

#Create a table with candidate name, max alt, time of max alt
max_alt_dict = {}
#For every candidate that is a good one... 
for k, v in candidate_az_alt.items():
    time_max_alt = {}
    max_alt = max(v['altitude']) #Find the maximum altitude for that candidate
    maxindex = v['altitude'].index(max_alt) #Find the hours after observing start time candidate reaches max alt
    max_time = four_hours[maxindex] 
    time_max_alt['time'] = float(max_time)
    time_max_alt['maximum altitude'] = float(max_alt)
    max_alt_dict[k] = time_max_alt



#Candid value, e.g: 643106264215010003, is the key of max_alt, whereas it is a value in candidates
#Match the two dictionaries based on this similarity, add the key/values from new dict to candidates
for keys, values in max_alt_dict.items():
    for k,v in candidates.items():
        if v['candid'] == keys:
            #v['max alt time'] = (observing_time + values['time']*u.hour) This is ideal but don't know how to sort by Time object
            v['max alt hours after 7pm'] = values['time']
            v['max alt'] = values['maximum altitude']


#The table is flipped at first
final_form_flipped = pd.DataFrame(candidates)

#Simply transpose the table to fix this
final_form = final_form_flipped.T 


#Pull only the 'useful' columns to the table. Note: There is way more availble columns to pull. Talk to Dr. C
final_form = final_form[['max alt hours after 7pm', 'max alt','ra','dec','candid','magap','magpsf','distnr','classtar', 'rb', 'filter']]

#Delete Rows which didn't make the observing cut (Above 30 deg for 3 hours min)
final_form = final_form.dropna()

#Order the table first by ascending time. If two objects reach their peak alt at same time, have higher alt go first
double_sorted = final_form.sort_values(by = ['max alt hours after 7pm', 'max alt'], ascending=[True, False])


#Give the index the proper name: ZTF candidate ID
sorted_with_cuts =  double_sorted.rename_axis('ZTF candidate ID')

#Change the hours after column to be times rather than others after 7pm
# sorted_with_cuts['max alt hours after 7pm'] =  pd.to_datetime(raw_data['Mycol'], format='%d%b%Y:%H:%M:%S.%f')


#CSV filename
observing_file_name = str(observing_time)
observing_file_name = observing_file_name.split('T')[0] 
csv_file = observing_file_name + '_organized_output_ZTF_data.csv'


#Write final table () to csv file 
sorted_with_cuts.to_csv(csv_file)

print(sorted_with_cuts)
print "See " + csv_file + " for more details"



##Plotting Functionality if desired
# for k, v in candidate_az_alt.items():
#   max_alt = max(v['altitude'])
#   maxindex = v['altitude'].index(max_alt)
#   max_time = four_hours[maxindex]
#   if max_alt > 35:
#       plt.scatter(four_hours, v['altitude'])
#       plt.scatter(max_time, max_alt)
#       plt.annotate(str(max_alt) + ' occurs at ' + str(max_time), xy=(max_time, max_alt), xytext = (max_time, max_alt - 10))
#       plt.ylim(0, 90)
#       plt.title(str(k) + 'Altitude vs Time during Observation Hours')
#       plt.ylabel('Altitude')
#       plt.xlabel('Minutes after 7pm ' + today)
#       plt.savefig(str(k) + '.png')
#       plt.clf()



