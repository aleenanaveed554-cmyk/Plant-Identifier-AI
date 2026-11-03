
import streamlit as st
import base64
import io
import os
from groq import Groq
from PIL import Image

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="Plant Identifier AI",
    page_icon="🌿",
    layout="wide"
)

# ---------------- GREEN THEME + BLACK TEXT ----------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #e8f5e9, #f5fff5);
}

header {
    background: transparent !important;
}

h1, h2, h3, h4, p, span, label,
.stMarkdown, .stMarkdown p, .stMarkdown li,
.stMarkdown strong, .stText, [data-testid="stCaptionContainer"],
[data-testid="stFileUploader"] label,
[data-testid="stWidgetLabel"] {
    color: #000000 !important;
}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #000000 !important;
}

.subtitle {
    text-align: center;
    font-size: 17px;
    color: #000000 !important;
}

div.stButton > button {
    background: #238b45;
    color: white !important;
    border-radius: 12px;
    border: none;
    height: 48px;
    font-weight: bold;
    width: 100%;
}

div.stButton > button:hover {
    background: #176b35;
    color: white !important;
}

.result-card {
    background: white;
    padding: 22px;
    border-radius: 15px;
    border-left: 5px solid #238b45;
    margin-top: 15px;
    color: black !important;
}

.result-card * {
    color: black !important;
}

section[data-testid="stFileUploader"] {
    background: white;
    padding: 15px;
    border-radius: 12px;
}

hr {
    border-color: #a5d6a7;
}
</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------

st.markdown(
    '<div class="main-title">🌿 Plant Identifier AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Discover plants with the power of Artificial Intelligence</div>',
    unsafe_allow_html=True
)

st.write("")
st.divider()

# ---------------- INTRODUCTION ----------------

st.markdown("### 🌱 Welcome to Plant Identifier AI")

st.write(
    "Upload a clear picture of any plant and let AI identify it. "
    "Discover its scientific name, benefits, growing conditions, "
    "care instructions and common diseases."
)

# ---------------- IMAGE UPLOAD ----------------

left, right = st.columns([1, 1])

with left:
    st.markdown("### 📸 Upload Plant Image")

    uploaded_file = st.file_uploader(
        "Choose a plant photo",
        type=["jpg", "jpeg", "png", "webp"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        image.thumbnail((1200, 1200))

        st.image(
            image,
            caption="Your Uploaded Plant",
            use_container_width=True
        )

with right:
    st.markdown("### 🔍 Plant Analysis")

    st.write(
        "Click the button below to identify your plant "
        "and receive complete information."
    )

    analyze = st.button("🌿 Analyze Plant")


# ---------------- AI ANALYSIS ----------------

if analyze:

    if uploaded_file is None:
        st.warning("Please upload a plant image first.")

    else:
        try:
            # Get API key from Streamlit Secrets or environment
            api_key = st.secrets.get("GROQ_API_KEY", "") or os.getenv(
                "GROQ_API_KEY", ""
            )

            if not api_key:
                st.error(
                    "Groq API Key not found. Please add GROQ_API_KEY "
                    "in Streamlit Secrets."
                )
                st.stop()

            client = Groq(api_key=api_key)

            # Prepare image
            image = Image.open(uploaded_file).convert("RGB")
            image.thumbnail((1200, 1200))

            image_buffer = io.BytesIO()
            image.save(image_buffer, format="JPEG", quality=85)

            image_data = base64.b64encode(
                image_buffer.getvalue()
            ).decode("utf-8")

            prompt = """
            You are an expert botanist and plant identification AI.

            Carefully examine the uploaded plant photograph.

            Identify the plant and provide a detailed report using
            the following headings:

            1. Plant Name
            2. Scientific Name
            3. Description
            4. Benefits and Uses
            5. Watering Requirements
            6. Sunlight Requirements
            7. Soil Type
            8. Care Instructions
            9. Common Diseases

            Explain every section in simple, clear language.

            Give practical plant care information.
            Mention uncertainty if the plant cannot be identified
            confidently.

            If the image does not contain a recognizable plant,
            clearly explain that identification is not possible.

            Use Markdown headings and bullet points.
            Do not invent scientific information.
            """

            with st.spinner("🌿 AI is identifying your plant..."):

                response = client.chat.completions.create(
                    model="qwen/qwen3.8-27b",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": prompt
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": (
                                            "data:image/jpeg;base64,"
                                            + image_data
                                        )
                                    }
                                }
                            ]
                        }
                    ],
                    temperature=0.2,
                    max_completion_tokens=2500
                )

                result = response.choices[0].message.content

            # Display results
            st.divider()
            st.markdown("## 🌿 Plant Identification Results")

            st.markdown(
                '<div class="result-card">',
                unsafe_allow_html=True
            )

            st.markdown(result)

            st.markdown("</div>", unsafe_allow_html=True)

            st.success("Plant analysis completed successfully!")

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")


# ---------------- FOOTER ----------------

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:black;">
        <h4>🌿 Plant Identifier AI</h4>
        <p>Powered by Python, Streamlit and Generative AI</p>
        <p>Made with care for plant lovers</p>
    </div>
    """,
    unsafe_allow_html=True
)


import streamlit as st
import base64
import os
from groq import Groq

st.set_page_config(
    page_title="Plant Identifier AI",
    page_icon="🌿",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #f0f7f0;
}
h1, h2, h3, p, label {
    color: black !important;
}
.result {
    background: white;
    padding: 20px;
    border-radius: 15px;
    color: black;
    border: 1px solid #cde5cd;
}
.stButton button {
    background: #218838;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("🌿 Plant Identifier AI")
st.write("Identify any plant using Artificial Intelligence.")

st.divider()

uploaded_file = st.file_uploader(
    "Upload Plant Image",
    type=["jpg", "jpeg", "png", "webp"]
)

if uploaded_file:
    st.image(uploaded_file, width=350)

if st.button("Identify Plant 🌱"):

    if uploaded_file is None:
        st.warning("Please upload a plant image.")

    else:
        api_key = st.secrets.get(
            "GROQ_API_KEY",
            os.getenv("GROQ_API_KEY")
        )

        if not api_key:
            st.error("Groq API Key is missing.")

        else:
            try:
                client = Groq(api_key=api_key)

                image_data = base64.b64encode(
                    uploaded_file.getvalue()
                ).decode("utf-8")

                with st.spinner("Analyzing your plant..."):

                    response = client.chat.completions.create(
                        model="meta-llama/llama-4-scout-17b-16e-instruct",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "Identify this plant. Give its common name, scientific name, description, features, watering needs, sunlight and care tips. Mention if identification is uncertain."
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:{uploaded_file.type};base64,{image_data}"
                                        }
                                    }
                                ]
                            }
                        ],
                        temperature=0.2,
                        max_completion_tokens=1000
                    )

                result = response.choices[0].message.content

                st.subheader("🌱 Plant Identification Result")

                st.markdown(
                    f'<div class="result">{result}</div>',
                    unsafe_allow_html=True
                )

                st.info("AI results may not always be accurate. Do not eat unidentified plants.")

            except Exception as e:
                st.error(f"Error: {e}")

st.divider()

st.caption("Plant Identifier AI | Powered by Generative AI")
