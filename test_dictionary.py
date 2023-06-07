dictionary = (
    {  
 'input': '''create a dynamic, modern, interactive website.  The purpose of the website is to allow a user to 
 have a dynamic chat with a large language model, save chat history, and reload prior chats to continue conversations as needed. \n
 The main page should be divided into two sections.  The left navigation, which will contain a history of previous chats, and the main page, which will be split into two horizontal halves.\n
The top half of the main page will display text from an article that the user will read and scroll through.  The text from the article will be interactive, and the user should be able to highlight and right click into the text and see a menu of options.  The menu should include the following: summarize section, ask a question, suggest a topic\n
The bottom half of the main page will be dynamically generated text based on the actions selected in the top half. if the user selects summarize, the bottom half will append text to an existing text box.  If the user selects "ask a question" a chat window will appear with a submit button.  If the user selects suggest a topic, a dynamic pane will appear on the right with a list of clickable topics.  Whatever is clicked will generate a prompt to the LLM for more information. \n
 There should also be an icon at the top right of the main page to save the chat, at which point it is added to the list on the left navigation. \n
 if the user selects a saved chat from the left nav, that chat should appear in the main page window as described above.  \n
 The color scheme should remind me of a forest on a sunny summer day''',
 'n': 3, 
 'pass': 'Yes\n', 
 'webpage_errors': '', 
 'previous_work': None,
 'webpage_code': 'code', 
 'code_pass': 'code_pass', 
 'code_pass_reason': 'code_pass_reason', 
 'task_1': 'I need to create a website with a left navigation menu. \n  ',              
    'task_2': 'I need to create a library of chats in the left navigation menu. \n  ',
    'task_3': 'I need to create a main page with a chat box. \n                    ', 
    'task_4': 'I need to create a button to send chats. \n                    ', 
    'task_5': 'I need to create space to see responses along with the chat history with a timestamp. \n                    ', 
    'task_6': 'I need to create a button to save the chat, at which point it is added to the list on the left navigation. \n                    ', 
    'task_7': 'I need to create a color scheme that reminds me of a forest on a sunny summer day.', 
    'goal': '''Create a website with a left navigation menu, a main page with a chat box, and a color scheme that reminds the user of a forest on a sunny summer day. \n                        \n ''',       
  'success_criteria_1': 'Left navigation menu should contain a library of chats. \n                        ', 
  'success_criteria_2': 'Main page should have a chat box with a button to send chats and space to see responses along with the chat history with a timestamp. \n                        ', 
  'success_criteria_3': 'Button to save the chat, at which point it is added to the list on the left navigation. \n                        ', 
  'success_criteria_4': 'Color scheme should remind the user of a forest on a sunny summer day. \n                        ', 
  'tasks': ['task_1: I need to create a website with a left navigation menu. \n                    ', 
            'task_2: I need to create a library of chats in the left navigation menu. \n                    ', 
            'task_3: I need to create a main page with a chat box. \n          ',
             'task_4: I need to create a button to send chats. \n                    ', 
             'task_5: I need to create space to see responses along with the chat history with a timestamp. \n                    ', 
             'task_6: I need to create a button to save the chat, at which point it is added to the list on the left navigation. \n                    ', 
             'task_7: I need to create a color scheme that reminds me of a forest on a sunny summer day.'], 
  'criteria': ['success_criteria_1: Left navigation menu should contain a library of chats. \n                        ', 
               'success_criteria_2: Main page should have a chat box with a button to send chats and space to see responses along with the chat history with a timestamp. \n                        ', 
               'success_criteria_3: Button to save the chat, at which point it is added to the list on the left navigation. \n                        ', 
               'success_criteria_4: Color scheme should remind the user of a forest on a sunny summer day.'], 
  'success_criteria_5': 'All tasks in the list should be completed before the goal is achieved. \n                        ', 
  'success_criteria_6': 'The completion of the current task should be handed off to the AI system to complete the next task.',
  'reason': "The AI's plan meets all of the criteria. Each sub-task is discrete with logical steps that can be accomplished by a Large Language Model AI, each sub-task is literal and specific, and each sub-task is big enough to be evaluated coherently but small enough to fit into a single prompt to an LLM. In total, completion of the sub-tasks will meet the project's success criteria.", 
  'current_task': 'task_1: I need to create a website with a left navigation menu. \n                    ', 
  'task_pass': 'Yes\n                    ', 
  'task_pass_reason': 'This task is ready to be passed on to a designer as it is a single deliverable, requires only one process, and does not lead to a response that is more than 2,000 words long.',
  'output_option_1': 'Design: The website will have a left navigation menu with a library of chats and a main page with a chat box. The chat box will have a button to send chats and space to see responses along with the chat history with a timestamp. There will also be a button to save the chat, at which point it is added to the list on the left navigation. The color scheme will be generated by the AI using a combination of colors that will remind the user of a forest on a sunny summer day.\n\n', 
  'output_option_2': 'Design: The website will have a left navigation menu with a library of chats and a main page with a chat box. The chat box will have a button to send chats and space to see responses along with the chat history with a timestamp. There will also be a button to save the chat, at which point it is added to the list on the left navigation. The color scheme will be generated by the AI using a combination of colors that will remind the user of a beach on a sunny summer day.\n\n', 
  'output_option_3': 'Design: The website will have a left navigation menu with a library of chats and a main page with a chat box. The chat box will have a button to send chats and space to see responses along with the chat history with a timestamp. There will also be a button to save the chat, at which point it is added to the list on the left navigation. The color scheme will be generated by the AI using a combination of colors that will remind the user of a mountain on a sunny summer day.', 
  'designs': [], 
  'design_output_choice': 'output option 2\n                    ', 
  'reason_for_choice': 'This output option best meets the goals and success criteria of the task. It includes a left navigation menu with a library of chats, a main page with a chat box with a button to send chats and space to see responses along with the chat history with a timestamp, and a button to save the chat, at which point it is added to the list on the left navigation. Additionally, the color scheme is designed to remind the user of a forest on a sunny summer day.', 
  'output': 'Design: The website will have a left navigation menu with a library of chats and a main page with a chat box. The chat box will have a button to send chats and space to see responses along with the chat history with a timestamp. There will also be a button to save the chat, at which point it is added to the list on the left navigation. The color scheme will be generated by the AI using a combination of colors that will remind the user of a beach on a sunny summer day.\n\n', 
  'title': 'Website Design Specification\n\n                    ', 
  'summary': 'This document outlines the design specifications for a website with a left navigation menu, a main page with a chat box, and a color scheme generated by an AI. \n\n                    ', 
  'output_format': 'The website will have a left navigation menu with a library of chats and a main page with a chat box. The chat box will have a button to send chats and space to see responses along with the chat history with a timestamp. There will also be a button to save the chat, at which point it is added to the list on the left navigation. The color scheme will be generated by the AI using a combination of colors that will remind the user of a beach on a sunny summer day.\n\n                    ', 
  'components': '- Left navigation menu\n                    - Main page\n                    - Chat box\n                    - Button to send chats\n                    - Space to see responses\n                    - Chat history with a timestamp\n             - Button to save the chat\n                    - Color scheme generated by AI\n\n                    ', 
  'sequence_of_steps_to_complete_output':       '1. Create left navigation menu with a library of chats.\n                    2. Create main page with a chat box.\n                    3. Add a button to send chats and space to see responses along with the chat history with a timestamp.\n                    4. Add a button to save the chat, at which point it is added to the list on the left navigation.\n                    5. Generate a color scheme using a combination of colors that will remind the user of a beach on a sunny summer day.\n\n                    ', 
  'tools_and_their_uses': '- AI: Generate a color scheme that will remind the user of a beach on a sunny summer day.\n\n                    ', 
  'success_criteria': '- success_criteria_1: Left navigation menu should contain a library of chats.\n                    - success_criteria_2: Main page should have a chat box with a button to send chats and space to see responses along with the chat history with a timestamp.\n                    - success_criteria_3: Button to save the chat, at which point it is added to the list on the left navigation.\n                    - success_criteria_4: Color scheme should remind the user of a beach on a sunny summer day.'
}
)