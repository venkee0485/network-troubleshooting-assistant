import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

st.set_page_config(
    page_title="Network Troubleshooting Assistant",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Generative AI Assistant for Network Troubleshooting")

st.write(
    "Describe your network problem below, and the assistant will "
    "help you troubleshoot it."
)

st.divider()

problem = st.text_area(
    "Describe the network problem",
    placeholder="Example: Users in VLAN 20 cannot access the internet..."
)

device = st.selectbox(
    "Select the network device or technology",
    [
        "Cisco Switch",
        "Cisco Router",
        "FortiGate Firewall",
        "Palo Alto Firewall",
        "Windows Server",
        "Azure Networking",
        "AWS Networking",
        "Other"
    ]
)

if st.button("🔍 Troubleshoot"):
    if problem.strip():
        prompt = f"""
        You are a network troubleshooting assistant.

        Device or Technology: {device}
        Network Problem: {problem}

        Analyze the problem and provide:
        1. Possible causes
        2. Step-by-step troubleshooting procedure
        3. Relevant commands or checks
        4. Recommended solution

        Keep the response practical and easy to understand.
        """
        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt
        )
        st.subheader("Troubleshooting Analysis")

        st.info(
            f"Device/Technology: {device}\n\n"
            f"Problem: {problem}"
        )

        st.subheader("AI Troubleshooting Response")
        st.markdown(interaction.output_text)
    else:
        st.warning("Please describe the network problem first.")