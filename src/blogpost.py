import json
import os

import openai
import requests
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
api_key = os.getenv("OPENAI_API_KEY")


def generate_images(summary, image_path):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    data = {"prompt": summary, "n": 4}

    response = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers=headers,
        data=json.dumps(data),
    )

    if response.status_code != 200:
        raise ValueError(f"Error generating image: {response.json()}")
    for i, image in enumerate(response.json()["data"]):
        with open(os.path.join(image_path, f"image{i}.png"), "wb") as f:
            f.write(requests.get(image["url"]).content)
    print(f"{i + 1} images generated and stored in {image_path}")


# Function to send request to GPT-3 API
def generate_text(prompt, max_tokens):
    response = requests.post(
        "https://api.openai.com/v1/engines/davinci-codex/completions",
        json={
            "prompt": prompt,
            "max_tokens": max_tokens,
            "stop": "",
            "temperature": 0.5,
        },
        headers={"Authorization": f"Bearer {api_key}"},
    )
    if response.status_code != 200:
        raise ValueError(f"Error generating text: {response.json()}")
    return response.json()


def generate_from_markdown(filepath: str, substring: str) -> str:
    try:
        # Load markdown file from Obsidian
        with open(filepath, "r") as file:
            md_text = file.read()
        # Extract text below specific headline
        headline = substring
        start_index = md_text.index(headline) + len(headline)
        text_to_use = md_text[start_index:].strip()
        print("Sending to GPT-3")

        prompt = f"Write a promotional twitter thread based on the content below. \n{text_to_use}"
        twitter = generate_text(prompt, 200)
        twitter = twitter["choices"][0]["text"]
        print("twitter post:\n", twitter)
        prompt = f"Create an informative LinkedIn post based on the content below. \n{text_to_use}"
        linkedIn = generate_text(prompt, 1000)
        linkedIn = linkedIn["choices"][0]["text"]
        print("linkedIn post:\n", linkedIn)
        # Send text to GPT-3 to generate summary
        summary_response = generate_text(text_to_use, 256)
        summary = summary_response["choices"][0]["text"]
        print("Summary:\n", summary)
        return summary
        prompt = f"Write an educational blog post based on the content below. \n{text_to_use}"
        blog_post_response = generate_text(prompt, 5000)
        blog_post = blog_post_response["choices"][0]["text"]
        print("Blog post:\n", blog_post)
        return summary

    except FileNotFoundError:
        print("The specified markdown file could not be found.")


if __name__ == "__main__":
    summary = generate_from_markdown("resources/pymc.md", "# PyMC")
    generate_images(summary, "data")
