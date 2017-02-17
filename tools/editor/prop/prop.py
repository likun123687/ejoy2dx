#coding:utf-8

import wx
import wx.propgrid as wxpg

import os
import json
from particle import ParticleProp
from label import LabelProp

template_path = os.path.join(os.path.dirname(__file__), "particle.json")
with open(template_path) as f:
	template = json.loads(f.read())

colorMap = {
	"startColor":("startColorRed", "startColorGreen", "startColorBlue"),\
	"startColorVariance":("startColorVarianceRed", "startColorVarianceGreen", "startColorVarianceBlue"),\
	"finishColor":("finishColorRed", "finishColorGreen", "finishColorBlue"),\
	"finishColorVariance":("finishColorVarianceRed", "finishColorVarianceGreen", "finishColorVarianceBlue"),\
}
rootCats = ("Emitter", "ParticleSettings", "ColorSettings")
emitterTypes = ("Gravity", "Radial")

class PropPanel( wx.Panel ):

	def __init__( self, parent, edit_callback ):
		wx.Panel.__init__(self, parent, wx.ID_ANY)
		self.edit_callback = edit_callback

		self.panel = panel = wx.Panel(self, wx.ID_ANY)
		topsizer = wx.BoxSizer(wx.VERTICAL)

		# Difference between using PropertyGridManager vs PropertyGrid is that
		# the manager supports multiple pages and a description box.
		self.pg = pg = wxpg.PropertyGridManager(panel,
																						style=wxpg.PG_SPLITTER_AUTO_CENTER |
																						# wxpg.PG_AUTO_SORT |
																						wxpg.PG_TOOLBAR)

		self.particle = ParticleProp(self.pg, self.edit_callback)
		self.label = LabelProp(self.pg, self.edit_callback)
		self.current = None

		# Show help as tooltips
		# pg.SetExtraStyle(wxpg.PG_EX_HELP_AS_TOOLTIPS)

		pg.Bind( wxpg.EVT_PG_CHANGED, self.OnPropGridChange )
		# pg.Bind( wxpg.EVT_PG_PAGE_CHANGED, self.OnPropGridPageChange )
		# pg.Bind( wxpg.EVT_PG_SELECTED, self.OnPropGridSelect )
		# pg.Bind( wxpg.EVT_PG_RIGHT_CLICK, self.OnPropGridRightClick )


		# self.pg.AddPage( "Particle" )
		# self.init_prop()
		
		topsizer.Add(pg, 1, wx.EXPAND)
		panel.SetSizer(topsizer)
		topsizer.SetSizeHints(panel)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(panel, 1, wx.EXPAND)
		self.SetSizer(sizer)
		self.SetAutoLayout(True)

	def Clear(self):
		if self.pg.GetPageCount() > 0:
			self.pg.RemovePage(0)

	def SetData(self, data):
		ope = data["ope"]
		if not ope: return

		self.Clear()
		self.current = None
		if ope == "particle_cfg":
			self.current = self.particle
		elif ope == "label_cfg":
			self.current = self.label
			
		if self.current:
			self.current.ShowData(data["data"])

	def OnPropGridChange(self, event):
		if self.current:
			self.current.OnPropGridChange(event)