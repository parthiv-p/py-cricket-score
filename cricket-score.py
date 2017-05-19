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

def userInput(inputPrompt, inputRange):
	userChoice = input(inputPrompt)

	if (0 < userChoice < inputRange):
		retryCount = 0
		return userChoice
	else:
		print 'Invalid Input!'

def printScorecard():
	pass

def printCommentary():
	pass

def printTeamDetails():
	matchScorecard = ET.XML(requests.get(matchDataPath + 'scorecard.xml').content)
	if (matchScorecard.find('state').get('mchState') != 'upcoming' and matchScorecard.find('state').get('mchState') != 'delay'):
		teams = matchScorecard.find('squads').findall('Team')
		for team in teams:
			print team.get('Name').upper()
			players = team.get('mem')
			players = players.split(',')					#the data gives us all the team members so we find the playing XI from this
			for player in players:
				if player[-2] != 'S':						#players with 'name'(S) indicate substitute
					print player
			print '\n'
	else:
		print 'Wait for the match to start'					#the playing XI are updated only after the match has started

def printVenueDetails():
	pass

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
matchSelected = userInput('\nSelect the match for further score updates: ', matchCount)
if matchSelected:
	matchDataPath = matches[(matchSelected - 1)].get('datapath')

	print '\n1. Scorecard    2. Commentary    3. Team Details    4. Venue Details'
	selection = userInput('Select an option: ', 5)
	if selection:
		if selection == 1:
			printScorecard()
		elif selection == 2:
			printCommentary()
		elif selection == 3:
			printTeamDetails()
		elif selection == 4:
			printVenueDetails()
