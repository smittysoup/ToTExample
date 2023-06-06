from NodeRunner import Agent
from ModifyDictionary import ModifyDictionary
from queue import Queue
from designer import designer

class planner(Agent):
    def __init__(self,running_dictionary,count_recurse,llm,filepath,test=False):
        self._running_dictionary = running_dictionary
        self._dictionaries = {}
        self._count_recurse = count_recurse
        self._llm = llm
        self._test = test
        self._filepath = filepath
        self.queue = Queue()
  
        
    def plan(self):
        self.create_plan()
        self.sign_off_plan()
        self.recurse_plan()
        return None        
        
    def recurse_plan(self):
        
        if self._count_recurse>1:
            self.create_plan()
            self.sign_off_plan()
        
        for task in self._running_dictionary["tasks"]:
            self._running_dictionary["current_task"] = task
            approve_task = self.start_thread("Evaluate Task",['tasks','current_task'])
            refine_goal = self.start_thread("Refine Goal",['tasks','criteria','goal','current_task'])
            self.run_thread(approve_task)
            self.run_thread(refine_goal)
            
            if self._running_dictionary["task_pass"].lower().strip() !="yes":
                '''
                if task needs to be broken down further, stash dictionary to archive,
                then restart planning process with current task as input
                ''' 
                #offload dictionary with signed off plan
                self._dictionaries[str(self.count_recurse)] = self._running_dictionary
                self._running_dictionary["input"]=task
                self._count_recurse +=1
                self.recurse_plan()
            else: 
                if self._test:
                    print(self._running_dictionary)
                else:
                    d = designer(self._running_dictionary,self._llm,self._filepath)                
                    d.design()
                
            return None
    
    def create_plan(self,**kwargs):
        plan = self.start_thread("Plan",["input"])
        if self._count_recurse==1:
            supervise = self.start_thread("Get Criteria",["input"])
        self.run_thread(plan)
        self.run_thread(supervise)
        
        modify_dictionary = ModifyDictionary(self._running_dictionary)   
        #collapse tasks and criteria to list variables        
        self._running_dictionary['tasks'] = modify_dictionary.get_items("task")      
        self._running_dictionary['criteria'] = modify_dictionary.get_items("criteria")
        
        return None
        
    def sign_off_plan(self):
        '''
        1. create an agent that will sign off on the plan
        2. the agent will ask the supervisor if the plan is acceptable, if not, the agent will replan
        '''  
        #initialize pass to null
        self._running_dictionary["pass"] = ""   
          
        while (self._running_dictionary["pass"]).lower().strip()!="yes":
            #start plan approval thread. 
            approve_plan = self.start_thread("Evaluate Plan",['tasks','criteria','goal'])
            self.run_thread(approve_plan)
            
            #if the plan is not approved, then replan and add new plan to dictionary, replacing old plan
            #loop will continue until the plan is approved
            if self._running_dictionary["pass"].lower().strip()!="yes":
                plan = self.start_thread("Replan",['input','tasks','reason'])
                self.run_thread(plan)
                modify_dictionary = ModifyDictionary(self._running_dictionary) 
                self._running_dictionary['tasks'] = modify_dictionary.get_items("task")
        
        return None
    
if __name__ == '__main__':
    import openai, os, test_dictionary
    openai.api_key=os.getenv("OPENAI_API_KEY")
    from langchain import OpenAI
    running_dictionary = test_dictionary.dictionary
    count_recurse = 1
    llm = OpenAI(model_name="text-davinci-003", temperature=0,max_tokens=3000)  
    filepath = "file1.html"
    
    p = planner(running_dictionary,count_recurse,llm,filepath,True)
    p.plan()
    print(p._running_dictionary)