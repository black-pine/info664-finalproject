# This file webscrapes data from http://comicbookpage.com/MayoReport/TopComics.php
# This file generates "comicsData.csv" saved to the same directory as this file

import requests
from bs4 import BeautifulSoup
import re
import csv


allData = []
dataHeader = ['year', 'month', 'quantity rank', 'item code', 'price', 'publisher', 'title', 'issue', 'reorder', 'estimated sales', 'delta']

moneyPattern = re.compile(r'\$(\d*\.\d\d)')

for year in range(2003, 2021):
	for month in range(1, 13):
		# adjustments to get only range [3/2003, 3/2020]
		if year == 2003 and month < 3:
			continue
		if year == 2020 and month > 3:
			break

		url = f"http://comicbookpage.com/MayoReport/TopComics.php?Year={year}&Month={month:02d}"
		r = requests.get(url)

		if r.status_code == 200:
			soup = BeautifulSoup(r.text, features="html.parser")
			dataRows = soup.find_all('tr')

			# loop through each row of data on the page: 'tr' elem without data do not contain 'td' elem
			for singleIssue in dataRows:
				tableData = singleIssue.find_all('td')
				if tableData:
					itemInfo = {
						'year' : year,
						'month' : month,
						'quantity rank' : tableData[0].text.strip().partition(' ')[0], # some ranks have extra characters
						'item code' : tableData[2].text.strip(),
						'price' : moneyPattern.search(tableData[3].text).group(1),
						'publisher' : tableData[4].text.strip(),
						'title' : tableData[5].text.strip(),
						'issue' : tableData[6].text.strip(),
						'reorder' : tableData[7].text.strip(),
						'estimated sales' : tableData[8].text.strip().replace(',',''), # remove commas from numeric value
						'delta' : tableData[11].text.strip().replace(',','') # remove commas from numeric value
					}

					# replace blank data with Python None
					for k in itemInfo:
						if len(str(itemInfo[k])) == 0:
							itemInfo[k] = None
					
					allData.append(itemInfo)

# write scraped data to csv file
with open('comicsData.csv', 'w') as scrapeInfo:
	w = csv.DictWriter(scrapeInfo, fieldnames=dataHeader)
	w.writeheader()
	for item in allData:
		w.writerow(item)