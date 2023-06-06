import NodeRunner

class agent(NodeRunner):

    def __init__(self, llm, running_dictionary):
        self._llm = llm
        self._running_dictionary = running_dictionary
        super().__init__(self._llm, self._running_dictionary,task=None,ilist=None)        
        
    def add_agent(self,task, ilist):
        super().task = task
        super().ilist = ilist 
        return super().start_thread()
