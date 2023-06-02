# Importing required modules and classes
from langchain import OpenAI
import openai, os, threading, test_input, BracketParser as b
from queue import Queue
import ModifyDictionary
from Persona import Persona

# Setting the OpenAI API key from the environment variables
openai.api_key=os.getenv("OPENAI_API_KEY")

# Defining NodeSupervisor class that extends the Supervisor class
class NodeRunner(Persona):
    '''
    Class create a persona thread that sends a type of query to GPT and stores the resut in the queue object that can then be used in other threads
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
        filtered_dictionary = ModifyDictionary.filter_dict(self.din, supervision_list)
        short_list = []
        # Execute the chain of tasks on the filtered dictionary
        response = self.chain.generate([filtered_dictionary])
        print("Tokens Used: " + str(response.llm_output["token_usage"]["total_tokens"])+ "\n")
        result = response.generations[0][0].text
        # Parse the response to create a structured output
        output = b.BracketParser(result)
        
        parsed_output = output.parse()
        for k in parsed_output:
            print(k + ": " + parsed_output[k] + "\n")
        # Put the parsed output to the queue
        self.queue.put(parsed_output)

    def start_thread(self):
        # Create and start a new thread for the supervise method
        print(f"Starting a new thread for {self.task} with {self.items_list}")
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
    dictionary_sample = {
        "input": test_input.input,
        "output": "output option 2: the ai will use the write code tool to create a webpage with a left navigation menu. the ai will use the internet search tool to find existing webpages with a left navigation menu that are aesthetically pleasing, functional, and optimized for mobile devices and seo. the ai will then use the write code tool to create a webpage with a left navigation menu based on the existing webpages. the ai will also use the write documentation tool to create detailed instructions on how to use the webpage and left navigation menu. the deliverable will be a webpage with a left navigation menu and accompanying documentation.",
        "goal": "make webpage",
        "tools": "write code",
        "criteria": '''
            success criteria 1: the webpage should be aesthetically pleasing.
            success criteria 2: the left navigation menu should be functional and easy to use.
            success criteria 3: the webpage should be optimized for mobile devices.
            success criteria 4: the webpage should be optimized for search engine optimization (seo).
        ''',
        "n":str(5)
        } #will be passed from KS

    # Create an instance of NodeSupervisor with the instantiated OpenAI model and the sample dictionary

    ns = NodeRunner(llm, dictionary_sample,"Design Plan",['output','criteria'])
    thread = ns.start_thread()   # Starting the thread
    thread.join #waiting for thread to finish
    print(ns.queue.get()) #printing Results

