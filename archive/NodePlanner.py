# Importing required modules and classes
from langchain import OpenAI
import openai, os, threading, test_input, BracketParser as b
from queue import Queue
import ModifyDictionary
from planner import Planner

# Setting the OpenAI API key from the environment variables
openai.api_key=os.getenv("OPENAI_API_KEY")

# Defining Nodeplanor class that extends the planor class
class NodePlanner(Planner):
    '''
    Class create a panning thread that sends a type of query to GPT and stores the resut in the queue object that can then be used in other threads
    requires and instance of Open AI API object from Langchain and a copy of the running dictionary
    
    '''
    def __init__(self, llm, din):
        # Call to the superclass's constructor
        super().__init__(llm)
        self.din = din  # storing din as an instance variable
        self.queue = Queue()  # creating a new queue object
        self.chain = None        

    def _plan(self, planning_list):
        # Filter the input dictionary according to the planing list
        short_list = ModifyDictionary.filter_dict(self.din, planning_list)
        # Execute the chain of tasks on the filtered dictionary
        response = self.chain(short_list)
        # Parse the response to create a structured output
        output = b.BracketParser(response)
        parsed_output = output.parse()
        # Put the parsed output to the queue
        self.queue.put(parsed_output)

    def start_thread(self, planning_list):
        # Create and start a new thread for the plane method
        thread = threading.Thread(
            target=self._plan,
            args=(planning_list,)
            )
        thread.start()
        return thread

    def set_task(self, task):
        # Define a chain of methods to be called based on the task
        self.chain = super().plan_chain() if task == "Plan" \
            else super().replan_chain() if task == "Replan" \
            else None

# The main execution of the program
if __name__ == '__main__':
    # variables for testing
    llm = OpenAI(model_name="text-davinci-003", temperature=0) 
    dictionary_sample = {"input": test_input.input} #will be passed from KS

    # Create an instance of Nodeplanor with the instantiated OpenAI model and the sample dictionary
    ns = NodePlanner(llm, dictionary_sample)
    ns.set_task("Plan")
    thread = ns.start_thread(["input"])   # Starting the thread
    thread.join #waiting for thread to finish
    print(ns.queue.get()) #printing Results

