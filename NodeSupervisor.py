# Importing required modules and classes
from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.chains import SequentialChain, TransformChain
import openai, os, threading
from queue import Queue
import ModifyDictionary

# Setting the OpenAI API key from the environment variables
openai.api_key=os.getenv("OPENAI_API_KEY")

# Defining NodeSupervisor class that extends the Supervisor class
class NodeSupervisor:
    def __init__(self, llm, din):
        # Call to the superclass's constructor
        super().__init__(llm = llm)
        self.din = din  # storing din as an instance variable
        self.queue = Queue()  # creating a new queue object
        self.task = "default"  # defining a default task

        # Define a chain of methods to be called based on the task
        self.chain = super()._get_criteria() if self.task=="Get Criteria" \
                else super()._eval_plan_chain() if self.task=="Evaluate Plan" \
                else super()._eval_task() if self.task=="Evaluate Task" \
                else super()._eval_design() if self.task=="Approve Design" \
                else super()._eval_output() if self.task=="Approve Deliverable" else None

    def supervise(self, supervision_list):
        # Filter the input dictionary according to the supervision list
        short_list = ModifyDictionary.filter_dict(self.din, supervision_list)
        # Execute the chain of tasks on the filtered dictionary
        self.response = self.chain(short_list)
        # Parse the response to create a structured output
        self.output = b.BracketParser(self.response)
        self.parsed_output = self.output.parse()
        # Put the parsed output to the queue
        self.queue.put(self.parsed_output)

    def start_thread(self, supervision_list):
        # Create and start a new thread for the supervise method
        thread = threading.Thread(
            target=self.supervise,
            args=(supervision_list,)
            )
        thread.start()
        return thread

    def set_task(self, task):
        # Method to set the task
        self.task = task

# The main execution of the program
if __name__ == '__main__':
    # Instantiate the OpenAI model
    llm = OpenAI(model_name="text-davinci-003", temperature=0) 

    # A dictionary sample
    dictionary_sample = {"input": input.input} #will be passed from KS

    # Create an instance of NodeSupervisor with the instantiated OpenAI model and the sample dictionary
    ns = NodeSupervisor(llm, dictionary_sample)
    ns.set_task("Get Criteria")  # Setting the task
    thread = ns.start_thread(["input"])   # Starting the thread
    thread.join
    print(ns.queue.get())

