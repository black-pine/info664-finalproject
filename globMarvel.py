import json
import glob

all_creators = {}
all_characters = {}

for file in glob.glob('records/*.json'):
	with open(file, 'r') as comic:
		data = json.load(comic)

		for creator in data['creators']['items']:
			if creator['name'] not in all_creators:
				all_creators[creator['name']] = []
			all_creators[creator['name']].append({
				'role': creator['role'],
				'issue': data['title']
			})
		
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
		if comic['role'].lower() == 'writer':
			writtenCt += 1
		if 'cover' in comic['role']:
			coverCreators.add(creator)

	if writtenCt > writtenComics:
		writtenComics = writtenCt
		bestWriter = [creator]
	elif writtenCt == writtenComics:
		bestWriter.append(creator)
if len(bestWriter) == 1:
	print (bestWriter[0],'has written',writtenComics,'of the top monthly Marvel comics.')
else:
	writerStr = ''
	for writer in bestWriter:
		writerStr += writer + ', '
	print (writerStr[:-2],'have each written',writtenComics,'of the top monthly Marvel comics.')


bestCharacter = ''
for character in all_characters:
	try:
		if len(all_characters[bestCharacter]) < len(all_characters[character]):
			bestCharacter = character
	except:
		bestCharacter = character
print(bestCharacter,'has appeared in',len(all_characters[bestCharacter]),'of the top monthly Marvel comics.')