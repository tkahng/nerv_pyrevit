#!/usr/bin/ipy
import testpath
import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from System.Windows.Forms import Application, Form, TextBox
from System.Windows.Forms import ToolBar, ToolBarButton, OpenFileDialog
from System.Windows.Forms import DialogResult, ScrollBars, DockStyle


class IForm(Form):

    def __init__(self):
        self.Text = "OpenDialog"

        toolbar = ToolBar()
        toolbar.Parent = self
        openb = ToolBarButton()


        self.textbox = TextBox()
        self.textbox.Parent = self
        self.textbox.Multiline = True
        self.textbox.ScrollBars = ScrollBars.Both
        self.textbox.WordWrap = False
        self.textbox.Parent = self
        self.textbox.Dock = DockStyle.Fill


        toolbar.Buttons.Add(openb)
        toolbar.ButtonClick += self.OnClicked


        self.CenterToScreen()

    def OnClicked(self, sender, event):
        dialog = OpenFileDialog()
        dialog.Filter = "C# files (*.cs)|*.cs"

        if dialog.ShowDialog(self) == DialogResult.OK:
            f = open(dialog.FileName)
            data = f.read()
            f.Close()
            self.textbox.Text = data


Application.Run(IForm())