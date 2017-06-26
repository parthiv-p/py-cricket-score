import sys
import requests
from elementtree import ElementTree as ET

class Cricket():

	cricbuzz_link = "http://synd.cricbuzz.com/j2me/1.0/livematches.xml"
	

	def __init__(self):
		pass
		

	def getData(self,url):
		try:
			return ET.XML(requests.get(url).content)
		except requests.exceptions.RequestException as e:
			print e
			sys.exit(1)

	def UserInput(self,inputPrompt,inputRange):
		userChoice = input(inputPrompt)

		if (0 < userChoice < inputRange):
			retryCount = 0
			return userChoice
		else:
			print 'Invalid Input!'


	def get_match_list(self):
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
		main_xml = self.getData(self.cricbuzz_link)
		matches = main_xml.findall('match')
		
		matchInfo = {}

		for matchCount,match in enumerate(matches):
			matchInfo[matchCount] = {}

			matchInfo[matchCount]['matchDesc'] = match.get('mchDesc')
			matchInfo[matchCount]['matchType'] = match.get('type')
			matchInfo[matchCount]['matchStatus'] = match.find('state').get('status')
			matchInfo[matchCount]['matchState'] = match.find('state').get('mchState')
			
		
		return matchInfo

