import os
import uuid
import json
from typing import List, Dict, Any
from openai import AsyncOpenAI

class PromptOptimizer:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.categories = ["awareness", "leads", "sales", "retention", "social"]
        self.model = "gpt-4"

    async def _get_completion(self, messages: List[Dict[str, str]]) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.5,  # Maintain a balanced output
                max_tokens=250  # Allow more tokens for detail
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error getting completion: {e}")
            raise

    async def analyze_prompt(self, user_prompt: str) -> Dict[str, str]:
        """
        Generate detailed ad prompt templates for each category with placeholders.
        """
        try:
            system_message = """
            You are an expert ad copywriter. For each category (awareness, leads, sales, retention, social), 
            generate a detailed yet concise ad template. Each template should be one to two sentences, 
            include placeholders for customization, and cover key elements such as:
            - A compelling call to action
            - A description of the target audience
            - Key features of the product or service
            For example:
            - Awareness: "Discover [brand name], the new trend in [industry]. Join [target audience] in embracing [key features]!"
            - Leads: "Looking for [solution]? Connect with [brand name] for personalized offers tailored for [target audience]."
            Ensure the templates are actionable and specific.
            """

            category_prompts = {}
            for category in self.categories:
                user_message = f"Create a template for '{category}' based on this prompt:\n\n{user_prompt}"
                
                messages = [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ]
                
                # Get a detailed completion
                response_text = await self._get_completion(messages)
                
                # Process the output as simple text
                category_prompts[category] = response_text.strip()

            return category_prompts

        except Exception as e:
            print(f"Error generating optimized prompts: {e}")
            return {"error": f"Unable to generate optimized prompts at this time: {str(e)}"}

async def split_prompt(optimized_prompts: Dict[str, str]) -> Dict[str, Any]:
    """
    Split each optimized marketing prompt into specific prompts for image, video, and ad copy generation for each category.
    """
    system_message = """
    You are an expert AI creative director specializing in multi-format advertising campaigns.
    Given a marketing prompt, create three specialized prompts in JSON format:
    
    1. image_prompt: A detailed DALL-E prompt describing the visual composition, style, mood, 
       lighting, and key elements to be included. Focus on creating a high-impact marketing image.
       
    2. video_prompt: A Luma AI-optimized prompt describing the video sequence, transitions, 
       motion elements, and timing. Include specific directions for a 15-30 second ad spot.
       
    3. adcopy_prompt: Marketing copy split into: headline, main body, and call-to-action. 
       Maintain brand voice and campaign objectives.
    
    Return ONLY a JSON object with these three keys and their values. No additional text.
    """

    split_prompts = {}
    client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    try:
        for category, prompt in optimized_prompts.items():
            response = await client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"Create specialized prompts for this marketing concept:\n\n{prompt}"}
                ]
            )
            response_text = response.choices[0].message.content
            
            # Attempt to parse the JSON-like text output
            try:
                prompts = json.loads(response_text)
            except json.JSONDecodeError:
                print(f"Failed to parse response for category '{category}', returning raw text.")
                prompts = {"image_prompt": response_text, "video_prompt": response_text, "adcopy_prompt": response_text}
                
            split_prompts[category] = {
                "success": True,
                "prompt_id": str(uuid.uuid4()),
                "display_data": prompts,
                "data": prompts
            }

        return split_prompts

    except Exception as e:
        raise ValueError(f"Error in splitting prompt: {str(e)}")