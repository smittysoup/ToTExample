
class ModifyDictionary:
    def __init__(self,running_dictionary):
        self._running_dictionary = running_dictionary
            
    def delete_items(self,dkey):
            for key in self._running_dictionary.keys():
                if dkey in key.lower():
                    del self._running_dictionary[key]
            return self._running_dictionary

    def get_items(self,dkey):
        task_list = []
        for key, value in self._running_dictionary.items():
            if dkey in key.lower():
                task_list.append(f"{key}: {value}")
        return task_list

    def collapse_dictionary_item(self,item_label,items):
        '''
        Purpose of this function is to combine multiple dictionary items into a single item for input to a prompt template.
        searches the dictionary for the item_label and deletes the item_label 
        then searches the dictionary for all items that contain the item_label and adds them to the dictionary as a collapsed list.
        '''
        self._running_dictionary[item_label] = self.get_items(items)

    def filter_dict(self,keys):
        return {k: self._running_dictionary[k.replace(" ","_")] for k in keys if k.replace(" ","_") in self._running_dictionary}