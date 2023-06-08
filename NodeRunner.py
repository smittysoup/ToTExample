# Importing required modules and classes
from langchain import OpenAI
import openai, os, threading, BracketParser as b, test_dictionary
from queue import Queue
from ModifyDictionary import ModifyDictionary
from Persona import Persona
import ExecutorAgent as ea

# Setting the OpenAI API key from the environment variables
openai.api_key=os.getenv("OPENAI_API_KEY")

# Defining NodeSupervisor class that extends the Supervisor class
class Agent(Persona):
    '''
    Class create a persona thread that sends a type of query to GPT and stores the resut in the queue object that can then be used in other threads
    requires and instance of Open AI API object from Langchain and a copy of the running dictionary
    
    '''
    def __init__(self, llm, din):
        # Call to the superclass's constructor
        self._running_dictionary = din  # storing din as an instance variable
        self.queue = Queue()  # creating a new queue object  
        self._llm = llm  # storing the llm as an instance variable      
        self._retry_count = 0

    def _check_label(self,task,result):
        result = result.strip()
        if task == "Write Code":
            if result.startswith("[WEBPAGE CODE]:"):
                return self._parse(result)
            else:
                return self._parse("[WEBPAGE CODE]: " + result)
        elif task == "Test Code":
            if result.startswith("[PUPPETEER SCRIPT]:"):
                return self._parse(result)
            else:
                return self._parse("[PUPPETEER SCRIPT]: " + result)
        elif result.startswith("["):
                return self._parse(result)
        else: 
            return "Invalid task"
        
    
    def _generate(self,task, items_list):
        '''
        This function gets the list of values for prompt input variables, passes the list 
        to the chain, and then returns a response.  The response is passed to the parse function
        '''
        # Filter the input dictionary according to the input list
        dict = ModifyDictionary(self._running_dictionary)
        filtered_dictionary = dict.filter_dict(items_list)
        # Execute the chain of tasks on the filtered dictionary
        chain = self.get_prompt_chain(items_list, task)        
        response = chain.generate([filtered_dictionary])
        print("Tokens Used: " + str(response.llm_output["token_usage"]["total_tokens"])+ "\n")
        # Parse the response to create a structured output
        validate = self._check_label(task,response.generations[0][0].text)
        if validate == "Invalid task" and self._retry_count<3:
            self._retry_count +=1
            print("failed to get valid result...retrying " + str(self._retry_count))
            self._generate(task, items_list)
        return None
    
    def _parse(self,result):
        '''
        This function takes the result from the generate function and parses it into a dictionary
        Each dictionary value is printed to the console and then the dictionary is put into the queue
        '''
        output = b.BracketParser(result)      
        parsed_output = output.parse()
        for k in parsed_output:
            print(k + ": " + parsed_output[k] + "\n")
        # Put the parsed output dictionary into the queue
        self.queue.put(parsed_output)
        return None

    def start_thread(self,task, items_list):
        # Create and start a new thread for the supervise method
        print(f"Starting a new thread for {task} with {items_list}")
        thread = threading.Thread(
            target=self._generate,
            args=(task, items_list)
            )
        thread.start()
        return thread

    def run_thread(self,thread,type=0):
        '''
        wait for thread to finish, then get the result and append it to the running dictionary
        '''
        thread.join()
        result = self.queue.get()
        if result=="Invalid task":
            return result
        elif type==0:
            self._running_dictionary = dict(self._running_dictionary,**result)
            return self._running_dictionary
        elif type==1:
            ea.save_code_to_file(list(result.values())[0],self._filepath)
            return None
        else:
            ea.save_code_to_file(list(result.values())[0],"puppeteer_script.js")
            return None
    
# The main execution of the program
if __name__ == '__main__':

    openai.api_key=os.getenv("OPENAI_API_KEY")
    from langchain import OpenAI
    running_dictionary = test_dictionary.dictionary
    llm = OpenAI(model_name="text-davinci-003", temperature=0) 

    # Create an instance of NodeSupervisor with the instantiated OpenAI model and the sample dictionary

    ns = Agent(llm, running_dictionary,"Test Code",['webpage_code'])
    thread = ns.start_thread()   # Starting the thread
    thread.join #waiting for thread to finish
    print(ns.queue.get()) #printing Results

