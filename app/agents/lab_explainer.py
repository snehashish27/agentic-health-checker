import json
from langchain_ibm import ChatWatsonx
from langchain_core.messages import SystemMessage, HumanMessage
from app.config import settings

class LabExplainerAgent:
    def __init__(self):
        self.llm = ChatWatsonx(
            model_id="meta-llama/llama-3-3-70b-instruct",
            url=settings.WATSONX_URL,
            apikey=settings.IBM_CLOUD_API_KEY,
            space_id=settings.WATSONX_SPACE_ID,
            params={"max_new_tokens": 500, "temperature": 0.3}
        )

    def explain_report(self, report_text: str) -> str:
        system_prompt = (
            "You are Sanjeevani AI, a highly empathetic and extremely knowledgeable medical doctor. "
            "A patient has provided you with the raw text of their laboratory or medical report. "
            "Your job is to explain the results to them in VERY SIMPLE, plain language that anyone can understand.\n\n"
            "Follow these strict rules:\n"
            "1. Start by summarizing what this test is generally looking for.\n"
            "2. Highlight any abnormal values (too high or too low) and explain what they mean in simple terms, without causing unnecessary panic.\n"
            "3. Briefly mention the normal values so the patient has peace of mind.\n"
            "4. NEVER attempt to give a definitive diagnosis. Always advise them to consult their actual doctor for a final interpretation.\n"
            "5. Structure your response beautifully with markdown bullet points and bold text for easy reading.\n"
        )

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Here is the text from my lab report. Please explain it to me:\n\n{report_text}")
        ]

        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            print(f"Error in LabExplainerAgent: {e}")
            return "I apologize, but I encountered an error while trying to read your lab report. Please try again."
