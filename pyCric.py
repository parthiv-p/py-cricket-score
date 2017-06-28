import sys
import requests
from elementtree import ElementTree as ET

class Cricket():

	cricbuzz_link = "http://synd.cricbuzz.com/j2me/1.0/livematches.xml"

	def __init__(self):
		self.getData()			#for now (just testing)
		
	def getData(self):
		try:
			global matches
			main_xml = ET.XML(requests.get(self.cricbuzz_link).content)
			matches = main_xml.findall('match')
		except requests.exceptions.RequestException as e:
			print e
			sys.exit(1)

	def get_match_list(self):
		matchInfo = {}
		'''
		matchInfo = {
			"0":{
				"matchDesc":val
				"matchType":val
				"matchStatus":val
				"matchState":val
				},
			"1":{
				"matchDesc":val
				"matchType":val
				"matchStatus":val
				"matchState":val
			},
		}
		'''
		for matchCount,match in enumerate(matches):
			matchInfo[matchCount] = {}

			matchInfo[matchCount]['matchDesc'] = match.get('mchDesc')
			matchInfo[matchCount]['matchType'] = match.get('type')
			matchInfo[matchCount]['matchStatus'] = match.find('state').get('status')
			matchInfo[matchCount]['matchState'] = match.find('state').get('mchState')
			
		return matchInfo

	def get_venue_details(self, userChoice):

		try:					#if match has not started then datapath is not updated
			matchDataPath = matches[userChoice].get('datapath')
			matchScorecard = ET.XML(requests.get(matchDataPath + 'scorecard.xml').content)
		except requests.exceptions.MissingSchema:
			return 0

		venueInfo = {}
		'''
		venueInfo = {
			'ground':val
			'city':val
			'country':val
		}
		'''
		venueInfo['ground'] = matchScorecard.get('grnd')
		venueInfo['city'] = matchScorecard.get('vcity')
		venueInfo['country'] = matchScorecard.get('vcountry')

		return venueInfo

	def get_teams(self, userChoice):
		'''
		Will return the full squad with Subs 

		If data does not exist for some reason then it will return 0
		'''
		try:					#if match has not started then datapath is not updated
			matchDataPath = matches[userChoice].get('datapath')
			matchScorecard = ET.XML(requests.get(matchDataPath + 'scorecard.xml').content)
		except requests.exceptions.MissingSchema:
			return 0

		if (matchScorecard.find('state').get('mchState') != 'upcoming' and matchScorecard.find('state').get('mchState') != 'delay'):
			teams = matchScorecard.find('squads').findall('Team')
			teamInfo = {}
			'''
			teamInfo = {
				'0': playingXI(separated by comma)
				'1':playingXI(separated by comma)
			}
			'''
			for teamCount,team in enumerate(teams):
				players = team.get('mem')
				teamInfo[teamCount] = players
		else:
			return 0

		return teamInfo
































