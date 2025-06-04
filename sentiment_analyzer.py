import requests
import os
import re
import configparser
from datetime import datetime
from dotenv import load_dotenv
import nltk
from nltk.corpus import words

# Download NLTK words dataset (run once)
nltk.download('words', quiet=True)
ENGLISH_WORDS = set(words.words())

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# API configuration
API_URL = config['API']['url']
API_KEY_ENV = config['API']['key_env_variable']
OUTPUT_DIR = config['Output']['directory']
MIN_WORDS = int(config['InputValidation']['min_words'])
MAX_WORDS = int(config['InputValidation']['max_words'])

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv(API_KEY_ENV)
if not API_KEY:
    raise ValueError(f"Hugging Face API key not found. Set {API_KEY_ENV} in .env file.")

def validate_input(text):
    """Validate and clean user input."""
    text = re.sub(r'\s+', ' ', text.strip())  # Collapse multiple spaces
    text = re.sub(r'[.!?]+', '.', text)  # Normalize punctuation to single periods
    if not text:
        raise ValueError("Input cannot be empty.")
    
    words = text.split()
    if len(words) < MIN_WORDS:
        raise ValueError(f"Input too short. Please provide at least {MIN_WORDS} words.")
    if len(words) > MAX_WORDS:
        raise ValueError(f"Input too long. Please limit to {MAX_WORDS} words.")
    
    # Check for meaningful words
    meaningful_words = [word.lower() for word in words if word.lower() in ENGLISH_WORDS]
    meaningful_ratio = len(meaningful_words) / len(words) if words else 0
    if meaningful_ratio < 0.6:  # Increased from 0.5 to 0.8
        raise ValueError("Input contains too many unrecognized words. Please provide meaningful text.")
    
    # Check for repetitive or gibberish words
    for word in words:
        if len(word) > 10 and len(set(word.lower())) < 4:
            raise ValueError(f"Input contains repetitive gibberish: '{word}'.")
        if len(word) > 15 and not word.lower() in ENGLISH_WORDS:
            raise ValueError(f"Input contains likely gibberish: '{word}'.")
    
    return text

def get_user_input():
    """Get text input from user via console."""
    print("Enter your restaurant comment (press Enter twice to finish):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    
    text = " ".join(lines)
    return validate_input(text)

def call_huggingface_api(text):
    """Send text to Hugging Face API and return result with rate limit info."""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {"inputs": text}
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        remaining = response.headers.get("X-RateLimit-Remaining", "Unknown")
        return result, remaining
    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:
            raise Exception("API rate limit reached. Please try again later.")
        raise Exception(f"API request failed: {str(e)}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error: {str(e)}")

def process_response(response):
    """Parse API response for sentiment analysis."""
    if isinstance(response, list) and len(response) > 0 and isinstance(response[0], list):
        predictions = response[0]
        if not predictions:
            raise ValueError("Empty predictions in API response.")
        best_prediction = max(predictions, key=lambda x: x.get("score", 0))
        label = best_prediction.get("label")
        score = best_prediction.get("score")
        if label and score:
            return f"Sentiment: {label}, Confidence: {score:.2%}"
    elif isinstance(response, dict):
        if "error" in response:
            raise ValueError(f"API error: {response['error']}")
        raise ValueError(f"Unexpected response format: {response}")
    raise ValueError(f"Unexpected API response format: {response}")

def save_results(text, result):
    """Save input and result to a text file in results directory."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(OUTPUT_DIR, f"results_{timestamp}.txt")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Task: Sentiment Analysis\n")
        f.write(f"Input Text:\n{text}\n\n")
        f.write(f"Result:\n{result}\n")
    
    return filename

def main():
    """Main function to run the sentiment analysis tool."""
    try:
        text = get_user_input()
        response, remaining_calls = call_huggingface_api(text)
        result = process_response(response)
        print("\nResult:")
        print(result)
        print(f"API calls remaining: {remaining_calls}")
        
        save_choice = input("\nSave result to file? (y/n): ").strip().lower()
        if save_choice == "y":
            filename = save_results(text, result)
            print(f"Results saved to {filename}")
        
    except ValueError as e:
        print(f"Input error: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()