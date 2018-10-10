import FC_daemoncollector
###########
# START OF CLASS daemontask
#
class daemontask:
    ''' Data structure holding information on a single task.

	A task consists of a command, a group of entities and a group
	of collectors. Each time the scheduler invokes the daemon
	the daemon runs cmd against each entity in the group
	collects the output and runs that through each collector in
	the group.'''
    
    def __init__(self,name,cmd):
	self.command=cmd
	self.entities={} # dict of entity onjects
	self.collectors={} # dict (name:object) of collectors objects
	self.name=name

    def getcommand(self):
	return self.command

    def setcommand(self,newcommand):
	self.command=newcommand

    def getentities(self):
	return self.entities 

    def addentity(self,entityobject): #pass an entity object to add it
	self.entities[entityobject.getname()]=entityobject

    def getsubscribers(self):
        return self.entities

    def removeentity(self,entityobject):
	del self.entities[entityobject.getname()] #pass an entity object to remove

    def addcollector(self,name,tag,skip,format,file): #add a named collector to the task
	self.collectors[name]=FC_daemoncollector.daemoncollector(tag,skip,format,file)

    def addcollectoralert(self,name,minval,maxval,alertmessage,alertmanager,pass_script,fail_script):
	self.collectors[name].addalert(minval,maxval,alertmessage,alertmanager,pass_script,fail_script)

    def removecollector(self,name): # remove a named collector from the task
	del self.collectors[name]

    def tostring(self):
	return ' '.join(self.command)

    def getcollectors(self):
	return self.collectors

    def getname(self):
	return self.name

#
# END OF CLASS daemontask
###########
