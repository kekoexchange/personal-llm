import ollama
import constants

def send_message(messages):
    all_messages = [{
        'role': 'system',
        'content': constants.LLM_SYSTEM_PROMPT
        }]
    
    all_messages.extend([
        {
            'role': message.role,
            'content': message.content
        } for message in messages
    ])

    stream = ollama.chat(
        model=constants.LLM_MODEL,
        messages=all_messages,
        stream=True,
    )

    return stream
    