import os

import openai
import trafilatura
from dotenv import load_dotenv

from datasets import load_dataset
ds = load_dataset("flax-community/german_common_crawl", "first")

load_dotenv()


def using_open_ai_davinci():
    openai.api_key = os.getenv("OPENAI_API_KEY")

    test_url = ds["train"][0]["url"]
    print(test_url)
    downloaded = trafilatura.fetch_url(test_url)
    fulltext = trafilatura.extract(downloaded, url=test_url, favor_precision=True)

    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=f"Fasse folgenden Text in einem kurzen deutschen Titel zusammen.\n\n{fulltext}",
        temperature=0.3,
        max_tokens=64,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=0
    )

    return response.choices[0]["text"]


if __name__ == '__main__':
    title_from_davinci = using_open_ai_davinci()
    print(f"Title: {title_from_davinci}")
