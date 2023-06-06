from langchain import OpenAI
import openai, os, test_input, BracketParser as b, ModifyDictionary
from NodeRunner import NodeRunner
import ExecutorAgent as ea

openai.api_key=os.getenv("OPENAI_API_KEY")

class Kitchen_Sink():
    def __init__(self,input:str,n_solution:int=3):
        self._input = input
        self._llm = OpenAI(model_name="text-davinci-003", temperature=0,max_tokens=3000)  
        self._n_solutions=self.n_solutions
        self.running_dictionary = {}   
        self.count_recurse = 0
        self.filepath = ""
        self.dictionaries={}
    
    def initialize_dictionary(self):
        '''initialize the dictionary with the input'''
        self.running_dictionary ={"input":self.input}
        self.running_dictionary["n"] = self._n_solutions

    def collapse_dictionary_item(self,item_label,items):
        '''
        Purpose of this function is to combine multiple dictionary items into a single item for input to a prompt template.
        searches the dictionary for the item_label and deletes the item_label 
        then searches the dictionary for all items that contain the item_label and adds them to the dictionary as a collapsed list.
        '''
        if self.running_dictionary[item_label]:
            del self.running_dictionary[item_label]
        self.running_dictionary[item_label] = ModifyDictionary.get_items(self.running_dictionary,items)

    def sign_off_plan(self):
        '''
        1. create an agent that will sign off on the plan
        2. the agent will ask the supervisor if the plan is acceptable, if not, the agent will replan
        '''  
        #initialize pass to null
        self.running_dictionary["pass"] = ""   
          
        while (self.running_dictionary["pass"]).lower()!="yes":
            #start plan approval thread. 
            approve_plan = self.add_agent("Evaluate Plan",['tasks','criteria','goal'])
            self.run_thread(approve_plan)
            
            #if the plan is not approved, then replan and add new plan to dictionary, replacing old plan
            #loop will continue until the plan is approved
            if self.running_dictionary["pass"].lower()!="yes":
                plan = self.add_agent("Replan",["input,criteria,goal"])
                self.run_thread(plan)
                self.collapse_dictionary_item("tasks","task")
    
    def correct_errors(self):
        while self.running_dictionary['webpage_errors'] != "":
            self._llm.max_tokens = 2000
            code = self.add_agent("Fix Code",['webpage_code','webpage_errors'])
            self.run_thread(code,1)
            if self.running_dictionary["webpage_code"] != ea.read_code_from_file(self.filepath):
                self.check_code()
            else:
                self.running_dictionary["webpage_errors"] = ""
        
    def check_code(self):
        self._llm.max_tokens = 3000
        self.running_dictionary["webpage_code"] = ea.lint(self.filepath)
        puppeteer = self.add_agent("Test Code",['webpage_code'])
        self.run_thread(puppeteer,2)
        stderr = ea.check_page_with_puppeteer(self.filepath)
        self.running_dictionary["webpage_errors"] = stderr
    
    def sign_off_code(self):
        approve_code = self.add_agent("Approve Deliverable",['webpage_code','criteria','goal'])
        self.run_thread(approve_code)
        if self.running_dictionary["code_pass"].lower()!="yes":
            executor = self.add_agent("Recode",['webpage_code','code_pass_reason'])
            self.run_thread(executor,1)            
            self.test()
        
    def design(self):
        '''
        get design options and have LLM choose best one based on goal and criteria
        '''
        design_options = self.add_agent("Design",['input','goal','criteria','n'])
        self.run_thread(design_options)
        self.collapse_dictionary_item("designs","design")
        
        choose_option = self.add_agent("Approve Design",['goal','criteria','designs','n'])
        self.run_thread(choose_option)
        
        key_text = self.running_dictionary["design_output_choice"].replace(" ","_")
        self.running_dictionary["output"] = self.running_dictionary[key_text]
        design_plan = self.add_agent("Design Plan",['output','criteria'])
        self.run_thread(design_plan)

    def execute(self):
        code = self.add_agent("Write Code",['output','criteria','title','summary','output_format','components','sequence_of_steps_to_complete_output'])
        self.run_thread(code,1)
        self.test()
    
    def test(self):
        self.check_code()
        self.correct_errors()
        self.sign_off_code()    
           
    def add_agent(self,task, ilist):
        runner = NodeRunner(self._llm, self.running_dictionary,task,ilist) 
        if runner:
            thread = runner.start_thread()
            return ([thread,runner])
        else:
            return ([None,runner])
    
    def run_thread(self,thread,type=0):
        '''
        wait for thread to finish, then get the result and append it to the running dictionary
        '''
        thread[0].join()
        result = thread[1].queue.get()
        if type==0:
            self.running_dictionary = dict(self.running_dictionary,**result)
        if type==1:
            ea.save_code_to_file(result,"file"+self.filepath)
        else:
            ea.save_code_to_file(result,"puppeteer_script.js")
    
    def create_plan(self,**kwargs):
        plan = self.add_agent("Plan",["input"])
        if self.count_recurse==1:
            supervise = self.add_agent("Get Criteria",["input"])
        self.run_thread(plan)
        self.run_thread(supervise)

        #collapse tasks and criteria to list variables        
        self.collapse_dictionary_item("tasks","task")      
        self.collapse_dictionary_item("criteria","criteria")
        
    
    def start_plan(self,**kwargs):
        
        self.count_recurse +=1
        self.filepath = "file"+str(self.count_recurse)+".html"
        
        self.create_plan()
        self.sign_off_plan()
        
        for task in self.running_dictionary["tasks"]:
            self.running_dictionary["current_task"] = task
            approve_task = self.add_agent("Evaluate Task",['tasks','current_task'])
            refine_goal = self.add_agent("Refine Goal",['tasks','criteria','goal','current_task'])
            self.run_thread(approve_task)
            self.run_thread(refine_goal)
            
            if self.running_dictionary["task_pass"].lower() !="yes":
                '''
                if task needs to be broken down further, stash dictionary to archive,
                then restart planning process with current task as input
                ''' 
                #offload dictionary with signed off plan
                self.dictionaries[str(self.count_recurse)] = self.running_dictionary
                self.running_dictionary["input"]=task
                self.plan()
            else:                 
                self.design()
                self.execute()

        
if __name__ == '__main__':
    ks = Kitchen_Sink(test_input.input)
    ks.initialize_dictionary()
    ks.start_plan()
