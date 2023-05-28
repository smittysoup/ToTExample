from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.chains import SequentialChain, TransformChain
import openai, os, re

class Planner():
    def __init__(self, llm:OpenAI):  
        self._llm=llm
        self._plan_prompt = '''You are a sophisticated AI system based on a large language model. You have been given a starting task by your Supervisor. 
                    Your job is to break this task into a chain of tasks that can be accomplished by a language model.  
                    A chain of tasks includes three important components:\n
                    1. task decomposition. The task should be decomposed into logical, discrete task steps. 
                        Each task represents a manageable piece of the overall task. \n
                    2. tasks are literal in the sense of computational literalism.  Every precise detail is outlined with no room for interpretation.
                    3. In general, a task should be “small” enough so that language models (LMs) can generate promising and diverse samples (e.g.generating
                    a whole book is usually too “big” to be coherent). \n
                    4.. A task should be “big” enough so that LMs can evaluate its prospect toward problem solving 
                    (e.g.generating one token is usually too “small” to evaluate).\n\n
                    
                    Your response should be formatted as a numbered list of tasks.  
                    Each task should start with the phrase "I need to..."\n
                    Your response should be labeled and formatted as shown below: \n\
                    [TASK 1]: \n
                    [TASK 2]: \n
                    etc..\n\n
                    
                    [STARTING TASK]:{input}
                    '''   
        
        self._replan_prompt = '''
                    You are a sophisticated AI system based on a large language model. You have been given a starting task by your supervisor. 
                    To accomplish your work, you previously generated a list of [TASKS] based on the following criteria:\n
                            1. each task is discrete with logical steps that can be accomplished by a Large Language Model AI.
                            2. A task is big enough to be evaluated coherently but small enough to fit into a single prompt to an LLM. 
                            3. In total, completion of the tasks will accomplish the users task. \n\n
                    
                    [STARTING TASK]: {input}\n\n
                    
                    [ORIGINAL TASKS]:{tasks}\n\n
                    
                    Your supervisor has rejected your list of tasks due to the reasons below. \n
                    [REJECTION REASONS]: {rejection}\n\n
                    
                    Modify your tasks to incorporate the feedback from your supervisor.
                    Your response should be formatted as a numbered list of tasks.  Label your tasks as [TASK 1], [TASK 2], etc. 
                    Each task should start with the phrase "I need to..."\n\n
                    [TASKS]:
                    ''' 
                    
    def plan_chain(self):
        prompt = PromptTemplate(input_variables=['input'], 
                template=(self._plan_prompt)
                )
        plan_chain= LLMChain(llm=self._llm, prompt=prompt,output_key="node_tasks",verbose=True)        
        return(plan_chain)
    
    def replan_chain(self):
        prompt = PromptTemplate(input_variables=['input','tasks','rejection'], 
                template=(self._replan_prompt)
                )
        plan_chain= LLMChain(llm=self._llm, prompt=prompt,output_key="node_tasks",verbose=True)        
        return(plan_chain)

