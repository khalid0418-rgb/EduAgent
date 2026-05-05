import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load your credentials
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# 1. Strategy Function (Updated)
def generate_marketing_strategy(goal, platform, tone, biz_profile):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a Senior Marketing Strategist for {biz_profile['name']} ({biz_profile['niche']})."},
            {"role": "user", "content": f"Create a 7-day strategy for {platform} targeting {biz_profile['audience']}. Goal: {goal}. Tone: {tone}."}
        ]
    )
    return response.choices[0].message.content

# 2. Single Post Function (Fixed the 'topic' vs 'goal' mismatch)
def generate_social_post(goal, platform, tone, biz_profile):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a content creator for {biz_profile['name']}. Target audience: {biz_profile['audience']}."},
            {"role": "user", "content": f"Write a {platform} post to achieve the goal of: {goal}. Tone: {tone}."}
        ]
    )
    return response.choices[0].message.content

# 3. Full Calendar Content (Updated)
def generate_full_calendar_content(strategy, platform, tone, biz_profile):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a copywriter for {biz_profile['name']}. Writing for {platform} targeting {biz_profile['audience']}."},
            {"role": "user", "content": f"Based on this strategy: {strategy}, write the full caption for all 7 days. Tone: {tone}."}
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