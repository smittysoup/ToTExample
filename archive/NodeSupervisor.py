# Importing required modules and classes
from langchain import OpenAI
import openai, os, threading, test_input, BracketParser as b
from queue import Queue
import ModifyDictionary
from Supervisor import Supervisor

# Setting the OpenAI API key from the environment variables
openai.api_key=os.getenv("OPENAI_API_KEY")

# Defining NodeSupervisor class that extends the Supervisor class
class NodeSupervisor(Supervisor):
    '''
    Class create a supervisor thread that sends a type of query to GPT and stores the resut in the queue object that can then be used in other threads
    requires and instance of Open AI API object from Langchain and a copy of the running dictionary
    
    '''
    def __init__(self, llm, din, task, items_list):
        # Call to the superclass's constructor
        super().__init__(llm)
        self.din = din  # storing din as an instance variable
        self.queue = Queue()  # creating a new queue object
        self.chain = super().get_prompt_chain(items_list,task)
        self.task = task
        self.items_list = items_list        

    def _supervise(self, supervision_list):
        # Filter the input dictionary according to the supervision list
        short_list = ModifyDictionary.filter_dict(self.din, supervision_list)
        # Execute the chain of tasks on the filtered dictionary
        response = self.chain(short_list)
        # Parse the response to create a structured output
        output = b.BracketParser(response)
        parsed_output = output.parse()
        # Put the parsed output to the queue
        self.queue.put(parsed_output)

    def start_thread(self):
        # Create and start a new thread for the supervise method
        thread = threading.Thread(
            target=self._supervise,
            args=(self.items_list,)
            )
        thread.start()
        return thread
    
# The main execution of the program
if __name__ == '__main__':
    # variables for testing
    llm = OpenAI(model_name="text-davinci-003", temperature=0) 
    dictionary_sample = {"input": test_input.input} #will be passed from KS

    # Create an instance of NodeSupervisor with the instantiated OpenAI model and the sample dictionary
    ns = NodeSupervisor(llm, dictionary_sample,"Get Criteria",["input"])
    thread = ns.start_thread()   # Starting the thread
    thread.join #waiting for thread to finish
    print(ns.queue.get()) #printing Results

