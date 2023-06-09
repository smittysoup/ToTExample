from NodeRunner import Agent
from ModifyDictionary import ModifyDictionary
from queue import Queue
import ExecutorAgent as ea

class executor(Agent):
    def __init__(self,running_dictionary,llm,filepath):
        self._running_dictionary = running_dictionary
        self._llm = llm
        self._filepath = filepath
        self.queue = Queue()
        self._retry_count=0
        #TODO: get file extension from exector for save code to file, rather than saving everything as html
    
    def correct_errors(self):
        err_count = 0
        while err_count < 1:
            code = self.start_thread("Fix Code",['code_files','code_errors'])
            self.run_thread(code,1)
            if self._running_dictionary["code_file"] != ea.read_code_from_file(self._filepath):
                self.check_code()

            err_count += 1
        
    def check_code(self):
        self._running_dictionary["code_file"] = ea.lint(self._filepath)
        puppeteer = self.start_thread("Test Code",['code_files'])
        self.run_thread(puppeteer,2)
        stderr = ea.check_page_with_puppeteer(self._filepath)
        self._running_dictionary["code_errors"] = stderr
        return None
    
    def sign_off_code(self):
        recode_count = 0
        approve_code = self.start_thread("Approve Deliverable",['code_files','criteria','goal','output_format','components'])
        self.run_thread(approve_code) and recode_count < 3
        if self._running_dictionary["code_pass"].lower().strip()!="yes":
            recode_count += 1
            executor = self.start_thread("Recode",['code_files','code_pass_reason'])
            self.run_thread(executor,1)            
            self.test()
    
    def execute(self):
        self._llm.max_tokens=4000
        code = self.start_thread("Write Code",['output','summary','output_format','components','sequence_of_steps_to_complete_output','previous_work'])
        self.run_thread(code,1)
        modify_dictionary = ModifyDictionary(self._running_dictionary)
        self._running_dictionary['code_files'] =[]
        self._running_dictionary['code_files'] = modify_dictionary.get_items("code")   
        self.test()
        self._running_dictionary["previous_work"] = self._running_dictionary["code_files"]
        return self._running_dictionary
    
    def test(self):
        #self.check_code()
        #self.correct_errors()
        self.sign_off_code()    
        
    
if __name__ == '__main__':
    import openai, os, test_dictionary
    openai.api_key=os.getenv("OPENAI_API_KEY")
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import HumanMessage, SystemMessage
    

    running_dictionary = test_dictionary.dictionary
    count_recurse = 1
    #llm = OpenAI(model_name="text-davinci-003", temperature=0,max_tokens=2000)  
    llm = ChatOpenAI(model_name='gpt-4',temperature=0,max_tokens=3000)
    
    filepath = "file1.html"
    
    p = executor(running_dictionary,llm,filepath)
    p.execute()
    print(p._running_dictionary)