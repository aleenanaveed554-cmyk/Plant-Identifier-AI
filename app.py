
import streamlit as st
import base64
import os
from groq import Groq

# Page Settings
st.set_page_config(
    page_title="Plant Identifier AI",
    page_icon="🌿",
    layout="wide"
)

# Custom Design
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f7faf6, #e8f5e9);
}
h1, h2, h3, p, label {
    color: #000000 !important;
}
.result-box {
    background: white;
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #d5e8d5;
    color: black !important;
}
.result-box p, .result-box h3, .result-box li {
    color: black !important;
}
.stButton button {
    background-color: #218838;
    color: white;
    border-radius: 10px;
    border: none;
}
.stButton button:hover {
    background-color: #176b2c;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("🌿 Plant Identifier AI")
st.write("Upload a plant image and let AI identify it.")

st.divider()

# Main Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("📷 Upload Plant Image")

    uploaded_file = st.file_uploader(
        "Choose a plant image",
        type=["jpg", "jpeg", "png", "webp"]
    )

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Plant", use_container_width=True)

with col2:
    st.subheader("🔍 Plant Analysis")

    st.write(
        "Our AI will analyze your plant image "
        "and provide its name, features and care information."
    )

    analyze = st.button(
        "Identify Plant 🌱",
        use_container_width=True
    )

    if analyze:

        if uploaded_file is None:
            st.warning("Please upload a plant image first.")

        else:
            try:
                # Get API Key
                api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

                if not api_key:
                    st.error("Groq API Key is missing. Please add it in Streamlit Secrets.")

                else:
                    client = Groq(api_key=api_key)

                    # Convert Image to Base64
                    image_bytes = uploaded_file.getvalue()
                    encoded_image = base64.b64encode(
                        image_bytes
                    ).decode("utf-8")

                    mime_type = uploaded_file.type

                    # AI Analysis
                    with st.spinner("AI is analyzing your plant... 🌿"):

                        response = client.chat.completions.create(
                            model="qwen/qwen3.8-27b",
                            messages=[
                                {
                                    "role": "system",
                                    "content": (
                                        "You are a helpful plant identification AI. "
                                        "Analyze plant images carefully. "
                                        "If you cannot identify a plant confidently, "
                                        "say so clearly. Never claim a plant is safe "
                                        "to eat or use as medicine based only on an image."
                                    )
                                },
                                {
                                    "role": "user",
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": """
                                            Identify this plant and provide:

                                            1. Common Name
                                            2. Scientific Name
                                            3. Plant Description
                                            4. Main Features
                                            5. Growing Conditions
                                            6. Watering Requirements
                                            7. Basic Care Tips

                                            If identification is uncertain, explain why.
                                            """
                                        },
                                        {
                                            "type": "image_url",
                                            "image_url": {
                                                "url": f"data:{mime_type};base64,{encoded_image}"
                                            }
                                        }
                                    ]
                                }
                            ],
                            temperature=0.2,
                            max_completion_tokens=1200
                        )

                    # Display Result
                    result = response.choices[0].message.content

                    st.markdown(
                        '<div class="result-box">',
                        unsafe_allow_html=True
                    )

                    st.subheader("🌱 Plant Identification Result")
                    st.markdown(result)

                    st.markdown("</div>", unsafe_allow_html=True)

                    st.info(
                        "AI identification can be incorrect. "
                        "Do not eat or use a plant based only on this result."
                    )

            except Exception as e:
                st.error(f"Something went wrong: {e}")

st.divider()

# Footer
st.markdown(
    "<center>🌿 Plant Identifier AI | Powered by Generative AI</center>",
    unsafe_allow_html=True
)

        font-size: clamp(2rem, 4vw, 3rem);
        margin: 0 0 8px 0;
        font-weight: 800;
        letter-spacing: -1.2px;
    }
    .hero p {
        color: #d9eadb;
        font-size: 1.02rem;
        margin: 0;
    }
    .section-card {
        background: rgba(255,255,255,.88);
        border: 1px solid #e1eadf;
        border-radius: 20px;
        padding: 22px;
        box-shadow: 0 8px 24px rgba(31, 67, 42, .05);
    }
    /* Keep AI analysis text readable without changing the surrounding design. */
    .st-key-analysis_result,
    .st-key-analysis_result p,
    .st-key-analysis_result li,
    .st-key-analysis_result h1,
    .st-key-analysis_result h2,
    .st-key-analysis_result h3,
    .st-key-analysis_result h4,
    .st-key-analysis_result strong,
    .st-key-analysis_result em,
    .st-key-analysis_result code {
        color: #000000 !important;
    }
    .small-label {
        color: #5b7863;
        text-transform: uppercase;
        letter-spacing: 1.4px;
        font-size: .72rem;
        font-weight: 800;
    }
    div.stButton > button {
        background: linear-gradient(100deg, #246b45, #39885a);
        color: white;
        border: 0;
        border-radius: 12px;
        padding: .72rem 1rem;
        font-weight: 700;
        width: 100%;
        transition: .2s ease;
    }
    div.stButton > button:hover {
        background: #174c32;
        color: white;
        border: 0;
        transform: translateY(-1px);
    }
    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,.82);
        border: 1px solid #e6eee4;
        border-radius: 16px;
        padding: 12px;
    }
    .tip {
        color: #55705b;
        background: #e8f2e6;
        border-left: 4px solid #43845a;
        padding: 12px 14px;
        border-radius: 8px;
        font-size: .9rem;
    }
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- Helpers --------------------
MODEL_NAME = "qwen/qwen3.8-27b"


def image_to_data_url(image: Image.Image) -> str:
    """Resize and encode an uploaded image for the Groq vision API."""
    image = image.convert("RGB")
    image.thumbnail((1600, 1600))
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=88, optimize=True)
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}"


def get_groq_client():
    api_key = st.secrets.get("GROQ_API_KEY", "") if hasattr(st, "secrets") else ""
    api_key = api_key or os.getenv("GROQ_API_KEY", "")
    if not api_key:
        return None
    return Groq(api_key=api_key)


def ask_about_image(client, image_data_url, question, previous_messages=None):
    messages = [
        {
            "role": "system",
            "content": (
                "You are Plant Identifier AI, a careful and helpful plant-image assistant. "
                "Identify plants only when the visible evidence supports it. If uncertain, "
                "say so and give likely possibilities rather than pretending certainty. "
                "Describe visible features clearly. For plant health questions, discuss only "
                "what can reasonably be inferred from the photo, mention that a photo cannot "
                "confirm a diagnosis, and suggest checking with a local horticulture expert "
                "for serious or worsening problems. Do not invent facts."
            ),
        }
    ]

    if previous_messages:
        messages.extend(previous_messages[-8:])

    messages.append(
        {
            "role": "user",
            "content": [
                {"type": "text", "text": question},
                {
                    "type": "image_url",
                    "image_url": {"url": image_data_url},
                },
            ],
        }
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.3,
        max_completion_tokens=1200,
    )
    return response.choices[0].message.content


# -------------------- Sidebar --------------------
with st.sidebar:
    st.markdown("## 🌿 Plant Identifier AI")
    st.caption("Your smart plant companion")
    st.markdown("---")
    st.markdown("### How to use")
    st.markdown(
        "1. Upload a clear plant photo.\n"
        "2. Choose an analysis option.\n"
        "3. Read the AI result.\n"
        "4. Ask follow-up questions."
    )
    st.markdown("---")
    st.markdown("### API connection")
    if os.getenv("GROQ_API_KEY") or (
        hasattr(st, "secrets") and st.secrets.get("GROQ_API_KEY", "")
    ):
        st.success("Groq API key detected")
    else:
        st.warning("Add your Groq API key to continue.")
    st.caption("Keep your API key private. Never upload it to GitHub.")


# -------------------- Main interface --------------------
st.markdown(
    """
    <div class="hero">
      <div class="small-label" style="color:#b9d9bf;">AI-POWERED PLANT DISCOVERY</div>
      <h1>Discover the world of plants. 🌱</h1>
      <p>Upload a photo, identify a plant, explore its features, and ask questions.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([1.02, 1], gap="large")

with left:
    st.markdown("### 📷 Upload your plant")
    uploaded_file = st.file_uploader(
        "Choose a plant image",
        type=["jpg", "jpeg", "png", "webp"],
        help="For best results, upload a clear photo showing the leaves or flowers.",
    )

    if uploaded_file:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Your uploaded image", use_container_width=True)
            st.session_state["plant_image"] = image.copy()
            st.session_state["plant_image_data"] = image_to_data_url(image)
            st.session_state["plant_file_name"] = uploaded_file.name
        except Exception:
            st.error("This image could not be opened. Please upload another image.")
            st.stop()
    else:
        st.markdown(
            """
            <div class="section-card">
              <div style="font-size:3rem;">🪴</div>
              <h3 style="color:#214b32;">Your plant journey starts here</h3>
              <p style="color:#647b69;">Upload a photo to discover the plant name, visible features, and helpful care information.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

with right:
    st.markdown("### ✨ Plant analysis")
    st.markdown(
        '<div class="small-label">CHOOSE WHAT YOU WANT TO KNOW</div>',
        unsafe_allow_html=True,
    )
    analysis_choice = st.radio(
        "Analysis type",
        [
            "Identify this plant",
            "Describe this image",
            "Analyze visible plant condition",
            "Plant care recommendations",
        ],
        label_visibility="collapsed",
    )

    if st.button("🔍 Analyze plant", disabled=not bool(st.session_state.get("plant_image_data"))):
        client = get_groq_client()
        if client is None:
            st.error(
                "Groq API key not found. Add GROQ_API_KEY in Streamlit Secrets "
                "or as an environment variable."
            )
        else:
            prompts = {
                "Identify this plant": (
                    "Identify the plant in this image. Give the likely common name, "
                    "scientific name if reasonably identifiable, confidence level, and "
                    "the visible clues used. If you cannot identify it confidently, say so."
                ),
                "Describe this image": (
                    "Describe the uploaded image. Focus on the plant's visible appearance, "
                    "leaves, flowers, colors, shape, and other noticeable details."
                ),
                "Analyze visible plant condition": (
                    "Describe the visible condition of this plant. Mention only visible "
                    "signs such as discoloration, spots, wilting, or damage. Give possible "
                    "causes carefully, explain uncertainty, and suggest safe general next steps."
                ),
                "Plant care recommendations": (
                    "If you can identify the plant, provide general care guidance for light, "
                    "watering, soil, and temperature. If identification is uncertain, explain "
                    "that the advice may vary by species."
                ),
            }
            with st.spinner("The AI is studying your plant photo..."):
                try:
                    answer = ask_about_image(
                        client,
                        st.session_state["plant_image_data"],
                        prompts[analysis_choice],
                    )
                    st.session_state["analysis_result"] = answer
                    st.session_state["chat_history"] = []
                except Exception as error:
                    st.error(f"Something went wrong: {error}")

    if st.session_state.get("analysis_result"):
        st.markdown("---")
        st.markdown("#### 🌿 AI results")
        with st.container(key="analysis_result"):
            st.markdown(st.session_state["analysis_result"])

st.markdown("---")
st.markdown("### 💬 Ask questions about your picture")
st.caption("Upload a plant photo first, then ask anything about the image.")

if st.session_state.get("plant_image_data"):
    for message in st.session_state.get("chat_history", []):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_question = st.chat_input("Example: How often should I water this plant?")
    if user_question:
        client = get_groq_client()
        if client is None:
            st.error("Please add your Groq API key before asking a question.")
        else:
            history = st.session_state.setdefault("chat_history", [])
            history.append({"role": "user", "content": user_question})
            with st.chat_message("user"):
                st.markdown(user_question)

            api_history = [
                {"role": item["role"], "content": item["content"]}
                for item in history[:-1]
            ]
            with st.chat_message("assistant"):
                with st.spinner("Thinking about your plant..."):
                    try:
                        reply = ask_about_image(
                            client,
                            st.session_state["plant_image_data"],
                            user_question,
                            api_history,
                        )
                        st.markdown(reply)
                        history.append({"role": "assistant", "content": reply})
                    except Exception as error:
                        st.error(f"Something went wrong: {error}")
                        history.pop()
else:
    st.info("Upload a plant picture to start asking questions.")

st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color:#718675; padding:8px 0 20px 0;">
      🌿 Plant Identifier AI · Powered by Python, Streamlit & Groq
      <br><small>AI results are estimates. Confirm important plant-health decisions with a local expert.</small>
    </div>
    """,
    unsafe_allow_html=True,
)
font-family: 'Sans', sans-serif;
    
    .stApp {
        background:
          radial-gradient(circle at 85% 5%, rgba(125, 190, 130, .13), transparent 28%),
          linear-gradient(135deg, #f7faf6 0%, #eef5ed 100%);
    }
    [data-testid="stSidebar"] {
        background: #102d24;
    }
    [data-testid="stSidebar"] * {
        color: #f2f8f1 !important;
    }
    .hero {
        padding: 30px 32px;
        border-radius: 24px;
        background: linear-gradient(120deg, #143c2d, #286b49);
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 14px 35px rgba(22, 65, 44, .15);
    }
    .hero h1 {
        color: white;
        font-size: clamp(2rem, 4vw, 3rem);
        margin: 0 0 8px 0;
        font-weight: 800;
        letter-spacing: -1.2px;
    }
    .hero p {
        color: #d9eadb;
        font-size: 1.02rem;
        margin: 0;
    }
    .section-card {
        background: rgba(255,255,255,.88);
        border: 1px solid #e1eadf;
        border-radius: 20px;
        padding: 22px;
        box-shadow: 0 8px 24px rgba(31, 67, 42, .05);
    }
    .small-label {
        color: #5b7863;
        text-transform: uppercase;
        letter-spacing: 1.4px;
        font-size: .72rem;
        font-weight: 800;
    }
    div.stButton > button {
        background: linear-gradient(100deg, #246b45, #39885a);
        color: white;
        border: 0;
        border-radius: 12px;
        padding: .72rem 1rem;
        font-weight: 700;
        width: 100%;
        transition: .2s ease;
    }
    div.stButton > button:hover {
        background: #174c32;
        color: white;
        border: 0;
        transform: translateY(-1px);
    }
    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,.82);
        border: 1px solid #e6eee4;
        border-radius: 16px;
        padding: 12px;
    }
    .tip {
        color: #55705b;
        background: #e8f2e6;
        border-left: 4px solid #43845a;
        padding: 12px 14px;
        border-radius: 8px;
        font-size: .9rem;
    }
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- Helpers --------------------
MODEL_NAME = "qwen/qwen3.8-27b"


def image_to_data_url(image: Image.Image) -> str:
    """Resize and encode an uploaded image for the Groq vision API."""
    image = image.convert("RGB")
    image.thumbnail((1600, 1600))
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=88, optimize=True)
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}"


def get_groq_client():
    api_key = st.secrets.get("GROQ_API_KEY", "") if hasattr(st, "secrets") else ""
    api_key = api_key or os.getenv("GROQ_API_KEY", "")
    if not api_key:
        return None
    return Groq(api_key=api_key)


def ask_about_image(client, image_data_url, question, previous_messages=None):
    messages = [
        {
            "role": "system",
            "content": (
                "You are Plant Identifier AI, a careful and helpful plant-image assistant. "
                "Identify plants only when the visible evidence supports it. If uncertain, "
                "say so and give likely possibilities rather than pretending certainty. "
                "Describe visible features clearly. For plant health questions, discuss only "
                "what can reasonably be inferred from the photo, mention that a photo cannot "
                "confirm a diagnosis, and suggest checking with a local horticulture expert "
                "for serious or worsening problems. Do not invent facts."
            ),
        }
    ]

    if previous_messages:
        messages.extend(previous_messages[-8:])

    messages.append(
        {
            "role": "user",
            "content": [
                {"type": "text", "text": question},
                {
                    "type": "image_url",
                    "image_url": {"url": image_data_url},
                },
            ],
        }
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.3,
        max_completion_tokens=1200,
    )
    return response.choices[0].message.content


# -------------------- Sidebar --------------------
with st.sidebar:
    st.markdown("## 🌿 Plant Identifier AI")
    st.caption("Your smart plant companion")
    st.markdown("---")
    st.markdown("### How to use")
    st.markdown(
        "1. Upload a clear plant photo.\n"
        "2. Choose an analysis option.\n"
        "3. Read the AI result.\n"
        "4. Ask follow-up questions."
    )
    st.markdown("---")
    st.markdown("### API connection")
    if os.getenv("GROQ_API_KEY") or (
        hasattr(st, "secrets") and st.secrets.get("GROQ_API_KEY", "")
    ):
        st.success("Groq API key detected")
    else:
        st.warning("Add your Groq API key to continue.")
    st.caption("Keep your API key private. Never upload it to GitHub.")


# -------------------- Main interface --------------------
st.markdown(
    """
    <div class="hero">
      <div class="small-label" style="color:#b9d9bf;">AI-POWERED PLANT DISCOVERY</div>
      <h1>Discover the world of plants. 🌱</h1>
      <p>Upload a photo, identify a plant, explore its features, and ask questions.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([1.02, 1], gap="large")

with left:
    st.markdown("### 📷 Upload your plant")
    uploaded_file = st.file_uploader(
        "Choose a plant image",
        type=["jpg", "jpeg", "png", "webp"],
        help="For best results, upload a clear photo showing the leaves or flowers.",
    )

    if uploaded_file:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Your uploaded image", use_container_width=True)
            st.session_state["plant_image"] = image.copy()
            st.session_state["plant_image_data"] = image_to_data_url(image)
            st.session_state["plant_file_name"] = uploaded_file.name
        except Exception:
            st.error("This image could not be opened. Please upload another image.")
            st.stop()
    else:
        st.markdown(
            """
            <div class="section-card">
              <div style="font-size:3rem;">🪴</div>
              <h3 style="color:#214b32;">Your plant journey starts here</h3>
              <p style="color:#647b69;">Upload a photo to discover the plant name, visible features, and helpful care information.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

with right:
    st.markdown("### ✨ Plant analysis")
    st.markdown(
        '<div class="small-label">CHOOSE WHAT YOU WANT TO KNOW</div>',
        unsafe_allow_html=True,
    )
    analysis_choice = st.radio(
        "Analysis type",
        [
            "Identify this plant",
            "Describe this image",
            "Analyze visible plant condition",
            "Plant care recommendations",
        ],
        label_visibility="collapsed",
    )

    if st.button("🔍 Analyze plant", disabled=not bool(st.session_state.get("plant_image_data"))):
        client = get_groq_client()
        if client is None:
            st.error(
                "Groq API key not found. Add GROQ_API_KEY in Streamlit Secrets "
                "or as an environment variable."
            )
        else:
            prompts = {
                "Identify this plant": (
                    "Identify the plant in this image. Give the likely common name, "
                    "scientific name if reasonably identifiable, confidence level, and "
                    "the visible clues used. If you cannot identify it confidently, say so."
                ),
                "Describe this image": (
                    "Describe the uploaded image. Focus on the plant's visible appearance, "
                    "leaves, flowers, colors, shape, and other noticeable details."
                ),
                "Analyze visible plant condition": (
                    "Describe the visible condition of this plant. Mention only visible "
                    "signs such as discoloration, spots, wilting, or damage. Give possible "
                    "causes carefully, explain uncertainty, and suggest safe general next steps."
                ),
                "Plant care recommendations": (
                    "If you can identify the plant, provide general care guidance for light, "
                    "watering, soil, and temperature. If identification is uncertain, explain "
                    "that the advice may vary by species."
                ),
            }
            with st.spinner("The AI is studying your plant photo..."):
                try:
                    answer = ask_about_image(
                        client,
                        st.session_state["plant_image_data"],
                        prompts[analysis_choice],
                    )
                    st.session_state["analysis_result"] = answer
                    st.session_state["chat_history"] = []
                except Exception as error:
                    st.error(f"Something went wrong: {error}")

    if st.session_state.get("analysis_result"):
        st.markdown("---")
        st.markdown("#### 🌿 AI results")
        st.markdown(st.session_state["analysis_result"])

st.markdown("---")
st.markdown("### 💬 Ask questions about your picture")
st.caption("Upload a plant photo first, then ask anything about the image.")

if st.session_state.get("plant_image_data"):
    for message in st.session_state.get("chat_history", []):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_question = st.chat_input("Example: How often should I water this plant?")
    if user_question:
        client = get_groq_client()
        if client is None:
            st.error("Please add your Groq API key before asking a question.")
        else:
            history = st.session_state.setdefault("chat_history", [])
            history.append({"role": "user", "content": user_question})
            with st.chat_message("user"):
                st.markdown(user_question)

            api_history = [
                {"role": item["role"], "content": item["content"]}
                for item in history[:-1]
            ]
            with st.chat_message("assistant"):
                with st.spinner("Thinking about your plant..."):
                    try:
                        reply = ask_about_image(
                            client,
                            st.session_state["plant_image_data"],
                            user_question,
                            api_history,
                        )
                        st.markdown(reply)
                        history.append({"role": "assistant", "content": reply})
                    except Exception as error:
                        st.error(f"Something went wrong: {error}")
                        history.pop()
else:
    st.info("Upload a plant picture to start asking questions.")

st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color:#718675; padding:8px 0 20px 0;">
      🌿 Plant Identifier AI · Powered by Python, Streamlit & Groq
      <br><small>AI results are estimates. Confirm important plant-health decisions with a local expert.</small>
    </div>
    """,
    unsafe_allow_html=True,
)
