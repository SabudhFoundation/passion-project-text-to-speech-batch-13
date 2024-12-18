import os
import subprocess
import streamlit as st
from langdetect import detect, DetectorFactory, LangDetectException

# Set seed for consistent language detection
DetectorFactory.seed = 0

# Custom CSS to style the Streamlit app
st.markdown("""
    <style>
        .stApp {
            background-color: #f0f8ff;
        }
        .main-title {
            color:#FFF; 
            text-align: center;
            font-weight: bold;
            margin-bottom: 10px;
            background-color:#00308F;
            padding: 5px;
            border-radius: 10px;
        }
        .subtitle {
            color: #333333;
            text-align: center;
            font-size: 25px;
            margin-top: -10px;
            font-weight: 600;
        }
        .section-title {
            color: #00308F;
            font-size: 20px;
            font-weight: bold;
            margin-top: 20px;
        }
        .btn {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# App Title with Colors and Design
st.markdown('<p class="main-title" style="font-size:40px;margin-top:-40px;"><img src="https://cdn-icons-png.flaticon.com/128/5336/5336273.png" style="width:60px;">&nbsp;&nbsp;&nbsp;&nbsp;Punjabi Text-to-Speech (TTS)</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Generate audio from Punjabi text with a natural voice!</p>', unsafe_allow_html=True)

st.markdown('<hr style="margin-top:-10px;">', unsafe_allow_html=True)

# Input Section
with st.container():
    st.markdown('<p class="section-title" style="font-size: 22px;margin-bottom:-10px;">📝 Input Text</p>', unsafe_allow_html=True)
    text_input = st.text_area("Enter text to synthesize:", "ਤੁਹਾਡਾ ਦਿਨ ਸ਼ਾਨਦਾਰ ਹੋਵੇ!", height=90)

# Speaker Selection
with st.container():
    st.markdown('<p class="section-title" style="font-size: 22px;margin-bottom:-10px;margin-top:10px;">🎤 Select Voice</p>', unsafe_allow_html=True)
    speaker_options = ["Female", "Male"]
    selected_speaker = st.radio("Choose a voice:", speaker_options, horizontal=True)

# Output Audio Path
output_folder = "static/audio"
os.makedirs(output_folder, exist_ok=True)  # Create folder if it doesn't exist
output_path = os.path.join(output_folder, "punj.wav")

# Function to Validate Punjabi Text
def is_punjabi_text(text):
    try:
        detected_lang = detect(text)
        return detected_lang == 'pa'
    except LangDetectException:
        return False

# TTS Generation Button
st.markdown('<p class="section-title" style="font-size: 22px;margin-top:10px;">🔊 Generate Speech</p>', unsafe_allow_html=True)
if st.button("🎧 Generate Speech", key="tts_btn"):
    if not is_punjabi_text(text_input):
        st.error("❌ Please enter text in Punjabi.")
    else:
        with st.spinner("⏳ Generating speech... Please wait."):

            # TTS Model Paths
            model_path = "models/v1/pa/fastpitch/best_model.pth"
            config_path = "models/v1/pa/fastpitch/config.json"
            vocoder_path = "models/v1/pa/hifigan/best_model.pth"
            vocoder_config_path = "models/v1/pa/hifigan/config.json"

            # TTS Command
            command = [
                "tts",
                "--text", text_input,
                "--model_path", model_path,
                "--config_path", config_path,
                "--vocoder_path", vocoder_path,
                "--vocoder_config_path", vocoder_config_path,
                "--speaker_idx", selected_speaker.lower(),
                "--out_path", output_path,
            ]

            try:
                # Run Command
                result = subprocess.run(command, check=True, text=True, capture_output=True, encoding='utf-8')
                st.success("✅ TTS generation successful!")
                st.audio(output_path)
                st.info(f"Audio saved at: {output_path}")

            except subprocess.CalledProcessError as e:
                st.error(f"❌ An error occurred while generating speech: {e.stderr}")
                st.text(f"Debug Info: {e.output}")

            except FileNotFoundError:
                st.error("❌ The 'tts' command is not found. Please ensure the TTS tool is installed and accessible.")

# Footer
st.markdown('<hr>', unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; color: #00308F;">
        Made with ❤ using Streamlit
    </div>
""", unsafe_allow_html=True)