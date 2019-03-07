import FC_LOCAL,FC_TSM,FC_TELNET,FC_DUMB,FC_ENTITYGROUP,wx, FC_SSH
import FC_formatter
###########
# START OF CLASS entitymanager
#

class entitymanager:

#
#Method functions
#
    def __init__(self,OutputNotebook,FocusReturnCtrl):
        self.Entities={} #dict of entity objects
        self.OutBook=OutputNotebook
        self.OutPages={} #entity name keyed, value is page for output

        #img=wx.Image('c:\\program files\\yab\\fatcontroller\\redalert.jpg', wx.BITMAP_TYPE_JPEG)
        img=wx.Image('/opt/yab/FatController/redalert.jpg', wx.BITMAP_TYPE_JPEG)
        self.RedBMP=wx.BitmapFromImage(img)
        img=wx.Image('/opt/yab/FatController/yellowalert.jpg', wx.BITMAP_TYPE_JPEG)
        self.AmberBMP=wx.BitmapFromImage(img)
        img=wx.Image('/opt/yab/FatController/greenalert.jpg', wx.BITMAP_TYPE_JPEG)
        self.GreenBMP=wx.BitmapFromImage(img)
        self.AlertImageList=wx.ImageList(12,12)
        self.AlertImageList.Add(self.RedBMP)
        self.AlertImageList.Add(self.AmberBMP)
        self.AlertImageList.Add(self.GreenBMP)
        self.OutBook.SetImageList(self.AlertImageList)
        self.ReturnFocus=FocusReturnCtrl
                
        self.LastExecutedEntity=''
        self.GeneralPage=OutputNotebook.GetPage(0).GetChildren()[0]
        self.HighestPageNumber=1 #post increment. first is 1
        self.display=FC_formatter.OutputFormatter(OutputNotebook,self.ReturnFocus)

    def SetAlertStatus(self,EntityName):
        self.OutBook.SetPageImage(self.OutPages[EntityName][3]-1,0)
        #self.OutBook.GetPage(self.OutPages[EntityName][3]-1).SetBackgroundColour(wx.Colour(255,200,200))

    def ClearAlertStatus(self,EntityName):
        self.OutBook.SetPageImage(self.OutPages[EntityName][3]-1,2)
        #self.OutBook.GetPage(self.OutPages[EntityName][3]-1).SetBackgroundColour(wx.Colour(25,25,25))


    def getentitytype(self,EntityName):
        return self.Entities[EntityName].getentitytype()
        
    def getentitylist(self):
        return self.Entities
        
    def getentityparms(self,EntityName):
        return self.Entities[EntityName].getparameterstring()

    # # Need to change this, coupling between entitymanager and entities. Shouldnt need to know numb of parms needed
    def define(self,type,typeparms):                                #TSMServer tpyeparms;    ['name','adminuser','adminpass']
        if type=='TSM':                                 #becomes Entites{'name',['adminuser','adminpass']}
            if len(typeparms)==6:
                EntityName=typeparms[0]
                self.Entities[EntityName]=FC_TSM.TSM(EntityName,typeparms[1],typeparms[2],typeparms[3],typeparms[4],typeparms[5]) # {'name',<TSM object>}
                self.display.infodisplay('Entity: TSM '+self.Entities[EntityName].getname()+" "+self.Entities[EntityName].getparameterstring()+" defined.")
            else:
                self.display.infodisplay('Error: Wrong number parameters for TSM entity.')
        elif type=='TELNET':
            if len(typeparms)==5:
                EntityName=typeparms[0]
                self.Entities[EntityName]=FC_TELNET.TELNET(EntityName,typeparms[1],typeparms[2],typeparms[3],typeparms[4])
                self.display.infodisplay('Entity: TELNET '+self.Entities[EntityName].getname()+" "+self.Entities[EntityName].getparameterstring()+" defined.")
            else:
                self.display.infodisplay('Error: Wrong number of parameters for TELNET entity.')
        elif type=='DUMB':
            if len(typeparms)==1:
                EntityName=typeparms[0]
                self.Entities[EntityName]=FC_DUMB.DUMB(EntityName)
                self.display.infodisplay('Entity: DUMB '+self.Entities[EntityName].getname()+" "+self.Entities[EntityName].getparameterstring()+" defined.")
            else:
                self.display.infodisplay('Error: Wrong number of parameters for DUMB entity.')
        elif type=='LOCAL':
            if len(typeparms)==1:
                EntityName=typeparms[0]
                self.Entities[EntityName]=FC_LOCAL.LOCAL(EntityName)
                self.display.infodisplay('Entity: LOCAL '+self.Entities[EntityName].getname()+" "+self.Entities[EntityName].getparameterstring()+" defined.")
            else:
                self.display.infodisplay('Error: Wrong number of parameters for LOCAL entity.')
        elif type=='SSH':
            if len(typeparms)==5:
                EntityName=typeparms[0]
                self.Entities[EntityName]=FC_SSH.SSH(*typeparms)
                self.display.infodisplay('Entity: SSH '+self.Entities[EntityName].getname()+" "+self.Entities[EntityName].getparameterstring()+"         defined.")
            else:
                self.display.infodisplay('Error: Wrong number of parameters for SSH entity.')
        elif type=='ENTITYGROUP':
            EntityName=typeparms[0]
            self.Entities[EntityName]=FC_ENTITYGROUP.ENTITYGROUP(EntityName,typeparms[1:],self)
            self.display.infodisplay('Entity: ENTITYGROUP '+self.Entities[EntityName].getname()+" "+self.Entities[EntityName].getparameterstring()+" defined.")
        else:
            self.display.infodisplay('Error: Don\'t know how to define '+type+' entities.')
        #Now attatch an output page
        try:
            if EntityName:
                self.OutPages[EntityName]=[wx.Panel(self.OutBook,style=wx.NO_BORDER)]
                self.OutBook.AddPage(self.OutPages[EntityName][0],EntityName,True,-1)
                self.HighestPageNumber+=1
                self.OutPages[EntityName].append(wx.TextCtrl(self.OutPages[EntityName][0],-1,'Entity Defined.\n',(0,0),(0,0),wx.TE_MULTILINE|wx.TE_DONTWRAP|wx.TE_RICH2))
                self.OutPages[EntityName][1].SetOwnFont(wx.Font(8,wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))
                self.OutPages[EntityName].append(wx.BoxSizer(wx.VERTICAL))
                self.OutPages[EntityName].append(self.HighestPageNumber)
                #0=wxpanel,1=textctrl,2=sizer,3=number(-1)=pgindex
                self.OutBook.SetPageImage(self.HighestPageNumber-1,2)
                self.OutPages[EntityName][2].Add(self.OutPages[EntityName][1],1,wx.EXPAND,5)
                self.OutPages[EntityName][0].SetSizer(self.OutPages[EntityName][2])
                self.OutPages[EntityName][1].SetAutoLayout(True)
                self.OutPages[EntityName][2].Fit(self.OutPages[EntityName][0])
                self.OutPages[EntityName][2].Layout()
        except UnboundLocalError, NameError:
            self.display.infodisplay('Exception caught in entitymanager define')
            pass


    def execute(self,EntityName,CmdList):
        DBGBN='entitymanagerexecute'
        try:
            EntityType=self.Entities[EntityName].getentitytype()
            output=self.Entities[EntityName].execute(CmdList) #list of output returned
            self.OutBook.SetSelection(self.OutPages[EntityName][3]-1)
            self.Entities[EntityName].display(output,self.OutPages[EntityName][1])
            self.OutPages[EntityName][1].ScrollLines(1)
            self.ReturnFocus.SetFocus()
            self.LastExecutedEntity=EntityName
        except KeyError:
            self.display.infodisplay('Error:    Don\'t know how to execute commands for '+EntityName+'.')

    def scheduledexecute(self,entity,cmd_list):
        EntityType=entity.getentitytype()
        output=entity.execute(cmd_list) #list of output returned
        return output

    def display(self,EntityName,OutputList):
        #self.display.infodisplay('Changing page selected index to '+str(self.OutPages[EntityName][3]))
        self.OutBook.SetSelection(self.OutPages[EntityName][3]-1)
        self.Entities[EntityName].display(OutputList,self.OutPages[EntityName][1])
        self.OutPages[EntityName][1].ScrollLines(1)
        #self.OutBook.Update()
        self.ReturnFocus.SetFocus()
        #self.fixpagestyle(self.OutPages[EntityName][1])

    def show(self):
        for e in self.Entities:
            self.display.infodisplay(''+self.Entities[e].getentitytype()+'\t'+e+'\t'+self.Entities[e].getparameterstring())
        self.display.infodisplay('')

    def getdefines(self): #Returns a list of strings, each string returned is the define command for the entity
        DBGBN='entitymanagergetdefines'
        DefineList=[]
        #dbg('starting to loop through self.entities',DBGBN)
        for e in self.Entities:
            #dbg('doing entity '+self.Entities[e].getname(),DBGBN)
            EntityType=self.Entities[e].getentitytype()
            ParmList=self.Entities[e].getparameterstring()
            DefineList.append('define entity '+EntityType+' '+e+' '+ParmList)
        #dbg('leaving entitymanagergetdefines',DBGBN)
        return DefineList

    def delete(self,EntityName):
        del self.Entities[EntityName]

    def isEntity(self,EntityName):
        try:
            self.Entities[EntityName]
            return 1
        except KeyError:
            return 0

    def getEntity(self,EntityName):
        return self.Entities[EntityName]

    def SetClassOption(self,EntityClass,option,value):
        DBGBN='entitymanagersetclassoption'
        #dbg('option '+option+' value '+value+' for entity class '+EntityClass,DBGBN)
        for e in self.Entities:
            if self.Entities[e].getentitytype()==EntityClass: #CHANGED INCIDENTALLY FRMO gettype() WARNING!!!!!!!!!
                #dbg('setting option >|'+option+'|< to value >|'+value+'|< for entity class >|'+EntityClass+'|<',DBGBN)
                self.Entities[e].setoption(option,value)
                break #only do one ## New!: should set classlvel attribute instead? (monkeypatch)

    def getentitytypes(self):
        types=[]
        for e in self.Entities:
            etype=self.Entities[e].getentitytype()
            if etype not in types:
                types.append(etype)
        return types

    def displayclassoptions(self):
        doneclasses={}
        for e in self.Entities:
            try:
                if doneclasses[self.Entities[e].getentitytype()]:
                    pass
            except KeyError:
                doneclasses[self.Entities[e].getentitytype()]='done'
            for option in self.Entities[e].getoptions():
                    self.display.infodisplay(self.Entities[e].getentitytype()+' '+option)

    def getclassoptiondefines(self):
        DBGBN='entitymanagergetclassoptiondefines'
        doneclasses={}
        OptList=[]
        formattedlist=[]
        for e in self.Entities:
            try:
                #dbg 'Checking if have got classoptiondefines for entitytype '+self.Entities[e].getentitytype(),DBGBN)
                if doneclasses[self.Entities[e].getentitytype()]:
                    #dbg('key found in doneclasses, I Have!',DBGBN)
                    pass
            except KeyError:
                #dbg('Havent got them for this entity type yet. Getting....',DBGBN)
                #dbg('setting doneclasses[self.Entities[e].getentitytype() {'+self.Entities[e].getentitytype()+'} to done',DBGBN)
                doneclasses[self.Entities[e].getentitytype()]='done'
            rawlist=self.Entities[e].getoptions()
            if len(rawlist)>0:
                #dbg('formatting the rawlist options',DBGBN)
                for l in rawlist:
                    #dbg('l is '+l,DBGBN)
                    #dbg('adding \'set '+self.Entities[e].getentitytype()+' '+l+'\'',DBGBN)
                    formattedlist.append('set '+self.Entities[e].getentitytype()+' '+l)
                    #dbg('appending formatted list to optlist',DBGBN)
                OptList.append(formattedlist)
                formattedlist=[]
        return OptList # list of lists


#
# END OF CLASS entitymanager
###########
