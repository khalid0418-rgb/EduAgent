import streamlit as st
import os
import sys

# Ensures the app can find your generator.py file in the current folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Notice we are now importing BOTH functions from your generator file
    from generator import generate_social_post, generate_weekly_calendar, generate_full_calendar_content, generate_image_for_post
except ImportError:
    st.error("Error: Could not find generator.py. Please ensure it is in the EduAgent folder.")

# Page Configuration
st.set_page_config(page_title="EduContent AI", page_icon="🎓")

# Sidebar for Global Settings (shared by both tabs)
with st.sidebar:
    st.header("Settings")
    platform = st.selectbox(
        "Target Platform",
        ("LinkedIn", "Twitter/X", "Instagram", "Facebook")
    )
    tone = st.select_slider(
        "Tone of Voice",
        options=["Academic", "Professional", "Casual", "Enthusiastic"]
    )

st.title("🎓 EduContent AI Agent")

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
                    result = generate_social_post(topic_single, platform, tone)
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
                st.session_state.current_strategy = generate_weekly_calendar(topic_week, tone)
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