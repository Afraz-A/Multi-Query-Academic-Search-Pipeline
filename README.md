# Multi-Query-Academic-Search-Pipeline

This Python script utilizes the Gemini API to execute parallel query reformulations (Synonyms, HyDE, Specific, Broad) for academic paper searching.

## Installation

```bash
pip install google-genai python-dotenv
```

## Configuration

1. Create a file named .env in the same directory as your Python script.
2. Add your Gemini API key to the .env file exactly like this:

```bash
GEMINI_API_KEY=your_api_key_here
```

## Run Program

```bash
python eval.py
```
