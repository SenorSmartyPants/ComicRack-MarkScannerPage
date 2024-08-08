'''
how to use:
For every book:
1. in dmProgressForm call dmparser.matchAllRules(ruleset,book)
2.		matchAllRules first initializes all variables
2.		matchAllRules calls AnalyzeRuleSet which sets the values of dmParser.actions and dmParser.rules
3.		matchAllRules calls matchRule for every rule in dmParser.rules
4.			matchRule calls AnalyzeRule which sets dmParser.theRuleKey, dmParser.theRuleModifier and dmParser.theRuleVals (via CastType)
4. if matchAllRules returns True:
5. make a copy of the original book to store the original field contents (book.Clone())
5. in dmProgressForm call dmparser.executeAllActions(book)
6.		executeAllActions calls executeAction for every action in dmParser.actions, sets dmparser.FieldsTouched to None
7.		executeAction calls AnalyzeAction to set dmParser.theActionKey, dmParser.theActionModifier, dmParser.theActionValue
8.		executeAction appends the field currently in use to dmparser.FieldsTouched
9.		executeAction finally executes the action


calc works like this:
1. executAction calc
2. castType


'''
import System
import clr
import re
clr.AddReference("ComicRack.Engine")
from System.IO import Path

import globalvars

# import dmutils
# from dmutils import customFields
# customField = customFields()
# from dmutils import ruleFile, iniFile, dmString, comparer, multiValue
# dmString = dmString()
# comparer = comparer()
# multiValue = multiValue()
# dataManIni = iniFile(globalvars.INIFILE)
# userIni = iniFile(globalvars.USERINI)

class mspProcesser(object):
	
	def __init__(self):
		self.initializeVars()

	def initializeVars(self):
		self.error = False
		self.errCount = 0
		self.theLog = ''

	# routine copied from https://gist.github.com/mxu007/4209efa6d6e79e3bce17ab6ce5679fb9#file-lcp_1-py
	def longestCommonPrefix(self, strs):
		longest_pre = ""
		if not strs: return longest_pre
		shortest_str = min(strs, key=len)
		for i in range(len(shortest_str)):
			if all([x.startswith(shortest_str[:i+1]) for x in strs]):
				longest_pre = shortest_str[:i+1]
			else:
				break
		return longest_pre

	def getPageNameList(self, pages, imgProvider):
		pageNameList = []
		
	#	for page in book.Pages:
		for page in pages:
			imgInfo = imgProvider.GetImageInfo(page.ImageIndex)
			#print imgInfo
			filename = Path.GetFileName(imgInfo.Name)
			pageNameList.append(filename)
		
		#print(pageNameList)
		return pageNameList

	# this routine copied from 
	# https://github.com/mylar3/mylar3/blob/python3-dev/lib/comictaggerlib/comicapi/comicarchive.py#L733 and
	# https://github.com/comictagger/comictagger/blob/develop/comicapi/comicarchive.py#L749 
	# and then modified
	def getScannerPage(self, book):
		scanner_page_index = None

		try:

			#Get the comicbook navigator to retrieve live archive info
			nav = book.CreateNavigator()
			pages = nav.GetPageInfos()
			
			# make a guess at the scanner page
			count = pages.Count
			imgProvider = book.OpenProvider(count)
			
			if count <= 0:
				self.theLog += '{0} returned zero page count. Marking not run.'.format(book.Caption)

			# too few pages to really know
			if count < 5:
				self.theLog += '{0} returned fewer than 5 pages ({1} pages reported). Not enough to find scanner page reliably.'.format(book.Caption, count)
				return None

			name_list = self.getPageNameList(pages, imgProvider)

			# count the length of every filename, and count occurences
			length_buckets = dict()
			for name in name_list:
				length = len(name)
				if length in length_buckets:
					length_buckets[length] += 1
				else:
					length_buckets[length] = 1

			# sort by most common
			sorted_buckets = sorted(
				iter(length_buckets.items()),
				key=lambda k_v: (
					k_v[1],
					k_v[0]),
				reverse=True)

			# statistical mode occurence is first
			mode_length = sorted_buckets[0][0]

			# we are only going to consider the final image file:
			final_name = name_list[count - 1]
			
			common_length_list = list()
			for name in name_list:
				if len(name) == mode_length:
					common_length_list.append(name)

			prefix = self.longestCommonPrefix(common_length_list)

			if mode_length <= 7 and prefix == "":
				# probably all numbers
				if len(final_name) > mode_length:
					scanner_page_index = count - 1

			# see if the last page doesn't start with the same prefix as most
			# others
			elif not final_name.startswith(prefix):
				scanner_page_index = count - 1

			#print(scanner_page_index)
			if scanner_page_index:
				return pages, pages[scanner_page_index], final_name
			else:
				return pages, None, None
		
		except Exception as err:
			self.theLog += str(Exception.args)
			self.error = True
			return None, None, None

				