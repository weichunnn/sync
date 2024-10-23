from anthropic import Anthropic
import logging
from dotenv import load_dotenv
load_dotenv()


class LLMClient:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        
    def generate(self, prompt: str) -> str:
        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                temperature=0.7,
                system="You are a research expert tasked with generating innovative research ideas. Focus on practical, impactful suggestions that build upon existing research while considering business context and feasibility.",
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            # Extract the string content from the message
            if hasattr(message.content[0], 'text'):
                return message.content[0].text
            return str(message.content)
        except Exception as e:
            logging.error(f"LLM generation error: {e}")
            return None