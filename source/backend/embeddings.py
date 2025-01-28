import ollama
import json
import os
import numpy as np
from numpy.linalg import norm


def save_embeddings(embeddings):
    """Stores embeddings in the local json database"""
    file_name = "all_embeddings"
    
    if not os.path.exists("embeddings"):
        os.makedirs("embeddings")
    
    with open(f"embeddings/{file_name}.json", "w") as file:
        json.dump(embeddings, file)

def save_paragraphs(paragraphs):
    """Stores paragraphs in the local json database"""
    file_name = "all_paragraphs"
    
    if not os.path.exists("embeddings"):
        os.makedirs("embeddings")
    
    with open(f"embeddings/{file_name}.json", "w") as file:
        json.dump(paragraphs, file)

def load_embeddings():
    """Checks whether embeddings are present or not and returns the embeddings"""
    file_name = "all_embeddings"
    
    if not os.path.exists(f"embeddings/{file_name}.json"):
        return False
    
    with open(f"embeddings/{file_name}.json", "r") as file:
        return json.load(file)


def get_embeddings(paragraphs):
    """Generates embeddings form the paragraphs and saves them"""
    
    valid_paragraphs = []
    valid_embeddings = []
    
    for paragraph in paragraphs:
        embedding = ollama.embeddings(model='nomic-embed-text', prompt=paragraph)["embedding"]
        if len(embedding) > 0:  # Check if the embedding is non-empty
            valid_paragraphs.append(paragraph)
            valid_embeddings.append(embedding)
            
    save_embeddings(valid_embeddings)
    save_paragraphs(valid_paragraphs)

def find_similar(prompt, embedding):
    needle_norm = norm(prompt)
    similarity_scores = [
        np.dot(prompt, item) / (needle_norm * norm(item)) for item in embedding
    ]
    return sorted(zip(similarity_scores, range(len(embedding))), reverse=True)

def get_paragraphs():
    with open('backend/embeddings/all_paragraphs.json', 'r') as json_file:
        paragraph = json.load(json_file)
    return paragraph

def get_embedding():
    with open('backend/embeddings/all_embeddings.json', 'r') as json_file:
        embedding = json.load(json_file)
    return embedding

def generate_context(prompt: str):
    prompt_embedding = ollama.embeddings(model="nomic-embed-text", prompt=prompt)["embedding"]
    
    paragraphs = get_paragraphs()
    embeddings = get_embedding()
    
    similar_paragraphs = find_similar(prompt_embedding, embeddings)[:5]
    
    context = " ".join(paragraphs[item[1]] for item in similar_paragraphs)
    
    return context
    