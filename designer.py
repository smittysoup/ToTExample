from NodeRunner import Agent
from ModifyDictionary import ModifyDictionary
from queue import Queue

class designer(Agent):
    def __init__(self,running_dictionary,llm,filepath):
        self._running_dictionary = running_dictionary
        self._llm = llm
        self._filepath = filepath
        self.queue = Queue()
  
    def design(self):
        '''
        get design options and have LLM choose best one based on goal and criteria
        '''
        design_options = self.start_thread("Design",['input','goal','criteria','n'])
        self.run_thread(design_options)
        modify_dictionary = ModifyDictionary(self._running_dictionary)      
        self._running_dictionary['designs'] = modify_dictionary.get_items("design")  
        
        choose_option = self.start_thread("Approve Design",['goal','criteria','designs','n'])
        self.run_thread(choose_option)
        
        key_text = self._running_dictionary["design_output_choice"].strip().replace(" ","_")
        self._running_dictionary["output"] = self._running_dictionary[key_text]
        design_plan = self.start_thread("Design Plan",['output','criteria'])
        self.run_thread(design_plan)
    
if __name__ == '__main__':
    import openai, os, test_dictionary
    openai.api_key=os.getenv("OPENAI_API_KEY")
    from langchain import OpenAI
    running_dictionary = test_dictionary.dictionary
    count_recurse = 1
    llm = OpenAI(model_name="text-davinci-003", temperature=0,max_tokens=3000)  
    filepath = "file1.html"
    
    p = designer(running_dictionary,llm,filepath)
    p.design()
    print(p._running_dictionary)