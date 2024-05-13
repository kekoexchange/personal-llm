import ollama
import constants

def send_chat(messages):
    all_messages = [{
        'role': 'system',
        'content': constants.LLM_SYSTEM_PROMPT
        }]
    
    all_messages.extend([
        {
            'role': role,
            'content': content
        } for role, content in messages
    ])

    stream = ollama.chat(
        model=constants.LLM_MODEL,
        messages=all_messages,
        stream=True,
    )

    return stream
    