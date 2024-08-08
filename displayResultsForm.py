import clr
import System
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import *
from System.Drawing import *

import globalvars

class displayResultsForm(Form):

	def __init__(self):
		self.Width = 300
		self.Height = 140
		self.StartPosition = FormStartPosition.CenterScreen
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.Fixed3D
		self.Icon = Icon(globalvars.ICON_SMALL)
		self.MaximizeBox = False
		self.MinimizeBox = False
		self.MaximizeBox = False
		self.Text = 'MSP for ComicRack %s' % globalvars.VERSION

		self.label = Label()
		self.label.Location = Point(10, 20)
		self.label.Width = 250
		self.label.Height = 30

		self.buttonYes = Button()
		self.buttonYes.Location = Point(10,70)
		self.buttonYes.Text = 'Yes'
		self.buttonYes.DialogResult = DialogResult.Yes

		self.buttonNo = Button()
		self.buttonNo.Location = Point(130,70)
		self.buttonNo.Text = 'No'
		self.buttonNo.DialogResult = DialogResult.No

		self.Controls.Add(self.label)
		self.Controls.Add(self.buttonYes)
		self.Controls.Add(self.buttonNo)

	def configure(self, label):
		self.label.Text = label
