from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.chains import SequentialChain, TransformChain
import openai, os, re

class Designer():
    def __init__(self):     
        self.design_prompt = '''You are a sophisticated AI system based on a large language model. You have been given a task by your supervisor. \n
                    The goals and success criteria for this task are below:\n
                    [TASK]:{task}\n
                    [GOAL]:{goal}\n
                    [SUCCESS CRITERIA]:{criteria}\n\n
                    
                    Your job is to design {n} unique deliverables that a Large Language model could generate to satisfy the goal and success criteria of this task.\n
                    - The AI has several tools optionally available, including {tools}. The AI can use as many of these tools as it needs to create an output.\n
                    - Each deliverable must be something that is achievable for an AI.  \n\n
                    - Each deliverable should contain detailed information about the design of the deliverable, including required inputs components, sub-components, how to handle any possible exceptions, and delivery format.                     
                    
                    Your response should return: \n\n
                    [OUTPUT OPTION 1]:\n
                    [OUTPUT OPTION 2]:\n
                    ...\n
                    [OUTPUT OPTION {n}]:\n
                    '''   
                    
        self.design_plan_prompt = '''You are a sophisticated AI system based on a large language model. You are designing a specification document for the output below:\n
                    [OUTPUT]:{output}\n
                    [SUCCESS CRITERIA]:{criteria}\n\n
                    
                    Format the above output into a specification document.  Return a response in the following format:\n
                    [TITLE]:\n
                    [SUMMARY]:\n
                    [OUTPUT FORMAT]:\n
                    [COMPONENTS]:\n
                    [SEQUENCE OF STEPS TO COMPLETE OUTPUT]:\n
                    [TOOLS AND THEIR USES]:\n                    
                    [SUCCESS CRITERIA]:   \n          

                    '''   
    def _design_chain(self):
        prompt = PromptTemplate(input_variables=['input','goal','tools','criteria','n'], 
                template=(self.design_prompt)
                )
        plan_chain= LLMChain(llm=self._llm, prompt=prompt,output_key="node_tasks",verbose=True)        
        return(plan_chain)
    
    def _design_plan_chain(self):
        prompt = PromptTemplate(input_variables=['output','criteria'], 
                template=(self.design_plan_prompt)
                )
        plan_chain= LLMChain(llm=self._llm, prompt=prompt,output_key="node_tasks",verbose=True)        
        return(plan_chain)
