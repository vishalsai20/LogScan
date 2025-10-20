from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

prompt = ChatPromptTemplate.from_template("""
You are a log classification assistant.

Classify the following log message into one of these categories:
1. Workflow Error — only if the workflow failed or an unexpected error occurred.
2. Deprecation Warning — if a deprecated feature or function is used.
3. Unclassified — if it doesn't fit the above.

**Important:** First reason step by step whether it counts as an error or not, then give only the category name as the result
Just give from Workflow Error, Deprecation Warning, Uncalssified.  NO Preamble
                                          
Log message: {log_msg}
""")

# Chain
chain = prompt | model | StrOutputParser()

# def classify_with_llm(log_msg: str):
#     result = chain.invoke({"log_msg": log_msg})
#     return result

def classify_with_llm(log_msg: str):
    result = chain.invoke({"log_msg": log_msg})
    
    # Take only the last non-empty line which the result
    lines = [line.strip() for line in result.splitlines() if line.strip()]

    
    final_line = lines[-1]  # last line
    return final_line



if __name__ == "__main__":
    print(classify_with_llm("The workflow passes due to missing input parameters."))
    print(classify_with_llm("Warning: The function 'predict' is deprecated."))
    print(classify_with_llm("Hello, welcome"))
    print(classify_with_llm("Scheduled job 560 executed successfully."))
