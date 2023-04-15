import json
import requests
import re
import string

# Replace 'file_path' with the path to your JSON file
file_path = 'Example.json'

with open(file_path, 'r') as file:
    data = json.load(file)

char_name = data['char_name']
char_persona = data['char_persona']
char_greeting = data['char_greeting']
world_scenario = data['world_scenario']
example_dialogue = data['example_dialogue']

# Now you can use these variables in your code
#print(char_name)
#print(char_persona)
#print(char_greeting)
#print(world_scenario)

# Replace placeholders in example dialogue
example_dialogue = example_dialogue.replace('{{user}}', 'User')
example_dialogue = example_dialogue.replace('{{char}}', char_name)

# Server address
server = "192.168.0.243"

# Generation parameters

params = {
    'max_new_tokens': 200,
    'do_sample': True,
    'temperature': 0.6,
    'top_p': 0.92,
    'typical_p': 1,
    'repetition_penalty': 1.05,
    'encoder_repetition_penalty': 1.0,
    'top_k': 0,
    'min_length': 0,
    'no_repeat_ngram_size': 0,
    'num_beams': 1,
    'penalty_alpha': 0,
    'length_penalty': 1,
    'early_stopping': True,
    'seed': -1,
}

# Memory for messages
memory = []

def process_output(output):
    # Remove 'User:' and everything after it
    output = re.sub(r'User:.*', '', output, flags=re.DOTALL | re.IGNORECASE)

    # Remove hashtags
    output = re.sub(r'#\w+', '', output)

    return output.strip()

def add_to_memory(message):
    global example_dialogue
    memory.append(message)
    example_dialogue += "\n" + message
    if len(memory) > 10:
        oldest_message = memory.pop(0)

def save_example_dialogue_to_file():
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Save only the last 10 messages in example_dialogue
    data['example_dialogue'] = "\n".join(memory)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def generate_text(full_prompt, conversation_history, params):
    context = " ".join(conversation_history)
    
    payload = json.dumps([full_prompt, params])

    response = requests.post(f"http://{server}:7861/run/textgen", json={
        "data": [
            payload
        ]
    }).json()

    return response["data"][0]

if 'keywords_list' in data:
    keywords_list = data['keywords_list']
else:
    keywords_list = {}

replace_indicators = ["new", "replace", "changed"]

def find_keywords(message):
    common_words = [r"\bis\b", r"\bI have a\b", r"\bwas\b"]

    for word in common_words:
        match = re.search(f"(\w+)?\s*{word}\s*(\w+)", message)
        if match:
            keyword = match.group(1).strip()
            info = match.group(2).strip()
            return keyword, info
    return None, None

def update_keywords_list(keyword, info, message):
    replace = False
    for indicator in replace_indicators:
        if indicator in message:
            replace = True
            break

    if keyword not in keywords_list:
        keywords_list[keyword] = [info]
    else:
        if replace:
            keywords_list[keyword] = [info]
        else:
            if info not in keywords_list[keyword]:
                keywords_list[keyword].append(info)

def insert_matching_info(message):
    words = message.split()
    new_words = []
    for word in words:
        stripped_word = word.strip(string.punctuation)
        lowercase_word = stripped_word.lower()
        if lowercase_word in keywords_list:
            info = ', '.join(keywords_list[lowercase_word])
            new_words.append(f"{word} ({info})")
        else:
            new_words.append(word)
    return ' '.join(new_words)

def save_keywords_to_file():
    with open(file_path, 'r') as file:
        data = json.load(file)

    data['keywords_list'] = keywords_list

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Get user input for generating tasks

add_to_memory(example_dialogue)

# Main loop
while True:
    # Loop chat
    prompt = input("User: ")

    keyword, info = find_keywords(prompt)
    if keyword and info:
        update_keywords_list(keyword, info, prompt)    
       
    prompt = insert_matching_info(prompt)       
    add_to_memory(f"User: {prompt}")
    #print(prompt)
    recent_memory = ' '.join(memory[-5:])
    full_prompt = f"Below is an instruction that describes a task. Write a response that appropriately completes the request. ### Instruction: Imagine you are an AI chatbot designed to engage in friendly and informative conversations with users. Your goal is to provide helpful information, answer questions, and keep the conversation flowing naturally. As you interact with the user, remember to be empathetic, respectful, and engaging. Respond ONLY as '{char_name}:'. DO NOT respond as the user. The user's most recent message is: '{prompt}'. Now, let's continue this conversation! {recent_memory} /n ### Response :  {char_name}:"

    #print(full_prompt)

    message_reply = generate_text(full_prompt, memory, params)
    message_reply = message_reply.replace(full_prompt, "")
    message_reply = process_output(message_reply)
    add_to_memory(f"{char_name}: {message_reply}")
    print(char_name + ": " + message_reply)
    save_example_dialogue_to_file()

    # Print JSON output
    json_output = json.dumps(keywords_list, indent=2)
    #print(json_output)
    
    save_keywords_to_file()
