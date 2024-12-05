import os
import openai
from fpdf import FPDF
from colbert import ColBERT
from sk import my_sk

os.environ["TOKENIZERS_PARALLELISM"] = "false"

openai.api_key = my_sk

DOCUMENTS_FOLDER = os.path.join(os.path.dirname(__file__), "DSC20 Assignments")

if not os.path.exists(DOCUMENTS_FOLDER):
    print(f"Error: Path does not exist -> {DOCUMENTS_FOLDER}")
    exit(1)
else:
    print(f"Path exists: {DOCUMENTS_FOLDER}")


TEST_QUERY = "Give me one really creative question for a final exam about recursion"

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

# Generate a creative question using OpenAI
def generate_question(top_k_documents, model="gpt-4", max_docs=5):
    # Limit the number of top-ranked documents
    top_docs = [doc for doc, _ in top_k_documents[:max_docs]]
    context = "\n".join(top_docs)

    # Truncate context to avoid exceeding token limits
    prompt = f"{TEST_QUERY}:\n\n{context[:3000]}"

    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a Computer Science and Data Science Professor."},
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content

# Generate a PDF file from the question
def generate_pdf(question, output_path = "output.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add title
    pdf.set_font("Arial", "B", size=16)
    pdf.cell(0, 10, "Generated Final Exam Question", ln=True, align="C")
    pdf.ln(10)  # Add a line break

    # Add the question content
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, question.encode("latin-1", "replace").decode("latin-1"))

    # Save the PDF
    pdf.output(output_path)
    print(f"PDF generated and saved to {output_path}")

if __name__ == "__main__":
    QUERY = os.getenv("QUERY", "Default query text")
    # QUERY = input("Input your Query: ")
    # Initialize ColBERT
    ColBERT_instance = ColBERT()

    # Load documents and rank them
    docs, _ = load_documents(DOCUMENTS_FOLDER)
    ranked_docs = ColBERT_instance.rank_documents(QUERY, docs)

    # Generate the exam question
    exam_question = generate_question(ranked_docs)

    # Print the question to the console
    print("Generated Exam Question:\n")
    print(exam_question)

    # Generate a PDF file with the question
    generate_pdf(exam_question)
