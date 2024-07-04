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
[A demo of Personal-LLM's features can be found here.](https://vimeo.com/977036847)

## Technical System Design
[A video of the technical system design of Personal-LLM can be found here.](https://vimeo.com/977028159)

This project's goal is twofold:

1. To enable anyone to be able to use LLMs to benefit their own day-to-day life and
2. To foster growth in the [Kekoexchange](https://kekoexchange.com) community through contribution to this project. Kekoexchange brings people looking to break into tech with software engineers looking for leadership opportunities together to contribute to open-source software so that we all can achieve our career growth, learn from each other, and give back to the public technical landscape that is open-source.

## Setup Instructions
1. Please download and install the following dependencies
  * [Python 3.11](https://www.python.org/downloads/release/python-3117/) 
  * [Google Chrome](https://www.google.com/chrome/)
  * [Ollama](https://ollama.com/)
    * Ollama is a LLM model backend that lets you download and access LLMs locally and use it in your applications. NOTE: Ensure Ollama is running before doing the below
2. Clone this repository
3. Run `npm run build` to build the project
    * As of this writing, we are using the [llama3 LLM](https://llama.meta.com/llama3/) from Meta, which is about 4.7 GB. The first run of this will take some time as Ollama downloads the llama3 LLM.
4. Run `npm run start` to run the project
