# Backend/app/utils/ad_generation.py
import os
import aiohttp
from fastapi import HTTPException

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CREATOMATE_API_KEY = os.getenv("CREATOMATE_API_KEY")
CREATOMATE_TEMPLATE_ID = "c4bbd8f7-c6b9-4228-9ebc-eac48f2ea575"


async def generate_image(prompt: str) -> str:
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    json_data = {
        "prompt": prompt,
        "n": 1,
        "size": "512x512",
        "response_format": "url"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=json_data) as response:
            if response.status == 200:
                data = await response.json()
                return data['data'][0]['url']
            else:
                error_message = await response.text()
                raise HTTPException(status_code=response.status, detail=f"Failed to generate image with DALL-E: {error_message}")

async def generate_video(brand_name: str, product_image: str, text_overlay: str) -> str:
    url = "https://api.creatomate.com/v1/renders"
    headers = {
        "Authorization": f"Bearer {CREATOMATE_API_KEY}",
        "Content-Type": "application/json"
    }
    json_data = {
        "template_id": CREATOMATE_TEMPLATE_ID,
        "modifications": {
            "090694a5-d715-40a4-a92c-2285240ed5d1": text_overlay,
            "Photo": product_image
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=json_data) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('render_url', '')
            else:
                error_message = await response.text()
                raise HTTPException(status_code=response.status, detail="Failed to generate video with Creatomate")

async def generate_ad_copy(prompt_text: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    json_data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt_text}],
        "max_tokens": 150,
        "temperature": 0.7
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=json_data) as response:
            if response.status == 200:
                data = await response.json()
                return data['choices'][0]['message']['content'].strip()
            else:
                error_message = await response.text()
                raise HTTPException(status_code=response.status, detail=f"Failed to generate ad copy with ChatGPT: {error_message}")
