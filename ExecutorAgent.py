'''
1.  The agent recieves a spec from the designer.  
2. The agent should decide what type of code needs to be written.  
3. The agent should write the code.
4. Depending on what type of code was chosen, run code through a validator and a linter.
5. Start with only HTML.  The agent should write HTML code.
6.  Along with the code the agent should use puppeteer to write a test for the code.
7.  the agent should write a python subprocess that runs the test.
8.  The agent should run the test.
'''

# Importing required modules and classes
from langchain import OpenAI
import openai, os, threading, test_input, BracketParser as b
from queue import Queue
import ModifyDictionary
from Persona import Persona
import html5lib

# Setting the OpenAI API key from the environment variables
openai.api_key=os.getenv("OPENAI_API_KEY")

# Defining NodeSupervisor class that extends the Supervisor class

def get_code(self):
    code = self.ks.add_agent("Write Code",['output','criteria','title','summary','output_format','components','sequence_of_steps_to_complete_output'])
    return code
def html_linter(self,code):
    parser = html5lib.HTMLParser(strict=True)
    return parser.parse(code)


if __name__ == '__main__':
    # variables for testing
    llm = OpenAI(model_name="text-davinci-003", temperature=0) 
    dictionary_sample = { "output": '''
                         Design a webpage with a left navigation menu that is aesthetically pleasing, functional, and optimized for mobile devices and seo. the webpage should be designed using html, css, and javascript. the left navigation menu should be designed using html and css. the webpage should be tested for responsiveness and compatibility with different browsers. additionally, the webpage should be optimized for accessibility, with features such as high contrast mode, keyboard navigation, and screen reader support.
                         ''', 'critieria': '''
                         success criteria 1: the webpage should be aesthetically pleasing.
                        success criteria 2: the left navigation menu should be functional and easy to use.
                        success criteria 3: the webpage should be optimized for mobile devices.
                        success criteria 4: the webpage should be optimized for search engine optimization (seo).
                        ''','title':'designing a webpage with a left navigation menu','summary':'''this document outlines the specifications for designing a webpage with a left navigation menu that is aesthetically pleasing, functional, and optimized for mobile devices and seo.
                        ''','output_format':'''the webpage should be designed using html, css, and javascript. the left navigation menu should be designed using html and css.  ''',
                        'components':'''the webpage should include a left navigation menu, and should be optimized for accessibility, with features such as high contrast mode, keyboard navigation, and screen reader support.''',
                        'sequence_of_steps_to_complete_ouptut': 
                        '''1. design the webpage using html, css, and javascript.
                        2. design the left navigation menu using html and css.
                        3. test the webpage for responsiveness and compatibility with different browsers.
                        4. optimize the webpage for accessibility, with features such as high contrast mode, keyboard navigation, and screen reader support.
                        5. optimize the webpage for mobile devices and seo.'''}
  