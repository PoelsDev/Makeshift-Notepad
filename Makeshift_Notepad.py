# First things, first. Import the wxPython package.
import wx, os

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800,400))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.makeMenuBar()
        self.CreateStatusBar()
        self.SetStatusText("This is a makeshift notepad.")
        self.Show(True)

    def makeMenuBar(self):
        #Create menu.
        menuFile = wx.Menu()
        menuTools = wx.Menu()
        menuExtra = wx.Menu()

        #Add stuff to the menu.
        file_new = menuFile.Append(wx.ID_NEW, "New", "New & empty file.")
        file_open = menuFile.Append(wx.ID_OPEN, "Open", "Open an existing file.")
        file_saveas = menuFile.Append(wx.ID_SAVEAS, "Save As", "Save your .txt-file.")

        tools_copy = menuTools.Append(wx.ID_COPY, "Copy", "Copy")
        tools_paste = menuTools.Append(wx.ID_PASTE,"Paste", "Paste")

        extra_about = menuExtra.Append(wx.ID_ABOUT, "About", "Information about this program.")

        #Create a menu bar to display the just-created menu.
        menuBar = wx.MenuBar()
        menuBar.Append(menuFile, "File") #Add the wx.Menu: filemenu
        menuBar.Append(menuTools,"Tools")
        menuBar.Append(menuExtra, "Extra")
        self.SetMenuBar(menuBar)
        
        #Bind an event to a menu
        self.Bind(wx.EVT_MENU, self.OnAbout, extra_about)

        self.Bind(wx.EVT_MENU, self.OnNew, file_new)
        self.Bind(wx.EVT_MENU, self.OnOpen, file_open)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, file_saveas)

        self.Bind(wx.EVT_MENU, self.OnCopy, tools_copy)
        self.Bind(wx.EVT_MENU, self.OnPaste, tools_paste)

    def OnAbout(self, e):
        #Create & show the "About" messagebox.
        dlg = wx.MessageDialog(self, "This is a work-in-progress makeshift Notepad.", "About Makeshift Notepad.", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
    
    def OnNew(self, e):
        self.control.SetValue("")
    
    def OnOpen(self, e):
        self.dirname = ''
        #Open Windows Explorer & choose your file.
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.FD_OPEN)
        #Check if "OK" has been pressed
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            #Textfiles which are not in a directory.
            if(self.dirname == "C:"):
                self.dirname = self.dirname + "\ "
                self.dirname = self.dirname.strip()
                f = open(os.path.join(self.dirname, self.filename), 'r')
            else:
                f = open(os.path.join(self.dirname, self.filename), 'r')
            #Set the TextCtrl value to the value of the text file.
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()
    
    def OnSaveAs(self, e):
        #Saving options (extensions)
        wildcard = "TXT files (*.txt)|*.txt"
        #Open File Explorer
        dlg = wx.FileDialog(
            self, message="Save file as ...", 
            defaultDir="", 
            defaultFile="", wildcard=wildcard, style=wx.FD_SAVE
            )
        #Put the TextCtrl Value in a string and in the file.
        if dlg.ShowModal() == wx.ID_OK:
            contents = self.control.GetValue()
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            filehandle = open(os.path.join(self.dirname, self.filename), 'w')
            filehandle.write(contents)
            filehandle.close()
        dlg.Destroy()

    def OnCopy(self, e):
        text = self.FindFocus()
        if text is not None:
            text.Copy()
    
    def OnPaste(self, e):
        text = ""
        if not wx.TheClipboard.IsOpened():
            do = wx.TextDataObject()
            wx.TheClipboard.Open()
            success = wx.TheClipboard.GetData(do)
            wx.TheClipboard.Close()
            if success:
                self.control.SetValue(self.control.Value + do.GetText())
            
        

if __name__ == "__main__":
    # Next, create an application object.
    app = wx.App()
    
    #Create an instance of "MyFrame" which makes a wx.Frame
    frm = MyFrame(None,"Makeshift Notepad")

    # Start the event loop.
    app.MainLoop()