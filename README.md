# Sentiment Analysis Tool

This repository contains a Python script for performing sentiment analysis using the Hugging Face API. The tool validates user input, sends it to the API, and processes the response to determine the sentiment of the input text.

## Features

- Validates user input for meaningful text.
- Sends text to the Hugging Face API for sentiment analysis.
- Displays the sentiment and confidence score.
- Optionally saves the results to a file.

## Requirements

- Python 3.8 or higher
- Hugging Face API key

## Quickstart

Follow these steps to set up and run the script:

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/llm-text-analysis.git
cd llm-text-analysis
```

### 2. Install Dependencies

Install the required Python libraries using `pip`:

```bash
pip install -r requirements.txt
```

### 3. Configure the Environment

1. **Set up the API key**:  
   Create a `.env` file in the root directory (if not already present) and add your Hugging Face API key, if you don't have the api key, please log onto Hugging Face and generate one here ([link](https://huggingface.co/settings/tokens/new?tokenType=read)):

   ```plaintext
   HF_API_KEY=your_huggingface_api_key
   ```

2. **Update the configuration**:  
   Modify the `config.ini` file to adjust API settings, input validation limits, or output directory if needed.

### 4. Run the Script

Run the script using Python:

```bash
python sentiment_analyzer.py
```

### 5. Provide Input

Enter your text input when prompted. The script will validate the input, send it to the Hugging Face API, and display the sentiment analysis result.

### 6. Save Results (Optional)

You can choose to save the results to a file in the `results` directory.

## Notes

- Ensure you have an active internet connection to access the Hugging Face API.
- The script automatically downloads the NLTK `words` dataset if not already available.
- API rate limits may apply. Check your Hugging Face account for details.

## Troubleshooting

- **Missing API Key**: Ensure the `.env` file contains a valid Hugging Face API key.
- **Input Validation Errors**: Follow the input guidelines (minimum and maximum word limits, meaningful text).
- **Network Issues**: Check your internet connection and API endpoint URL in `config.ini`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.