# backend/check_models.py

import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyAIom_ftRgc4UDla78mWeG8xBwSQvPEyvs"

try:
    genai.configure(api_key=GEMINI_API_KEY)

    print("--- Available Models ---")
    print("Models that support the 'generateContent' method:")
    
    count = 0
    for model in genai.list_models():

        if 'generateContent' in model.supported_generation_methods:
            print(f" - {model.name}")
            count += 1
            
    if count == 0:
        print("\nNo models supporting 'generateContent' found.")
        print("This might be an issue with your API key or region restrictions.")

except Exception as e:
    print(f"\nAn error occurred: {e}")
    print("Please double-check that your API key is correct and has been enabled for the Gemini API.")