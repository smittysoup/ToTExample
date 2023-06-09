from langchain import OpenAI, PromptTemplate, LLMChain


class Persona():
    def __init__(self, llm):
        self._llm = llm
        
    def get_template(self,template_name):
        result = None

        if template_name == "Get Criteria":
            result = '''
                        You are a the supervisor of a sophisticated AI system based on a large language model. As the supervisor, your job is to understand your users goals, and 
                        monitor the work done by the AI system to ensure that these goals are met.  \n\n
                    
                        The AI system is working on the task below:  \n\n
                        [TASK]: {input}
                        
                        Evaluate the task.  What is the overarching goal that the AI system needs to meet to complete this task?
                        Describe the goal including a discrete list of success criteria.  The success criteria will be used to evaluate whether or not the AI system is successful in completing the task.\n
                        Your response should be labeled and formatted as shown below. \n\n
                        [GOAL]:\n
                        [SUCCESS CRITERIA 1]:\n
                        [SUCCESS CRITERIA 2]:\n
                        ...\n
                        [SUCCESS CRITERIA N]:\n
                        '''
        
        if template_name == "Evaluate Plan":
            result = '''You are a the supervisor of a sophisticated AI system based on a large language model. As the supervisor, your job is to understand your users goals, and 
                        monitor the work done by the AI system to ensure that these goals are met.  \n\n
                        
                        The AI System is creating a plan to complete the user-entered task below.  The plan consists of a task and several sub-tasks that are needed to complete that task.  
                        Evaluate the AI's tasks against the following criteria:  \n
                            1. each sub-task is discrete with logical steps that can be accomplished by a Large Language Model AI.
                            2. each sub-task is literal and specific.  There is sufficient detail in the task that there is no room for interpretation on what is required.
                            3. each sub-task can be encapsulated in a single modular output that can be combined with other outputs. 
                            4. A sub-task is big enough to be evaluated coherently but small enough to fit into a single prompt to an LLM. 
                            5. In total, completion of the sub-tasks will meet your projects success criteria:\n
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
        if template_name == "Refine Goal":
            result = '''You are a the supervisor of a sophisticated AI system based on a large language model. As the supervisor, your job is to
                        monitor the work done by the AI system to ensure goals are met.  \n\n
                    
                    Your project is: {goal} \n\n
                    the success criteria for this project are: {criteria} \n\n
                    
                    Think about the list of tasks for the project, then think about the current task in the list. \n
                    All Tasks: {tasks}\n
                    Current Task: {current_task}\n\n
                    
                    Create a new goal for the current task in your list.  This goal must describe a deliverable that can be accomplished in on query to a large language model. 
                    Assume that you will be able to use the outputs of the tasks that come before your task to complete your goal.  \n\n
                    Write your new goal and new success criteria for this smaller goal.  \n\n  Your output be labeled and formatted as shown below: \n\n
                        [GOAL]:\n
                        [SUCCESS CRITERIA 1]:\n
                        [SUCCESS CRITERIA 2]:\n
                        ...\n
                        [SUCCESS CRITERIA N]:\n                  
                        '''
                        
        if template_name == "Evaluate Task":
            result = '''You are a the supervisor of a sophisticated AI system based on a large language model. As the supervisor, your job is to
                        monitor the work done by the AI system to ensure goals are met.  \n\n
                    
                    The AI System has a planner that thinks about tasks, a designer that comes up with options to complete the task, and an executor who creates task outputs. \n
                    The planner has created a list of tasks that you have approved.  Think about the list of tasks, then think about the current task in the list, exactly as described. 
                    Decide if the task should be further broken down into sub-tasks prior to handing it off to a designer.  A task should be broken down into sub-tasks 
                    if any of the following are true: 
                    1. The tasks would have multiple deliverables
                    2. The task would require multiple processes, technologies or tools to complete. 
                    3. The task would lead to a response that is more than 2,000 words long. 
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
        
        if template_name == "Approve Design":
            result = '''You are a the supervisor of a sophisticated AI system based on a large language model. As the supervisor, your job is to
                        monitor the work done by the AI system to ensure goals are met.  \n\n
                    
                    The AI System has a planner that thinks about tasks, a designer that comes up with options to complete the task, and an executor who creates task outputs. \n
                    The designer has just come up with a list of {n} outputs.  Evaluate the outputs and select one that best fits the goals and success criteria of the task. \n\n
                    [TASK GOAL]: {goal} \n
                    [TASK SUCCESS CRITERIA]: {criteria} \n
                    [DESIGNER OUTPUT OPTIONS]: {designs} \n
                    
                    Your response should be labeled and formatted as shown below: \n
                    [DESIGN OUTPUT CHOICE]: output option [n]\n
                    [REASON FOR CHOICE]: \n
                    '''
                    
        if template_name == "Approve Deliverable":
            result = '''You are a the supervisor of a sophisticated AI system based on a large language model. As the supervisor, your job is to
                        monitor the work done by the AI system to ensure goals are met.  \n\n
                    
                    The system has been working on a job based on the goals and success criteria below:\n
                    [OUTPUT]:{code_files}\n
                    [GOAL]:{goal}\n
                    [SUCCESS CRITERIA]:{criteria}\n\n
                    [REQUIRED COMPONENTS]:{components}\n\n
                    [OUTPUT FORMAT]:{output_format}\n\n
                    
                    Review the output against the requirements, carefully and step by step.  
                    1. Does the output meet all of the success criteria listed above? \n
                    2. Are all the components present in the output? \n
                    3. Is the output in the correct format? \n\n
                    
                    if the code meets all requirements specified, return [CODE PASS]: Yes, and explain why the code passed.  
                    If the code does not meet all of the criteria specified, return [CODE PASS]: No, and explain why the code didn't pass. 
                    The explanation you provide will be used as feedback to iteratively improve the output, so make sure you are specific and clear about what is missing.\n
                    Your response should be labeled and formatted as shown below: \n\n
                            [CODE PASS]: \n
                            [CODE PASS REASON]:   
                    '''
                    
        if template_name == "Plan":
            result = '''Your job is to break this task into a chain of tasks that can be accomplished by a language model.  
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
        
        if template_name == "Replan":
            result = '''You are a sophisticated AI system based on a large language model. You have been given a starting task by your supervisor. 
                    To accomplish your work, you previously generated a list of [TASKS] based on the following criteria:\n
                            1. each task is discrete with logical steps that can be accomplished by a Large Language Model AI.
                            2. A task is big enough to be evaluated coherently but small enough to fit into a single prompt to an LLM. 
                            3. In total, completion of the tasks will accomplish the users task. \n\n
                    
                    [STARTING TASK]: {input}\n\n
                    
                    [ORIGINAL TASKS]:{tasks}\n\n
                    
                    Your supervisor has rejected your list of tasks due to the reasons below. \n
                    [REJECTION REASONS]: {reason}\n\n
                    
                    Modify your tasks to incorporate the feedback from your supervisor.
                    Your response should be formatted as a numbered list of tasks.  Label your tasks as [TASK 1], [TASK 2], etc. 
                    Each task should start with the phrase "I need to..."\n\n
                    [TASKS]:
                    ''' 
                    
        if template_name == "Design":
            result = '''You are a sophisticated AI system based on a large language model. You have been given a task by your supervisor. \n
                    The goals and success criteria for this task are below:\n
                    [TASK]:{input}\n
                    [GOAL]:{goal}\n
                    [SUCCESS CRITERIA]:{criteria}\n\n
                    
                    Your job is to design {n} unique options for deliverables that a Large Language model could generate to satisfy the goal and success criteria of this task. Your supervisor will select from among these options to determine the final output. \n
                    - Each deliverable must be something that is achievable for an AI.  \n\n
                    - Each deliverable must result in only one, modular output.  For example, if the task is to create a website, the output of your design can be a webpage or a python script, but not both.  
                    - Each deliverable should contain detailed information about the design of the deliverable.
                    - Each deliverable should be unique from the other deliverables. \n\n
                    Your response should be labeled and formatted as shown below: \n
                    [OUTPUT OPTION 1]:\n
                    [OUTPUT OPTION 2]:\n
                    etc...
                    '''   
                    
        if template_name == "Design Plan":
            result = '''You are a sophisticated AI system based on a large language model. You are designing a specification document for the output below:\n
                    [OUTPUT]:{output}\n
                    [SUCCESS CRITERIA]:{criteria}\n\n
                    
                    Format the above output into a specification document.  Return a response in the following format:\n
                    [TITLE]:\n
                    [SUMMARY]:\n
                    [OUTPUT FORMAT]:\n
                    [COMPONENTS]:\n
                    [SEQUENCE OF STEPS TO COMPLETE OUTPUT]:\n     

                    '''   
                    
        if template_name == "Write Code":
            result = '''You are a skilled developer.  Your designer has provided you with a specification for a development task. \n
                    Use the requirements below to produce code that meets the success criteria.  \n
                    The code you output must be modular and concise, with liberal use of placeholder text, comments or links if required. \n
                    You may also have completed previous work on this task.  If so, you can use the previous work to help you complete this task, either as a base input or as a reference to complete the task. \n\n
                    [OUTPUT]:{output}\n
                    [SUMMARY]:{summary}\n
                    [OUTPUT FORMAT]:{output_format}\n
                    [COMPONENTS]:{components}\n
                    [SEQUENCE OF STEPS TO COMPLETE OUTPUT]:{sequence_of_steps_to_complete_output}\n
                    [PREVIOUS WORK]:{previous_work}\n\n
                    
                    Use the placeholder http://www.test.com for any hyperlinks. \n Comment out any code that would link to resources such as image files that don't currently exist in your context. \n
                    Your response should be labeled and formatted as shown below.\n\n
                    
                    You must include the label for the [CODE FILE] that you create.  If you have multiple different code files, due to multiple classes within a single language, or due to different languages or components needed for development, label each output as shown. \n\n
                    Note that your response will be parsed by a computer program.  Please ensure that your response is formatted as shown below without additional text:\n\n
                    [CODE FILE 1]: (your code goes here...)\n
                    [CODE FILE 2]: (your code goes here...)\n
                    .....
                    [CODE FILE N]: (your code goes here...)\n

                    '''   
        if template_name == "Recode":
            result = '''You are a skilled web developer and have just finished reviewing a new webpage with your supervisor.  Your supervisor has rejected your code based on the reasons listed below. 
                    webpage: {code_files}\n\n
                    reason for rejection: {code_pass_reason}\n\n
                                        
                    fix the issues in your code and return the corrected code along with an explanation of what you changed.\n
                    if you are unable to fix the issues, return the original code, again with the explanation of why you weren't able to make changes. \n\n
                    You must include the label for the [CODE FILE] that you create.  If you have multiple different code files, due to multiple classes within a single language, or due to different languages or components needed for development, label each output as shown. \n
                    Note that your response will be parsed by a computer program.  Please ensure that your response is formatted as shown below without additional text:\n\n
                    [EXPLANATION]:\n
                    [CODE FILE 1]: (your code goes here...)\n
                    [CODE FILE 2]: (your code goes here...)\n
                    .....
                    [CODE FILE N]: (your code goes here...)\n


                    '''   
        if template_name == "Test Code":
            result = '''You are a skilled web developer.  You have already created an HTML script and will now create a separate Node.js script to use Puppeteer to test your code. 
                    This script would need to do the following: \n
                    1. require libraries for puppeteer and path.\n
                    2. Get the path to the generated page from the command line arguments, specifically process.argv[2].\n
                    3. convert the path to a file://, as it is a local path in the current working directory. 
                       - make sure you get the cwd for the path at runtime, for example: path.resolve(process.cwd(), pagePath)\n
                    4. Load the generated page.\n
                    4.1 add headless: "new" in curly brackets to the launch command: const browser = await puppeteer.launch();\n
                    5. Interact with the page as needed to test any form input fields.  If there are no fields, do not test them.\n
                    6. Evaluate any JavaScript on the page to check for errors.\n
                    7. log any errors to the console. \n
                    
                    Here is the HTML Page you will be testing: \n
                    {code_files}\n\n
                    
                    Your response should be labeled and formatted as shown below: \n
                    [PUPPETEER SCRIPT]: (your script goes here...)\n'''
                    
        if template_name == "Fix Code":
            result = '''You are a skilled web developer and have just finished testing a new webpage.  The webpage render returned the below error messages. 
                    webpage: {code_files}\n\n
                    errors: {code_errors}\n\n
                                        
                    fix the errors in your code and return the corrected code. If the errors are due to links not working, you can assume that the links are placeholders and will be corrected in the final version. \n\n
                    if you are unable to fix the errors, return the original code. \n\n
                    You must include the label for the [CODE FILE] that you create.  If you have multiple different code files, due to multiple classes within a single language, or due to different languages or components needed for development, label each output as shown. \n\n
                    [CODE FILE 1]: (your code goes here...)\n
                    [CODE FILE 2]: (your code goes here...)\n
                    .....
                    [CODE FILE N]: (your code goes here...)\n


                    '''   
                    
        if template_name == "Cleanup":
            result = '''You are a skilled software engineer and architect.  You have just inherited a project with the success criteria described below.  Unfortunately, the code is a mess. \n
                    Each file was not named or commented correctly, and many versions of the same files exist.  some files are markdown, some are html, some are css, some are python, etc.  \n
                    Your job is to sort through all these files and make sure that a final version for each type of code file is created with the full and updated code.  \n\n 
                    Project Goal: {goal}\n\n
                    Project Success Criteria: {criteria}\n\n
                    Code Files: {code_files}\n\n
                                        
                    Return consolidated, commented and clean code files representing the full scale of the work that has been done.\n
                    You must include the label for the [CODE FILE] that you create.  If you have multiple different code files, due to multiple classes within a single language, or due to different languages or components needed for development, label each output as shown. \n\
                    Note that your response will be parsed by a computer program.  Please ensure that your response is formatted as shown below without additional text:\n\n
                    
                    [CODE FILE 1]: (your code goes here...)\n
                    [CODE FILE 2]: (your code goes here...)\n
                    .....
                    [CODE FILE N]: (your code goes here...)\n


                    '''   
        return result
            

    def get_prompt_chain(self,prompt_list,template_name):
        from langchain.prompts.chat import SystemMessagePromptTemplate, ChatPromptTemplate
        string_template = self.get_template(template_name)
       
        prompt = PromptTemplate(input_variables=prompt_list, 
                template=(string_template)
                )
        
        system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt])
        
        eval_plan_chain= LLMChain(llm=self._llm, prompt=chat_prompt,verbose=True)      
        return(eval_plan_chain)
    
 