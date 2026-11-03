

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
