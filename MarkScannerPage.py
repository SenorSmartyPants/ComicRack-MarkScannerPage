# MarkScannerPage.py
#
# Marks scanner page as deleted pagetype
#
# You are free to modify and distribute this file
##########################################################################
from utils import *

from System.IO import Path

import clr
clr.AddReferenceByPartialName('ComicRack.Engine')
from cYo.Projects.ComicRack.Engine import ComicPageType

markScannerAs = ComicPageType.Deleted

def getPageNameList(book):
	pageNameList = []
	imgProvider = book.OpenProvider(book.Pages.Count)

	for page in book.Pages:
		imgInfo = imgProvider.GetImageInfo(page.ImageIndex)
		filename = Path.GetFileName(imgInfo.Name)
		pageNameList.append(filename)
	
	return pageNameList

# this routine copied from 
# https://github.com/mylar3/mylar3/blob/python3-dev/lib/comictaggerlib/comicapi/comicarchive.py#L733 and
# https://github.com/comictagger/comictagger/blob/develop/comicapi/comicarchive.py#L749 
# and then modified
def getScannerPage(book):
	scanner_page_index = None

	# make a guess at the scanner page
	count = book.Pages.Count

	# too few pages to really know
	if count < 5:
		return None

	name_list = getPageNameList(book)

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

	prefix = longestCommonPrefix(common_length_list)

	if mode_length <= 7 and prefix == "":
		# probably all numbers
		if len(final_name) > mode_length:
			scanner_page_index = count - 1

	# see if the last page doesn't start with the same prefix as most
	# others
	elif not final_name.startswith(prefix):
		scanner_page_index = count - 1

	if scanner_page_index:
		return book.Pages[scanner_page_index]
	else:
		return None

#@Name	Mark scanner page...
#@Hook	Books
#@Description Mark scanner page as deleted
def MarkScannerPage(books):
	for book in books:

		scanner_page = getScannerPage(book)
		if scanner_page and scanner_page.PageType != markScannerAs:
			print 'unmarked scanner page found in {0}. Setting to {1}'.format(book.Caption, markScannerAs)
			book.UpdatePageType(scanner_page, markScannerAs)

	print 'Finished checking for scanner pages'