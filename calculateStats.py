# Track / Results:
# Overall sales count per publisher (by year)
# Income by title (including issue count)
# Percentage of income from first issues by publisher
# Top reordered items
# Most lucrative month

# 'year', 'month', 'quantity rank', 'item code', 'price', 'publisher', 'title', 'issue', 'reorder', 'estimated sales', 'delta'

import csv

with open('comicsData.csv', 'r') as comics:
	reader = csv.DictReader(comics)

	publisherSales = {}
	seriesSales = {}
	reorders = {}
	monthlySales = {
		'1' : 0,
		'2' : 0,
		'3' : 0,
		'4' : 0,
		'5' : 0,
		'6' : 0,
		'7' : 0,
		'8' : 0,
		'9' : 0,
		'10' : 0,
		'11' : 0,
		'12' : 0,
	}

	for row in reader:
		salesIncome = float(row['price']) * int(row['estimated sales'])

		# add issue sales amount, unit count, and issue count to total by publisher > year
		if row['publisher'] not in publisherSales:
			publisherSales[row['publisher']] = {
				'2003' : {'units' : 0, 'issues': 0, 'income' : 0},
				'2004' : {'units' : 0, 'issues': 0, 'income' : 0},
				'2005' : {'units' : 0, 'issues': 0, 'income' : 0},
				'2006' : {'units' : 0, 'issues': 0, 'income' : 0},
				'2007' : {'units' : 0, 'issues': 0, 'income' : 0},
				'2008' : {'units' : 0, 'issues': 0, 'income' : 0},
				'2009' : {'units' : 0, 'issues': 0, 'income' : 0},
				'2010' : {'units' : 0, 'issues': 0, 'income' : 0},
				'2011' : {'units' : 0, 'issues': 0, 'income' : 0},
				'2012' : {'units' : 0, 'issues': 0, 'income' : 0},
				'2013' : {'units' : 0, 'issues': 0, 'income' : 0},
				'2014' : {'units' : 0, 'issues': 0, 'income' : 0},
				'2015' : {'units' : 0, 'issues': 0, 'income' : 0},
				'2016' : {'units' : 0, 'issues': 0, 'income' : 0},
				'2017' : {'units' : 0, 'issues': 0, 'income' : 0},
				'2018' : {'units' : 0, 'issues': 0, 'income' : 0},
				'2019' : {'units' : 0, 'issues': 0, 'income' : 0},
				'2020' : {'units' : 0, 'issues': 0, 'income' : 0},
				'types' : {'oneShot' : { 'count' : 0, 'revenue' : 0 }, 
					'numOne' : { 'count' : 0, 'revenue' : 0 },	
					'ongoing' : { 'count' : 0, 'revenue' : 0 }}
			}
		publisherSales[row['publisher']][row['year']]['income'] += salesIncome
		publisherSales[row['publisher']][row['year']]['units'] += int(row['estimated sales'])
		if not row['reorder']:
			publisherSales[row['publisher']][row['year']]['issues'] += 1
			# add issue type to count by publisher
			if not row['issue']:
				publisherSales[row['publisher']]['types']['oneShot']['count'] += 1
				publisherSales[row['publisher']]['types']['oneShot']['revenue'] += salesIncome
			elif row['issue'] == '1':
				publisherSales[row['publisher']]['types']['numOne']['count'] += 1
				publisherSales[row['publisher']]['types']['numOne']['revenue'] += salesIncome
			else:
				publisherSales[row['publisher']]['types']['ongoing']['count'] += 1
				publisherSales[row['publisher']]['types']['ongoing']['revenue'] += salesIncome
		
		# add issue sales amount and issue number to total by series
		if row['title'] not in seriesSales:
			seriesSales[row['title']] = {
				'issues' : set(),
				'income' : 0,
			}
		seriesSales[row['title']]['income'] += salesIncome
		seriesSales[row['title']]['issues'].add(row['issue'])

		# add issue sales amount to the monthly sales total
		monthlySales[row['month']] += salesIncome

		if row['reorder']:
			if row['item code'] not in reorders:
				reorders[row['item code']] = {
					'series': row['title'],
					'issue': row['issue'],
					'count': 0,
					'units': 0
				}
			reorders[row['item code']]['count'] += 1
			reorders[row['item code']]['units'] += int(row['estimated sales'])


with open('publisherData.csv', 'w') as publisherInfo:
	publisherHeader=['publisher', 'year', 'units', 'issues', 'income']
	w = csv.DictWriter(publisherInfo, fieldnames=publisherHeader)
	w.writeheader()
	for pub in publisherSales:
		row = { 'publisher': pub }
		for year in publisherSales[pub]:
			if year == 'types':
				break
			row['year'] = year
			row['units'] = publisherSales[pub][year]['units']
			row['issues'] = publisherSales[pub][year]['issues']
			row['income'] = publisherSales[pub][year]['income']
			w.writerow(row)

with open('issueTypeData.csv', 'w') as typeInfo:
	typeHeader=['publisher', 'one shot', 'first issue', 'ongoing', 'one shot rev', 'first rev', 'ongoing rev', 'one percent', 'first percent', 'ongoing percent', 'one rev percent', 'first rev percent', 'ongoing rev percent']
	w = csv.DictWriter(typeInfo, fieldnames=typeHeader)
	w.writeheader()
	for pub in publisherSales:
		totalIss = publisherSales[pub]['types']['oneShot']['count'] + publisherSales[pub]['types']['numOne']['count'] + publisherSales[pub]['types']['ongoing']['count']
		if totalIss == 0:
			totalIss = 1
		totalRev = publisherSales[pub]['types']['oneShot']['revenue'] + publisherSales[pub]['types']['numOne']['revenue'] + publisherSales[pub]['types']['ongoing']['revenue']
		if totalRev == 0:
			totalRev = 1
		row = {
			'publisher' : pub,
			'one shot' : publisherSales[pub]['types']['oneShot']['count'],
			'first issue' : publisherSales[pub]['types']['numOne']['count'],
			'ongoing' : publisherSales[pub]['types']['ongoing']['count'],
			'one shot rev' : publisherSales[pub]['types']['oneShot']['revenue'],
			'first rev' : publisherSales[pub]['types']['numOne']['revenue'],
			'ongoing rev' : publisherSales[pub]['types']['ongoing']['revenue'],
			'one percent' : (publisherSales[pub]['types']['oneShot']['count'] / totalIss) * 100,
			'first percent' : (publisherSales[pub]['types']['numOne']['count'] / totalIss) * 100,
			'ongoing percent' : (publisherSales[pub]['types']['ongoing']['count'] / totalIss) * 100,
			'one rev percent' : (publisherSales[pub]['types']['oneShot']['revenue'] / totalRev) * 100,
			'first rev percent' : (publisherSales[pub]['types']['numOne']['revenue'] / totalRev) * 100,
			'ongoing rev percent' : (publisherSales[pub]['types']['ongoing']['revenue'] / totalRev) * 100
			
		}
		w.writerow(row)

with open('seriesData.csv', 'w') as seriesInfo:
	seriesHeader=['title', 'total issues', 'income']
	w = csv.DictWriter(seriesInfo, fieldnames=seriesHeader)
	w.writeheader()
	for series in seriesSales:
		row = {
			'title' : series,
			'total issues' : len(seriesSales[series]['issues']),
			'income' : seriesSales[series]['income']
		}
		w.writerow(row)

with open('reorderData.csv', 'w') as reorderInfo:
	reorderHeader=['series', 'issue', 'count', 'units']
	w = csv.DictWriter(reorderInfo, fieldnames=reorderHeader)
	w.writeheader()
	for item in reorders:
		w.writerow(reorders[item])

with open('monthlyData.csv', 'w') as monthlyInfo:
	monthlyHeader=['month', 'income', 'avg']
	w = csv.DictWriter(monthlyInfo, fieldnames=monthlyHeader)
	w.writeheader()
	for month in monthlySales:
		temp = 17
		if month == 3:
			temp = 18
		row = {
			'month' : month,
			'income' : monthlySales[month],
			'avg' : monthlySales[month] / temp
		}
		w.writerow(row)