class BracketParser():
    def __init__(self,output:str):
        self._text = output["node_tasks"]       
        self._lines = self._text.split('\n')
        
    def parse(self):
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

