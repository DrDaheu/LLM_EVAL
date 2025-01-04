# LLM_EVAL


This project evaluates the performance of large language models (LLMs) using the deepeval library to test answer relevancy metrics. It uses Streamlit for a web-based UI and integrates with the GROQ API for generating responses from various LLMs.

Features
User-Friendly Interface: Enter queries via a Streamlit-based UI to test model performance.
LLM Integration: Fetch responses from multiple LLMs via the GROQ API.
Answer Relevancy Test: Evaluate the relevancy of model outputs to user queries using deepeval metrics.
Performance Metrics: Visualize response times and evaluate model accuracy.
Secure Configuration: Leverages .env for managing sensitive API keys.
How It Works
1. Environment Setup
The program uses environment variables to securely store API keys. It loads the keys from a .env file:

python
Copy code
from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
2. User Input
Users can input queries through a text box in the Streamlit UI:

python
Copy code
context = st.text_input("What do you want to learn today?")
if not context:
    st.stop()
3. Model Response Fetching
The program connects to GROQ's API to fetch responses from three LLMs (mixtral, gemma2, and llama):

python
Copy code
def model_response(content, text, model, col):
    try:
        chat_completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": text},
                {"role": "user", "content": content},
            ],
        )
        response = chat_completion.choices[0].message.content
        return response
    except Exception as e:
        return ""
4. Answer Relevancy Evaluation
The deepeval library evaluates the relevancy of model responses using an adjustable threshold:

python
Copy code
def test_answer_relevancy(user_input, model_output):
    try:
        answer_relevancy_metric = AnswerRelevancyMetric(threshold=0.5)
        test_case = LLMTestCase(input=user_input, actual_output=model_output)
        return assert_test(test_case, [answer_relevancy_metric])
    except AssertionError as e:
        return str(e), None
5. Performance Metrics
Performance metrics, such as response times and answer relevancy scores, are displayed in the UI:

Response Time Visualization: Simulated with a placeholder chart:
python
Copy code
st.line_chart({"mixtral": [0.2, 0.4, 0.6], "gemma2": [0.3, 0.5, 0.7], "llama": [0.4, 0.6, 0.8]})
Relevancy Results: Output displayed with scores for each model:
python
Copy code
st.write(f"Mixtral Test Result: {result1}, Score: {score1}")
Setup and Installation
Prerequisites
Python 3.8 or higher
Streamlit, dotenv, deepeval, and GROQ packages installed.
Installation Steps
Clone the repository:

bash
Copy code
git clone https://github.com/your-repo/llm-evaluation.git
cd llm-evaluation
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Create a .env file and add your API keys:

plaintext
Copy code
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
Run the application:

bash
Copy code
streamlit run app.py
Usage
Open the application in your browser (Streamlit provides the local URL).
Enter a query in the text box.
View responses from three LLMs, along with relevancy scores and performance metrics.
Sample Output
Here’s an example of what the app might display:

User Query: "What is AI?"
Model Responses:
Mixtral: "AI is the simulation of human intelligence..." (Score: 0.85)
Gemma2: "Artificial Intelligence refers to..." (Score: 0.90)
Llama: "AI, short for Artificial Intelligence, is..." (Score: 0.75)
Customization
Adjust Thresholds: Modify the threshold parameter in AnswerRelevancyMetric to tweak the evaluation sensitivity.
Add More Models: Extend the model_response function to include additional models.
Integrate Real-Time Data: Replace placeholder charts with actual response-time metrics.
Future Enhancements
Add more detailed evaluation metrics.
Implement multi-language support.
Integrate with other LLM APIs.
