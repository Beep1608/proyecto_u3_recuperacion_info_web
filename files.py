import PyPDF2  # You'll need to install this: pip install PyPDF2
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK resources if not already present
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.download('punkt_tab')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    

def _clean_text(text):
    """
    Clean extracted text by removing binary content and other unwanted elements.
    
    Args:
        text (str): The extracted text from a PDF page
        
    Returns:
        str: Cleaned text with binary elements removed
    """
    if not text:
        return ""
    
    # Remove control characters and non-printable characters
    # Keep only printable ASCII and common Unicode characters
    cleaned = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]', '', text)
    
    # Remove binary data markers or patterns often found in PDFs
    cleaned = re.sub(r'(<<|>>|\(binary data\)|obj|endobj|stream|endstream)', '', cleaned)
    
    return cleaned

def _preprocess_text(text):
    """
    Preprocess text by converting to lowercase without removing stopwords.
    
    Args:
        text (str): The text to preprocess
        
    Returns:
        str: Preprocessed text
    """
    # Convert to lowercase
    text = text.lower()
    
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Join tokens back into text (keeping all words including stopwords)
    processed_text = ' '.join(tokens)
    
    return processed_text

def get_all_pages_content(pdf_path, skip_pages=0):
    """
    Extract and return the content of all pages in the PDF.
    
    Args:
        pdf_path (str): Path to the PDF file
        skip_pages (int): Number of initial pages to skip (default: 0)
        
    Returns:
        dict: Dictionary with page numbers as keys and content as values
    """
    pages_content = {}
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            
            if total_pages <= skip_pages:
                print(f"The PDF has only {total_pages} pages, but you're trying to skip {skip_pages} pages.")
                return {}
                
            # Process pages starting from skip_pages
            for i in range(skip_pages, total_pages):
                page = pdf_reader.pages[i]
                try:
                    # Extract text from the page
                    raw_text = page.extract_text()
                    
                    # Clean the text to remove binary elements
                    cleaned_text = _clean_text(raw_text)
                    
                    # Skip pages that only contain binary data
                    if not cleaned_text.strip():
                        print(f"Page {i+1} appears to contain only binary data - skipping")
                        continue
                    
                    # Preprocess the text (lowercase and keep stopwords)
                    processed_text = _preprocess_text(cleaned_text)
                    
                    # Store the processed page content
                    page_num = i + 1
                    pages_content[page_num] = processed_text
                    
                except Exception as page_error:
                    print(f"Error processing page {i+1}: {page_error}")
                    continue
                    
            print(f"Successfully extracted and preprocessed text content from {len(pages_content)} pages")
            return pages_content
    
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return {}


def preprocess_text(text):
    """
    Preprocess text by converting to lowercase and removing stopwords.
    
    Args:
        text (str): The text to preprocess
        
    Returns:
        str: Preprocessed text
    """
    # Convert to lowercase
    text = text.lower()
    
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    
    # Join tokens back into text
    processed_text = ' '.join(filtered_tokens)
    
    return processed_text