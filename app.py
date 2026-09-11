import streamlit as st

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
        st.subheader("Troubleshooting Analysis")
        st.info(
            f"Device/Technology: {device}\n\n"
            f"Problem: {problem}"
        )
    else:
        st.warning("Please describe the network problem first.")