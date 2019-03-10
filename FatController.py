#!/usr/bin/python
#
#Copyright 2005 MatthewWarren.matthew_j_warren@hotmail.com

fcversion="v1f11r1a"
__version__ = fcversion

import os,sys,telnetlib,re,shutil,time,threading,pprint 

import config
import FC_entity,FC_daemonschedule,FC_daemontask,FC_daemon
import FC_ScheduledTask,FC_ScheduledTaskHandler,FC_ThreadedScheduler,FC_entitymanager,FC_daemonmanager
import FC_ENTITYGROUP,FC_LOCAL,FC_DUMB,FC_TSM,FC_TELNET
import wx
import FC_formatter

startmessage='Welcome to FatController '+fcversion


class FatController(wx.Frame):
    '''is essentially the command processor'''
    
    def __init__(self):
        self.aliases={}  #Dictionary of aliasname/command 
        self.substitutions={}
        self.scripts={}
        self.trace={}
        self.FCScheduler=FC_ThreadedScheduler.ThreadedScheduler()
        self.FCScheduler.start()
        self.opts={}

        #############
        # GUI bits
        #############
        wx.Frame.__init__(self,None,-1,"FatController",size=(1024,768))

        # Main Splitters
        self.VSplitter=wx.SplitterWindow(self,-1,(0,0),(0,0),wx.SP_3DSASH)
        self.VSplitter.SetMinimumPaneSize(20)
        self.LSplitter=wx.SplitterWindow(self.VSplitter,-1,(0,0),(0,0),wx.SP_3DSASH)
        self.LSplitter.SetMinimumPaneSize(20)
        self.RSplitter=wx.SplitterWindow(self.VSplitter,-1,(0,0),(0,0),wx.SP_3DSASH)
        self.RSplitter.SetMinimumPaneSize(20)

        # Base panels
        self.TLPanel=wx.Panel(self.LSplitter,style=wx.NO_BORDER)
        self.BLPanel=wx.Panel(self.LSplitter,style=wx.NO_BORDER)
        self.TRPanel=wx.Panel(self.RSplitter,style=wx.NO_BORDER)
        self.BRPanel=wx.Panel(self.RSplitter,style=wx.NO_BORDER)

        self.VSplitter.SplitVertically(self.LSplitter,self.RSplitter,-100)
        self.LSplitter.SplitHorizontally(self.TLPanel,self.BLPanel,-100)
        self.RSplitter.SplitHorizontally(self.TRPanel,self.BRPanel,-100)

        # Starting controls
        self.OutBook=wx.Notebook(self.TLPanel,-1,(0,0),(100,100),style=wx.NB_TOP|wx.NB_MULTILINE,name='notebook name')
        self.IDOutBook=1002
        
            #wx.EVT_COMMAND(self.IDOutBook,wx.EVT_COMMAND_NOTEBOOK_PAGE_CHANGED,self.NotebookPageChangeEvent)
        self.FirstPagePanel=wx.Panel(self.OutBook,style=wx.NO_BORDER)
        self.OutBook.AddPage(self.FirstPagePanel,'GENERAL',True,-1)
        self.FirstPageTextCtrl=wx.TextCtrl(self.FirstPagePanel,-1,'',(0,0),(0,0),wx.TE_MULTILINE|wx.TE_DONTWRAP|wx.TE_RICH2)
        self.FirstPageTextCtrl.SetOwnFont(wx.Font(8,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))
        self.FirstPageTextCtrl.SetValue(startmessage)

        self.IDShellTextCtrl=1001 # used for tying to events
        self.ShellTextCtrl=wx.TextCtrl(self.BLPanel,self.IDShellTextCtrl,'',(0,0),(0,18),wx.TE_PROCESS_ENTER)
        self.display=FC_formatter.OutputFormatter(self.OutBook,self.ShellTextCtrl)
        #
        # Now make the Daemon and Entity managers as the items they require have been defined
        #
        self.EntityManager=FC_entitymanager.entitymanager(self.OutBook,self.ShellTextCtrl)
        self.DaemonManager=FC_daemonmanager.daemonmanager(self.EntityManager,self.FCScheduler,self)
        
        #
        #decide initial prompt value
        #
        
        self.prompt=''
        self.prompt='FC:'+self.EntityManager.LastExecutedEntity+'> '
        self.ShellTextCtrl.AppendText(self.prompt)

        wx.EVT_TEXT_ENTER(self.ShellTextCtrl,self.IDShellTextCtrl,self.ShellWindowEnterEvent)

        self.ObjectTreeCtrl=wx.TreeCtrl(self.TRPanel,-1,(0,0),(0,0))
        #self.OutBook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED,self.NotebookPagechangeEvent)


        # Sizers

        #add a sizer to stretch notebook
        self.OutBookSizer=wx.BoxSizer(wx.VERTICAL)
        self.OutBookSizer.Add(self.OutBook,1,wx.EXPAND|wx.ALL,5)
        self.TLPanel.SetSizer(self.OutBookSizer)
        self.OutBook.SetAutoLayout(True)
        self.OutBookSizer.Fit(self.TLPanel)

        #sizer for shell text window
        self.ShellTextSizer=wx.FlexGridSizer(2,1,1,1)
        self.ShellTextSizer.SetFlexibleDirection(wx.HORIZONTAL)
        self.ShellTextSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_NONE)
        self.ShellTextSizer.AddGrowableCol(0)
        self.ShellTextSizer.Add(self.ShellTextCtrl,0,wx.EXPAND)
        self.ShellTextCtrl.SetAutoLayout(True)

        #add a grid sizer to a growable (down) row in flexgridsizer
        #for alert indicators
        #self.ShellTextSizer.AddGrowableRow(1)
        #self.AlertIconSizer=wx.GridSizer(0,0,0,0)
        #self.AlertIconSizer.SetCols(8)
        #self.AlertIconSizer.SetRows(3)
        #self.ShellTextSizer.Add(self.AlertIconSizer,wx.EXPAND)
        
        #make an image+label to display in grid sizer
        #
        # make temp 10 img,lbl pairs
        #
        #self.ctrlslbls=[]
        #for n in range(1,11):
        #    img=wx.Image('c:\\program files\\yab\\fatcontroller\\redalert.jpg', wx.BITMAP_TYPE_JPEG)
        #    bmp=wx.BitmapFromImage(img)
        #    ctrl=wx.StaticBitmap(self.BLPanel,-1,bmp,size=(12,12),name='name of bmp')
        #    ctrl.SetAutoLayout(True)
        #    lbl=wx.StaticText(self.BLPanel,-1,'test label'+str(n),name='named text')
        #    lbl.SetAutoLayout(True)
        #    self.AlertIconSizer.Add(ctrl)
        #    self.AlertIconSizer.Add(lbl)

        
        self.BLPanel.SetSizer(self.ShellTextSizer)
        self.ShellTextSizer.Fit(self.BLPanel)
        
        

        #sizer for ObjectTreeCtrl
        self.ObjectTreeSizer=wx.BoxSizer(wx.VERTICAL)
        self.ObjectTreeSizer.Add(self.ObjectTreeCtrl,1,wx.EXPAND)
        self.TRPanel.SetSizer(self.ObjectTreeSizer)
        self.ObjectTreeCtrl.SetAutoLayout(True)
        self.ObjectTreeSizer.Fit(self.TRPanel)


        #Add a sizer to stretch self.FirstPageTextCtrl
        self.FirstPageSizer=wx.BoxSizer(wx.VERTICAL)
        self.FirstPageSizer.Add(self.FirstPageTextCtrl,1,wx.EXPAND,5)
        self.FirstPagePanel.SetSizer(self.FirstPageSizer)
        self.FirstPageTextCtrl.SetAutoLayout(True)
        self.FirstPageSizer.Fit(self.FirstPagePanel)


        #load stuff to build tree ctrl
        self.processcommand('load general')
        #self.FirstPageTextAttribs=wx.TextAttr(font=wx.Font(8,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))
        #self.FirstPageTextCtrl.SetStyle(0,len(self.FirstPageTextCtrl.GetValue()),self.FirstPageTextAttribs)
        # populate the TreeCtrl
        self.ConfigRoot=self.ObjectTreeCtrl.AddRoot("Configure Objects:")
        self.Entities=self.EntityManager.getentitylist()
        self.EntityRoot=self.ObjectTreeCtrl.AppendItem(self.ConfigRoot,"Entities")
        self.Daemons=self.DaemonManager.getDaemons()
        self.DaemonRoot=self.ObjectTreeCtrl.AppendItem(self.ConfigRoot,"Daemons")
        self.ScriptsRoot=self.ObjectTreeCtrl.AppendItem(self.ConfigRoot,"scripts")
        self.AliasesRoot=self.ObjectTreeCtrl.AppendItem(self.ConfigRoot,"aliases")
        self.SubsRoot=self.ObjectTreeCtrl.AppendItem(self.ConfigRoot,"substitutions")
        self.InsertIntoTreeCtrl(self.Entities.keys(),self.ObjectTreeCtrl,self.EntityRoot)
        self.InsertIntoTreeCtrl(self.Daemons.keys(),self.ObjectTreeCtrl,self.DaemonRoot)
        self.InsertIntoTreeCtrl(self.scripts.keys(),self.ObjectTreeCtrl,self.ScriptsRoot)
        self.InsertIntoTreeCtrl(self.aliases.keys(),self.ObjectTreeCtrl,self.AliasesRoot)
        self.InsertIntoTreeCtrl(self.substitutions.keys(),self.ObjectTreeCtrl,self.SubsRoot)

    def InsertIntoTreeCtrl(self,ListOfItems,Ctrl,RootNode):
        for item in ListOfItems:
            Ctrl.AppendItem(RootNode,item.__str__())

    def ShellWindowEnterEvent(self,wxcommandevent):
        textCtrl=wxcommandevent.GetEventObject()
        CommandInput=textCtrl.GetValue()
        if len(CommandInput)<len(self.prompt):
            CommandInput=self.prompt+CommandInput
        InputCommand=CommandInput[len(self.prompt):]
        self.processcommand(InputCommand)
        OldShellWindowText=textCtrl.GetValue()
        if len(self.DaemonManager.getOutstandingAlerts())>0:
            self.ShellTextCtrl.SetBackgroundColour(wx.Colour(255,200,200))
            self.ShellTextCtrl.Refresh()
        else:
            self.ShellTextCtrl.SetBackgroundColour(wx.Colour(255,255,255))
            self.ShellTextCtrl.Refresh()
        self.prompt='FC:'+self.EntityManager.LastExecutedEntity+'> '
        self.ShellTextCtrl.SetValue("")
        self.ShellTextCtrl.AppendText(self.prompt)
        #self.FirstPageTextCtrl.SetStyle(0,len(self.FirstPageTextCtrl.GetValue()),self.FirstPageTextAttribs)

    def NotebookPagechangeEvent(self,wxcommandevent): #force focus to input box each page change
        self.ShellTextCtrl.SetFocus()
        wxcommandevent.Skip()

    ###########
    #

    #TODO: logger

    def dbg(self,Msg,Fn,execclass=None):
        try:
            if (self.trace[Fn] or self.trace["ALL"]):
                self.display.infodisplay('DBG:'+Fn+': '+Msg)
        except KeyError: 
            pass
    #
    #
    ###########

    # start fc methods

    def indicate_alert_state(self):
        self.ShellTextCtrl.SetBackgroundColour(wx.Colour(255,200,200))
        self.ShellTextCtrl.ClearBackground()
        self.ShellTextCtrl.Refresh()

    def reset_alert_indicator(self):
        self.ShellTextCtrl.SetBackgroundColour(wx.Colour(255,255,255))
        self.ShellTextCtrl.ClearBackground()
        self.ShellTextCtrl.Refresh()

    def show_alert_queue(self):
        self.display.infodisplay('F!HAlert Queue:')
        generatedalerts=self.DaemonManager.getOutstandingAlerts()
        ctr=0
        info=[]
        for alert in generatedalerts:
            info.append(str(ctr)+' : '+alert)
            ctr=ctr+1
        self.display.infodisplay(info)
        
    def show_active_daemons(self):
        self.display.infodisplay('F!HCurrently Active Daemons:')
        info=[]
        for active in self.DaemonManager.getactivedaemons():
            info.append(active)
        self.display.infodisplay(info)
        
    def show_daemons(self):
        outlines=self.DaemonManager.getprettydaemons()
        self.display.infodisplay('F!HCurrently defined daemons/tasks/schedules and associated entities:')
        self.display.infodisplay(outlines)
                 
    def create_daemon(self,name):
        self.DaemonManager.addDaemon(name)
        self.display.infodisplay('Daemon '+name+' Defined.')
        
    def remove_daemon(self,name):
        self.DaemonManager.deleteDaemon(name)
        self.display.infodisplay('Daemon '+name+' Deleted.')

    def schedule_daemon(self,name,begin,end,period):
        self.DaemonManager.setdaemonschedule(name,begin,end,period)
        self.display.infodisplay('Schedule for daemon '+name+' Begin='+begin+' end='+end+' period='+period+' Set.')
            
    def add_daemon_task(self,daemonname,taskname,command):
        self.DaemonManager.addTask(daemonname,taskname,command)
        self.display.infodisplay('Task '+taskname+' for daemon '+daemonname+' '.join(command)+' Defined.')

    def remove_daemon_task(self,daemonname,taskname):
        self.DaemonManager.deleteTask(daemonname,taskname)
        self.display.infodisplay('Daemon '+daemonname+'Task '+taskname+' Deleted.')

    def add_daemon_task_collector(self,daemonname,taskname,collectorname,tag,skip,format,file):
        self.DaemonManager.addCollector(daemonname,taskname,collectorname,tag,skip,format,file)
        self.display.infodisplay('Collector '+collectorname+' for task '+taskname+' owned by daemon '+daemonname+' Datatag '+tag+' Skip '+skip+' Format '+format+' File '+file+' Defined.')

    def remove_daemon_task_collector(self,daemonname,taskname,collectorname):
        self.DaemonManager.deleteCollector(daemonname,taskname,collectorname)
        self.display.infodisplay('Daemon '+daemonname+' task '+taskname+' Collector '+collectorname+' Deleted.')

    def add_daemon_task_entity(self,daemonname,taskname,entityname):
        self.DaemonManager.subscribeEntity(daemonname,taskname,entityname)
        self.display.infodisplay('Daemon '+daemonname+' task '+taskname+' Entity '+entityname+' Subscribed.')

    def remove_daemon_task_entity(self,daemonname,taskname,entityname):
        self.DaemonManager.unsubscribeEntity(daemonname,taskname,entityname)
        self.display.infodisplay('Daemon '+daemonname+' task '+taskname+' Entity '+entityname+' Deleted.')

    def add_daemon_task_collector_alert(self,daemonname,taskname,collectorname,minval,maxval,textmessage,pass_script,fail_script):
        pass_script=pass_script[0]
        fail_script=fail_script[0]
        if not self.isScript(pass_script):
            pass_script='NoScript'
        if not self.isScript(fail_script):
            fail_script='NoScript'
        self.DaemonManager.addAlert(daemonname,taskname,collectorname,minval,maxval,textmessage,pass_script,fail_script)
        self.display.infodisplay('Daemon '+daemonname+' task '+taskname+' collector '+collectorname+' Alert '+str(minval)+' '+str(maxval)+' '+textmessage+' scripts pass: '+pass_script+' fail: '+fail_script+' Defined.')

    def make_daemon_live(self,daemonname):
        DBGBN='FCmakedaemonlive'
        #dbg('Making daemon live.',DBGBN)
        #be carefull with the task naming here... what about removing from the middle of the list? will it pop() the same?
        #...and dont confuse scheduer tasks with daemon tasks...
        self.DaemonManager.makeLive(daemonname)
        self.display.infodisplay('Daemon '+daemonname+' Activated.')

    def update_daemon_task(self,daemonname,taskname,command):
        self.DaemonManager.updateTask(daemonname,taskname,command)
        self.display.infodisplay('Task '+taskname+' Updated.')

    def kill_daemon(self,daemonname):
        DBGBN='FCkilldaemon'
        self.DaemonManager.kill_daemon(daemonname)
        self.display.infodisplay('Daemon '+daemonname+' Deactivated.')

    def is_daemon(self,daemonname):
        return self.DaemonManager.is_daemon(daemonname)

    def get_alias_defines(self,AliasDict):
        DefinitionList=[]
        for a in AliasDict:
            DefinitionList.append('alias '+a+' '+' '.join(AliasDict[a]))
        return DefinitionList

    def get_substituted_defines(self,SubstituteDict):
        DefinitionList=[]
        for s in SubstituteDict:
            DefinitionList.append('substitute '+s+' '+' '.join(self.substitutions[s]))
        return DefinitionList

    def save_list_as_lines_with_cr(self,Filename,AList,clobber=0):
        if clobber:
            SaveToFile=file(Filename,'w')
        else:
            SaveToFile=file(Filename,'a')
        for Line in AList:
            SaveToFile.write(Line.rstrip()+'\n')
        SaveToFile.close()

    def save_data(self,pathandname):
        #save entities, then aliases, then options
        DBGBN='save_data'
        EntityDefinitionList=self.EntityManager.getdefines()
        AliasDefinitionList=self.get_alias_defines(self.aliases)
        SubstituteDefinitionList=self.get_substituted_defines(self.substitutions)
        classoptionlists=self.EntityManager.getclassoptiondefines()
        #dbg('classoptionlists is '+str(len(classoptionlists))+' elements',DBGBN)
        fatcontrolleroptionlist=self.getfatcontrolleroptiondefines()
        scriptdefinitions=self.getscriptdefines()
        #
        #This block saves daemons and activestates #############################
        daemondefines=self.DaemonManager.getdaemondefines() #FC function returns list
        scheduledefines=self.DaemonManager.getscheduledefines() #FC function returns a list
        taskdefines=self.DaemonManager.gettaskdefines() # FC function returns a list
        collectordefines=self.DaemonManager.getcollectordefines() #
        alertdefines=self.DaemonManager.getalertdefines()
        subscriptiondefines=self.DaemonManager.getsubscriberdefines() # FC function returns a list
        activates=self.DaemonManager.getactivatedefines() # FC Function returns a list
        ########################################################################
        #
        self.save_list_as_lines_with_cr(pathandname,EntityDefinitionList,1)
        self.save_list_as_lines_with_cr(pathandname,AliasDefinitionList,0)
        self.save_list_as_lines_with_cr(pathandname,SubstituteDefinitionList,0)
        for optlist in classoptionlists:
            self.save_list_as_lines_with_cr(pathandname,optlist,0)
        self.save_list_as_lines_with_cr(pathandname,scriptdefinitions,0) # scripts before dameons cos daemons use 'em
        self.save_list_as_lines_with_cr(pathandname,fatcontrolleroptionlist)
        self.save_list_as_lines_with_cr(pathandname,daemondefines,0)
        self.save_list_as_lines_with_cr(pathandname,scheduledefines,0)
        self.save_list_as_lines_with_cr(pathandname,taskdefines,0)
        self.save_list_as_lines_with_cr(pathandname,collectordefines,0)
        self.save_list_as_lines_with_cr(pathandname,alertdefines,0)
        self.save_list_as_lines_with_cr(pathandname,subscriptiondefines,0)
        self.save_list_as_lines_with_cr(pathandname,activates,0)

        
    def save(self,WhatToSave,ProfileName):
        DBGBN='FCsave'
        if WhatToSave=='all':
            #DEVELOPR TOOLS MAKES THE SAVES INTO THE INSTALL PACKAGE
            # set FATCONTROLLER DEVELOPER yes
            # set FATCONTROLLER DEVELOPERPATH .....
            if self.opts.has_key('DEVELOPER') and self.opts['DEVELOPER']=='yes':
                pathandname=self.opts['DEVELOPERPATH']+ProfileName+'.sav'
                self.save_data(pathandname)
                pathandname=self.installroot+ProfileName+'.sav'
                #dbg('FATCONTROLLER DEVELOPER is yes. Doing save to DEVELOPERPATH',DBGBN)
                #dbg('-pathandname is '+pathandname,DBGBN)
                self.save_data(pathandname)
            else:
                pathandname=self.installroot+ProfileName+'.sav'
                #dbg('doing straight save. pathandname is '+pathandname,DBGBN)
                self.save_data(pathandname)
            #
        else:
            self.display.infodisplay('Error: Don\'t know how to save '+WhatToSave  +'.')
        self.display.infodisplay('Saved\t'+WhatToSave+'Succesfully.')

    def define_alias(self,Name,List):
        self.aliases[Name]=List
        self.display.infodisplay('Alias: '+Name+' '+' '.join(List)+' Defined.')

    def show_aliases(self,):
        info=['F!HDefined aliases:']
        for a in self.aliases:
            info.append(''+a+'\t'+' '.join(self.aliases[a]))
        self.display.infodisplay(info)
        
    def del_alias(self,AliasName):
        del self.aliases[AliasName]
        self.display.infodisplay('Alias '+AliasName+' Deleted.')

    def is_alias(Name):
        try:
            self.aliases[Name]
            return 1
        except KeyError:
            return 0

    def insert_to_script(self,scriptname,linenumber,cmdtokens):
        linenumber=int(linenumber)
        cmdlist=self.scripts[scriptname]
        lowerlist=cmdlist[:linenumber]
        lowerlist.append(' '.join(cmdtokens))
        for ul in cmdlist[linenumber:]:
            lowerlist.append(ul)
        self.scripts[scriptname]=lowerlist
        return 0

    def delfromscript(self,scriptname,linenumber):
        try:
            self.scripts[scriptname].pop(int(linenumber)-1)
        except IndexError:
            self.display.infodisplay("ERROR: No line "+linenumber+" to delete.")
        return 0

    def appendtoscript(self,scriptname,cmdtokens):
        cmdstring=' '.join(cmdtokens)
        if scriptname not in self.scripts:
            self.scripts[scriptname]=[]
            self.scripts[scriptname].append(cmdstring)
        else:
            self.scripts[scriptname].append(cmdstring)
        self.display.infodisplay('Line '+cmdstring+' Appended.')

    def delscript(self,scriptname):
        if self.isScript(scriptname):
            del self.scripts[scriptname]
            self.display.infodisplay('Script '+scriptname+' Deleted.')
        else:
            self.display.infodisplay('Could not find script '+scriptname+' to delete.')

    def runscript(self,scriptname,parmlist):
        num=1
        for parmsub in parmlist:
            self.processcommand('sub '+str(num)+' '+parmsub)
            num=num+1
        cmdlist=self.scripts[scriptname]
        for cmd in cmdlist:
            self.processcommand(cmd)
        num=1
        for parmsub in parmlist:
            self.processcommand('del sub '+str(num))
            num=num+1


    def isScript(self,scriptname):
        if scriptname not in self.scripts:
            return 0
        else:
            return 1

    def showscripts(self,scriptname):
        DBGBN='showscripts'
        if scriptname=='all':
            scriptlist=self.scripts.keys()
        else:
            scriptlist=[scriptname]
        #for script in scriptlist:
            #dbg('script '+script+' is in scriptlist to display',DBGBN)
        self.display.infodisplay('F!HDefined scripts:')
        for script in scriptlist:
            self.display.infodisplay('F!h'+script)
            ctr=1
            for cmds in self.scripts[script]:
                self.display.infodisplay(str(ctr)+' : '+cmds)
                ctr=ctr+1

    def getscriptdefines(self):
        definelist=[]
        for scriptname in self.scripts:
            for scriptline in self.scripts[scriptname]:
                definelist.append('addline '+scriptname+' '+scriptline)
        return definelist

    def message(self,msg):
        self.display.infodisplay(' '.join(msg))
                

    def definesubstitution(self,SubName,SubList):
        self.substitutions[SubName]=SubList
        self.display.infodisplay('Substitution '+SubName+' Defined.',switchfocus=False)

    def delsubstitution(self,SubName,switchfocus=False):
        del self.substitutions[SubName]
        self.display.infodisplay('Substitution '+SubName+' Deleted.',switchfocus=False)

    def showsubstitutions(self):
        self.display.infodisplay('F!HSubstitutions:')
        for s in self.substitutions:
            if len(s)<8:
                tabs='\t\t'
            else:
                tabs='\t'
            self.display.infodisplay(s+tabs+' '.join(self.substitutions[s]))

    def issubstitute(self,SubName):
        try:
            self.substitutions[SubName]
            return 1
        except KeyError:
            return 0
            
    def processsubstitutions(self,RawCmd):
        DBGBN='processsubstitutions'
        infprotect=1
        subhit=1
        while subhit==1:
            subhit=0
            for sub in self.substitutions:
                SubCheck=RawCmd
                RawCmd=re.sub('~'+sub,' '.join(self.substitutions[sub]),RawCmd)
                if SubCheck!=RawCmd:
                    #dbg('Made Substitution '+sub+' to get '+RawCmd,DBGBN)
                    subhit=1
            infprotect=infprotect+1
            if infprotect>100:
                return "ERROR: Infinitely deep substitution levels detected."
        return RawCmd

    def displayhelp(self):
        helpfile=file(self.installroot+'FatController.hlp','r')
        for lines in helpfile:
            self.display.infodisplay(lines)#.strip())
        self.processcommand('show entities')
        self.processcommand('show aliases')
        self.processcommand('show substitutions')
        self.processcommand('show options')
        self.processcommand('show daemons')
        self.processcommand('show active daemons')
        self.processcommand('show scripts')

    def displayopts(self):
        self.display.infodisplay('F!HCurrently Set Options:')
        self.EntityManager.displayclassoptions()
        fcopts=self.getfatcontrolleroptiondefines()
        for d in fcopts:
            dl=d.split()
            d=' '.join(dl[1:])
            self.display.infodisplay(d) # twiddle becasue need to remove the set)

    def toggletrace(self,Fn):
        try:
            if self.trace[Fn]:
                self.trace[Fn]=0
                self.display.infodisplay('Stop tracing block '+Fn)
            else:
                self.trace[Fn]=1
                self.display.infodisplay('Start tracing block '+Fn)
        except KeyError:
            self.trace[Fn]=1
            self.display.infodisplay('Start tracing block '+Fn)


    def SetOption(self,EntityClass,Opt,Val):
        if EntityClass=='FATCONTROLLER':
            #dbg('Trapped OK',DBGBN)
            self.opts[Opt]=Val
        else:
            self.EntityManager.SetClassOption(EntityClass,Opt,Val)
            self.display.infodisplay('Option '+EntityClass+' '+Opt+' '+Val+' Has been set.')

    def getfatcontrolleroptiondefines(self):
        optlist=[]
        for opt in self.opts:
            optlist.append('set FATCONTROLLER '+opt+' '+self.opts[opt])
        return optlist

    def deleteentity(self,EntityName):
        self.EntityManager.delete(EntityName)
        self.display.infodisplay('Entity '+EntityName+' Deleted.')

    def ComprehendCommand(Command):
        #ok, only (usually) makes sense to have one set of [[]]'s so
        #split out the middle
        leftindex=Command.find('[[')
        rightindex=Command.find(']]')+2
        leftpart=Command[:leftindex]
        rightpart=Command[rightindex:]
        tokens=Command[leftindex+2:rightindex-2]
        #now parse the middle part. Will be either
        # start with number. if token is .. then range to number on the end
        #if , then just this number
        ranges=[]
        singles=[]
        elements=tokens.split(',')
        for item in elements:
            if item.find('..')==-1:
                singles.append(item)
            else:
                startval=item[:item.find('..')]
                endval=item[item.find('..')+2:]
                ranges.append((startval,endval))
        CommandList=[]
        for nrange in ranges:
            for n in range(int(nrange[0]),int(nrange[1])+1):
                CommandList.append(leftpart+str(n)+rightpart)
        for n in singles:
            CommandList.append(leftpart+n+rightpart)
        return CommandList

    def processcommand(self,Command): #CODE PROBABLY NOT SAFE. USES EVAL()
        DBGBN='processcommand'
        self.dbg('Before Substitution: '+Command,DBGBN)
        CommandList=[]
        #see if we are going to be using a list comprehension
        if Command.find('[[')!=-1 and Command.find(']]')!=-1:
            #generate list of commands to process
            CommandList=ComprehendCommand(Command)
        else:
            CommandList=[Command]
        for Command in CommandList:
            print "Command is:",Command
            Command=self.processsubstitutions(Command)  #  if ! aliascmd then flow is,  RawCmd->subbed->executed
                                    # is IS aliascmd then flow is   RawCmd->Subbed->aliashit->subbed->executed
            self.dbg('After Substitution: '+Command,DBGBN)
            AliasHit=0
            CommandHit=0
            SplitCmd=Command.split()
            SplitLen=len(SplitCmd)
            Cmd=SplitCmd[0]
            InEtcRun=0
            Error=0
            CommandDefs=file(self.installroot+'FatControllerCommands.sav','r')
            for Def in CommandDefs:
                self.dbg("Scanning cdef ::"+Def,DBGBN)
                if Def!='ENDCOMMANDDEFS' and not Def.startswith('#'):
                    DefTokens=Def.split()
                    ctr=0
                    for Token in DefTokens:
                        self.dbg("Doing token "+Token,DBGBN)
                        if re.search('input:',Token):
                            if SplitLen>ctr:
                                self.dbg("Is an input tag. ValExp=",DBGBN)
                                ValidateExpression=Token.replace('input:','').replace('<<',SplitCmd[ctr]).replace('::SPACE::',' ')
                                self.dbg(ValidateExpression,DBGBN)
                            else:
                                Error=1
                                break
                            if not eval(ValidateExpression):##NOT SAFE NOT SAFE. Need to come up with entirely new
                                                            ##way to do all this
                                Error=1
                                break
                        elif re.search('create:',Token):
                            CreateExpression=Token.replace('create:','').replace('::SPACE::',' ')
                        elif Token!='+*':
                            if ctr>=SplitLen:
                                Error=1
                                break
                            if Token!=SplitCmd[ctr]:
                                Error=1
                                break
                        ctr+=1
                        CommandHit=1
                    else: #{EndOf for Token} all tokens found for else
                        eval(CreateExpression)
                        break
            else:   #{EndOf for Def} Check aliases
                for AliasName in self.aliases:
                    if Cmd==AliasName: #then, make cmdstring alias cmd string and re-process
                        AliasCmd=' '.join(self.aliases[AliasName])
                        AliasHit=1
                        self.dbg('Made alias hit to get '+AliasCmd,DBGBN)
                        break
                else: #FOR loop else  not an alias, so try execute as last entity command
                    if not CommandHit:
                        if self.EntityManager.LastExecutedEntity!='':
                            #global LastExecutedEntity
                            self.EntityManager.execute(self.EntityManager.LastExecutedEntity,SplitCmd[0:])
                        else:
                            self.display.infodisplay('Error: Dont know which entity to use.')
                    else:
                        print "DEBUGMJW: Command is ",Command
                        self.display.infodisplay('Error: Bad command.\t'+Command)
                if AliasHit==1:
                    AliasHit=0
                    CommandDefs.close()
                    self.processcommand(AliasCmd)
            CommandDefs.close()
                

    def load(self,Profile):#will be load(profile)
        #EntityManager=FC_entitymanager.entitymanager()
        self.aliases={} #Is this right?
        try:
            print "DEBUGMJW: "+self.installroot+Profile+'.sav'
            FileToLoad=file(self.installroot+Profile+'.sav')
            for Line in FileToLoad:
                self.processcommand(Line)
        except IOError,(errno,strerror):
            self.display.infodisplay("Error: ["+str(errno)+"] "+strerror+"\t"+self.installroot+Profile+".sav")
        #makeObjectBrowser()

    def handlealertrange(self,fromalert,toalert=None):
        if toalert==None:
            toalert=fromalert
        self.DaemonManager.handlealert(fromalert,toalert+1)


FCApp=wx.PySimpleApp()
FatControllerGui=FatController()
FatControllerGui.Show(1)
FCApp.MainLoop()
    
