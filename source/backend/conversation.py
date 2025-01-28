import ollama

SYSTEM_PROMPT = """
   Your are a smart assistant helping user with their gardening.
   You talk about different flowers Rhododendron, jasmine, azalea, golden-dewdrop.
   You are to keep your answers short and consice. Do not add unnecessary details and just answer what has been asked.
   You are to be polite and helpful to the user. Do not give long answers make it very short.  
"""

conversation_history = []

def update_context(context):
    """Updates the system context"""
    for item in conversation_history:
        if item['role'] == 'system':
            item['content'] = context
    


def conversationAI(prompt: str, context: str):
    """Function to have conversation with the bot"""
    ### Adding System Prompt ###
    if not conversation_history:
        conversation_history.append({
            "role": "system",
            "content": SYSTEM_PROMPT + " \n " + context,
        })
    else:
        update_context(context)
    
    ### Adding User Prompt ###
    conversation_history.append({
        "role": "user",
        "content": prompt,
    })

    ### Prompting the Model ###
    response = ollama.chat(
        model="llama3.2",
        messages=conversation_history
    )
    
    ### Adding Assistant Responst ###
    conversation_history.append({
        "role": "assistant",
        "content": response["message"]["content"],
    })
    
    return response["message"]["content"]
    