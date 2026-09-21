import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

app_username = os.getenv("APP_USERNAME")
app_password = os.getenv("APP_PASSWORD")

# Page configuration
st.set_page_config(
    page_title="Network Troubleshooting Assistant",
    page_icon="🌐",
    layout="wide"
)

# Initialize login state
# Initialize login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ---------------- LOGIN PAGE ----------------

if not st.session_state.logged_in:

    st.title("🌐 Network Troubleshooting Assistant")

    left, center, right = st.columns([1, 2, 1])

    with center:
        st.subheader("🔐 User Login")

        st.write(
            "Please enter your credentials to access the "
            "Generative AI Network Troubleshooting Assistant."
        )

        username = st.text_input(
            "Username",
            placeholder="Enter username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password"
        )

        if st.button("🔐 Login", type="primary"):

            if username == app_username and password == app_password:
                st.session_state.logged_in = True
                st.rerun()

            else:
                st.error("Invalid username or password.")

    st.stop()

# ---------------- LOGOUT ----------------

col1, col2 = st.columns([8, 1])

with col2:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# Header
st.title("🌐 Generative AI Assistant for Network Troubleshooting")

st.caption(
    "AI-powered assistance for analyzing and resolving common "
    "network infrastructure problems."
)

st.divider()

# Input section
st.subheader("Network Issue")

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

problem = st.text_area(
    "Describe the network problem",
    placeholder=(
        "Example: Users in VLAN 20 cannot access the internet, "
        "but users in VLAN 10 can access the internet."
    ),
    height=150
)

# Troubleshoot button
if st.button("🔍 Analyze & Troubleshoot", type="primary"):

    if problem.strip():

        prompt = f"""
        You are a professional network troubleshooting assistant.

        Device or Technology: {device}
        Network Problem: {problem}

        Analyze the network problem and provide the response
        using the following structure:

        1. Problem Analysis
        2. Possible Causes
        3. Step-by-Step Troubleshooting Procedure
        4. Relevant Commands or Checks
        5. Recommended Solution
        6. Additional Verification

        Keep the response practical, technically accurate,
        structured, and easy to understand.
        """

        try:
            with st.spinner("Analyzing the network problem..."):

                interaction = client.interactions.create(
                    model="gemini-3.6-flash",
                    input=prompt
                )

            st.success("Analysis completed successfully.")

            st.divider()

            # Analysis summary
            st.subheader("📋 Troubleshooting Analysis")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Device / Technology**")
                st.write(device)

            with col2:
                st.markdown("**Analysis Status**")
                st.write("Completed")

            st.markdown("**Reported Problem**")
            st.info(problem)

            # AI response
            st.subheader("🤖 AI Troubleshooting Response")
            st.markdown(interaction.output_text)

        except Exception as e:
            st.error(
                "Unable to generate the troubleshooting response. "
                "Please try again."
            )

            with st.expander("Technical Details"):
                st.code(str(e))

    else:
        st.warning("⚠️ Please describe the network problem first.")

st.divider()

st.caption(
    "Generative AI Assistant for Network Troubleshooting | "
    "MCA Mini Project"
)