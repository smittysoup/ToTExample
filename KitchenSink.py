from langchain import OpenAI
import openai, os, test_input, BracketParser as b, ModifyDictionary
from NodeRunner import NodeRunner
import ExecutorAgent as ea

openai.api_key=os.getenv("OPENAI_API_KEY")

class Kitchen_Sink():
    def __init__(self,input:str):
        self._input = input
        self._llm = OpenAI(model_name="text-davinci-003", temperature=0,max_tokens=3000)  
        self._n_solutions=3   
        self.running_dictionary ={"input":input}
        self.count_recurse = 0
        self.dictionaries={}


    def sign_off_plan(self):
        while (self.running_dictionary["pass"]).lower()!="yes":
            self.running_dictionary=ModifyDictionary.delete_tasks(self.running_dictionary)
            plan = self.add_agent("Replan",["input,criteria,goal"])
            plan[0].join()
            self.running_dictionary = dict(self.running_dictionary,**(plan[1]).queue.get())
            self.running_dictionary["tasks"] = b.BracketParser.get_tasks(self.running_dictionary) 

            supervise = self.add_agent("Evaluate Plan",['tasks','goal','criteria'])
            supervise[0].join()
            self.running_dictionary = dict(self.running_dictionary,**(supervise[1]).queue.get())
         
    def design(self):
        supervise = self.add_agent("Get Criteria",['input'])
        supervise[0].join()
        self.running_dictionary = dict(self.running_dictionary,**(supervise[1]).queue.get())
        self.running_dictionary["criteria"] = b.BracketParser.get_criteria(self.running_dictionary)
        self.running_dictionary["n"] = self._n_solutions
        
        design_options = self.add_agent("Design",['input','goal','criteria','n'])
        design_options[0].join()
        self.running_dictionary = dict(self.running_dictionary,**(design_options[1]).queue.get())
        self.running_dictionary["designs"] = b.BracketParser.get_designs(self.running_dictionary)
        supervise = self.add_agent("Approve Design",['goal','criteria','designs','n'])
        supervise[0].join()
        self.running_dictionary = dict(self.running_dictionary,**(supervise[1]).queue.get())
        self.running_dictionary["output"] = self.running_dictionary[self.running_dictionary["design output choice"]]
        design = self.add_agent("Design Plan",['output','criteria'])
        design[0].join()
        self.running_dictionary = dict(self.running_dictionary,**design[1].queue.get())

    def execute(self):
        code = self.add_agent("Write Code",['output','criteria','title','summary','output_format','components','sequence_of_steps_to_complete_output'])
        code[0].join()
        self.running_dictionary = dict(self.running_dictionary,**code[1].queue.get())
        self.running_dictionary["webpage_code"] = ea.html_linter(self.running_dictionary["webpage_code"])
        puppeteer = self.add_agent("Test Code",['webpage_code'])
        puppeteer[0].join()
        self.running_dictionary = dict(self.running_dictionary,**puppeteer[1].queue.get())
           
    def add_agent(self,task, ilist):
        runner = NodeRunner(self._llm, self.running_dictionary,task,ilist) 
        if runner:
            thread = runner.start_thread()
            return ([thread,runner])
        else:
            return ([None,runner])
    
    def plan(self,**kwargs):
        self.count_recurse +=1

        plan = self.add_agent("Plan",["input"])
        supervise = self.add_agent("Get Criteria",["input"])
        plan[0].join()
        supervise[0].join()
        
        #combine dictionaries
        self.running_dictionary = dict(self.running_dictionary,**(plan[1]).queue.get(),**(supervise[1]).queue.get())
        self.running_dictionary["tasks"] = b.BracketParser.get_tasks(self.running_dictionary)        
        self.running_dictionary["criteria"] = b.BracketParser.get_criteria(self.running_dictionary)
        
        supervise = self.add_agent("Evaluate Plan",['tasks','criteria','goal'])
        supervise[0].join()
        self.running_dictionary = dict(self.running_dictionary,**(supervise[1]).queue.get())
        self.sign_off_plan()
        #offload dictionary with signed off plan
        self.dictionaries[str(self.count_recurse)] = self.running_dictionary
        
        for task in self.running_dictionary["tasks"]:
            self.running_dictionary["current task"] = task
            supervise = self.add_agent("Evaluate Task",['tasks','current_task'])

            supervise[0].join()
            self.running_dictionary = dict(self.running_dictionary,**(supervise[1]).queue.get())
            ispass = self.running_dictionary["task pass"].lower()
            self.running_dictionary = {}
            self.running_dictionary["input"]=task
            
            if ispass!="yes":
                self.plan()
            else: 
                
                self.design()
                self.execute()

        
    def run_nodes(self):
        self.plan()
        
if __name__ == '__main__':
    ks = Kitchen_Sink(test_input.input)
    ks.run_nodes()
