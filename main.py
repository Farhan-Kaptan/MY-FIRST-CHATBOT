import streamlit as st

from google import genai

from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="Kaptan's AI",
    page_icon="✨", 
    layout="centered"
)
#--------------------------------------------------------------------------------------------
# Printing "AI Assistant"
#--------------------------------------------------------------------------------------------
TITLE = "AI Assistant"  # your assistant's name
CSS = """<style>
.live-title {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 1rem;
}
 
.live-title-text {
    font-size: clamp(2.2rem, 7vw, 3.75rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.2;
    padding-bottom: 0.08em;
    /* colors flow across the text */
    background: linear-gradient(90deg, #8B5CF6, #3B82F6, #06B6D4, #8B5CF6);
    background-size: 200% auto;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: flow 4s linear infinite;
}
 
/* pulsing green "live" dot */
.live-dot {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: #22C55E;
    animation: pulse 1.8s ease-out infinite;
}
 
@keyframes flow { to { background-position: 200% center; } }
 
@keyframes pulse {
    0%   { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.6); }
    70%  { box-shadow: 0 0 0 12px rgba(34, 197, 94, 0); }
    100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
}
 
@media (prefers-reduced-motion: reduce) {
    .live-title-text, .live-dot { animation: none; }
}
</style>"""
 
HTML = f"""
<div class="live-title">
<div class="live-title-text">{TITLE}</div>
<span class="live-dot"></span>
</div>
"""
 
st.markdown(CSS + HTML, unsafe_allow_html=True)
#--------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------
# Choosing assistant
#--------------------------------------------------------------------------------------------
picked = st.menu_button("Select Model", options=["Fast", "Powerful"])
if picked:
    st.session_state.choice = picked      # save it
choice = st.session_state.get("choice")   # read it on every run

if choice == "Fast":
    st.write(":green[**Ask Fast**]")
    model_name = "gemini-3.5-flash-lite"
    token_limit = 8192
elif choice == "Powerful":
    st.write(":rainbow[**Powerful on work**]")
    model_name = "gemini-3.8-flash"
    token_limit = 32758

#--------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------
# Api Call 
#--------------------------------------------------------------------------------------------
client = genai.Client()
if choice:
  prompt = st.chat_input(f"Talk with {choice}", key="chat")
  if prompt:
   st.write(":blue[User:]", prompt)
   
   st.write(":blue[Assistant:]")
   response_placeholder = st.empty()
        
   # Use streaming for instant responses
   # Gemini 3.8's reasoning process happens seamlessly during the stream
   response_stream = client.models.generate_content_stream(
       model=model_name,
       contents=prompt,
       config={
           "max_output_tokens": token_limit
       }
   )
   
   # Update the UI token by token as they arrive
   full_response = ""
   for chunk in response_stream:
       full_response += chunk.text
       response_placeholder.markdown(full_response)