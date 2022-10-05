import os

import openai
from dotenv import load_dotenv

load_dotenv()


def create_title(text: str) -> str:
    # Create title with DaVinci2 Model on OpenAI

    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=f"Fasse folgenden Text in einem kurzen deutschen Titel zusammen.\n\n{text}",
        temperature=0.3,
        max_tokens=64,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=0
    )

    return response.choices[0]["text"].replace("\n", "")


def determine_title_from_text(filename: str):
    # read file and make text out of it
    with open(f"../resources/{filename}") as file:
        fulltext = file.readlines()

    fulltext = " ".join(fulltext)
    if len(fulltext) > 10000:  # current limitation of the OpenAI prompt, rather arbitrary
        return

    # create title
    title_from_davinci: str = create_title(fulltext)
    print(f"Title for '{filename}': {title_from_davinci}")


if __name__ == '__main__':
    list(map(determine_title_from_text, os.listdir("../resources")))  # list() is needed to execute the map
