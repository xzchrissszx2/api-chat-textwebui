# api-chat-textwebui
Little hacky script to get a chat like interface through the API for Oogaboga text webui

(GPT3 Generated Description of the script below) 

AI Chatbot with Memory and Keyword Extraction. 
This is a Python script that creates an AI chatbot that can engage in friendly and informative conversations with users. The chatbot is designed to be empathetic, respectful, and engaging while providing helpful information and answering questions.

The script uses a JSON file, which is a typical format for storing character information in AI chatbots. However, note that this script modifies the 'Example.json' file, so it is recommended to make a copy of the file before running the script to avoid losing any existing data.

The 'Example.json' file contains the following fields:

char_name: The name of the chatbot character

char_persona: The personality of the chatbot character

char_greeting: The greeting of the chatbot character

world_scenario: The scenario in which the chatbot operates

example_dialogue: A sample dialogue that the chatbot can use as a starting point
The script uses a text-webui server to generate text responses to user inputs. The server address is specified in the script.

The script includes the following functions:

process_output: Removes the 'User:' prefix and any hashtags from the generated text output

add_to_memory: Adds messages to the chatbot's memory

save_example_dialogue_to_file: Saves the last 10 messages in the chatbot's memory to the 'Example.json' file

generate_text: Generates text responses using the text-webui server and the given prompt and conversation history

find_keywords: Extracts keywords and information from user inputs

update_keywords_list: Updates a dictionary of keywords and associated information based on user inputs

insert_matching_info: Inserts associated information for keywords found in user inputs

save_keywords_to_file: Saves the updated keywords dictionary to the 'Example.json' file

To run the script, replace 'file_path' with the path to your copy of the 'Example.json' file and run the script. The chatbot will prompt the user for inputs and generate responses based on the example dialogue and text-webui server. The chatbot's memory and keyword dictionary will be saved to the 'Example.json' file
