
from pptx import Presentation
import os
import openai
import json
import asyncio

#api_key = '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' for excellentim
API_KEY= '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' #excellentim tal

# set the behaviour of the system
messages = [
    {"role": "system",
     "content": "You should explain the slide content a user gives you, You should write it in a way"
                "the age group provided can understand, when explaining the slide,"
                "take into consideraton the extra information given to you, in order to explain"
                "the slide even better."}
]
slide_explanation=[]
openai.api_key = API_KEY


'''
gets response from chatgpt
'''
def sendToChatGPT(explanation_data, slide_dict_info,slide_number):

    print(slide_dict_info)
    content=""
    for key,value in slide_dict_info.items():
        content += " "+key + " : " + value+" "
    #print(content)
    #print("\n")
    #sets the instructions
    messages.append({"role": "user",
                     "content": content })

    completion = ( openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    ))

    chat_response = (completion.choices[0].message.content)
    print(chat_response)
    print("\n")
    #save the previous responses
    messages.append({"role": "assistant", "content": chat_response})


    slide_explanation.append("explanation for slide "+str(slide_number)+" : \n"+chat_response)
    # Add the chat response to the JSON object
    explanation_data[f"slide_{slide_number}"] = {
        #"slide_info": slide_dict_info,
        "explanation": chat_response
    }

    return explanation_data  # Return the updated explanation data



# def main():
#     openai.api_key = API_KEY
#     ppName = 'End of course exercise - kickof - upload (1)'
#     read_powerpoint(ppName)
#
#     #print(list_to_read)
#     #print(len(list_to_read))
#     with open('slide_explanations.json', 'w') as json_file:
#         json.dump(slide_explanation, json_file, indent=4)
#
#
# if __name__ == '__main__':
#     main()

