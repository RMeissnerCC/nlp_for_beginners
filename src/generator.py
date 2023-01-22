import datetime
import os

import nlpcloud
import nltk
import openai
import requests
import spacy as spacy
from dotenv import load_dotenv
from keybert import KeyBERT
from nltk.corpus import stopwords

nltk.download("stopwords")
STOPWORDS = set(stopwords.words("german")).union(set(stopwords.words("english")))

load_dotenv()

resource_directory = "../resources/"

openai.api_key = os.getenv("OPENAI_API_KEY")
api_key = os.getenv("NLPCLOUD_API_KEY")


def create_title(text: str) -> str:
    # Create title with DaVinci2 Model on OpenAI
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=f"Fasse folgenden Text in einem kurzen deutschen Titel zusammen.\n\n{text}",
        temperature=0.3,
        max_tokens=64,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=0,
    )

    return response.choices[0]["text"].replace("\n", "")


def create_keywords_mit_davinci(text: str) -> list[str]:
    # Create keywords with DaVinci2 Model on OpenAI

    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=f"Gib eine Liste der fünf wichtigsten Schlagwörtern zurück.\n\n{text}",
        temperature=0.3,
        max_tokens=64,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=0,
    )

    return response.choices[0]["text"].replace("\n", "").replace("-", " ")


def create_keywords(fulltext: str) -> list[str]:
    nlp = spacy.load("de_dep_news_trf")

    keyword_model = KeyBERT(model=nlp)
    keywords = keyword_model.extract_keywords(
        fulltext,
        highlight=False,
        keyphrase_ngram_range=(1, 1),
        stop_words=list(STOPWORDS),
    )

    return [
        keyword for keyword, weight in keywords
    ]  # Remove the weights and only return keywords


def create_preview(filename: str, title: str):
    client = nlpcloud.Client("stable-diffusion", api_key, gpu=True, lang="de")

    # If this yields 429 - wait a while
    response = client.image_generation(f"Erstelle ein Bild aus diesem Titel: {title}")

    # Download image
    response = requests.get(response["url"])

    file_name = f"{filename}_preview_{datetime.datetime.now().timestamp()}.png"
    # Save the image
    if response.status_code == 200:
        with open(file_name, "wb") as f:
            f.write(response.content)
        print(f"Preview created for '{filename}'.")


def determine_title_from_text(filename: str):
    # read text from file and process it
    with open(f"{resource_directory}{filename}") as file:
        fulltext = file.readlines()

    fulltext = " ".join(fulltext)
    if (
        len(fulltext) > 10500
    ):  # current limitation of the OpenAI prompt, rather arbitrary
        return

    # create title
    title_from_davinci: str = create_title(fulltext)
    print(f"Title for '{filename}': {title_from_davinci}")

    # create keywords
    keywords = create_keywords(fulltext)
    print(f"KeyBERT Keywords for '{filename}': {' '.join(keywords)}")

    keywords = create_keywords_mit_davinci(fulltext)
    print(f"Davinci2 Keywords for '{filename}': {keywords}")

    # create preview
    create_preview(filename, title_from_davinci)


if __name__ == "__main__":
    # cycle through all files in the resource's folder - for these I want to generate data automatically
    list(
        map(determine_title_from_text, os.listdir(resource_directory))
    )  # list() is needed to execute the map
