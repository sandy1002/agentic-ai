import streamlit as st
from app.email_reader import fetch_unseen_emails
from app.agent import process_email  # your agent logic

st.title("📧 Agentic Email Assistant")

st.sidebar.header("Login")
email = st.sidebar.text_input("Email Address")
password = st.sidebar.text_input("App Password", type="password")

if st.sidebar.button("Fetch Emails"):
    if email and password:
        with st.spinner("Fetching unread emails..."):
            emails = fetch_unseen_emails(email, password)
            if emails:
                st.session_state['emails'] = emails
                st.success(f"Found {len(emails)} unread emails.")
            else:
                st.warning("No unread emails found.")
    else:
        st.error("Please enter credentials.")

if 'emails' in st.session_state:
    for idx, mail in enumerate(st.session_state['emails']):
        with st.expander(f"Email #{idx+1} - {mail['subject']}"):
            st.markdown(f"**From:** {mail['from']}")
            st.markdown(mail['body'])

            if st.button(f"Summarize Email #{idx+1}"):
                with st.spinner("Running agent..."):
                    summary = process_email(mail['body'])  # langgraph + llama3
                    st.success("Summary:")
                    st.markdown(summary)

if st.button(f"Suggest Reply #{idx+1}"):
    with st.spinner("Thinking..."):
        reply = suggest_reply(mail['body'])
        st.success("Suggested Reply:")
        st.text_area("Reply Text", value=reply, height=150)
