# Original code from https://github.com/technovangelist/videoprojects/blob/main/2024-04-04-build-rag-with-python/import.py

import ollama
import chromadb
import time
from mattsollamatools import chunk_text_by_sentences
import sys
import logging

logger = logging.getLogger(__name__)

def main():
    collectionname = "buildragwithpython"

    chroma = chromadb.HttpClient(host="localhost", port=8100)
    logging.info(chroma.list_collections())
    if any(collection.name == collectionname for collection in chroma.list_collections()):
        logging.info('deleting collection')
        chroma.delete_collection("buildragwithpython")
    collection = chroma.get_or_create_collection(name="buildragwithpython", metadata={"hnsw:space": "cosine"})

    embedmodel = "nomic-embed-text"
    starttime = time.time()

    for filename in sys.argv[1:]:
        with open(filename, 'rb') as f:
            text = f.read().decode('utf-8')
            chunks = chunk_text_by_sentences(source_text=text, sentences_per_chunk=7, overlap=0)
            logging.info(f"with {len(chunks)} chunks")
            for index, chunk in enumerate(chunks):
                embed = ollama.embeddings(model=embedmodel, prompt=chunk)['embedding']
                collection.add([filename + str(index)], [embed], documents=[chunk], metadatas={"source": filename})

    logging.info("--- %s seconds ---" % (time.time() - starttime))


if __name__ == "__main__":
    main()