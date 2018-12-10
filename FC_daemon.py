import FC_ScheduledTask,FC_daemonschedule,FC_daemontask,os,time
###########
# Some POSIX / winos setups ((this needs to be moved out of here. FC should
# provide 'environment' services to entities.
#
# Sets up disk 'root', point where all filenames
# for collector output etc.. are generated from.
# will make configurable option at some point...

if os.name=='posix':
    system='UNIX'
    installroot='/opt/yab/FatController/'
    copycmd='cp'
    driveroot=installroot
else:
    system='WINDOWS'
    installroot='c:\\program files\\yab\\FatController\\'
    copycmd='copy'
    driveroot='c:\\'
#
#
#####################

####################
# START OF CLASS daemon
#
class daemon(FC_ScheduledTask.ScheduledTask):
    '''A top level object holding info for scheduled commands.

	A daemon consists of a schedule and a group of tasks. each
	task is a group of entities and collectors and a command. Each
	collector is a set of rules for extracting data from the results
	of cmd run against each entity, and an optional alert set on that data.'''

    def __init__(self,entitymanager,alertmanager,Name):
        FC_ScheduledTask.ScheduledTask.__init__(self)
        '''Parms.

        entitymanager is an entitymanager object the daemon can ask to execute the command
        using the scheduledexecute(EntityName,Cmd) method
        scheduler is the scheduler handling the executions, needed so
        daemon can rescheule itself for period units in the future'''
        self.name=Name
        self.processor=entitymanager
        self.tasks={}
        self.schedule=FC_daemonschedule.daemonschedule()
        self.AlertManager=alertmanager

    def run(adaemon): #adaemon
        for tsk in adaemon.tasks:
            for ent in adaemon.tasks[tsk].getentities():
                output=adaemon.processor.scheduledexecute(ent,adaemon.tasks[tsk].getcommand())
                collectors=adaemon.tasks[tsk].getcollectors()
                for collector in collectors:
                        # will collect and return alert back if generated
                    collectors[collector].read(output,adaemon.getname(),adaemon.tasks[tsk].getname(),collector,ent)
                    collectorfile=collectors[collector].getfile()
                    
                    #TODO: Fix this
                    if os.name=='posix':
                        collectorfile=collectorfile.replace('\\','/')
                    else:
                        collectorfile=collectorfile.replace('/','\\')
                    if collectorfile!='none':
                        global driveroot
                        outfile=file(driveroot+collectorfile+'_'+adaemon.getname()+tsk+ent+collector,'a')
                        outfile.write(str(time.ctime(float(time.time())))+','+collectors[collector].lastoutline+'\n')
                        outfile.close()

    def setschedule(self,start,end,period):
        self.schedule.updateschedule(start,end,period)

    def getschedule(self):
        return self.schedule

    def addtask(self,name,command):
        self.tasks[name]=FC_daemontask.daemontask(name,command)

    def gettasks(self):
	return self.tasks #returns dict of tasks

    def gettask(self,name):
        return self.tasks[name] #returns single task

    def removetask(self,name):
        del self.tasks[name]

    def addtaskcollector(self,taskname,collectorname,tag,skip,format,file):
        self.tasks[taskname].addcollector(collectorname,tag,skip,format,file)

    def addtaskcollectoralert(self,taskname,collectorname,minval,maxval,alertmessage,pass_script,fail_script):
        self.tasks[taskname].addcollectoralert(collectorname,minval,maxval,alertmessage,self.AlertManager,pass_script,fail_script)

    def removetaskcollector(self,taskname,collectorname):
        self.tasks[taskname].removecollector(collectorname)

    def addtaskentity(self,taskname,entity):
        self.tasks[taskname].addentity(entity)

    def removetaskentity(self,taskname,entity):
        self.tasks[taskname].removeentity(entity)

    def getnumtasks(self):
        return len(self.tasks)

    def getname(self):
        return self.name
#
# END OF CLASS DAEMON
###########
