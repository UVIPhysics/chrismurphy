# For every candidate, find which ones will be above the horizon during our observing hours
# First set the observer location: (latitude, longitude, elevation)

import pandas as pd
import json
import ephem 
from astropy.coordinates import EarthLocation,SkyCoord
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import AltAz
import matplotlib.pyplot as plt



observing_location = EarthLocation(lat='18.3381', lon='-64.8941', height=500*u.m) 
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


#Today at 7 pm (ast) = 11pm UTC
#Current strategy at Etelman is to observe from ~7-11 pm
now = Time.now()
print("Current UTC time: " + str(now))
print("\n")
now_str = str(now)
today = now_str.split(' ')[0]
today_7 = today + ' 23:00:00'
observing_time = Time(today_7) 
print("Observations begin: " + str(observing_time) + " UTC") 
print('\n')


#File to open = File we wrote in part one, Assuming we do part one and part two on same day
file = today + '_ztf_interesting_candidates.txt'

with open(file, 'r') as f:
    data = json.load(f)
results = data['results']

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
# print ra, dec, candid
# print len(ra), len(dec), len(candid)
print(str(len(ra)) + " transient candidates above certain real/bogus threshold")
print('\n')


# four_hours_in_minutes = list(range(4*60)) # 0 - (4*60) consecutive numbers
# time_change = four_hours_in_minutes*u.minute # let astropy know that every number represents a minute


four_hours = list(range(5)) #Create list of 0-4
time_change = four_hours*u.hour # let astropy know that every number represents an hour
#print(time_change)

candidate_az_alt = {}

for i, r, d in zip(candid, ra, dec):
	az = []
	alt = []
	az_alt_dict = {}
	for x in time_change:
		time = observing_time + x # add one minute
		azimuth , altitude = az_alt(time, r, d)
		az.append(float(azimuth))
		alt.append(float(altitude))
		az_alt_dict['azimuth'] = az 
		az_alt_dict['altitude'] = alt
	#print az_alt_dict
	candidate_az_alt[i] =  az_alt_dict
	#print '\n'

#print candidate_az_alt


#Create a table of candidate info
new_dict = {}
for k, v in candidate_az_alt.items():
    time_max_alt = {}
    max_alt = max(v['altitude'])
    maxindex = v['altitude'].index(max_alt)
    #print(maxindex, max_alt)
    max_time = four_hours[maxindex] 
#     print(max_time)
#     print(maxindex, max_time, max_alt)
    time_max_alt['time'] = float(max_time)
    time_max_alt['maximum altitude'] = float(max_alt)
    new_dict[k] = time_max_alt

#Merge candidates candidates and new_dict into one table
for k,v in candidates.items():
    for keys, values in new_dict.items():
        if v['candid'] == keys:
            #v['max alt time'] = (observing_time + values['time']*u.hour) This is ideal but don't know how to sort by Time object
            v['max alt hours after 7pm'] = values['time']
            v['max alt'] = values['maximum altitude']
            #v['check'] = keys

#The table is flipped at first
final_form_flipped = pd.DataFrame(candidates)

#Simply transpose the table to fix this
final_form = final_form_flipped.T 

#Pull only the 'useful' columns to the table. Note: There is way more availble columns to pull. Talk to Dr. C
final_useful = final_form[['max alt hours after 7pm', 'max alt','ra','dec','candid','magap','magpsf','distnr','classtar', 'rb', 'filter']]

#Order the table first by ascending time. If two objects reach their peak alt at same time, have higher alt go first
double_sorted = final_useful.sort_values(by = ['max alt hours after 7pm', 'max alt'], ascending=[True, False])

#Cut out objects that don't go above an altitude of 35 degrees during our observing time
sorted_with_cuts = double_sorted.drop(double_sorted[double_sorted['max alt'] < 35].index)

#Show the final table
print("Final Table")
print(sorted_with_cuts)


#CSV filename
csv_file = today + '_organized_output_ZTF_data.csv'


#Write final table () to csv file 
sorted_with_cuts.to_csv(csv_file)


###Plotting Functionality if desired
# for k, v in candidate_az_alt.items():
# 	max_alt = max(v['altitude'])
# 	maxindex = v['altitude'].index(max_alt)
# 	max_time = four_hours[maxindex]
# 	plt.scatter(four_hourss, v['altitude'])
# 	plt.scatter(max_time, max_alt)
# 	plt.annotate(str(max_alt) + ' occurs at ' + str(max_time), xy=(max_time, max_alt), xytext = (max_time, max_alt - 10))
# 	plt.ylim(0, 90)
# 	plt.title(str(k) + 'Altitude vs Time during Observation Hours')
# 	plt.ylabel('Altitude')
# 	plt.xlabel('Minutes after 7pm ' + today)
# 	plt.savefig(str(k) + '.png')
# 	plt.clf()



























