from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.chains import SequentialChain, TransformChain
import openai, os, re, input, Supervisor as s, Designer, Executor, planner as p, threading, time, BracketParser as b, \
Designer as d, Executor as e
from queue import Queue

openai.api_key=os.getenv("OPENAI_API_KEY")

class Kitchen_Sink():
    def __init__(self,input:str):
        self._input = input
        self._llm = OpenAI(model_name="text-davinci-003", temperature=0)  
        self._n_solutions=5    
        self.supervisor_queue = Queue()
        self.planner_queue = Queue()
        self.designer_queue = Queue()
        self.executor_queue = Queue()
        self.running_dictionary ={"input":input}
        self.count_recurse = 0
        self.dictionaries={}

    def root_node_supervisor(self,queue,task,**kwargs):
        print("Initiate supervisor")
        supervisor = s.Supervisor(self._llm)
        chain = supervisor._get_criteria() if task=="Get Criteria" \
                else supervisor._eval_plan_chain() if task=="Evaluate Plan" \
                else supervisor._eval_task() if task=="Evaluate Task" \
                else supervisor._eval_design() if task=="Approve Design" \
                else supervisor._eval_output() if task=="Approve Deliverable" else None
                    
        response = chain(kwargs)
        output = b.BracketParser(response)
        parsed_output = output.parse()
        queue.put(parsed_output)
    
    def root_node_planner(self,queue,task,**kwargs):
        planner = p.Planner(self._llm)
        chain = planner._plan_chain() if task == "Plan" \
            else planner._replan_chain() if task == "Replan" \
            else None
        response = chain(kwargs)
        output = b.BracketParser(response)
        parsed_output = output.parse()
        queue.put(parsed_output)
        
    def root_node_designer(self,queue,task,**kwargs):
        designer = d.Designer(self)
        chain = designer._design_chain() if task == "Design" \
            else designer._design_plan_chain() if task == "Design Plan" \
            else None
        response = chain(kwargs)
        output = b.BracketParser(response)
        parsed_output = output.parse()
        queue.put(parsed_output)
        
    def root_node_executor(self,queue,task,**kwargs):
        executor = e.ExecutorAgent(self)
        
    def delete_tasks(self):
            for key in self.running_dictionary.keys():
                if 'task ' in key.lower():
                    del self.running_dictionary[key]
            return self.running_dictionary
        
    def filter_dict(self,keys):
        return {k: self.running_dictionary[k] for k in keys if k in self.running_dictionary}
    
    def start_supervising(self,type,supervision_list):
        supervisor_criteria = threading.Thread(
            target=self.root_node_supervisor,
            args=(self.supervisor_queue,type),
            kwargs=               
            self.filter_dict(supervision_list)
            )
        supervisor_criteria.start()
        return supervisor_criteria
    
    def make_plan(self,type,planning_list):
        planner_plan = threading.Thread(
            target=self.root_node_planner,
            args=(self.planner_queue,type),
            kwargs=
            self.filter_dict(planning_list)
            )
        planner_plan.start()
        return planner_plan
    
    def create_design(self,type,planning_list):
        designer_design = threading.Thread(
            target=self.root_node_designer,
            args=(self.designer_queue,type),
            kwargs=
            self.filter_dict(planning_list)
            )
        designer_design.start()
        return designer_design

    def sign_off_plan(self):
        while (self.running_dictionary["pass"]).lower()!="yes":
            self.running_dictionary=self.delete_tasks()
            del self.running_dictionary['pass']
            plan = self.make_plan("Replan",['input','criteria','goal'])
            plan.join()
            self.running_dictionary = dict(self.running_dictionary,**self.planner_queue.get())
            self.running_dictionary["tasks"] = b.BracketParser.get_tasks(self.running_dictionary) 

            supervise = self.start_supervising("Evaluate Plan",['tasks','goal','criteria'])
            supervise.join()
            self.running_dictionary = dict(self.running_dictionary,**self.supervisor_queue.get())
         
    def design(self):
        supervise = self.start_supervising("Get Criteria",['input'])
        supervise.join()
        self.running_dictionary = dict(self.running_dictionary,**self.supervisor_queue.get())
        self.running_dictionary["n"] = self._n_solutions
        self.running_dictionary['tools'] = ["Internet Search","write code","write documentation"]
        design_options = self.create_design("Design",['input','goal','tools','criteria','n'])
        design_options.join()
        self.running_dictionary = dict(self.running_dictionary,**self.designer_queue.get()  )
        supervise = self.start_supervising("Evaluate Designs",['goal','criteria','designs'])
        
    
    def execute(self):
        pass
           
    def get_plan(self,**kwargs):
        self.count_recurse +=1

        plan = self.make_plan("Plan",['input'])
        supervise = self.start_supervising("Get Criteria",['input'])
        plan.join()
        supervise.join()
        
        #combine dictionaries
        self.running_dictionary = dict(self.running_dictionary,**self.supervisor_queue.get(),**self.planner_queue.get())
        self.running_dictionary["tasks"] = b.BracketParser.get_tasks(self.running_dictionary)        
        self.running_dictionary["criteria"] = b.BracketParser.get_criteria(self.running_dictionary)
        
        supervise = self.start_supervising("Evaluate Plan",['tasks','criteria','goal'])
        supervise.join()
        self.running_dictionary = dict(self.running_dictionary,**self.supervisor_queue.get())
        self.sign_off_plan()
        self.dictionaries[str(self.count_recurse)] = self.running_dictionary
        
        for task in self.running_dictionary["tasks"]:
            self.count_recurse+=1
            self.running_dictionary["current_task"] = task
            supervise = self.start_supervising("Evaluate Task",['tasks','current_task'])
            supervise.join()
            self.running_dictionary = dict(self.running_dictionary,**self.supervisor_queue.get())
            
            if (self.running_dictionary["task pass"].lower)!="yes":
                self.get_plan()
            else: 
                self.running_dictionary = {}
                self.running_dictionary["input"]=task
                self.design()
                self.execute()

        
    def run_nodes(self):
        self.get_plan()
        
       
    
if __name__ == '__main__':
    ks = Kitchen_Sink(input.input)
    ks.run_nodes()
    print(ks.running_dictionary)