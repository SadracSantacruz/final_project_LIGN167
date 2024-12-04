import os
import openai
from sk import my_sk
from colbert import ColBERT
os.environ["TOKENIZERS_PARALLELISM"] = "false"

openai.api_key = my_sk
# Path to folder containing .txt files
DOCUMENTS_FOLDER = "./DSC20 Assignments"
#QUERY = "Give me one really creative question for a final exam about recursion"

# Load documents from .txt files
def load_documents(folder_path):
    documents = []
    file_paths = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                documents.append(file.read())
                file_paths.append(file_path)
    return documents, file_paths

def generate_question(top_k_documents, model= "gpt-4o-mini"):
    top_docs = [doc for doc, _ in top_k_documents]
    context = "\n".join(top_docs)
    prompt = f"{QUERY}:\n\n{context}"

    response = openai.chat.completions.create(
        model= model,
        messages= [
            {
                "role": "system", 
                "content": "You are a Computer Science and Data Science Professor"
            },
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    QUERY = input("Enter your query: ")
    ColBERT = ColBERT()
    docs, _ = load_documents(DOCUMENTS_FOLDER)
    ranked_docs = ColBERT.rank_documents(QUERY, docs)
    question = generate_question(ranked_docs)
    print(question)
