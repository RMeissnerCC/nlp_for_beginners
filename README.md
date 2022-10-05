# Einleitung

Ein kleines Tool um automatisch aus Volltext einen Titel, Schlagwörter und Cover-Art zu generieren.

## Vorbereitung

Zur Benutzung werden ein Gratis-Account bei [OpenAI](https://beta.openai.com/) und [NLPCloud](https://nlpcloud.com/home/playground/image-generation) benötigt. 
Die dort generierten API Keys werden entsprechend dem `.env.example` in `.env` hinterlegt.

Die benötigten Python packages werden mit dem Tool `poetry` und dem Befehl `poetry install` installiert.

Für die deutschen Texte benutze ich ein deutsches Modell, dieses muss explizit heruntergeladen werden:

`python -m spacy download de_dep_news_trf`

## Benutzung

In `resources` eine Textdatei (e.g. .md) mit dem Volltext darin ablegen. Die Datei soll sonst nichts enthalten.

Das Skript `src/blogpost_title.py` ausführen.

