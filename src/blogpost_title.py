from title import using_open_ai_davinci

if __name__ == '__main__':
    with open("../resources/knowledge_management.md") as file:
        fulltext = file.readlines()

    fulltext = " ".join(fulltext)
    title_from_davinci = using_open_ai_davinci(fulltext)
    print(f"Title: {title_from_davinci}")
