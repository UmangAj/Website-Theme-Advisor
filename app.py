import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import time

# load api key
load_dotenv()

# load llm model
llm = ChatGroq(
    model="gemma2-9b-it",
    temperature=0
)

# streamlit UI
st.set_page_config(
    page_title="Website Theme Advisor",
    page_icon="🔗",
    layout="centered"
)

st.markdown("<h1 style='text-align: center;'>Website Theme Advisor 🔗</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center;'>Need a theme? AI designs it. Just tell it what you need.</h5>", unsafe_allow_html=True)

user_input = st.chat_input("Describe your website needs...")
st.divider()

st.sidebar.write("##### Number of Pages:")
no_of_pages = st.sidebar.number_input("None", min_value=1, max_value=8, value=5, label_visibility = "collapsed")

st.sidebar.write("##### Select Menu Items:")
menu = st.sidebar.multiselect("None", 
                          ["Home", "About Us", "Services", "Portfolio / Projects", "Blog", "Contact Us", "FAQ","Testimonials", "Pricing", "Careers"], 
                          ["Home"],
                          label_visibility = "collapsed")

st.sidebar.write("##### Include Demo Code:")
demo_code = st.sidebar.radio("None", ["Yes", "No"], horizontal=True, label_visibility = "collapsed")

st.sidebar.divider()
st.sidebar.write("### About")
st.sidebar.write("This is a website theme advisor AI tool. You describe what you need, and it provides a page structure with menu options and demo code.")

# # prompt template
# template = f"""

# You are an expert website theme advisor. If the user ask any generalised question then you have to response that i have not able to give your answer. 

# * Website Structure Outline with title.*

# ## Website Specifications  
# - Total Pages: {no_of_pages},
# - Menu Items: provide menu items

# * Provide addition content of user requiremts with well-structured.
# * Ensure the total number of pages matches **"Total Pages"** specified.  
# * If additional pages are needed beyond menu items, include relevant ones (e.g., *Contact, Blog, FAQ*) with suitable content.  

# Demo code: {demo_code}

# **Demo Code**

# [If Include Demo Code is "Yes", generate basic HTML and CSS code for the website structure. The HTML should include the navigation menu based on the "Menu Items" and basic page divisions. The CSS should provide minimal styling to demonstrate the layout. Do not include excessive styling. Keep it simple and focused on structure.]

# [If Include Demo Code is "No", omit this section.]

# ** Keep the response clean, well-structured, and easy to understand. **

# ## Avoid  
# - If the user asks about topics not related to website building, then do not give response. 

# """


# prompt template
template = f"""

You are an expert website theme advisor. If the user ask any generalised question then you have to response that i have not able to give your answer. 

**Website Structure Outline with title.**

## Website Specifications  
- **Total Pages:** {no_of_pages} 
- **Menu Items:** provide menu items

## Detailed Page Breakdown  

For each page, provide the following details in a structured format:  

### **Page Name (Page Number)** 
- **Purpose:** A concise description of the page's role and key content areas, considering the user request for style and layout.  
- **Key Sections:** List of main sections or elements to include on the page.  

* Ensure the total number of pages matches **"Total Pages"** specified.  
* If additional pages are needed beyond menu items, include relevant ones (e.g., *Contact, Blog, FAQ*) with suitable content.  

Demo code: {demo_code}

**Demo Code**

[If Include Demo Code is "Yes", generate basic HTML and CSS code for the website structure. The HTML should include the navigation menu based on the "Menu Items" and basic page divisions. The CSS should provide minimal styling to demonstrate the layout. Do not include excessive styling. Keep it simple and focused on structure.]

[If Include Demo Code is "No", omit this section.]

Keep the response clean, well-structured, and easy to understand.

## Avoid  
- If the user asks about topics not related to website building, then do not give response. 

"""


prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("user", "{user_input}")
])

# create chain
chain = prompt | llm | StrOutputParser()

# initialize the chat history in streamlit session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input:
    if not user_input.strip():
        st.warning("Please enter a description.")
    elif not menu:
        st.warning("Please select at least one menu item.")
    else:

        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.write(f"###### {user_input}")
        
        with st.chat_message("ai"):
            placeholder = st.empty()
            try:
                response = chain.invoke(user_input)
                if demo_code == "No":
                    response = response.split("Demo code: No")[0]
                
                # Simulate streaming output with animation
                animated_response = "###### AI Response\n" #include the title in the response.
                for char in response:
                    animated_response += char
                    placeholder.markdown(animated_response)
                    time.sleep(0.001)  # Adjust speed as needed

                st.session_state.chat_history.append({"role": "ai", "content": animated_response}) #use the animated response

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.session_state.chat_history.append({"role": "ai", "content": f"An error occurred: {e}"})

if st.session_state.chat_history:
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()