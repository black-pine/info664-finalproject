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
				'types' : {'oneShot' : 0, 'numOne' : 0,	'ongoing' : 0}
			}
		publisherSales[row['publisher']][row['year']]['income'] += salesIncome
		publisherSales[row['publisher']][row['year']]['units'] += int(row['estimated sales'])
		if not row['reorder']:
			publisherSales[row['publisher']][row['year']]['issues'] += 1
			# add issue type to count by publisher
			if not row['issue']:
				publisherSales[row['publisher']]['types']['oneShot'] += 1
			elif row['issue'] == 1:
				publisherSales[row['publisher']]['types']['numOne'] += 1
			else:
				publisherSales[row['publisher']]['types']['ongoing'] += 1
		
		# add issue sales amount and issue number to total by series
		if row['title'] not in seriesSales:
			seriesSales['title'] = {
				'issues' : set(),
				'income' : 0,
			}
		seriesSales['title']['income'] += salesIncome
		seriesSales['title']['issues'].add(row['issue'])

		# add issue sales amount to the monthly sales total
		monthlySales[row['month']] += salesIncome

		if row['reorder']:
			if row['item code'] not in reorders:
				reorders[row['item code']] = {
					'title': row['title'],
					'count': 0,
					'units': 0
				}
				if row['issue']:
					reorders[row['item code']]['title'] += ' iss. ' + row['issue']
			reorders[row['item code']]['count'] += 1
			reorders[row['item code']]['units'] += int(row['estimated sales'])

	# print(publisherSales)
	# print(round(publisherSales['Image Comics']['income'], 2))