import re
class BracketParser():
    def __init__(self,output:str):
        self._text = output["node_tasks"]       
        self._lines = self._text.split('\n')
        
    def parse(self):
        pattern_key = r'\[?(?P<key>.+?)\]?:'
        pattern_value = r'(?P<value>.*)'
        text = self._text.strip()
        data_dict = {}
        while text:
            key_match = re.search(pattern_key, text)
            if key_match:
                text = text[key_match.end():].strip()
                value_match = re.search(pattern_value, text)
                if key_match.group('key').lower().strip()=='sequence of steps to complete output':
                    next_key_match = re.search(pattern_key, text)
                    if next_key_match:
                        value_match_str = text[:next_key_match.start()].lower().strip()
                        value_match_str = value_match_str.lower().strip()
                    else: 
                        value_match_str = text
                else:   
                    value_match_str = value_match.group('value').lower().strip()
                if value_match_str:
                    new = {key_match.group('key').lower().strip(): value_match_str}
                    data_dict = dict(data_dict, **new)
                    if key_match.group('key').lower().strip()=='sequence of steps to complete output':
                        if next_key_match:
                            text = text[next_key_match.start():].strip()
                        else: 
                            text = None
                    else: 
                        text = text[value_match.end():].strip()
                        
            else: 
                '''If there is no key, then the value is the output to avoid an infinite loop'''
                if text:
                    new = {'output': text}
                    data_dict = dict(data_dict, **new)
                    text = None
        return data_dict

        
    def split_parse(self):
        data_dict={}
        current_key=None
        for line in self._lines:
            stripped_line = line.strip()
            if stripped_line:
                lines = stripped_line.split(': ')
                for line in lines:
                    stripped_line = line.strip()
                    if stripped_line.startswith('[') and stripped_line.endswith(']'):
                        # If the line is a section title, remove the brackets and colon and set it as the current key
                        current_key = stripped_line[1:-1]
                    elif current_key is not None:
                        # If the line is not a section title and a current key is set, add the line's content to the dictionary under the current key
                        data_dict[current_key.lower()] = stripped_line
                        #reset key
                        current_key = None
        return data_dict
    
    def get_tasks(dictionary):
        task_list = []
        for key, value in dictionary.items():
            if 'task' in key.lower():
                task_list.append(f"{key}: {value}")
        return task_list
    
    def get_criteria(dictionary):
        task_list = []
        for key, value in dictionary.items():
            if 'criteria' in key.lower():
                task_list.append(f"{key}: {value}")
        return task_list
    
    def get_designs(dictionary):
        task_list = []
        for key, value in dictionary.items():
            if 'output' in key.lower():
                task_list.append(f"{key}: {value}")
        return task_list
    
    



