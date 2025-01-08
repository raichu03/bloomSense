import pdfplumber
import ollama
import json
import os
import numpy as np
from numpy.linalg import norm


def extract_pdf(file_path):
    
    with pdfplumber.open(file_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    
    paragraphs = text.split('.\n')
    paragraphs = [p.replace('\n',' ').strip() for p in paragraphs if p.strip()]
    
    return paragraphs


def save_embeddings(file_name, embeddings):
    """Stores embeddings in the local json database"""
    
    if not os.path.exists("embeddings"):
        os.makedirs("embeddings")
    
    with open(f"embeddings/{file_name}.json", "w") as file:
        json.dump(embeddings, file)


def load_embeddings(file_name):
    """Checks whether embeddings are present or not and returns the embeddings"""
    
    if not os.path.exists(f"embeddings/{file_name}.json"):
        return False
    
    with open(f"embeddings/{file_name}.json", "r") as file:
        return json.load(file)


def get_embeddings(file_name, paragraphs):
    """Generates embeddings form the paragraphs and saves them"""
    
    # if (embeddings := load_embeddings(file_name)) is not False:
    #     return embeddings
    
    embeddings = [
        ollama.embeddings(model='nomic-embed-text', prompt=paragraph)["embedding"]
        for paragraph in paragraphs
    ]
    save_embeddings(file_name, embeddings)
    return embeddings

def find_similar(prompt, embedding):
    needle_norm = norm(prompt)
    similarity_scores = [
        np.dot(prompt, item) / (needle_norm * norm(item)) for item in embedding
    ]
    return sorted(zip(similarity_scores, range(len(embedding))), reverse=True)

def get_paragraphs():
    with open('backend/embeddings/paragraphs.json', 'r') as json_file:
        paragraph = json.load(json_file)
    return paragraph

def get_embedding():
    with open('backend/embeddings/embedding.json', 'r') as json_file:
        embedding = json.load(json_file)
    return embedding

def generate_context(prompt: str):
    prompt_embedding = ollama.embeddings(model="nomic-embed-text", prompt=prompt)["embedding"]
    
    paragraphs = get_paragraphs()
    embeddings = get_embedding()
    
    similar_paragraphs = find_similar(prompt_embedding, embeddings)[:5]
    
    context = " ".join(paragraphs[item[1]] for item in similar_paragraphs)
    
    return context
    