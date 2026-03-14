import os  # Used for file system operations, like walking through folders.
import chromadb
from chromadb.utils import embedding_functions

# It reads all Python files in a repo → converts them to embeddings → stores them in a vector database.

"""
Vector DB purpose:

text/code → embedding vector → stored

Later you can query:

error message → embedding → similar code files
"""

# This creates a connection to the Chroma database.
# By default it runs in-memory locally unless configured for persistence.
client = chromadb.Client()

# This code initializes an embedding function using the all-MiniLM-L6-v2 sentence-transformer model from Hugging Face.
# This class from chromadb.utils acts as a wrapper around the sentence-transformers library to make it compatible with ChromaDB, enabling automatic vectorization of text data.
#: The resulting variable holds the function object that can be passed to a ChromaDB collection to generate embeddings for input documents
# chromadb provides some ready-made embedding functions
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# A collection is like a table in a database.
# You attach the embedding function to the collection, so Chroma automatically:
# document → embedding → store
collection = client.get_or_create_collection(
    name="repo_code", embedding_function=embedding_function
)


# The Indexing Logic
# The function index_repository(repo_path) handles the heavy lifting of data ingestion
def index_repository(repo_path):

    # Prepare Storage Lists
    documents = []  # Stores file content.
    ids = []  # Stores unique identifiers for documents.

    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    code = f.read()
                documents.append(code)
                ids.append(file_path)

    # Add to Collection
    collection.add(documents=documents, ids=ids)


"""
os.walk() recursively scans directories.
The os.walk() method yields a 3-tuple for each directory in the tree: 
root: A string representing the path to the current directory.
dirs: A list of the names of the subdirectories in the current root.
files: A list of the names of the non-directory files in the current root. 

Example repo:

repo/
 ├ service/
 │   └ auth.py
 ├ models/
 │   └ user.py

Iteration output:

root = repo/service
files = ["auth.py"]

root = repo/models
files = ["user.py"]
----------------------------

Filter Python Files - Only Python files are indexed.
 if file.endswith(".py"):

Build File Path - os.path.join(root, file)
repo/service/auth.py

----------------------------

Read File Content
with open(file_path, "r") as f:
    code = f.read()

 Example stored text:
def login(user, password):
    if authenticate(user,password):
        return token

This reads the entire code file as text.

with statement: This acts as a context manager
 that ensures the file is automatically closed, 
 even if errors occur within the associated code block. 
 This prevents resource leaks and makes the code cleaner than explicitly using f.close().

 open(file_path, "r")
open() is a built-in function in Python used for file handling

file_path is a variable 


"r" specifies the file mode,
 which in this case is "read mode" (the default mode). 
 This allows you to read the contents of the file but not write to it. 
 If the file does not exist, a FileNotFoundError will be raised.

 as f: This assigns the opened file object to the variable f 
 f (or any other variable name you choose). You then use this variable to perform operations on the file 
 for example, reading its contents with f.read().
----------------------------
"""


"""
This stores:

vector embedding
file content
file path

The id is the primary identifier of the vector record.
Think of it like a primary key in SQL.

id → /repo/service/auth.py. 
 uniquely identifies the document.

Without ids, the vector DB would not know how to reference the stored document.


Q. How Retrieval Usually Works (Vector Search)

Normally you do NOT search by id.
You search by semantic similarity.

results = collection.query(
    query_texts=["authentication failure"],
    n_results=3
)

Chroma does:

query text
   ↓
embedding
   ↓
vector similarity search
   ↓
return closest documents


Example result:

documents:
  - "def login(user): ..."
  - "def validate_token(): ..."

ids:
  - "/repo/service/auth.py"
  - "/repo/service/token.py"

Here the ids help you know which files those documents came from.
"""


def search_code(query, top_k=3):

    results = collection.query(
        query_texts=[query], n_results=top_k  # like LIMIT in SQL
    )

    """
    why we need below code, we can directly return right?
    The problem is that search_code() 
    returns the raw ChromaDB query result (which contains metadata), 
    not the actual file contents with file paths

    Now let's improve the prompt in the code_writer agent to ensure the LLM provides the actual file path from the context:
    
    key Fixes Applied
Vector Store (vector_store.py:175-191)
Now returns formatted results with file paths: "File: /path/to/file.py\n\ncode..."
LLM can now see actual file paths to use in the response
Code Writer Prompt (code_writer.py:43-68)
Fixed f-string formatting by escaping curly braces {{ and }} in prompt -> code_context
Added explicit instructions to extract EXACT file path from code context
Emphasized JSON-only output
File Editor (file_editor.py:4-25)
Handles both absolute and relative file paths
Converts absolute paths to relative paths automatically
Creates missing directories before writing files
JSON Extraction (code_writer.py:7-14)
Uses regex fallback to extract JSON from LLM responses
Catches specific json.JSONDecodeError instead of bare except
    """

    # Format results properly with file paths and code
    formatted_results = []

    if results and "documents" in results and results["documents"]:
        documents = results["documents"][0]  # First query result
        ids = results["ids"][0]  # File paths

        for file_path, code in zip(ids, documents):
            formatted_results.append(f"File: {file_path}\n\n{code}")

    return formatted_results


""" Example
[
 "File: /repo/service/auth.py\n\ndef login()...",
 "File: /repo/models/user.py\n\nclass User..."
]
"""
