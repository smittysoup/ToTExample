from NodeRunner import Agent
from ModifyDictionary import ModifyDictionary
from queue import Queue
import os, glob

class Architect(Agent):
    def __init__(self, dictionaries, running_dictionary,llm,filepath):
        self._running_dictionary = running_dictionary
        self._llm = llm
        self._filepath = filepath
        self.queue = Queue()
        self._retry_count=0
        self._dictionaries = dictionaries
    
    def Consolidate(self):
        # Join the subdirectory with the wildcard string to match all .txt files
        path = os.getcwd()

        # Initialize an empty string to hold all file contents
        content = ''
        pattern = "*.txt"
        # Loop over all .txt files in the subdirectory
        full_pattern = os.path.join(path, pattern)
        print(path)
        for filename in glob.glob(full_pattern):
            # Open each file
            with open(filename, 'r') as file:
                # Read the file content and add it to the content string
                content += file.read()

        return content

    def execute(self):
        self._llm.max_tokens=1800
        dict = self._dictionaries["task1 subtask0"]
        code_files = self.Consolidate()
        goal = dict["goal"]
        criteria = dict["criteria"]
        new_dict = {"code_files":code_files,"goal":goal,"criteria":criteria}
        self._running_dictionary = new_dict
        self._filepath = "Final.txt"
        code = self.start_thread("Cleanup",['goal','criteria','code_files'])
        
        self.run_thread(code,1)

        return None

        
    
if __name__ == '__main__':
    import openai, os, test_dictionary
    openai.api_key=os.getenv("OPENAI_API_KEY")
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import HumanMessage, SystemMessage
    

    running_dictionary = test_dictionary.dictionary
    dictionaries = test_dictionary.get_dictionaries()
    count_recurse = 1
    #llm = OpenAI(model_name="text-davinci-003", temperature=0,max_tokens=2000)  
    llm = ChatOpenAI(model_name='gpt-4',temperature=0,max_tokens=1800)
    
    filepath = "file1.html"
    
    p = Architect(dictionaries,running_dictionary,llm,filepath)
    p.execute()
    print(p._running_dictionary)