# Following up on Zwicky Transient Facility (ZTF) candidates with the Virgin Islands Robotic Telescope (VIRT)

For usage guide, skip to the end of page.

## ZTF Background

ZTF uses a new robotic camera with a 47 square degree field of view mounted on the Samuel Oschin 48-inch Schmidt telescope. 47 degrees is an unprecedented amount of sky view! Thats the equivalent sky area of 247 full moons! With such a large field of view, ZTF will capture hundreds of thousands of stars and galaxies in a single shot. Every night, ZTF will observe 3750 square degrees per hour.

### ZTF Science Goals
+ Active Galactic Nuclei & Tidal Disruption Events
+ Stellar Astrophyiscs
+ Cosmology with type Ia Supernovae
+ Electromagnetic, Gravitationnal Waves & Neutrinos Counterparts
+ Solar System Bodies
+ Physics of Supernovae & Relativistic Explosions 
+ Detailed study of the Andromeda Galaxy

### Make Alerts Really Simple (MARS)
MARS provides access to all public alerts issued by ZTF since the start of the public alert stream on June 1, 2018. Alerts can be accessed by using the [website](https://mars.lco.global/) or the API they have set up.

## Etelman Observatory & VIRT
Located in St. Thomas, USVI, the Etelman Observatory hosts the 0.5m Virgin Island Robotic Telescope (VIRT).
We are the easternmost location compared to the continental U.S. and therefore we are well sited to follow-up transients not observable by
facilities in the Canary Islands or in the mainland U.S. 
Using VIRT at Etelman we are interested in following up on all of the ZTF science goals, especially Tidal Disruption Events, Stellar Astrophyiscs, Physics of Supernovae & Relativistic Explosions, and Solar System Bodies.
VIRT data will be combined with other faiclities that UVI has access to, including the Las Cumbres Observatory network and the Gemini telescopes.

## Acessing Alerts using the MARS API 
This python based code utilizes the MARS API to download the most recent transient candidates from ZTF.

## Following up on Candidates using VIRT
Our ultimate goal is to select a subsample of ZTF interesting candidates (rb >0.95)  is so that we can follow up using VIRT and our other telescopes.

## DISCLAIMER
1.The code is not finished yet


2. I'd like others to be able to use the code I have written. The code is useful for others who would like to see how to use the MARS API, and also useful for finding which candidates are available to view and at what time they will be highest in the sky.


3. Feel free to contact me with any suggestions or critics to improve it


## Usage Guide
1. **Download mars_from_ztf.py and mars_from_ztf_pt2.py**


2. **Run mars_from_ztf.py** . This step downloads all the previous nights transient candidates with rb > .95 . If your curious what the output from this step looks like, the results will be stored in as <todays date> + ztf_interesting_candidates.txt


3. **Run mars from_ztf_pt2.py** . For every candidate found in the previous step, this part finds when each candidate will be highest in the sky, relative to VIRT, between the times of 7pm and 11pm est. **The final result of this code will be a file titled with todays date + organized_output_ZTF_data.csv .**


```bash
python mars_from_ztf.py
python mars_from_ztf_pt2.py
```


### Understanding the output table
###### Column Desciptions
+ **ZTF candidate ID:** objectID 
+ **max alt hours after 7pm:** Hours after 7pm when candidate reaches highest altitude relative to virt
+ **max alt:** Maximum altitude between 7-11pm relative to VIRT. 
+ **ra:** Right Ascension of candidate; J2000 [deg]
+ **dec:** Declination of candidate; J2000 [deg]
+ **candid:** The value of the candid field of the alert. Exact match.
+ **magap:** Aperture mag using 8 pixel diameter aperture measured from difference image [mag]
+ **magpsf:** Magnitude from PSF-fit photometry measured from difference image [mag]
+ **distnr:** Distance to nearest source in reference image PSF-catalog within 30 arcsec (1 pixel = 1.0 arcsecond) [pixels]
+ **classtar:** Star/Galaxy classification score from SExtractor measured from the difference image.
+ **rb:** RealBogus quality score; range is 0 to 1 where closer to 1 is more reliable.
+ **filter:** Filter name (g, r, i)


Chris Murphy, Physics major at the University of the Virgin Islands


christopher.murphy@students.uvi.edu
