from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.chains import SequentialChain, TransformChain
import openai, os, re

class ExecutorAgent():
    def __init__(self):     
        self.executor_prompt = '''You are a sophisticated AI system based on a large language model. You have a task to complete. \n
                    The goals and success criteria for this task are below:\n
                    [TASK]:{task}\n
                    [GOAL]:{goal}\n
                    [SUCCESS CRITERIA]:{criteria}\n\n
                    
                    You have also been given a detailed design specification by your supervisor for what you should accomplish.  
                    [DESIGN]:{design}
                    
                    Review the design document, first think about what you should do, and then create the output described in the specification. 
                    After you have created the output, review the output against the success criteria above and iterate as needed.  
                    '''   
        