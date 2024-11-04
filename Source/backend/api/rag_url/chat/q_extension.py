from openai import OpenAI
from langchain.prompts import ChatPromptTemplate
from api.rag_url.chat.prompts_collection import get_q_extn_prompt_template
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

MODEL = "gpt-3.5-turbo"
model_name = "text-davinci-002"
openai = OpenAI(api_key=api_key)


def expand_query(original_query):
    PROMPT_TEMPLATE = get_q_extn_prompt_template()
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(original_query=original_query)

    # response = send_request(prompt=prompt)
    # return response

    # completion = openai.Completion.create(
    #     model=model_name,
    #     prompt=prompt,
    #     n=1,
    #     stop=None,
    #     temperature=0.5,
    #     max_tokens=150
    # )
    # generated_text = completion.choices[0].text

    # return generated_text

    response = openai.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content


# # Example usage
# original_query = "좋은 틴트 "
# expanded_queries = expand_query(original_query)

# print("Original query:", original_query)
# print("\nExpanded queries:")
# print(expanded_queries)
