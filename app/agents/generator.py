import json
from langchain_ibm import ChatWatsonx
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.config import settings

class ClinicalGeneratorAgent:
    def __init__(self):
        self.llm = ChatWatsonx(
            model_id="meta-llama/llama-3-3-70b-instruct",
            url=settings.WATSONX_URL,
            apikey=settings.IBM_CLOUD_API_KEY,
            space_id=settings.WATSONX_SPACE_ID,
            params={"max_new_tokens": 300, "temperature": 0.2}
        )

    def generate_response(self, user_complaint: str, retrieved_guidelines: list, history: list = []) -> str:
        # Convert retrieved guidelines into a formatted text block
        guidelines_context = ""
        if not retrieved_guidelines:
            guidelines_context = "No specific guidelines found for these symptoms."
        else:
            for idx, g in enumerate(retrieved_guidelines, 1):
                guidelines_context += f"Guideline {idx}:\n"
                guidelines_context += f"- Condition: {g.get('condition')}\n"
                guidelines_context += f"- Urgency: {g.get('urgency')}\n"
                guidelines_context += f"- Home Care: {g.get('home_care')}\n"
                guidelines_context += f"- Hospital Trigger: {g.get('hospital_trigger')}\n\n"

        system_prompt = (
            "You are Sanjeevani AI, a helpful and precise medical AI assistant. Your role is to provide "
            "recommendations based EXCLUSIVELY on the provided medical guidelines. "
            "Do not invent medical advice. If the guidelines are not sufficient, state that "
            "a doctor should be consulted.\n\n"
            "*** COMMUNICATION STYLE ***\n"
            "- Format the response in a conversational, empathetic tone.\n"
            "- You MUST always end your response by wishing the patient 'Get well soon' (or the equivalent in the language you are speaking).\n"
            "- CRITICAL: You MUST detect the language of the user's input (e.g., Bengali, Tamil, Hindi, Marathi, Telugu, Hinglish, English) and reply entirely in that EXACT SAME language and script. If the user writes in Bengali script, you MUST reply in Bengali script. If they write in Tamil script, reply in Tamil script.\n\n"
            "*** TOOL USAGE - CRITICAL INSTRUCTION ***\n"
            "You have access to a tool called `[TOOL: HOSPITAL_FINDER]`.\n"
            "1. If a patient EXPLICITLY asks for a hospital, you MUST IMMEDIATELY trigger the tool by including EXACTLY THIS STRING: `[TOOL: HOSPITAL_FINDER]` anywhere in your response.\n"
            "2. If a patient has severe/urgent symptoms but hasn't asked for a hospital, you MUST ask them first.\n"
            "   - CRITICAL: When asking for permission, DO NOT output the string `[TOOL: HOSPITAL_FINDER]`. Just ask 'Do you want me to find a hospital?'.\n"
            "   - ONLY output the exact string `[TOOL: HOSPITAL_FINDER]` in your NEXT response AFTER they reply 'Yes'.\n"
            "   - IF they have already said 'No' or declined, DO NOT ask them again. Drop the subject.\n"
            "3. If a patient says 'No' or declines, you MUST NOT output the tool string. Respect their choice.\n"
            "NEVER mention `[TOOL: HOSPITAL_FINDER]` in passing. Uttering the string immediately executes the tool."
        )

        messages = [SystemMessage(content=system_prompt)]
        
        for msg in history:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "user":
                messages.append(HumanMessage(content=content))
            else:
                messages.append(AIMessage(content=content))

        user_prompt = (
            f"Patient Complaint: {user_complaint}\n\n"
            f"Retrieved Medical Guidelines:\n{guidelines_context}\n"
            "Please generate a response for the patient."
        )
        
        messages.append(HumanMessage(content=user_prompt))
        
        print("Executing Generator Agent with LangChain Memory...")
        try:
            response = self.llm.invoke(messages)
            return response.content.strip()
        except Exception as e:
            print(f"Generator Agent Error: {e}")
            return "I'm sorry, I am currently unable to generate a response. Please consult a doctor."
