from langchain import OpenAI, PromptTemplate, LLMChain


class Persona():
    def __init__(self, llm:OpenAI):
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
                        Your output be labeled and formatted as shown below: \n\n
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
        if template_name == "Refine Goal":
            result = '''You are a the supervisor of a sophisticated AI system based on a large language model. As the supervisor, your job is to
                        monitor the work done by the AI system to ensure goals are met.  \n\n
                    
                    The AI System has a planner that thinks about tasks, a designer that comes up with options to complete the task, and an executor who creates task outputs. \n
                    Your main goal is: {goal} \n\n
                    the success criteria for this goal are: {criteria} \n\n
                    
                    The planner has created a list of tasks that you have approved.  First think about the list of tasks, then think about the current task in the list, exactly as described. \n
                    All Tasks: {tasks}\n
                    Current Task: {current_task}\n\n
                    
                    Refine your goal to account for the tasks that are either before your task, after your task, or both. Assume that the AI system will complete all of the tasks in the list,
                    and that you will be able to use the outputs of the tasks that come before your task to complete your goal.  
                    Also assume that the completion of your current tasks should be handed off to the AI to complete the next task.
                    Make sure these assumptions are added as success criteria to your goal. \n\n
                    Make any modifications or additions to your goal needed to take into account this new information.  \n\n  Your output be labeled and formatted as shown below: \n\n
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
                    [OUTPUT]:{webpage_code}\n
                    [GOAL]:{goal}\n
                    [SUCCESS CRITERIA]:{success_criteria}\n\n
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
                    [TOOLS AND THEIR USES]:\n                    
                    [SUCCESS CRITERIA]:   \n          

                    '''   
                    
        if template_name == "Write Code":
            result = '''You are a skilled web developer.  Your designer has provided you with a specification for a webpage. \n
                    use the requirements below to produce webpage code that meets the success criteria.  Your response should be coded using HTML, CSS and Javascript as needed. \n\n
                    [OUTPUT]:{output}\n
                    [SUCCESS CRITERIA]:{criteria}\n\n
                    
                    Format the above output into a specification document.  Return a response in the following format:\n
                    [TITLE]:{title}\n
                    [SUMMARY]:{summary}\n
                    [OUTPUT FORMAT]:{output_format}\n
                    [COMPONENTS]:{components}\n
                    [SEQUENCE OF STEPS TO COMPLETE OUTPUT]:{sequence_of_steps_to_complete_output}\n
                    
                    Use the placeholder http://www.test.com for any hyperlinks. \n Comment out any code that would link to resources such as image files that don't currently exist in your context. \n
                    Your response should be labeled and formatted as shown below.  You must include the label for the [WEBPAGE CODE]: \n
                    [WEBPAGE CODE]: <YOUR HTML CODE...>\n

                    '''   
        if template_name == "Recode":
            result = '''You are a skilled web developer and have just finished reviewing a new webpage with your supervisor.  Your supervisor has rejected your code based on the reasons listed below. 
                    webpage: {webpage_code}\n\n
                    reason for rejection: {code_pass_reason}\n\n
                                        
                    fix the issues in your code and return the corrected code.\n
                    if you are unable to fix the issues, return the original code. \n\n
                    Your response should be labeled and formatted as shown below: \n
                    [WEBPAGE CODE]: <YOUR HTML CODE...>\n

                    '''   
        if template_name == "Test Code":
            result = '''You are a skilled web developer.  You have already created an HTML script and will now create a separate Node.js script to use Puppeteer to test your code. 
                    This script would need to do the following: \n
                    1. require libraries for puppeteer and path.\n
                    2. Get the path to the generated page from the command line arguments, specifically process.argv[2].\n
                    3. convert the path to a file://, as it is a local path in the current working directory. 
                       - make sure you get the cwd for the path at runtime, for example: path.resolve(process.cwd(), pagePath)\n
                    4. Load the generated page.\n
                    4.1 add headless mode to the launch command: const browser = await puppeteer.launch({ headless: "new" });\n
                    5. Interact with the page as needed to test any form input fields.  If there are no fields, do not test them.\n
                    6. Evaluate any JavaScript on the page to check for errors.\n
                    7. log any errors to the console. \n
                    
                    Here is the HTML Page you will be testing: \n
                    {webpage_code}\n\n
                    
                    after you create the code for puppeteer, review the script.  Make sure that it is well formed and will run without any errors.  Add error handling if needed.  Correct any errors you find before returning the script.
                    Your response should be labeled and formatted as shown below: \n
                    [PUPPETEER SCRIPT]: (your script goes here...)\n'''
                    
        if template_name == "Fix Code":
            result = '''You are a skilled web developer and have just finished testing a new webpage.  The webpage render returned the below error messages. 
                    webpage: {webpage_code}\n\n
                    errors: {webpage_errors}\n\n
                                        
                    fix the errors in your code and return the corrected code. If the errors are due to links not working, you can assume that the links are placeholders and will be corrected in the final version. \n\n
                    if you are unable to fix the errors, return the original code. \n\n
                    Your response should be labeled and formatted as shown below: \n
                    [WEBPAGE CODE]: <YOUR HTML CODE...>\n

                    '''   
        return result
            

    def get_prompt_chain(self,prompt_list,template_name):
        string_template = self.get_template(template_name)

        prompt = PromptTemplate(input_variables=prompt_list, 
                template=(string_template)
                )
        
        eval_plan_chain= LLMChain(llm=self._llm, prompt=prompt,output_key="node_tasks",verbose=True)      
        return(eval_plan_chain)
    
 