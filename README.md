# Medical Jargon Translator

A Streamlit-based healthcare application that uses an LLM API to translate medical and clinical terminology into simple, patient-friendly language.

## Project Goal

The goal of this project is to make clinical notes easier to understand while preserving the original medical information.

The application:

* Accepts a clinical note from the user
* Sends the note to an LLM
* Translates medical terminology into simpler language
* Preserves important clinical details and numerical values
* Preserves negations such as "denies chest pain"
* Supports Zero-Shot and Few-Shot prompting
* Provides adjustable temperature and maximum token settings
* Handles API errors and rate limits

> **Safety:** This tool explains medical terminology. It does not provide diagnosis, treatment, or medical advice.

## Technologies Used

* Python
* Streamlit
* Groq API
* `openai/gpt-oss-20b`
* python-dotenv
* Zero-Shot Prompting
* Few-Shot Prompting
* System Prompt Design

## Project Structure

```text
medical-jargon-translator/
│
├── app.py
├── requirements.txt
├── .gitignore
├── .env              # Local only — never upload
└── README.md
```

## ⚙️ Features

### Medical Note Input

Users can enter a clinical note into a text area.

### Prompting Methods

The application supports:

* **Zero-Shot Prompting** — translates the note without examples.
* **Few-Shot Prompting** — provides examples to guide the translation style.

### Adjustable LLM Settings

The sidebar allows the user to control:

* Prompting method
* Temperature
* Maximum tokens

### Safety-Focused Translation

The system prompt instructs the model to:

* Preserve the original meaning
* Explain medical terminology simply
* Preserve numerical values
* Preserve negations
* Avoid unsupported medical interpretations
* Avoid diagnosis
* Avoid treatment recommendations
* Avoid adding information not present in the clinical note

### Error Handling

The application handles:

* Missing API keys
* Authentication errors
* Rate limits
* Unavailable models
* General API errors

### Session State

Streamlit session state is used to retain:

* Last clinical note
* Last translation
* Last prompting method

### User Experience

The application includes:

* Loading spinner during API calls
* Clear button
* Empty-input validation
* Original clinical note display
* Patient-friendly translation display
* Safety information

## API Key Security

The Groq API key is stored in an environment file:

```text
GROQ_API_KEY=your_api_key_here
```

The `.env` file is excluded from Git using `.gitignore`.

**Never commit or publicly share your API key.**

## Installation

Clone the repository and create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```text
GROQ_API_KEY=your_api_key_here
```

Run the application:

```bash
streamlit run app.py
```

## Example

### Clinical Note

```text
Patient presents with dyspnea and tachycardia.
Blood pressure is 145/90 mmHg and HbA1c is 7.8%.
```

### Patient-Friendly Output

```text
The patient is experiencing difficulty breathing and a
faster-than-normal heart rate.

Their blood pressure reading is 145/90 mmHg.

Their HbA1c level is 7.8%.
```

The exact wording may vary because LLM output can change with prompting and temperature settings.

## Concepts Practiced

This project combines the major concepts learned during the LLM and Streamlit tasks:

1. Understanding LLMs and autoregressive text generation
2. Zero-Shot Prompting
3. Few-Shot Prompting
4. System Prompt Design
5. Secure LLM API calls
6. Environment variables and API-key security
7. API error and rate-limit handling
8. Streamlit widgets
9. Streamlit sidebar controls
10. Session state
11. Conditional UI updates
12. Loading states
13. Input validation

## Prompting Comparison

Zero-shot prompting provides instructions without examples.

Few-shot prompting provides examples of the desired translation style.

During testing, Few-Shot prompting produced more structured and consistent translations for the tested medical examples. However, this project does not claim that Few-Shot prompting is universally better.

## Safety Testing

The application was tested with:

* Medical terminology such as dyspnea and tachycardia
* Multiple medical conditions
* Negated symptoms
* Blood pressure values
* HbA1c values
* Heart-rate values
* Empty clinical-note input

Testing showed that the system was able to preserve important clinical information and negations while converting medical terminology into simpler language.

One observed limitation was that the model could sometimes add an interpretation such as describing a blood-pressure value as "higher than normal" when that interpretation was not explicitly included in the input.

The system prompt was strengthened to reduce this behavior.

## Limitations

This project is an educational prototype.

LLM-generated translations may still contain errors or unsupported interpretations. The application should not be used as a substitute for professional medical judgment.

No patient-identifying information should be entered into the application unless the system has been appropriately secured and approved for such use.

## Future Improvements

Possible future improvements include:

* Translation history
* Downloadable translation reports
* More medical terminology examples
* Additional prompt templates
* Automated evaluation of translation quality
* More comprehensive clinical safety testing
* Support for additional LLM providers

##  Learning Outcome

This project demonstrates how Python, Streamlit, prompt engineering, and an LLM API can be combined to build a practical healthcare-focused AI application.
