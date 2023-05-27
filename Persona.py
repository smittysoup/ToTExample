from langchain import OpenAI, PromptTemplate, LLMChain


class Persona():
    def __init__(self, llm:OpenAI):
        self._llm = llm

        self.get_success_criteria = '''
                        You are a the supervisor of a sophisticated AI system based on a large language model. As the supervisor, your job is to understand your users goals, and 
                        monitor the work done by the AI system to ensure that these goals are met.  \n\n
                    
                        The AI system is working on the task below:  \n\n
                        [TASK]: {input}
                        
                        Evaluate the task.  What is the overarching goal that the AI system needs to meet to complete this task?
                        Describe the goal including a discrete list of success criteria.  The success criteria will be used to evaluate whether or not the AI system is successful in completing the task.\n
                        Your output be labeled and formatted as shown below: \n\n
                        [GOAL]:\n
                        [SUCCESS CRITERIA 1]:\n
                        [SUCCESS CRITERIA 2]:\n
                        ...\n
                        [SUCCESS CRITERIA N]:\n
                        '''
        
        self.eval_tasks = '''You are a the supervisor of a sophisticated AI system based on a large language model. As the supervisor, your job is to understand your users goals, and 
                        monitor the work done by the AI system to ensure that these goals are met.  \n\n
                        
                        The AI System is creating a plan to complete the user-entered task below.  The plan consists of a task and several sub-tasks that are needed to complete that task.  
                        Evaluate the AI's tasks against the following criteria:  \n
                            1. each sub-task is discrete with logical steps that can be accomplished by a Large Language Model AI.
                            2. each sub-task is literal and specific.  There is sufficient detail in the task that there is no room for interpretation on what is required.
                            3. A sub-task is big enough to be evaluated coherently but small enough to fit into a single prompt to an LLM. 
                            4. In total, completion of the sub-tasks will meet your projects success criteria:\n
                                 {criteria}\n
                                \n
                        [USER TASK]: {goal}
                        [AI PLAN]: {tasks} \n\n
                        
                        If the tasks meet all of the criteria, return [PASS]: Yes, and explain why the response passed.  
                        If the tasks do not meet the criteria, return [PASS]: No, and explain why the result didn't pass. \n
                        Your response should be labeled and formatted as shown below: \n\n
                            [PASS]: \n
                            [REASON]:       
                        '''
        self.eval_task = '''
                    You are a the supervisor of a sophisticated AI system based on a large language model. As the supervisor, your job is to
                        monitor the work done by the AI system to ensure goals are met.  \n\n
                    
                    The AI System has a planner that thinks about tasks, a designer that comes up with options to complete the task, and an executor who creates task outputs. \n
                    The planner has created a list of tasks that you have approved.  Think about the list of tasks, then think about the current task in the list, exactly as described. 
                    Decide if the task should be further broken down into sub-tasks prior to handing it off to a designer.  A task should be broken down into sub-tasks 
                    if the tasks would have multiple deliverables, require multiple processes, technologies or tools to complete, or lead to a response that is more than 2,000 words long. 
                    Make sure you are only considering the current task in the list, remembering that you will not need to make subtasks that are already in the plan.  
                    Make sure that you only consider what is literally listed in the task with the simplest interpretation possible, without making up any additional requirements.  \n\n
                    
                    [Overall Plan]: {tasks}\n
                    [AI Current task]: {current_task}\n\n
                    
                    If the task is ready to passed on to a designer, return [TASK PASS]: Yes, and explain why the response passed.  
                    If the tasks is not ready to be passed on to a designer, return [TASK PASS]: No, and explain why the result didn't pass. \n
                    Your response should be labeled and formatted as shown below: \n\n
                            [TASK PASS]: \n
                            [TASK PASS REASON]:   
                    '''
        
        self.eval_design = '''
                    You are a the supervisor of a sophisticated AI system based on a large language model. As the supervisor, your job is to
                        monitor the work done by the AI system to ensure goals are met.  \n\n
                    
                    The AI System has a planner that thinks about tasks, a designer that comes up with options to complete the task, and an executor who creates task outputs. \n
                    The designer has just come up with a list of {n} outputs.  Evaluate the outputs and select one that best fits the goals and success criteria of the task. \n\n
                    [TASK GOAL]: {goal} \n
                    [TASK SUCCESS CRITERIA]: {criteria} \n
                    [DESIGNER OUTPUT OPTIONS]: {designs} \n
                    
                    Your response should be labeled and formatted as shown below: \n
                    [DESIGN OUTPUT CHOICE]: \n
                    [REASON FOR CHOICE]: \n
                    '''
                    
        self.eval_output = '''
                    You are a the supervisor of a sophisticated AI system based on a large language model. As the supervisor, your job is to
                        monitor the work done by the AI system to ensure goals are met.  \n\n
                    
                    The system has been working on an [OUTPUT] based on the task, goals and success criteria below:\n
                    [OUTPUT]:{output}\n
                    [GOAL]:{goal}\n
                    [SUCCESS CRITERIA]:{criteria}\n\n
                    
                    Evaluate the output and decide whether it meets the goal and success criteria described. If the output meets all of the criteria, return [YES].  If the output does not meet the criteria, return
                            [NO]\n
                            [REASON]  
                    '''
                    
        self.plan_prompt = '''You are a sophisticated AI system based on a large language model. You have been given a starting task by your Supervisor. 
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
        
        self.replan_prompt = '''
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
                    
        self.design_prompt = '''You are a sophisticated AI system based on a large language model. You have been given a task by your supervisor. \n
                    The goals and success criteria for this task are below:\n
                    [TASK]:{input}\n
                    [GOAL]:{goal}\n
                    [SUCCESS CRITERIA]:{criteria}\n\n
                    
                    Your job is to design {n} unique options for deliverables that a Large Language model could generate to satisfy the goal and success criteria of this task. Your supervisor will select from among these options to determine the final output. \n
                    - The AI has several tools optionally available, including {tools}. The AI can use as many of these tools as it needs to create an output.\n
                    - Each deliverable must be something that is achievable for an AI.  \n\n
                    - Each deliverable should contain detailed information about the design of the deliverable, including required inputs components, sub-components, how to handle any possible exceptions, and delivery format.                     
                    
                    Return a response in the following format: \n\n
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
    def get_prompt_chain(self,prompt_list,template_name):
        string_template = self.get_success_criteria if template_name == "Get Criteria" \
            else self.eval_tasks if template_name == "Evaluate Plan" \
            else self.eval_task if template_name=="Evaluate Task" \
            else self.eval_design if template_name=="Approve Design" \
            else self.eval_output if template_name=="Approve Deliverable" \
            else self.plan_prompt if template_name=="Plan" \
            else self.replan_prompt if template_name=="Replan" \
            else self.design_prompt if template_name=="Design" \
            else self.design_plan_prompt if template_name=="Design Plan" else None

        prompt = PromptTemplate(input_variables=prompt_list, 
                template=(string_template)
                )
        
        eval_plan_chain= LLMChain(llm=self._llm, prompt=prompt,output_key="node_tasks")        
        return(eval_plan_chain)
    
 