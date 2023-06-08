import re
class BracketParser():
    def __init__(self,output:str):
        self._text = output.strip() 
        
    def parse(self):
        '''this parser will capture any text that is between the first set of brackets
        then it will capture any text that is after the first set of brackets.  The text position is used to 
        extract the key and value from the text.  The key is the text between the brackets and the value is the text'''
        pattern_key = r'\[(?P<key>[A-Za-z0-9\s]+)\]:?'
        text = self._text
        data_dict = {}
        
        #start parsing text
        while text:
            #look for the first set of brackets in the text string
            key_match = re.search(pattern_key, text)
            print("searching for key in text: "+text)
            
            if key_match:
                #clean the text - lower case, strip, replace spaces with underscores
                dkey = key_match.group('key')
                key_val = self.clean(dkey)
                
                #create a new text string with everything following the key
                new_text = text[key_match.end():].strip()
                
                #check if there was any text after the key
                # if so, check if there is another key, add text until the new key is found 
                # if not, add the remaining text to the value
                if new_text:                    
                    next_key_match = re.search(pattern_key, new_text)
                    
                    if next_key_match and key_val != "puppeteer_script" and (key_val != "code_file_1" or key_val != "code_file_2" or key_val != "code_file_3"):
                        value_match = new_text[:next_key_match.start()]
                    else:
                        value_match = new_text
                        
                else: 
                    value_match = 'Unable to get any value for key from parser!!'
                    
                #add the key and value to the dictionary
                new_entry = {key_val: value_match}
                data_dict = dict(data_dict, **new_entry)
                
                #reset text to the remaining text
                if len(new_text) > len(value_match)+1:
                    text = text[len(value_match):]
                else:
                    text = None
                
            #handle cases where no key is found
            else: 
                print("No Key Found in text to parse!!")
                text = None #exit loop
                
        return data_dict
    
    def clean(self, text,opt=1):
        text = text.lower()
        text = text.strip()
        if opt==1:
            text = text.replace(" ","_")
        return text

        
    



