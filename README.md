**Why hesitate when uploading your data to an LLM such as chatGPT or Grok ? If you have data that might contain sensitive data, why not sanitise the data before loading it to an LLM ? **


Data Masking Tool (using Microsoft Presidio)
A simple, powerful Python tool to automatically detect and anonymize sensitive personal information (PII) in text-based files. Perfect for de-identifying patient notes, emails, logs, reports, or any natural-language text while preserving readability.
Why this tool?

Accurately masks real people’s names (e.g., "Dr. Sarah Johnson") without touching places, organizations, or titles like "White House" or "Main Street".
Handles emails, phone numbers, dates, addresses, and more with context awareness.
Replaces data with realistic fake values (e.g., John Doe → Maria Garcia, john@example.com → a.smith@example.org).
Works on plain text, CSV, JSON, and HL7 files.
Detailed log file shows exactly what was changed and why.
No complex configuration — just run it!

Features

Powered by Microsoft Presidio (industry-standard PII detection)
Context-aware name recognition (no more over-masking natural language)
Realistic fake replacements using Faker
Supports multiple file types
Easy command-line interface
Detailed, human-readable log with timestamps, locations, entity types, and confidence scores
Runs locally — your data never leaves your machine

Requirements

Python 3.8 or higher
A virtual environment is recommended (you already have .venv)

Quick Setup (one-time only)
Open a terminal in your project folder and run:
Bashpip install presidio-analyzer presidio-anonymizer faker
python -m spacy download en_core_web_lg
That’s it! No other dependencies.

Project Structure
**textDataMasking/**
**├── main.py                  ← Run this file
├── handlers.py              ← Handles different file types
├── presidio_masker.py       ← Core masking logic
├── Files/                   ← Put your input files here
│   └── tkls3886.txt
├── mask_log.txt             ← Created automatically (what was changed)
└── masked_tkls3886.txt      ← Your clean output file**
How to Use

Place your file inside the Files folder (e.g., tkls3886.txt).
Open a terminal in the project folder.
Run one of these commands:

For plain text files (most common)
_Bashpython main.py text tkls3886.txt masked_tkls3886.txt_
For CSV files
_Bashpython main.py csv data.csv masked_data.csv_
For JSON files
Bashpython main.py json input.json masked_output.json
For HL7 messages
_Bashpython main.py hl7 messages.hl7 masked_messages.hl7_

You're all set!
Just drop a file in the Files folder and run the command. Your original file stays untouched, and you get a clean masked version plus a full audit log.
Questions? Reply here and I’ll help instantly.
Enjoy safe, easy data masking!
