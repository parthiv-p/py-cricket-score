import sys
import requests
from elementtree import ElementTree as ET

cricbuzz_link = "http://synd.cricbuzz.com/j2me/1.0/livematches.xml"

matchCount = 0

try:
	livematches = ET.XML(requests.get(cricbuzz_link).content)
except requests.exceptions.RequestException as e:
	print e
	sys.exit(1)

#Make a local copy of the XML just for reference
xml_copy = open('livematches.xml', 'w')
xml_copy.write(requests.get(cricbuzz_link).content)
xml_copy.close()

#Print list of all recent matches with the score
matches = livematches.findall('match')

for matchCount,match in enumerate(matches, 1):			#(,1) is so that matchCount starts from 1 and not 0
	matchDesc = match.get('mchDesc')
	matchType = match.get('type')
	matchstatus = match.find('state').get('status')
	matchState = match.find('state').get('mchState')

	print str(matchCount) + '. ' + matchDesc + '	' + matchType + '	' + matchstatus + ' -({})'.format(matchState)

#Take input from user and move on to give the match summary or live score

matchSelected = input('\nSelect the match for further score updates: ')
if  (0 < matchSelected <= matchCount):
	matchDataPath = matches[(matchSelected - 1)].get('datapath')
	print matchDataPath
else:
	print "Invalid Input!"
