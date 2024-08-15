from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_google_genai import GoogleGenerativeAI
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set your Google API key from environment variable
api_key = os.getenv('GOOGLE_API_KEY')

# Initialize the LLM with LangChain and Google Generative AI
llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=api_key, temperature=0.35)

@app.route('/extract-recipe', methods=['POST'])
def extract_recipe():
    data = request.json
    html_content = data['html']

    # Generate prompts and get responses from the LLM
    ingredients_prompt = f"I want to extract the list of ingredients. Give me just the list from the following HTML content:\n\n{html_content}"
    instructions_prompt = f"I want to extract the list of instructions or simple steps for making the recipe in order. Give me just the list from the following HTML content:\n\n{html_content}"

    # Fetch ingredients and instructions using the LLM
    ingredients = llm(ingredients_prompt).text.strip()
    instructions = llm(instructions_prompt).text.strip()

    return jsonify({
        'ingredients': ingredients,
        'instructions': instructions
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
