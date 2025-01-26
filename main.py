import streamlit as st
from hugging_face_model import *
from PyPDF2 import PdfReader

# Function to clear the input box and store the input in session state
def clear_input():
    if "user_input" in st.session_state:
        st.session_state.messages.append({"role": "user", "content": st.session_state.user_input})
        st.session_state.user_input = ""  # Clear the input box

# Function to extract text from a PDF file
def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def main():
    # Path to the logo
    matrickz_logo = r"C:\Users\BharadwajKrishnan\PycharmProjects\MatGPT\logo-full.png"

    # Custom CSS to fix the input box at the bottom
    st.markdown(
        """
        <style>
        /* Fixed input box at the bottom */
        .fixed-bottom {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: white;
            padding: 10px;
            z-index: 1000;
            border-top: 1px solid #e1e1e1;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Display title and company logo
    st.title("MatGPT Co-pilot")
    st.image(matrickz_logo)

    # Initialize chat history and Hugging Face model in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "hugging_face_obj" not in st.session_state:
        st.session_state.hugging_face_obj = HuggingFace_Matrickz()

    # Display chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.write(f"**You:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.write(f"**AI:** {msg['content']}")

    # Fixed input box at the bottom
    st.markdown('<div class="fixed-bottom">', unsafe_allow_html=True)
    st.text_input("Type your message here", key="user_input", on_change=clear_input)
    uploaded_file = st.file_uploader("Upload file")
    st.markdown('</div>', unsafe_allow_html=True)

    # Process user input and generate AI response
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        user_message = st.session_state.messages[-1]["content"]

        # Read file content if a file is uploaded
        file_content = None
        if uploaded_file is not None:
            if uploaded_file.type == "application/pdf":
                file_content = extract_text_from_pdf(uploaded_file)
            else:
                pass

        # Call Hugging Face model
        response = st.session_state.hugging_face_obj.query(user_message, file_content)

        # Append AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Rerun to display the updated chat history
        st.rerun()

if __name__ == "__main__":
    main()