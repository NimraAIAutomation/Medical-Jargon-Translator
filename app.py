import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
from groq import APIError, AuthenticationError, RateLimitError, NotFoundError

#Env Variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY was not found. Please check your .env file.")
    st.stop()

client = Groq(api_key=api_key)

#App configurations
st.set_page_config(
    page_title="Medical Jargon Translator",
    layout="wide"
)

if "last_note" not in st.session_state:
    st.session_state.last_note = ""

if "last_translation" not in st.session_state:
    st.session_state.last_translation = ""

if "last_prompting_method" not in st.session_state:
    st.session_state.last_prompting_method = "Zero-Shot"

st.title("Medical Jargon Translator")
st.write("Convert clinical notes into simple, patient-friendly language.")
st.info(
    "This tool explains medical terminology in simple language. "
    "It does not provide diagnosis, treatment, or medical advice."
)

st.sidebar.header("Settings")

prompting_method = st.sidebar.selectbox(
    "Prompting Method",
    ["Zero-Shot", "Few-Shot"]
)

temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.2,
    step=0.1
)

max_tokens = st.sidebar.number_input(
    "Maximum Tokens",
    min_value=50,
    max_value=1000,
    value=300,
    step=50
)

st.header("Clinical Note")

def clear_app():
    st.session_state["clinical_note"] = ""
    st.session_state["last_note"] = ""
    st.session_state["last_translation"] = ""
    st.session_state["last_prompting_method"] = "Zero-Shot"

clinical_note = st.text_area(
    "Enter the clinical note:",
    height=200,
    placeholder="Example: Patient presents with hypertension and elevated HbA1c.",
    key="clinical_note"
)

SYSTEM_PROMPT = """
You are a medical jargon translator.

Your task is to translate clinical notes into simple,
patient-friendly language while preserving the original meaning.

Rules:

1. Translate medical terminology into simple everyday language.
2. Preserve all facts, measurements, symptoms, conditions, and statements
   from the original note.
3. Preserve negation exactly. For example, "denies chest pain" must remain
   a statement that the patient does not have or report chest pain.
4. Do not add medical facts, assumptions, interpretations, or conclusions.
5. Do not judge whether a measurement is normal, abnormal, high, or low
   unless the original clinical note explicitly states this.
6. Do not diagnose the patient.
7. Do not recommend medications, treatments, or medical actions.
8. Do not add advice such as "see your doctor", "keep monitoring",
   or "get regular check-ups" unless it is explicitly present in the note.
9. Preserve numerical values accurately.
10. Explain abbreviations and medical terms when helpful.
11. Use clear, neutral, patient-friendly language.
12. Prefer "the patient" rather than directly addressing the reader as "you".
13. Do not remove clinically relevant information.
14. Return only the patient-friendly translation.
"""

def create_zero_shot_prompt(clinical_note):
    return f"""
Translate the following clinical note into simple,
patient-friendly language.

Clinical note:
{clinical_note}
"""

def create_few_shot_prompt(clinical_note):
    return f"""
Translate the clinical note into simple,
patient-friendly language.

Follow the style shown in these examples.

Example 1:

Clinical note:
"Patient has hypertension and elevated blood glucose."

Patient-friendly explanation:
"The patient has high blood pressure and a higher-than-normal blood sugar level."


Example 2:

Clinical note:
"Patient reports dyspnea and tachycardia."

Patient-friendly explanation:
"The patient reports difficulty breathing and a faster-than-normal heart rate."


Example 3:

Clinical note:
"Patient has an elevated HbA1c level."

Patient-friendly explanation:
"The patient's HbA1c level is higher than normal. HbA1c is a blood test that shows average blood sugar levels over the past few months."


Now translate the following clinical note using the same style.

Clinical note:
{clinical_note}
"""

#Sending request to the LLM
def get_llm_response(system_prompt, user_prompt, temperature, max_tokens):

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content

    except AuthenticationError:
        st.error(
            "Authentication failed. Please check your Groq API key."
        )
        return None

    except RateLimitError:
        st.warning(
            "Groq API rate limit reached. Please wait and try again later."
        )
        return None

    except NotFoundError:
        st.error(
            "The selected Groq model was not found or is unavailable."
        )
        return None

    except APIError as e:
        st.error(
            f"Groq API error: {e}"
        )
        return None

    except Exception as e:
        st.error(
            f"Unexpected error: {e}"
        )
        return None
    
translate_button = st.button("Translate")

if translate_button:

    if clinical_note.strip() == "":
        st.warning("Please enter a clinical note.")

    else:
        if prompting_method == "Zero-Shot":
            prompt = create_zero_shot_prompt(clinical_note)

        else:
            prompt = create_few_shot_prompt(clinical_note)
        
        with st.expander("View Generated Prompt"):
            st.code(prompt)

        with st.spinner("Translating clinical note..."):
            translation = get_llm_response(
                SYSTEM_PROMPT,
                prompt,
                temperature,
                max_tokens
            )

        if translation:
            st.session_state.last_note = clinical_note
            st.session_state.last_translation = translation
            st.session_state.last_prompting_method = prompting_method
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Original Clinical Note")
                st.info(clinical_note)

            with col2:
                st.subheader("Patient-Friendly Explanation")
                st.success(translation)
clear_button = st.button(
    " Clear All ",
    on_click=clear_app
)





