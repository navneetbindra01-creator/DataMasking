# presidio_masker.py
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from faker import Faker
from datetime import datetime

# Initialize engines and Faker once (efficient)
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()
fake = Faker()

# Entities to detect and mask
ENTITIES_TO_MASK = [
    "PERSON",          # Accurate person names (context-aware!)
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "DATE_TIME",       # Covers DOBs and other dates
    "LOCATION",        # Addresses, cities, etc. (disable if too aggressive)
    # Add more if needed: "CREDIT_CARD", "IBAN_CODE", "US_SSN", etc.
    # Full list: https://microsoft.github.io/presidio/supported_entities/
]

# Custom realistic replacements
operators = {
    "PERSON": OperatorConfig("custom", {"lambda": lambda _: fake.name()}),
    "EMAIL_ADDRESS": OperatorConfig("custom", {"lambda": lambda _: fake.safe_email()}),
    "PHONE_NUMBER": OperatorConfig("custom", {"lambda": lambda _: fake.phone_number()}),
    # For dates, simple redaction (or customize further if needed)
    "DATE_TIME": OperatorConfig("replace", {"new_value": "<DATE>"}),
    # Fallback for any other detected entity
    "DEFAULT": OperatorConfig("replace", {"new_value": "<REDACTED>"}),
}

def mask_text_presidio(text: str, log, location: str):
    if not text.strip():
        return text + '\n'  # Preserve empty lines

    # Detect PII
    analyzer_results = analyzer.analyze(
        text=text,
        entities=ENTITIES_TO_MASK,
        language="en",
        score_threshold=0.35,  # Adjust: lower = more detections, higher = stricter
    )

    if not analyzer_results:
        return text + '\n'

    # Anonymize
    anonymized_result = anonymizer.anonymize(
        text=text,
        analyzer_results=analyzer_results,
        operators=operators
    )

    # Log each detection
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for result in analyzer_results:
        orig = text[result.start:result.end]
        # Extract the replaced text from the final anonymized output
        # (positions shift due to replacements of varying lengths)
        # Simple but effective: find the segment around the original position
        approx_start = result.start
        approx_end = result.end + (len(anonymized_result.text) - len(text))
        new = anonymized_result.text[max(0, approx_start-10):approx_end+10]  # context snippet
        # Better: just show the full anonymized line later if needed, but log original span
        log.write(
            f"{timestamp} | Location: {location} | "
            f"Type: {result.entity_type} | Score: {result.score:.3f} | "
            f"Original span: \"{orig}\" | "
            f"Replaced with: (see anonymized text)\n"
        )

    return anonymized_result.text + '\n'