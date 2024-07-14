# Personal LLM - a desktop ChatGPT clone that runs 100% local off of the cloud

## Author
[Kay Ashaolu](https://www.linkedin.com/in/kayashaolu/)

## Description
Unlock the power of Language Models in your own hands! Personal LLM is a revolutionary desktop application that brings the capabilities of Large Language Models (LLMs) to your very own computer. With Personal LLM, you can now harness the intelligence and creativity of AI-powered language processing, without relying on internet connectivity or costly subscriptions. Simply download, install, and start leveraging the limitless potential of LLMs for free, right from your desktop

## Technologies Used
- HTML
- CSS
- JavaScript
- Python
- Ollama
- LLM
- ORM [Peewee](https://docs.peewee-orm.com/en/latest/)
- RDBMS [Sqlite3](https://sqlite.org/)
- [Python-Eel](https://github.com/python-eel/Eel)

## Demo
[![Personal-LLM Demo Video](http://img.youtube.com/vi/BwRgVGhxm70/0.jpg)](http://www.youtube.com/watch?v=BwRgVGhxm70 "Personal-LLM Demo Video")

## Technical System Design
[![Personal-LLM System Design Video](http://img.youtube.com/vi/MgdypIh9wrA/0.jpg)](http://www.youtube.com/watch?v=MgdypIh9wrA "Personal-LLM System Design Video")

## Setup Instructions
1. Please download and install the following dependencies
  * [Python 3.11](https://www.python.org/downloads/release/python-3117/) 
  * [Google Chrome](https://www.google.com/chrome/)
  * [Ollama](https://ollama.com/)
    * Ollama is a LLM model backend that lets you download and access LLMs locally and use it in your applications. NOTE: Ensure Ollama is running before doing the below
2. Clone this repository
3. Run `npm run start ` to r the project
    * As of this writing, we are using the [llama3 LLM](https://llama.meta.com/llama3/) from Meta, which is about 4.7 GB. The first run of this will take some time as Ollama downloads the llama3 LLM.
