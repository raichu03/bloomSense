import pdfplumber
import ollama
import json
import os
import numpy as np

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
    with open(f"embeddings/{file_name}.json", "w") as file:
        return json.load(file)


def get_embeddings(file_name, paragraphs):
    """Generates embeddings form the paragraphs and saves them"""
    
    if (embeddings := load_embeddings(file_name)) is not False:
        return embeddings
    
    embeddings = [
        ollama.embeddings(model='nomic-embed-text', prompt=paragraph)["embedding"]
        for paragraph in paragraphs
    ]
    save_embeddings(file_name, embeddings)
    return embeddings

