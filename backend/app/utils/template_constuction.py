# Backend/app/utils/template_construction.py
import json
import os

def construct_creatomate_template_data(brand_name, product_image_url, ad_copy, call_to_action):
    """
    Constructs the JSON payload for the Creatomate API using user-provided data.
    """
    return {
        "template_id": "c4bbd8f7-c6b9-4228-9ebc-eac48f2ea575",
        "modifications": {
            "090694a5-d715-40a4-a92c-2285240ed5d1": ad_copy,
            "Photo": product_image_url,
            "brand_name": brand_name,
            "call_to_action": call_to_action
        }
    }

def save_prompt_data(file_path, data):
    """
    Saves prompt data for analysis or reuse in future campaigns.
    """
    with open(file_path, "w") as file:
        json.dump(data, file)
