import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import openai
import textwrap

# --- CONFIG ---
openai.api_key = st.secrets["openai_api_key"]  # You'll add this in Streamlit later
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Uses built-in font

# --- UI ---
st.title("🖼️ AI Brand Image Generator")
st.markdown("Generate branded ad visuals with AI-powered captions and customizable tone.")

prompt = st.text_input("Describe your idea (e.g. squirrel on a skateboard):")
tone = st.selectbox("Select brand tone", ["Playful", "Premium", "Eco-Friendly", "Bold", "Minimalist"])
background_img = st.file_uploader("Optional: Upload a background template image", type=["png", "jpg"])
generate_button = st.button("Generate Image")

# --- Template ---
def generate_template(text, bg_path=None):
    if bg_path:
        base_img = Image.open(bg_path).convert("RGB")
    else:
        base_img = Image.open("ai_image_generator_template_demo.png").convert("RGB")

    draw = ImageDraw.Draw(base_img)
    font = ImageFont.truetype(font_path, 28)
    wrapped_text = textwrap.fill(text, width=25)
    draw.text((400, 200), wrapped_text, fill="#333333", font=font)

    return base_img

# --- GPT Caption Generator ---
def generate_caption(prompt, tone):
    system_prompt = f"You write short, clever brand captions in a {tone.lower()} tone."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Write a brand caption about: {prompt}"}
        ],
        max_tokens=30,
        temperature=0.7
    )
    return response['choices'][0]['message']['content'].strip()

# --- Run Logic ---
if generate_button and prompt:
    with st.spinner("Generating..."):
        caption = generate_caption(prompt, tone)
        bg_source = background_img if background_img else None
        final_img = generate_template(caption, bg_path=bg_source)

        st.image(final_img, caption=caption)
        final_img.save("output.png")
        st.download_button("Download Image", data=open("output.png", "rb"), file_name="generated_ad.png")
