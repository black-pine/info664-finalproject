# This file reads .JSON files (generated by "marvelAPI.py") located in the 'records' directory
# This file calculates and aggregates statistics based on .JSON files saved from the Marvel API
# This file prints output


import json
import glob

# dictionary key: creator name
# dictionary value: list of dictionaries
# 		dictionary key: 'role' ; value: creator's role (e.g. writer, penciller, inker)
# 		dictionary key: 'issue' ; value: title of comic
all_creators = {}
# dictionary key: character name
# dictinoary value: list of comic titles
all_characters = {}

for file in glob.glob('records/*.json'):
	with open(file, 'r') as comic:
		data = json.load(comic)

		# add each creator to all_creators
		for creator in data['creators']['items']:
			if creator['name'] not in all_creators:
				all_creators[creator['name']] = []
			all_creators[creator['name']].append({
				'role': creator['role'],
				'issue': data['title']
			})
		
		# add each character to all_characters
		for character in data['characters']['items']:
			if character['name'] not in all_characters:
				all_characters[character['name']] = []
			all_characters[character['name']].append(data['title'])

bestWriter = []
writtenComics = 0
coverCreators = set()
for creator in all_creators:
	writtenCt = 0
	for comic in all_creators[creator]:
		# count how many comics the creator is credited as a writer
		if comic['role'].lower() == 'writer':
			writtenCt += 1
		# add all creators who contributed only to the cover
		if 'cover' in comic['role']:
			coverCreators.add(creator)

	# find the most prolific writer(s)
	if writtenCt > writtenComics:
		writtenComics = writtenCt
		bestWriter = [creator]
	elif writtenCt == writtenComics:
		bestWriter.append(creator)

# print the most prolific writer(s)
if len(bestWriter) == 1:
	print (bestWriter[0],'has written',writtenComics,'of the top monthly Marvel comics.')
else:
	writerStr = ''
	for writer in bestWriter:
		writerStr += writer + ', '
	print (writerStr[:-2],'have each written',writtenComics,'of the top monthly Marvel comics.')

# print the number of cover creators
print(len(coverCreators),'creators contributed only to the cover art of at least one issue.')

# find the character that appears in the most issues
bestCharacter = ''
for character in all_characters:
	try:
		if len(all_characters[bestCharacter]) < len(all_characters[character]):
			bestCharacter = character
	# EXCEPT for the first character in the list
	except:
		bestCharacter = character
# print the most featured character
print(bestCharacter,'has appeared in',len(all_characters[bestCharacter]),'of the top monthly Marvel comics.')