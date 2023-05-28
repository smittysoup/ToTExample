from langchain import OpenAI, chains, prompts, PromptTemplate, LLMChain
from langchain.chains import SequentialChain, TransformChain
import openai, os, re

openai.api_key=os.getenv("OPENAI_API_KEY")
llm = OpenAI(model_name="text-davinci-003", temperature=0)
tree_depth = 2
current_depth = 0
n_solutions=5

input = '''create a webpage that has a left navigation menu with a library of chats and a main page that has a chat box. 
                        there should be a button to send chats and space to see responses along with the chat history with a timestamp. 
                        There should also be a button to save the chat, at which point it is added to the list on the left navigation. 
                        The color scheme should remind me of a forest on a sunny summer day'''

def do_output_update(current_thought, current_thought_list, outer_thoughts):
    continue_prompt = """
    You are a sophisticated AI system based on a large language model helping a [USER] with a request to build a web page. 
    You have developed a detailed [PLAN] using a chain of thoughts to respond to your users request.  You are detailed and methodical.
    You always work on one [TASK] and [THOUGHT] at a time. You also review the entire plan, including thoughts that came before and after your current thought, to 
    ensure that your thoughts make sense in the context of your overall plan. \n\n
    [PLAN]: {outer_thoughts}\n\n
    [USER]: {current_thought}\n
    [CURRENT THOUGHTS]: {current_thought_list}\n
    
    Come up with {n_solutions} unique variations of responses to the user question for your current thoughts. 
    """
    ToT_prompt = PromptTemplate(input_variables=['outer_thoughts','current_thought','current_thought_list','n_solutions'], 
                template=(continue_prompt))
    
    chain1= LLMChain(llm=llm, prompt=ToT_prompt,output_key="Thoughts",verbose=True)
    result = chain1({'outer_thoughts':outer_thoughts,'current_thought':current_thought,'current_thought_list':current_thought_list,'n_solutions':n_solutions})
    print(result)
    pass

def check_yes(text):
    if re.search(r'\[YES\]', text):
        return '[YES]'
    else:
        return '[NO]'                        
     
def parse_thoughts(input:str):
    
    starting_prompt = '''
                        You are a sophisticated AI system based on a large language model. You have been given a task by your [USER]. 
                        Break this task into a chain of thoughts that can be accomplished by a language model.  
                        A chain of thoughts includes three important components:\n
                        1. Thought decomposition. The task should be decomposed into logical, discrete thought steps. 
                            Each thought represents a manageable piece of the overall task. \n
                        2. In general, a thought should be “small” enough so that language models (LMs) can generate promising and diverse samples (e.g.generating
                        a whole book is usually too “big” to be coherent). \n
                        3. a thought should be “big” enough so that LMs can evaluate its prospect toward problem solving 
                        (e.g.generating one token is usually too “small” to evaluate).\n\n
                        
                        Your response should be formatted as a numbered list of thoughts.  Label your thoughts as [THOUGHT 1], [THOUGHT 2], etc. 
                        Each thought should start with the phrase "I need to..."\n\n
                        '''

    ToT_prompt = PromptTemplate(input_variables=['input','starting_prompt'], 
                    template=('''
                            {starting_prompt}
                            
                            [USER]: {input}                        
                            
                            ''')
                    )
    chain1= LLMChain(llm=llm, prompt=ToT_prompt,output_key="Thoughts",verbose=True)


    ToT_self_eval = PromptTemplate(input_variables=['Thoughts','input','starting_prompt'],
                                template=('''
                            {starting_prompt}
                            
                            [USER]: {input}. \n\n
                            [AI THOUGHTS]: {Thoughts}\n\n
                            
                            Evaluate your thoughts above for the following criteria:
                            1. each thought is discrete with logical steps that can be accomplished by a Large Language Model AI.
                            2. A thought is big enough to be evaluated coherently but small enough to fit into a single prompt to an LLM. 
                            3. In total, completion of the thoughts will meet the users request. 
                            
                            If the thoughts meet the criteria, return [YES].  If the thoughts do not meet the criteria, return
                            [NO]\n
                            [REASON]
                                                
                            
                            ''')
                                )
    chain2 = LLMChain(llm=llm, prompt=ToT_self_eval,output_key="eval",verbose=True)

    #parse1 = TransformChain(input_variables=["eval"],output_variables=["final_thoughts"],transform=parse_thoughts)
    ssc = SequentialChain(
        input_variables=["input","starting_prompt"],
        chains=[chain1,chain2],
        output_variables=["eval","Thoughts"])

    result = ssc({"input":input,"starting_prompt":starting_prompt})

    print(result["eval"],result["Thoughts"])

    evalstring=(result["eval"].strip())
    checkyes = check_yes(evalstring)
    while checkyes!="[YES]":
        ToT_re_eval = PromptTemplate(input_variables=['Thoughts','input','starting_prompt','eval'],
                                template=('''
                            {starting_prompt}
                            
                            [USER]: {input}. \n\n
                            [AI THOUGHTS]: {Thoughts}\n\n
                            
                            when asked to determine if your thoughts were correct and complete you said: {eval}.
                            Modify the thoughts above based on your self-evaluation.  
                            Your response should be a new list of thoughts in the format of [THOUGHT 1], [THOUGHT 2] etc.
                            
                            '''))
        
        ToT_self_eval = PromptTemplate(input_variables=['rethink','input','starting_prompt'],
                                template=('''
                            {starting_prompt}
                            
                            [USER]: {input}. \n\n
                            [AI THOUGHTS]: {rethink}\n\n
                            
                            Evaluate your thoughts above for the following criteria:
                            1. each thought is discrete with logical steps that can be accomplished by a Large Language Model AI.
                            2. A thought is big enough to be evaluated coherently but small enough to fit into a single prompt to an LLM. 
                            3. In total, completion of the thoughts will meet the users request. 
                            
                            If the thoughts meet the criteria, return [YES].  If the thoughts do not meet the criteria, return
                            [NO]\n
                            [REASON]
                                                
                            
                            ''')
                                )
        chain2_1=LLMChain(llm=llm,prompt=ToT_re_eval,output_key=["rethink"],verbose=True)
        chain2_2=LLMChain(llm=llm,prompt=ToT_self_eval,output_key=["reeval"],verbose=True)
        rsc=SequentialChain(input_variables=['Thoughts','input','starting_prompt','eval'],
                            chains=[chain2_1,chain2_2],
                            output_variables=["reeval","rethink"])
        reeval_result = rsc({"Thoughts":result["Thoughts"],"input":input,"starting_prompt":starting_prompt,"eval":evalstring})
        result["Thoughts"]=reeval_result["rethink"]        
        evalstring=reeval_result["reeval"]
        
    return result
        
def do_thought(thought:str,outerthought=[],current_depth=1):
    result = parse_thoughts(thought)
    result["Thoughts"]=result["Thoughts"].strip()
    try:
        thought_list = re.findall(r'\[THOUGHT \d+](?:\:)? (.+)', result["Thoughts"])
    except: 
        print("unable to parse thoughts, please run again")
    
    if current_depth < tree_depth:
        current_depth+=1
        for thought in thought_list:
            new_input = input + "\n\n[YOUR TASK]: " + thought +"\n\n"
            do_thought(new_input,result["Thoughts"],current_depth)
    else:
        do_output_update(result["input"], result["Thoughts"],outerthought)

do_thought(input)

    
    
    