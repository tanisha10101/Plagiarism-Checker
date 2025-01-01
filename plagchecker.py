from flask import Flask, request, render_template, jsonify
import re
import math
import os
import shutil
import time
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

def preprocess_text(text):
    """Converts text to lowercase, removes special characters, and tokenizes."""
    return re.sub(r"[^\w\s]", "", text.lower()).split()

def calculate_cosine_similarity(query, document):
    """Calculates the cosine similarity between two sets of words."""
    query_words = preprocess_text(query)
    document_words = preprocess_text(document)
    unique_words = set(query_words).union(set(document_words))

    query_vector = [query_words.count(word) for word in unique_words]
    document_vector = [document_words.count(word) for word in unique_words]

    dot_product = sum(q * d for q, d in zip(query_vector, document_vector))
    query_magnitude = math.sqrt(sum(q ** 2 for q in query_vector))
    document_magnitude = math.sqrt(sum(d ** 2 for d in document_vector))

    if query_magnitude == 0 or document_magnitude == 0:
        return 0  

    return (dot_product / (query_magnitude * document_magnitude)) * 100

# Additional Features
def highlight_similarities(query, document):
    """Highlights similar words between query and document."""
    query_words = set(preprocess_text(query))
    document_words = set(preprocess_text(document))
    common_words = query_words.intersection(document_words)
    return common_words

def save_query_to_file(query):
    """Saves the user query to a timestamped file."""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"queries/query_{timestamp}.txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as file:
        file.write(query)

def generate_similarity_chart(results):
    """Generates a bar chart for similarity results."""
    fig, ax = plt.subplots()
    documents = list(results.keys())
    similarities = list(results.values())

    ax.barh(documents, similarities, color="skyblue")
    ax.set_xlabel("Similarity (%)")
    ax.set_title("Similarity Analysis")

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    chart_data = base64.b64encode(buf.getvalue()).decode("utf-8")
    buf.close()
    return chart_data

@app.route("/upload", methods=["POST"])
def upload_document():
    """Allows users to upload a document for plagiarism checking."""
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file part in the request."}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected."}), 400

        if not file.filename.endswith(".txt"):
            return jsonify({"error": "Only .txt files are allowed."}), 400

        upload_folder = "documents"
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)
        return jsonify({"success": "File uploaded successfully.", "filename": file.filename}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/delete", methods=["POST"])
def delete_documents():
    """Allows users to delete all uploaded documents."""
    try:
        shutil.rmtree("documents")
        os.makedirs("documents", exist_ok=True)
        return jsonify({"success": "All documents have been deleted."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    """Renders the home page."""
    return render_template("index.html", query="", output="", report="", details="", chart_data="")

@app.route("/", methods=["POST"])
def plagiarism_checker():
    """Handles plagiarism check requests."""
    try:
        query_text = request.form["query"]
        threshold = float(request.form.get("threshold", 50))  # Default threshold is 50%
        documents = [f for f in os.listdir("documents") if f.endswith(".txt")]

        if not query_text.strip():
            raise ValueError("Input text cannot be empty.")

        if not documents:
            return render_template("index.html", query=query_text, output="No documents found for comparison.", report="", details="", chart_data="")

        save_query_to_file(query_text)

        results = {}
        highlighted_matches = {}
        for document_name in documents:
            with open(os.path.join("documents", document_name), "r") as file:
                document_text = file.read()
            similarity = calculate_cosine_similarity(query_text, document_text)
            results[document_name] = similarity
            highlighted_matches[document_name] = highlight_similarities(query_text, document_text)

      
        chart_data = generate_similarity_chart(results)

     
        best_match = max(results, key=results.get)
        best_match_percentage = results[best_match]
        matches_above_threshold = {doc: sim for doc, sim in results.items() if sim >= threshold}

       
        details = "\n".join(
            [f"{doc}: {sim:.2f}%" for doc, sim in results.items()]
        )
        highlighted_text = "\n".join(
            [f"{doc}: {', '.join(words)}" for doc, words in highlighted_matches.items()]
        )
        output_message = (
            f"Best match is '{best_match}' with a similarity of {best_match_percentage:.2f}%.<br>"
            f"{len(matches_above_threshold)} document(s) exceeded the threshold of {threshold}%."
        )

        return render_template(
            "index.html", 
            query=query_text, 
            output=output_message, 
            report=details, 
            details=highlighted_text, 
            chart_data=chart_data
        )

    except Exception as e:
        return render_template(
            "index.html", query=request.form["query"], output="Error: " + str(e), report="", details="", chart_data=""
        )

if __name__ == "__main__":
   
    os.makedirs("documents", exist_ok=True)
    os.makedirs("queries", exist_ok=True)
    app.run(debug=True)

