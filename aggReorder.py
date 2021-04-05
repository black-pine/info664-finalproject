import csv

with open('reorderData.csv', 'r') as comics:
	reader = csv.DictReader(comics)

	seriesSum = {}

	for row in reader:
		if row['series'] not in seriesSum:
			seriesSum[row['series']] = {
				'issues': 0,
				'units': 0
			}
		seriesSum[row['series']]['issues'] += 1
		seriesSum[row['series']]['units'] += int(row['units'])


with open('reorderDataAgg.csv', 'w') as reorderInfo:
	reorderHeader=['series', 'issues', 'units']
	w = csv.DictWriter(reorderInfo, fieldnames=reorderHeader)
	w.writeheader()
	for item in seriesSum:
		row = {
			'series': item,
			'issues': seriesSum[item]['issues'],
			'units': seriesSum[item]['units']
		}
		w.writerow(row)