# Einleitung

Ein kleines Tool um automatisch aus Volltext einen Titel, Schlagwörter und Vorschaubild zu generieren.

## Vorbereitung

Zur Benutzung werden ein Gratis-Account bei [OpenAI](https://beta.openai.com/) und 
[NLPCloud](https://nlpcloud.com/home/playground/image-generation) benötigt. 
Die dort generierten API Keys werden entsprechend dem `.env.example` in `.env` hinterlegt.

Die benötigten Python packages werden mit dem Tool `poetry` und dem Befehl `poetry install` installiert.

Für die deutschen Texte benutze ich ein deutsches Modell, dieses muss explizit heruntergeladen werden:

`poetry run python -m spacy download de_dep_news_trf`

## Benutzung

In `resources` eine Textdatei (e.g. .md) mit dem Volltext darin ablegen. Die Datei darf sonst nichts enthalten.

Das Skript `src/generator.py` ausführen. Das Skript durchsucht den Ordner `resources` und generiert für alle Dateien
eine entsprechende Ausgabe.
