
import System.Drawing
import System.Windows.Forms
from System.Windows.Forms import OpenFileDialog, SaveFileDialog

import System.IO
from System.IO import File

from System.Drawing import *
from System.Windows.Forms import *

import globalvars

#import aboutForm
#from aboutForm import aboutForm

#parser = utils.parser()

class configuratorForm(Form):
	def __init__(self):
		self.InitializeComponent()
		self.theFile = ''
		self.textBoxHeight = 500
		self.textBoxMinHeight = 260
		self.textBoxWidth = 760
		self.textBoxMinWidth = 717
		self.MaximizeBox = False
		self.MinimizeBox = False
		self.Icon = Icon(globalvars.ICON_SMALL)
		
	def InitializeComponent(self):
		self._components = System.ComponentModel.Container()
		self._textBox1 = System.Windows.Forms.TextBox()
		self._statusStrip1 = System.Windows.Forms.StatusStrip()
		self._toolStripStatusLabel1 = System.Windows.Forms.ToolStripStatusLabel()
		self._toolStripStatusLabel2 = System.Windows.Forms.ToolStripStatusLabel()
		self._toolStripStatusLabel3 = System.Windows.Forms.ToolStripStatusLabel()
		self._statusStrip1.SuspendLayout()
		self.SuspendLayout()
		# 
		# textBox1
		# 
		self._textBox1.AcceptsReturn = True
		self._textBox1.AcceptsTab = True
		self._textBox1.Font = System.Drawing.Font("Courier New", 8.25, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._textBox1.HideSelection = False
		self._textBox1.Location = System.Drawing.Point(12, 52)
		self._textBox1.Multiline = True
		self._textBox1.Name = "textBox1"
		self._textBox1.ScrollBars = System.Windows.Forms.ScrollBars.Both
		self._textBox1.Size = System.Drawing.Size(722, 260)
		self._textBox1.TabIndex = 0
		self._textBox1.TabStop = False
		self._textBox1.WordWrap = False
		self._textBox1.Click += self.TextBox1Click
		self._textBox1.KeyPress += self.TextBox1KeyPress
		self._textBox1.KeyUp += self.TextBox1KeyUp
		self._textBox1.Leave += self.TextBox1Leave
		self._textBox1.MouseDown += self.TextBox1MouseDown
		# 
		# statusStrip1
		# 
		self._statusStrip1.Items.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._toolStripStatusLabel1,
			self._toolStripStatusLabel2,
			self._toolStripStatusLabel3]))
		self._statusStrip1.Location = System.Drawing.Point(0, 569)
		self._statusStrip1.Name = "statusStrip1"
		self._statusStrip1.Size = System.Drawing.Size(784, 30)
		self._statusStrip1.TabIndex = 2
		self._statusStrip1.Text = "statusStrip1"
		# 
		# toolStripStatusLabel1
		# 
		self._toolStripStatusLabel1.AutoSize = False
		self._toolStripStatusLabel1.BorderSides = System.Windows.Forms.ToolStripStatusLabelBorderSides.Left | System.Windows.Forms.ToolStripStatusLabelBorderSides.Top | System.Windows.Forms.ToolStripStatusLabelBorderSides.Right | System.Windows.Forms.ToolStripStatusLabelBorderSides.Bottom
		self._toolStripStatusLabel1.BorderStyle = System.Windows.Forms.Border3DStyle.SunkenInner
		self._toolStripStatusLabel1.Name = "toolStripStatusLabel1"
		self._toolStripStatusLabel1.Size = System.Drawing.Size(100, 25)
		self._toolStripStatusLabel1.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# toolStripStatusLabel2
		# 
		self._toolStripStatusLabel2.AutoSize = False
		self._toolStripStatusLabel2.BorderSides = System.Windows.Forms.ToolStripStatusLabelBorderSides.Left | System.Windows.Forms.ToolStripStatusLabelBorderSides.Top | System.Windows.Forms.ToolStripStatusLabelBorderSides.Right | System.Windows.Forms.ToolStripStatusLabelBorderSides.Bottom
		self._toolStripStatusLabel2.BorderStyle = System.Windows.Forms.Border3DStyle.SunkenInner
		self._toolStripStatusLabel2.Name = "toolStripStatusLabel2"
		self._toolStripStatusLabel2.Size = System.Drawing.Size(30, 25)
		# 
		# configuratorForm
		# 
		self.ClientSize = System.Drawing.Size(784, 599)
		self.Controls.Add(self._textBox1)
		self.Controls.Add(self._statusStrip1)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.Fixed3D
		self.MaximizeBox = False
		self.Name = "configuratorForm"
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent
		self.Text = "Form1"
		self.FormClosing += self.ConfiguratorFormFormClosing
		self.Load += self.ConfiguratorFormLoad
		self._statusStrip1.ResumeLayout(False)
		self._statusStrip1.PerformLayout()
		self.ResumeLayout(False)
		self.PerformLayout()

	def TextBox1Click(self, sender, e):
		self.setLineInfo()
		
	def setLineInfo(self):
		line = self.currentLine()
		col = self._textBox1.SelectionStart - self._textBox1.GetFirstCharIndexFromLine(line);
		self._toolStripStatusLabel1.Text = 'Line %d - Col %d' % (line + 1, col + 1)

	def TextBox1KeyPress(self, sender, e):
		self.setLineInfo()

	def TextBox1KeyUp(self, sender, e):
		self.setLineInfo()

	def showTheFile(self):
		if self.theFile != '':			
			self._textBox1.Text  = self.readFile()
	
	def readFile(self):
		if File.Exists(self.theFile):
			s = File.ReadAllLines(self.theFile)
			tmp = str('')
			for line in s:
				tmp += '%s%s' % (line, System.Environment.NewLine)
			if len(s) == 0 and theFile == globalvars.LOGFILE:
				tmp = 'Your criteria matched no book. No data was touched by the Data Manager.'
			return tmp
		else:
			return str('')

	def setFile(self, f):
		self.theFile = f
		self.showTheFile()
		self.setLineInfo()
		return

	def ConfiguratorFormLoad(self, sender, e):
		self.Text = 'Mark Scanner Pages logfile'
		self.showTheFile
		self._textBox1.SelectionLength = 0
		self._textBox1.SelectionStart = 1
		self.setLineInfo()

	def ConfiguratorFormFormClosing(self, sender, e):
		pass

	def TextBox1MouseDown(self, sender, e):
		pass

	def TextBox1Leave(self, sender, e):
		if self._textBox1.SelectionLength == 0:
			self._textBox1.SelectionLength = 1
		
	def currentLine(self):
		return self._textBox1.GetLineFromCharIndex(self._textBox1.SelectionStart)
	
	def lineLength(self, line):
		# returns the length of line 'line'
		# returns 0 if line out of index
		# note: lines start with index 0
		line = int(line)
		tmp = self._textBox1.Text.split(System.Environment.NewLine)
		if line > len(tmp) - 1: return 0		
		return len(tmp[line])
	
	def lineContent(self,line):
		# returns the texxt of line 'line'
		# returns '' if line out of index
		# note: lines start with index 0
		line = int(line)
		tmp = self._textBox1.Text.split(System.Environment.NewLine)
		if line > len(tmp) - 1: return 0
		return tmp[line]
		
		
	def selectLine(self,line):
		'''
		highlights the line 'line'
		attention: lines start with index 0
		'''
		line = int(line) 
		self._textBox1.SelectionStart = self._textBox1.GetFirstCharIndexFromLine(line)
		self._textBox1.SelectionLength = self.lineLength(line)
		self._textBox1.ScrollToCaret()
