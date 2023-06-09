import openai, os
import pprint


openai.api_key=os.getenv("OPENAI_API_KEY")
print(openai.api_key)
GPT4 = 'gpt-4-0314'
MODEL_NAME = GPT4
model = openai.Model(MODEL_NAME)

def list_all_models():
    model_list = openai.Model.list()['data']
    model_ids = [x['id'] for x in model_list]
    model_ids.sort()
    pprint.pprint(model_ids)

if __name__ == '__main__':
    list_all_models()
    
    import openai, os, test_dictionary
    openai.api_key=os.getenv("OPENAI_API_KEY")
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import HumanMessage, SystemMessage
    

    running_dictionary = test_dictionary.dictionary
    count_recurse = 1
    #llm = OpenAI(model_name="text-davinci-003", temperature=0,max_tokens=2000)  
    llm = ChatOpenAI(model_name='gpt-4',temperature=0,max_tokens=2000)
    filepath = "file1.html"
    batch_messages = [
    
        SystemMessage(content="You are a helpful assistant that translates English to French."),
        HumanMessage(content="I love programming.")
    ]
    
    print(llm([HumanMessage(content="Translate this sentence from English to French. I love programming.")]))