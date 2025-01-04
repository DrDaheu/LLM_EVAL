# Import necessary frameworks/packages
import streamlit as st
from groq import Groq
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = "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"

# Streamlit title and UI header
st.title("LLM Evaluation Test")
st.divider()

# Function to test answer relevancy
def test_answer_relevancy(user_input, model_output):
    """
    Tests the relevancy of the model's output to the user's input.
    Returns the score, threshold, and result status.
    """
    try:
        answer_relevancy_metric = AnswerRelevancyMetric(threshold=0.5)  # Adjust threshold as needed
        test_case = LLMTestCase(
            input=user_input,
            actual_output=model_output,
        )
        result = assert_test(test_case, [answer_relevancy_metric])
        return result, answer_relevancy_metric.score
    except AssertionError as e:
        return str(e), None

# Set up GROQ API client
userdata = {"GROQ_API_KEY": "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"}
client = Groq(api_key=userdata.get("GROQ_API_KEY"))

# User input
context = st.text_input("What do you want to learn today?")
if not context:
    st.stop()

# System prompt
system_prompt = (
    "You'll be tasked to undergo a performance test. Try to devise the most accurate and "
    "correct answers after receiving each question."
)

# Function to fetch response from GROQ models
def model_response(content, text, model, col):
    """
    Fetches response from a specified GROQ model and displays it in a Streamlit column.
    """
    try:
        chat_completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": text},
                {"role": "user", "content": content},
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
        )
        
        response = chat_completion.choices[0].message.content
        with col:
            st.subheader(model)
            st.markdown(response)
        
        return response
    except Exception as e:
        with col:
            st.subheader(model)
            st.error(f"Error: {str(e)}")
        return ""

# Streamlit layout
col1, col2, col3 = st.columns(3, gap="medium")

# Fetch and display model responses
response1 = model_response(context, system_prompt, "mixtral-8x7b-32768", col1)
response2 = model_response(context, system_prompt, "gemma2-9b-it", col2)
response3 = model_response(context, system_prompt, "llama-3.3-70b-versatile", col3)

# Visualize response time of each LLM
st.divider()
st.subheader("Response Time Visualization")
# Simulated response time chart (placeholder, replace with real data if available)
st.line_chart({"mixtral": [0.2, 0.4, 0.6], "gemma2": [0.3, 0.5, 0.7], "llama": [0.4, 0.6, 0.8]})

# Performance metrics
st.divider()
st.subheader("Performance Metrics")
if response1:
    result1, score1 = test_answer_relevancy(context, response1)
    st.write(f"Mixtral Test Result: {result1}, Score: {score1}")
if response2:
    result2, score2 = test_answer_relevancy(context, response2)
    st.write(f"Gemma Test Result: {result2}, Score: {score2}")
if response3:
    result3, score3 = test_answer_relevancy(context, response3)
    st.write(f"Llama Test Result: {result3}, Score: {score3}")

# Accuracy metrics placeholder
st.divider()
st.subheader("Accuracy Metrics")
st.write("Further analysis can be implemented here based on specific requirements.")
