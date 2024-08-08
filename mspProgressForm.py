'''
new version of progressForm.py
'''
import clr
from System import DateTime

import System.Drawing
import System.Windows.Forms
import System.Threading
from System.IO import File

from System.Drawing import *
from System.Windows.Forms import *

import globalvars
from globalvars import *

clr.AddReferenceByPartialName('ComicRack.Engine')
from cYo.Projects.ComicRack.Engine import ComicPageType
markScannerAs = ComicPageType.Deleted

import mspprocesser
from mspprocesser import mspProcesser
mspProcesser = mspProcesser()

ERRCOUNT = 0
theLog = ""

# initialize this with
# 1.) For GUI testing:
# theForm = progressForm(books, PROCESS_TEST)
# 2.) for ID'ing without marking:
# theForm = progressForm(books, PROCESS_OFF)
# 3.) for marking as deleted:
# theForm = progressForm(books, PROCESS_ON)
# OR
# theForm = progressForm(books)

class mspProgressForm(Form):
	def __init__(self, books = None, theProcess = 2):
		self.InitializeComponent()
		self.Icon = Icon(globalvars.ICON_SMALL)
		self.Text = 'Mark Scanner Page for ComicRack %s' % globalvars.VERSION
		self.theProcess = theProcess
		self.theBooks = books
		self.errorLevel = 0
		self.cancelledByUser = False
		self.stepsPerformed = 0
		self.maxVal = 0
		self.stop_the_Worker = False	
	
	def InitializeComponent(self):
		self._progressBar = System.Windows.Forms.ProgressBar()
		self._label1 = System.Windows.Forms.Label()
		self._backgroundWorker1 = System.ComponentModel.BackgroundWorker()
		self._buttonCancel = System.Windows.Forms.Button()
		self.SuspendLayout()
		# 
		# progressBar
		# 
		self._progressBar.Location = System.Drawing.Point(12, 39)
		self._progressBar.Name = "progressBar"
		self._progressBar.Size = System.Drawing.Size(413, 23)
		self._progressBar.Style = System.Windows.Forms.ProgressBarStyle.Continuous
		self._progressBar.TabIndex = 0
		# 
		# label1
		# 
		self._label1.AutoSize = True
		self._label1.BackColor = System.Drawing.SystemColors.Control
		self._label1.Location = System.Drawing.Point(13, 13)
		self._label1.Name = "label1"
		self._label1.Size = System.Drawing.Size(22, 13)
		self._label1.TabIndex = 1
		self._label1.Text = "xxx"
		# 
		# backgroundWorker1
		# 
		self._backgroundWorker1.WorkerReportsProgress = True
		self._backgroundWorker1.WorkerSupportsCancellation = True
		self._backgroundWorker1.DoWork += self.BackgroundWorker1DoWork
		self._backgroundWorker1.ProgressChanged += self.BackgroundWorker1ProgressChanged
		self._backgroundWorker1.RunWorkerCompleted += self.BackgroundWorker1RunWorkerCompleted
		self._backgroundWorker1.CancellationPending += self.BackgroundWorker1Cancellation
		# 
		# buttonCancel
		# 
		self._buttonCancel.Location = System.Drawing.Point(185, 71)
		self._buttonCancel.Name = "buttonCancel"
		self._buttonCancel.Size = System.Drawing.Size(75, 23)
		self._buttonCancel.TabIndex = 2
		self._buttonCancel.Text = "Cancel"
		self._buttonCancel.UseVisualStyleBackColor = True
		self._buttonCancel.Click += self.ButtonCancelClick
		# 
		# progressForm
		# 
		self.ClientSize = System.Drawing.Size(436, 106)
		self.Controls.Add(self._buttonCancel)
		self.Controls.Add(self._label1)
		self.Controls.Add(self._progressBar)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.Fixed3D
		self.MaximizeBox = False
		self.MinimizeBox = False
		self.Name = "progressForm"
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
		self.Text = "progressForm"
		self.FormClosing += self.ProgressFormFormClosing
		self.FormClosed += self.ProgressFormFormClosed
		self.Load += self.ProgressFormLoad
		self.Shown += self.ProgressFormShown
		self.ResumeLayout(False)
		self.PerformLayout()


	def ProgressFormLoad(self, sender, e):
		pass

	def BackgroundWorker1DoWork(self, sender, e):

		theLog = ''
		parserErrors = 0
		procNames = {0:'TEST',1:'Display Only',2:'FULL'}

		theLog += 'Process level {0}\n'.format(procNames[self.theProcess])
		
		if self.theProcess == 0: # just for testing
			i = 0
			while i <= 100:
				i += 1
				# Report progress to 'UI' thread
				self._backgroundWorker1.ReportProgress(i)
				# Simulate long task
				System.Threading.Thread.Sleep(100)
			return

		# ------------------------------------------------------
		# run the parsed code over the books:
		# ------------------------------------------------------
		dtStarted = System.DateTime.Now
		theLog += 'Time: {0}\n'.format(dtStarted)

		if self.theProcess in (PROCESS_ON, PROCESS_OFF):
			self.maxVal = self.theBooks.Length
			self._progressBar.Maximum = self.maxVal
			self._progressBar.Step = 1
			f=open(globalvars.LOGFILE, "w")	# open logfile

			# no books or values were touched until now:
			allBooksTouched = 0

			for book in self.theBooks:
				if not self._backgroundWorker1.CancellationPending: 
					self.stepsPerformed += 1
					self._backgroundWorker1.ReportProgress(self.stepsPerformed / self.maxVal * 100)
					
					#Retrieve all pages and the scanner page index
					pages, scanner_page, page_name = mspProcesser.getScannerPage(book)
					theLog += mspProcesser.theLog

					if mspProcesser.error:
						self.stop_the_Worker = True
						break
					
					if scanner_page and scanner_page.PageType != markScannerAs:
						#Since the comic might have bad ComicInfo (especially if unopened)
						#Get the books info, update the pages and save it back before marking the deleted page
						ci = book.GetInfo()
						ci.SetPages(pages)
						book.SetInfo(ci)

						theLog += 'Page #{3} {0} found in {1}. Setting to {2}\n'.format(page_name, book.Caption, markScannerAs, scanner_page.ImageIndex)
						if self.theProcess == PROCESS_OFF:
							continue
						else:
							book.UpdatePageType(scanner_page, markScannerAs)
						allBooksTouched += 1
				else:
					theLog += ('\n\nExcecution cancelled by user.')
					self.cancelledByUser = True
					break
				if self.stop_the_Worker == True: break
			
			if allBooksTouched > 0:
				theLog += '\n\n' + '*' * 60 + '\n'
				theLog += '%d scanner pages were marked' % (allBooksTouched)
				theLog += '*' * 60 + '\n'
					
			dtEnded = System.DateTime.Now
			dtDuration = dtEnded - dtStarted
			theLog += 'Time Completed: {0}; Processing {2} books took {1}\n'.format(dtEnded, dtDuration, self.maxVal)
			f.write(theLog)
			f.close()
		return
			

	def BackgroundWorker1ProgressChanged(self, sender, e):
		# progressBar.Value = xxx  did not update the progressBar properly
		# so we use PerformStep()
		self._progressBar.PerformStep()
		self._label1.Text = 'Mark Scanner Page worked on %d books' % self.stepsPerformed
		return

	def BackgroundWorker1RunWorkerCompleted(self, sender, e):
		self.Close()
		pass

	def ProgressFormShown(self, sender, e):
		self._backgroundWorker1.RunWorkerAsync()
		
	def ButtonCancelClick(self, sender, e):
		self._backgroundWorker1.CancelAsync()
		pass
	
	def ProgressFormFormClosed(self, sender, e):
		self._backgroundWorker1.CancelAsync()

		
	def ProgressFormFormClosing(self, sender, e):
		self._backgroundWorker1.CancelAsync()

	def BackgroundWorker1Cancellation(self, sender, e):
		self.stop_the_Worker = True


