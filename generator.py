import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load your credentials
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 2. Your existing function for single posts
def generate_social_post(topic, platform, tone):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are an expert content creator. Write in a {tone} tone for {platform}."},
            {"role": "user", "content": f"Create a post about: {topic}"}
        ]
    )
    return response.choices[0].message.content

# 3. ADD THE NEW FUNCTION HERE
def generate_weekly_calendar(topic, tone):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a strategic content planner. Create a 7-day social media calendar (Monday-Sunday)."},
            {"role": "user", "content": f"Topic: {topic}. Tone: {tone}. Provide a brief hook and a goal for each day."}
        ]
    )
    return response.choices[0].message.content
def generate_full_calendar_content(strategy, platform, tone):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a master copywriter for {platform}. Write in a {tone} tone."},
            {"role": "user", "content": f"Based on this strategy: {strategy}, write the full caption for all 7 days. Include relevant hashtags and emojis."}
        ]
    )
    return response.choices[0].message.content
def generate_image_for_post(post_text):
    # FIRST, we ask GPT to write a professional artist prompt based on the post text.
    prompt_request = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional prompt engineer for AI image generators. Create a highly detailed, photorealistic prompt for DALL-E 3 that captures the essence of the following social media post text. Do not include any text or words inside the image itself."},
            {"role": "user", "content": f"Write an image prompt based on this post: {post_text}"}
        ]
    )
    
    # This is the specialized prompt GPT designed for the artist.
    dalle_prompt = prompt_request.choices[0].message.content
    
    # NEXT, we send that specialized prompt to the AI Artist (DALL-E 3).
    image_response = client.images.generate(
        model="dall-e-3",
        prompt=dalle_prompt,
        n=1,
        size="1024x1024",
        quality="standard"
    )
    
    # This is the final URL where the AI stored your finished masterpiece.
    image_url = image_response.data[0].url
    return image_url