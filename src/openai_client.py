import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class OpenAIClient:

    def __init__(self, api_key=None, model="gpt-4.1", temperature=0.7):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.temperature = temperature
        
        if self.api_key is None:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=self.api_key)
    
    def send_prompt(self, prompt, system_message=None, model=None, temperature=None):
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
    
        # Use instance defaults if not provided
        model = model or self.model
        temperature = temperature or self.temperature
        
        try:
            response = self.client.responses.create(
                instructions=system_message,
                model=model,
                input=prompt,
                temperature=temperature
            )
            
            return response.output_text
        
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def summarize_text(self, text, max_length=50):
        system_message = f"""You are a friendly morning news presenter that summarizes news text for voice reading. 
        Keep summaries under {max_length} words and make them natural for text-to-speech.
        Remove any special characters that don't sound good when spoken."""
        
        prompt = f"""Please analyze the following news content and create a voice-friendly summary focusing on developer-relevant information:

        CONTENT: {text}

        REQUIREMENTS:
        - Focus on: APIs, programming languages, frameworks, developer tools, tech companies, software releases, security issues, and industry trends
        - Exclude: General business news, marketing content, and non-technical announcements  
        - Keep summary conversational and natural for text-to-speech
        - Use simple sentences and avoid complex punctuation
        - Include specific version numbers, dates, or key details when relevant
        - If no developer-relevant content is found, respond with "No developer news found in this content"

        Format as a brief, engaging summary suitable for a morning news briefing."""

        return self.send_prompt(prompt, system_message)
    