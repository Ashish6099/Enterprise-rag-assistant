# Import PyPDFLoader to read and extract text from PDF files
from langchain_community.document_loaders import PyPDFLoader

# Import a text splitter that intelligently breaks large text into smaller chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_and_chunk_pdf(pdf_path):
    """
    Loads a PDF file and splits its content into smaller overlapping chunks.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        list: A list of Document objects, where each Document contains
              a chunk of the original PDF text along with metadata.
    """

    # Create a PDF loader object for the given file path.
    # PyPDFLoader extracts text page by page from the PDF.
    loader = PyPDFLoader(pdf_path)

    # Load the PDF content.
    # This returns a list of Document objects, typically one Document per page.
    #
    # Example:
    # documents = [
    #     Document(page_content="Page 1 text...", metadata={"page": 0}),
    #     Document(page_content="Page 2 text...", metadata={"page": 1}),
    # ]
    documents = loader.load()
    for doc in documents:
        doc.page_content = doc.page_content.encode(
        "utf-8",
        errors="ignore"
        ).decode("utf-8")
    # Create a text splitter.
    #
    # chunk_size=1000:
    #   Maximum number of characters allowed in each chunk.
    #
    # chunk_overlap=200:
    #   Consecutive chunks share 200 characters.
    #   This helps preserve context between chunks when using
    #   embeddings, retrieval, or LLM-based question answering.
    #
    # RecursiveCharacterTextSplitter tries to split text at natural
    # boundaries (paragraphs, newlines, sentences, spaces) before
    # falling back to character-level splitting.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    # Split all loaded documents into smaller chunks.
    #
    # Example:
    # Original text:
    #   "This is a very long document..."
    #
    # Result:
    #   Chunk 1: characters 0-1000
    #   Chunk 2: characters 800-1800
    #   Chunk 3: characters 1600-2600
    #
    # Each chunk remains a Document object and retains metadata
    # such as page number.
    chunks = splitter.split_documents(documents)

    # Return the final list of chunked Document objects.
    return chunks