###########
# START OF CLASS SCHEDULEDTASK
# ((subclassed by Daemon))
#
#
# ** Recognition to Tom Schwaller & the WebWare group for the base scheduling code **
# For more info on WebWare,
#
# [1] Webware: http://webware.sourceforge.net/ 
# [2] Ganymede: http://www.arlut.utexas.edu/gash2/
#
# For more info on the code snippets used here
#
# http://webware.sourceforge.net/Webware-0.7/TaskKit/Docs/QuickStart.html
#
import threading
class ScheduledTask(threading.Thread):

    def __init__(self):
	threading.Thread.__init__(self)
	''' Subclasses should invoke super for this method. '''
	# Nothing for now, but we might do something in the future.
	pass

    def run(self):
	'''
	Override this method for you own tasks. Long running tasks can periodically 
	use the proceed() method to check if a task should stop. 
	'''
	raise SubclassResponsibilityError
    
	
    ## Utility method ##    
    
    def proceed(self):
	"""
	Should this task continue running?
	Should be called periodically by long tasks to check if the system wants them to exit.
	Returns 1 if its OK to continue, 0 if its time to quit
	"""
	return self._handle._isRunning
	
	
    ## Attributes ##
    
    def handle(self):
	'''
	A task is scheduled by wrapping a handler around it. It knows
	everything about the scheduling (periodicity and the like).
	Under normal circumstances you should not need the handler,
	but if you want to write period modifying run() methods, 
	it is useful to have access to the handler. Use it with care.
	'''
	return self._handle

    def name(self):
	'''
	Returns the unique name under which the task was scheduled.
	'''
	return self._name


    ## Private method ##

    def _run(self, handle):
	'''
	This is the actual run method for the Task thread. It is a private method which
	should not be overriden.
	'''
	DBGBN='scheduledtask_run'
	#dbg('Entering ...',DBGBN)
	self._name = handle.name()
	self._handle = handle
	#dbg('handing over to self.run()',DBGBN)
	self.run()
	#dbg('Now going to notify completion',DBGBN)
	handle.notifyCompletion()

#
# END OF CLASS SCHEDULEDTASK
###########
