class OutputFormatter(object):
    def __init__(self,notebook,FocusReturn):
        self.notebook=notebook
        self.textctrl=notebook.GetPage(0).GetChildren()[0]
        self.FocusReturn=FocusReturn

    def infodisplay(self,msg,switchfocus=True): # takes list of lines and writes to GENERAL tab
        #support some very basic formatting. if line startswith F! then 3rd char indicates type of line
    # F! chars
    # H - line is main header. Will be indented once, bulleted, \n\n before & \n\n\n after
    # h - line is sub header. Will be bulleted. \n before and \n\n after
    #
        if type(msg)==type('a string'):
            msg=[msg]
        if switchfocus:
            self.notebook.SetSelection(0)
        bullet=' * '
        for line in msg:
            linestyle='N' # NORMAL line. no indent no bullet \n after
            if line.startswith('F!'):
                linestyle=line[2:3]
                line=line[3:]
            if linestyle=='H':
                fline='\n\n\t'+bullet+line+'\n\n\n'
            elif linestyle=='h':
                fline='\n'+bullet+line+'\n\n'
            else:
                fline=line.rstrip()+'\n'
            self.textctrl.AppendText(fline)
        self.textctrl.ScrollLines(1)
        self.FocusReturn.SetFocus()
