import os
from dotenv import load_dotenv
import google.generativeai as genai
import sys  # Import sys for better error handling

# Load environment variables from .env file
load_dotenv()

# Get the Gemini API key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found in .env file.", file=sys.stderr)
    sys.exit(1)  # Exit with an error code
else:
    try:
        # Configure the Generative AI library with your API key
        genai.configure(api_key=GEMINI_API_KEY)
        print("Configured Gemini API successfully. Attempting to list models...\n")

        found_gemini_pro = False
        gemini_pro_supported_methods = []

        # Iterate through all available models
        for model in genai.list_models():
            print(f"  Found Model: {model.name}")
            print(f"    Description: {model.description}")
            print(f"    Supported Methods: {model.supported_generation_methods}")
            print("-" * 30)

            if model.name == 'models/gemini-pro':
                found_gemini_pro = True
                gemini_pro_supported_methods = model.supported_generation_methods

        print("\n--- Model Listing Complete ---")

        if not found_gemini_pro:
            print(
                "\nCritical: 'models/gemini-pro' WAS NOT FOUND in the list of available models for your API key and project.")
            print("This is the root cause of your 404 error.")
            print("Possible reasons:")
            print(
                "1. Propagation delay: It might take some time for the model to become available after enabling APIs/billing.")
            print(
                "2. Regional restriction: Though unlikely for gemini-pro, check if you're in a specific region with limitations.")
            print("3. Project/Key association issue: The key might not be fully linked to a project that has access.")
            print(
                "\nRecommendation: Try waiting 10-15 minutes and rerunning this script. If it still doesn't appear, try creating a NEW Google Cloud Project, enable Generative Language API, link billing, and generate a NEW API key for that new project, then try again.")
        elif 'generateContent' not in gemini_pro_supported_methods:
            print(
                f"\nCritical: 'models/gemini-pro' was found, but 'generateContent' is NOT among its supported methods: {gemini_pro_supported_methods}.")
            print("This is also a potential root cause for your 404 error.")
            print(
                "Recommendation: Similar to above, try waiting, or check for specific permissions needed for `generateContent` with your key.")
        else:
            print("\nSuccess! 'models/gemini-pro' was found and supports 'generateContent'.")
            print(
                "Now you should be able to run `python test_gemini.py` with the 'Hello World' example (from previous step) successfully.")
            print(
                "If that still fails, check the model's actual availability in your region or try a different project/key.")

    except Exception as e:
        print(f"\nAn unexpected error occurred while listing models: {e}", file=sys.stderr)
        print("This indicates a more fundamental issue with API access or network.", file=sys.stderr)
        print("Please double-check your internet connection, API key, and ensure no firewalls are blocking access.",
              file=sys.stderr)
        sys.exit(1)