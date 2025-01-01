# Plagiarism Checker System

A web-based plagiarism checker that allows users to compare input text with multiple uploaded documents. The system calculates cosine similarity between the query and documents, highlights matching words, generates detailed reports, and visualizes results with bar charts.

---

## Features

- **Text Preprocessing**: Converts input text to lowercase, removes special characters, and tokenizes for accurate comparison.
- **Cosine Similarity Calculation**: Measures similarity between the input query and each document.
- **Highlight Matching Words**: Identifies and highlights common words between the input query and documents.
- **Document Upload**: Allows users to upload `.txt` files for comparison.
- **Delete Documents**: Users can delete all uploaded documents at once.
- **Similarity Bar Chart**: Visualizes document similarity percentages in a horizontal bar chart.
- **Save Queries**: Automatically saves user queries with timestamps for reference.
- **Dynamic Threshold**: Allows users to set a similarity threshold to filter results.

---

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript (Bootstrap for styling)
- **Visualization**: Matplotlib for similarity charts
- **Storage**: File system for documents and queries

---

## Setup Instructions

### Prerequisites

1. Python 3.7+
2. pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/plagiarism-checker.git
   cd plagiarism-checker
    ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
    ```
3. Run the application:
   ```bash
   Run the application:
   ```

## Usage

1. **Open the application** in your browser.
2. **Upload `.txt` files** for comparison.
3. **Enter the input text** in the query box.
4. **Set a similarity threshold** (optional).
5. Click **"Check Plagiarism"** to view results:
   - Best matching document
   - Documents exceeding the threshold
   - Matching words
   - Detailed similarity report
   - Similarity bar chart
6. Use the **"Upload Document"** feature to add files or **"Delete All Documents"** to clear the comparison pool.

---


# Future Enhancements

- Add support for other document formats (e.g., PDF, DOCX).
- Implement user authentication for personalized document storage.
- Add export functionality for reports in CSV or PDF format.

---


