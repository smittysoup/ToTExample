# Importing required modules and classes
from langchain import OpenAI
import openai, os, threading, test_input, BracketParser as b
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
        self._parse(response.generations[0][0].text)
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
        if type==0:
            self._running_dictionary = dict(self._running_dictionary,**result)
            return self._running_dictionary
        if type==1:
            ea.save_code_to_file(result,"file"+self._filepath)
            return None
        else:
            ea.save_code_to_file(result,"puppeteer_script.js")
            return None
    
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
        "n":str(5),
        'webpage_code': '''<!DOCTYPE html>
        <html>
            <head>
                <title>Website with Left Navigation Menu</title>
                <style>
                    /* CSS styling for the left navigation menu */
                    #left-nav {
                        position: fixed;
                        width: 200px;
                        height: 100%;
                        background-color: #f1f1f1;
                    }
                    #left-nav ul {
                        list-style-type: none;
                        padding: 0;
                    }
                    #left-nav li {
                        padding: 8px;
                    }
                    #left-nav a {
                        text-decoration: none;
                        color: #000;
                    }
                    #left-nav a:hover {
                        background-color: #555;
                        color: #fff;
                    }
                </style>
            </head>
            <body>
                <div id="left-nav">
                    <ul>
                        <li><a href="#">Home</a></li>
                        <li><a href="#">About</a></li>
                        <li><a href="#">Services</a></li>
                        <li><a href="#">Contact</a></li>
                    </ul>
                </div>
                <script>
                    // Javascript code to make the left navigation menu functional
                    const leftNav = document.getElementById('left-nav');
                    leftNav.addEventListener('click', (e) => {
                        const target = e.target;
                        if (target.tagName === 'A') {
                            const href = target.getAttribute('href');
                            window.location.href = href;
                        }
                    });
                </script>
            </body>
        </html>'''
        } #will be passed from KS

    # Create an instance of NodeSupervisor with the instantiated OpenAI model and the sample dictionary

    ns = NodeRunner(llm, dictionary_sample,"Test Code",['webpage_code'])
    thread = ns.start_thread()   # Starting the thread
    thread.join #waiting for thread to finish
    print(ns.queue.get()) #printing Results

