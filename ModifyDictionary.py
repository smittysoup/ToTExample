def delete_tasks(running_dictionary):
        for key in running_dictionary.keys():
            if 'task ' in key.lower():
                del running_dictionary[key]
        return running_dictionary
    
def filter_dict(running_dictionary,keys):
    return {k: running_dictionary[k] for k in keys if k in running_dictionary}