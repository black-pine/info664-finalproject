# 'year', 'month', 'quantity rank', 'item code', 'price', 'publisher', 'title', 'issue', 'reorder', 'estimated sales', 'delta'

import csv
from openpyxl import Workbook

def deltaRank(deltaDict, itemCode):
	ranked = sorted(deltaDict, key=deltaDict.get, reverse=True)
	rank = ranked.index(itemCode)
	rank += 1
	return rank

marvelData = []

with open('comicsData.csv', 'r') as comics:
	reader = csv.DictReader(comics)

	for row in reader:
		if row['month'] not in [partial['month'] for partial in marvelData if partial['year'] == row['year']]:
			if len(marvelData) != 0:
				marvelData[-1]['topDelta']['rank'] = deltaRank(deltaData, marvelData[-1]['topDelta']['data']['item code'])
			
			marvelData.append({
				'year': row['year'],
				'month': row['month'],
				'topIss': {'data': {}, 'rank': 0},
				'topNumOne': {'data': {}, 'rank': 0},
				'topReord': {'data': {}, 'rank': 0},
				'topDelta': {'data': {}, 'rank': 0}
			})
			
			numOneCt = 0
			reordCt = 0
			deltaTemp = -500000
			deltaData = {}

		# Increase counts
		if row['issue'] == '1':
			numOneCt += 1
		if row['reorder']:
			reordCt += 1
		if row['delta']:
			deltaData[row['item code']] = int(row['delta'])

		# Set data for top monthly Marvel issue
		if marvelData[-1]['topIss']['rank'] == 0 and row['publisher'] == 'Marvel Comics':
			marvelData[-1]['topIss']['data'] = row
			marvelData[-1]['topIss']['rank'] = int(row['quantity rank'])

		# Set data for top monthly Marvel first issue
		if marvelData[-1]['topNumOne']['rank'] == 0 and row['publisher'] == 'Marvel Comics' and row['issue'] == '1':
			marvelData[-1]['topNumOne']['data'] = row
			marvelData[-1]['topNumOne']['rank'] = numOneCt
		
		# Set data for top monthly reordered Marvel issue
		if marvelData[-1]['topReord']['rank'] == 0 and row['publisher'] == 'Marvel Comics' and row['reorder']:
			marvelData[-1]['topReord']['data'] = row
			marvelData[-1]['topReord']['rank'] = reordCt

		# Set data for top monthly Marvel delta
		if row['delta'] and deltaTemp < int(row['delta']) and row['publisher'] == 'Marvel Comics':
			marvelData[-1]['topDelta']['data'] = row
			deltaTemp = int(row['delta'])

	marvelData[-1]['topDelta']['rank'] = deltaRank(deltaData, marvelData[-1]['topDelta']['data']['item code'])

typesKey = {
	'Top Issue': 'topIss',
	'Top First Issue': 'topNumOne',
	'Top Reorder': 'topReord',
	'Highest Delta': 'topDelta'
}
wb = Workbook()
ws = wb.active
ws.title = 'Top Months'
for item in marvelData:
	sheet = wb.create_sheet(title=item['year']+'_'+item['month'])

	header = ['type', 'rank']
	header.extend(item['topIss']['data'].keys())
	sheet.append(header)

	for topType in typesKey:
		values = [topType, item[typesKey[topType]]['rank']]
		values.extend(list(item[typesKey[topType]]['data'].values()))
		sheet.append(values)
	
	if len(set([item[partial]['rank'] for partial in item if partial.startswith('top')]).difference({1})) == 0:
		ws.append([item['year'], item['month']])
	
wb.save('marvelData.xlsx')