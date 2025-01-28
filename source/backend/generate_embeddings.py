from bs4 import BeautifulSoup
import requests
import re

from embeddings import get_embeddings

def get_links():
    with open('links.txt', 'r') as file:
        data = file.readlines()
    data = [line.strip() for line in data]
    return data

def check_links(links):
    with open('saved_embd.txt', 'r') as file:
        saved_links = file.readlines()
    saved_links = [line.strip() for line in saved_links]
    
    if links not in saved_links:
        return True
    else:
        return False

def get_paragraphs(url: str):
    print(f"Getting paragraphs from {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Remove unwanted tags like <a> (links), <script> (JavaScript), <style> (CSS)
    for unwanted_tag in soup(['a', 'script', 'style', 'footer', 'header']):
        unwanted_tag.decompose()
    
    # Extract paragraphs
    paragraphs = soup.find_all('p')
    
    # Get clean text from each paragraph
    cleaned_paragraphs = []
    for p in paragraphs:
        text = p.get_text()
        cleaned_text = re.sub(r'\s+', ' ', text)
        cleaned_text = re.sub(r'[^\w\s,.!?]', '', cleaned_text)
        cleaned_paragraphs.append(cleaned_text.strip())
    
    return cleaned_paragraphs

def main():

    links = get_links()
    paragraphs = []
    
    for link in links:
        check = check_links(link)
        if check:
            paragraphs.extend(get_paragraphs(link))
        else:
            print(f"Skipping {link}")
            continue
    
    if len(paragraphs) > 0:
        get_embeddings(paragraphs)
        print("Embeddings and Paragraphs generated successfully")


if __name__ == "__main__":
    main()