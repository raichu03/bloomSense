# bloomSense

This is a QA automation project for bloomSense. It is written in Python and uses a FastAPI backend. The system allows the user to interact with the llm that has the knowledge base of various flowers and user can have question answering session with the system.

## Installation
This project requires **python 3.8** or higher. It requires the installation of ollama.

You can install ollama using the following command in linux system:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```
or you can download for your preferred system from [ollama](https://ollama.com/download).

I am using llama3.2 for this project but you can your preferred model. To install llama3.2, you can use the following command:
```bash
ollama run llama3.2
```
You can download you r preferred model from [models](https://ollama.com/search).

Finally to install the project dependencies, you can use the following command from inside the project folder:
```bash
pip install -r requirements.txt
```

After installing the requirements run change the directory to the source folder and run:
```bash
uvicorn main:app
```
This will run the project on localhost you can click on the link to open the project in your browser.

