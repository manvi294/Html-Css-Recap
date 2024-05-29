import os
import spacy
from spacy.cli.download import download

def setup_proxy_and_download_model(proxy):
    # Set the proxy environment variables
    os.environ['http_proxy'] = proxy
    os.environ['https_proxy'] = proxy

    # Download the spaCy model
    download("en_core_web_sm")

# Replace 'http://your_proxy' with your actual proxy address
proxy_address = 'http://your_proxy'
setup_proxy_and_download_model(proxy_address)

# Load the model to check if it works
nlp = spacy.load("en_core_web_sm")
print("Model loaded successfully.")
