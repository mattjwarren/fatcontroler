import FC_entity,os
###########
# START OF CLASS LOCAL
#

class LOCAL(FC_entity.entity):
    '''Implementation of an entity that executes commands on the local machine'''
    def __init__(self,name):
        self.Name=name
        pass

    ##########
    # START OF INTERFACE ENTITY
    #


    Opts={}

    def execute(self,CmdList):
        din,dout,derr=os.popen3(' '.join(CmdList))
        output=dout.readlines()
        errout=derr.readlines()
        dummy=[output.append(err) for err in errout]  
        return output# List of lines readable by display() method

    def display(self,LineList,OutputCtrl):
        '''Generic method for displaying output from entity.execute().

        This method should be implmented by the subclasser and translate
        the given LineList to human-readable output.'''
        for line in LineList:
            OutputCtrl.AppendText(line.rstrip()+"\n")
        return # print LineList, LineList is (minimally) output from execute() method
    
    def getparameterdefs(self):
        '''Should return a dict of parm:parmtype pairs for the GUI
        to build a config box'''
        return ["Name"]
    
    def getname(self):
        '''Convenience method for getting entity name.

        should return a string representing the entity uniquely'''
        return self.Name # string that is entity name

    def getparameterstring(self):
        DBGBN='localgetparameterstring'
        '''Method to determine how the entity was defined.

        Should return a string that can be fed to FatController.processcommand()#outdate see aboce
        that will re-define this entity in its entirety'''
        #dbg('returning define entity LOCAL '+self.Name,DBGBN)
        return ''

    def getparameterlist(self):
        '''returns a list of the value given as string by getparameterstring'''
        parmstring=self.getparameterstring()
        lst=parmstring.split()
        return lst

    def getentitytype(self):
        '''Get the type of entity.

        Should return qa string indicating the entities type (TELNET , TSM , BROCADE etc..)'''
        return 'LOCAL'

    def gettype(self):
        '''Return the kind of instance of a given entity.

        For example, TSM entities have an entitytype of 'TSM'
        but a type of single or configmanger. This should
        return a string indicating the kind of entity this is'''
        return 'simple'

    def setoption(self,option,value):
        '''Set a global option.

        this method should take option and value pair and set them
        as requried. (IE: TELNET.setoption(self,ShowRawTelnet,yes instructs
        the TELNET entities to begin displaying their raw telnet dialogues)'''
        LOCAL.Opts[option]=value
        return

    def getoptions(self):
        '''Get a list of set options.

        Should return a list of the format
        CLASS OPTION VALUE'''
        OptList=[]
        for o in LOCAL.Opts:
            OptList.append(o+' '+LOCAL.Opts[o])
        return OptList

    #
    # END OF INTERFACE Entity
    ###########
#
# END OF CLASS LOCAL
############
