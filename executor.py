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
  
    
    def correct_errors(self):
        err_count = 0
        while err_count < 1:
            code = self.start_thread("Fix Code",['webpage_code','webpage_errors'])
            self.run_thread(code,1)
            if self._running_dictionary["webpage_code"] != ea.read_code_from_file(self._filepath):
                self.check_code()

            err_count += 1
        
    def check_code(self):
        self._running_dictionary["webpage_code"] = ea.lint(self._filepath)
        puppeteer = self.start_thread("Test Code",['webpage_code'])
        self.run_thread(puppeteer,2)
        stderr = ea.check_page_with_puppeteer(self._filepath)
        self._running_dictionary["webpage_errors"] = stderr
    
    def sign_off_code(self):
        approve_code = self.start_thread("Approve Deliverable",['webpage_code','success_criteria','goal','output_format','components'])
        self.run_thread(approve_code)
        if self._running_dictionary["code_pass"].lower().strip()!="yes":
            executor = self.start_thread("Recode",['webpage_code','code_pass_reason'])
            self.run_thread(executor,1)            
            self.test()
    
    def execute(self):
        code = self.start_thread("Write Code",['output','success_criteria','summary','output_format','components','sequence_of_steps_to_complete_output','previous_work'])
        self.run_thread(code,1)
        self.test()
        self._running_dictionary["previous_work"] = self._running_dictionary["webpage_code"]
    
    def test(self):
        self.check_code()
        self.correct_errors()
        self.sign_off_code()    
        
    
if __name__ == '__main__':
    import openai, os, test_dictionary
    openai.api_key=os.getenv("OPENAI_API_KEY")
    from langchain import OpenAI
    running_dictionary = test_dictionary.dictionary
    count_recurse = 1
    llm = OpenAI(model_name="text-davinci-003", temperature=0,max_tokens=3000)  
    filepath = "file1.html"
    
    p = executor(running_dictionary,llm,filepath)
    p.execute()
    print(p._running_dictionary)