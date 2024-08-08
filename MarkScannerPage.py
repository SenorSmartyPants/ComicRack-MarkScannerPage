# MarkScannerPage.py
#
# Marks scanner page as deleted pagetype
#
# You are free to modify and distribute this file
##########################################################################
from System.IO import Path

import clr
import sys
import re
import System
import System.Text
from System import String
from System.IO import File,  Directory, Path, FileInfo, FileStream
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
from System.Windows.Forms import *
from System.Drawing import *
clr.AddReferenceByPartialName('ComicRack.Engine')
from cYo.Projects.ComicRack.Engine import ComicPageType

import globalvars

from displayResultsForm import displayResultsForm
from mspProgressForm import mspProgressForm
from configuratorForm import configuratorForm

# this handles unicode encoding:
bodyname = System.Text.Encoding.Default.BodyName
sys.setdefaultencoding(bodyname)

markScannerAs = ComicPageType.Deleted



#@Name	Mark scanner page
#@Hook	Books
#@Description Mark scanner page as deleted
#@Image scan-icon.png
def MarkScannerPage(books):

	#shoutouts to docdoom and T3KNOGHO57
	progBar = mspProgressForm(books, globalvars.PROCESS_ON)
	
	progBar.ShowDialog()

	if progBar.errorLevel == 0:
		msg = "Finished. I've inspected %d books.\nDo you want to take look at the log file?" % (progBar.stepsPerformed)
	
		form = displayResultsForm()
		form.configure(msg)
		form.ShowDialog(ComicRack.MainWindow)
		form.Dispose()

		if form.DialogResult == DialogResult.Yes:
	
			form = configuratorForm()
			form.setFile(globalvars.LOGFILE)
			form.Text = 'Data Manager Logfile %s' % globalvars.VERSION
			form.ShowDialog(ComicRack.MainWindow)
			form.Dispose()