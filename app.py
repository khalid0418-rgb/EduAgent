import streamlit as st
import os
from supabase import create_client, Client

@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()
import streamlit as st
import os
from supabase import create_client, Client

# --- CLEAN IMPORT SECTION ---
try:
    from generator import (
        generate_marketing_strategy, 
        generate_social_post, 
        generate_full_calendar_content, 
        generate_image_for_post
    )
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.stop() # This stops the app here so we can read the error

# Initialize Supabase connection
@st.cache_resource
def init_connection():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    return create_client(url, key)

supabase = init_connection()

# --- DATABASE FUNCTIONS (Insert Step 2 Here) ---
def load_user_profile(email):
    try:
        response = supabase.table("profiles").select("*").eq("email", email).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        st.error(f"Error loading profile: {e}")
        return None
    
def save_user_profile(email, biz_data):
    try:
        # NOTICE: The keys here must match what is sent from the UI
        supabase.table("profiles").upsert({
            "email": email,
            "biz_name": biz_data['biz_name'],
            "biz_niche": biz_data['biz_niche'],
            "target_audience": biz_data['target_audience']
        }).execute()
        st.success("Profile saved to cloud!")
    except Exception as e:
        st.error(f"Error saving profile: {e}")

# Page Configuration
st.set_page_config(page_title="AI Marketing Strategist", page_icon="📈")

# --- SIDEBAR UI ---
with st.sidebar:
    st.header("🏢 Business Intelligence Profile")
    
    # 1. Email is the master key
    user_email = st.text_input("Enter your email to load/save profile", key="user_email")

    # 2. LOAD BUTTON
    if st.button("🔍 Load My Profile"):
        if user_email:
            profile = load_user_profile(user_email)
            if profile:
                st.session_state['biz_name'] = profile.get('biz_name', '')
                st.session_state['biz_niche'] = profile.get('biz_niche', '')
                st.session_state['target_audience'] = profile.get('target_audience', '')
                st.success("Profile Loaded!")
            else:
                st.warning("No profile found.")
        else:
            st.error("Please enter email first.")

    st.divider()

    # 3. Inputs (The ONLY place these should exist)
    biz_name = st.text_input("Business Name", value=st.session_state.get('biz_name', ''), key="bn")
    biz_niche = st.text_input("Niche", value=st.session_state.get('biz_niche', ''), key="bniche")
    target_audience = st.text_input("Target Audience", value=st.session_state.get('target_audience', ''), key="ta")

    # 4. SAVE BUTTON
    if st.button("💾 Save Profile"):
        if user_email and biz_name:
            biz_data = {
                "biz_name": biz_name,
                "biz_niche": biz_niche,
                "target_audience": target_audience
            }
            save_user_profile(user_email, biz_data)
        else:
            st.error("Email and Name required.")

    st.divider()
    
    platform = st.selectbox("Target Platform", ("LinkedIn", "Twitter/X", "Instagram", "Facebook"))
    tone = st.select_slider("Tone of Voice", options=["Academic", "Professional", "Casual", "Enthusiastic"])

# --- PREPARE DATA FOR AI ---
# We define this AFTER the sidebar logic so it has the latest data
biz_profile = {
    "name": biz_name,
    "niche": biz_niche,
    "audience": target_audience
}

st.title("📈 AI Marketing Strategist")

# --- TAB SYSTEM START ---
tab1, tab2, tab3 = st.tabs(["📝 Single Post", "📅 Weekly Calendar", "🎨 Image Generator"])

with tab1:
    st.subheader("Write one perfect post")
    topic_single = st.text_input(
        "What topic do you want to share today?", 
        placeholder="e.g., The benefits of active learning",
        key="single_topic"
    )
    
    if st.button("Generate Single Post"):
        if topic_single:
            with st.spinner(f'Writing your {platform} post...'):
                try:
                    result = generate_social_post(topic_single, platform, tone, biz_profile)
                    st.success("Post Generated!")
                    st.markdown("---")
                    st.write(result)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a topic!")

with tab2:
    st.subheader("Plan your whole week")
    topic_week = st.text_input("Enter a theme for the week", key="week_topic")
    
    if st.button("Generate 7-Day Strategy"):
        if topic_week:
            with st.spinner("Creating strategy..."):
                # Save the strategy to the "session state" so the next button can see it
                st.session_state.current_strategy = generate_weekly_calendar(topic_week, tone, biz_profile)
                st.success("Strategy Ready!")
                st.info(st.session_state.current_strategy)
        else:
            st.warning("Please enter a theme!")

    # NEW: If a strategy exists, show the button to write the actual posts
    if "current_strategy" in st.session_state:
        if st.button("✨ Write Full Captions for All 7 Days"):
            with st.spinner("Writing 7 days of content..."):
                full_content = generate_full_calendar_content(
                    st.session_state.current_strategy, platform, tone
                )
                st.markdown("---")
                st.write(full_content)
                st.download_button("Download Calendar as Text", full_content)

with tab3:
    st.subheader("Create a matching visual")
    # A text box where you can paste the post text the AI just wrote for you.
    content_to_match = st.text_area(
        "Paste the caption you want to match", 
        placeholder="e.g., K-12 students get a chance to learn how to build Agentic AI using python...",
        height=150
    )
    
    if st.button("Generate Matching Image"):
        if content_to_match:
            with st.spinner('AI Artist is painting your visual (this takes about 10-15 seconds)...'):
                try:
                    # 1. Generate the visual.
                    generated_image_url = generate_image_for_post(content_to_match)
                    st.success("Visual generated successfully!")
                    
                    # 2. Display the visual directly in the app.
                    st.image(generated_image_url, caption=f"Matching image for: {platform}")
                    
                except Exception as e:
                    # In 2026, the trend has shifted to identifiable outcomes, so we catch errors clearly.
                    st.error(f"Could not generate image. Sometimes the AI finds educational topics like 'Agentic AI' hard to visualize, or you may be out of OpenAI API image credits. Technical error: {e}")
        else:
            st.warning("Please paste some content first so the AI knows what to draw!")                
# --- TAB SYSTEM END ---