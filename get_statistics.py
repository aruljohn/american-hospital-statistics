import re
import requests
import pandas as pd

# Constants
user_agent = 'Mozilla/5.0 (compatible; NoBot/1.1)'
url = 'https://www.ahd.com/state_statistics.html'
regex = re.compile('<td><a href="states/hospital_.+">(.+?)</a></td>\s*\
<td align="right">(.+?)</td>\s*<td align="right">(.+?)</td>\s*<td align="right">(.+?)</td>\s*\
<td align="right">(.+?)</td>\s*<td align="right">(.+?)</td>')
csv_filename = 'ahd.csv'

# Vars
states = []
number_hospitals = []
staffed_beds = []
total_discharges = []
patient_days = []
gross_patient_revenue = []

# Get page
page = requests.get(url, headers={'user-agent': user_agent})
html = page.text

# Parse HTML
html = re.sub(r'\s{2,}', ' ', html)
trs = re.findall(r'<tr>(.+?)</tr>', str(html))
for tr in trs:
	tds = regex.search(tr)
	if tds:
		states.append(tds.group(1))
		number_hospitals.append(tds.group(2))
		staffed_beds.append(tds.group(3))
		total_discharges.append(tds.group(4))
		patient_days.append(tds.group(5))
		gross_patient_revenue.append(tds.group(6))

dictionary = {
	'State': states,
	'Number Hospitals': number_hospitals,
	'Staffed Beds': staffed_beds,
	'Total Discharges': total_discharges,
	'Patient Days': patient_days,
	'Gross Patient Revenue': gross_patient_revenue
}
columns = dictionary.keys()

# Create dataframe
ahd = pd.DataFrame(dictionary, columns=columns)
ahd.to_csv(csv_filename)
