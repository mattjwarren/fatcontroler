import FC_ScheduledTask,FC_daemonschedule,FC_daemontask,os,time
import config
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

    def __init__(self,entitymanager,alertmanager,name):
        FC_ScheduledTask.ScheduledTask.__init__(self)
        '''Parms.

        entitymanager is an entitymanager object the daemon can ask to execute the command
        using the scheduledexecute(EntityName,Cmd) method
        scheduler is the scheduler handling the executions, needed so
        daemon can rescheule itself for period units in the future'''
        self.name=name
        self.processor=entitymanager
        self.tasks={}
        self.schedule=FC_daemonschedule.daemonschedule()
        self.AlertManager=alertmanager

    def run(adaemon): #adaemon
        for task_name,task in list(adaemon.tasks.items()):
            entities=list(adaemon.tasks[tsk].entities.items())
            for entity_name,entity in entities:
                cmd_output=entity.execute(adaemon.tasks[task_name].command)
                collectors=list(adaemon.tasks[tsk].collectors.items())
                for collector_name,collector in collectors:
                    collector.read(cmd_output,adaemon,adaemon.tasks[tsk],collector,ent)
                    collectorfile=collectors[collector].data_filename
                    if collectorfile!=None:
                        outfile_path=os.path.join(config.data_path,collectorfile)
                        outfile_path=outfile_path+("_%s_%s_%s_%s" % (adaemon.name,tsk,ent,collector.name)) 
                        outfile=open(outfile_path,'a')
                        timestamp=str(time.ctime(float(time.time())))
                        outfile.write(timestamp+','+collectors[collector].lastoutline+'\n')
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

#
# END OF CLASS DAEMON
###########
