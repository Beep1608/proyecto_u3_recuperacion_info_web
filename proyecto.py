from google import genai
import google.generativeai as genai2
import glob
import pandas as pd
import numpy as np
from files import get_all_pages_content  


API_KEY = "AIzaSyDJChiN_dmmtpfKQkSwi6NQQ21mwshJPD4"
genai2.configure(api_key=API_KEY)

model = 'models/embedding-001'

def embed_fn(title, text):
  return genai2.embed_content(model=model,
                             content=text,
                             task_type="retrieval_document",
                             title=title)['embedding']

if __name__ == "__main__":

    pdf_files = glob.glob("*.pdf")
    
    if pdf_files:
        pdf_path = pdf_files[0]
        print(f"Processing PDF: {pdf_path}")
        

        all_pages_content = get_all_pages_content(pdf_path)
        
        if all_pages_content:
            print(f"Successfully retrieved content from {len(all_pages_content)} pages")
 
            first_page = list(all_pages_content.keys())[0]
            print(f"First page content sample: {all_pages_content[first_page][:100]}...")
            
            # Create embeddings for all pages
            print("Creating embeddings for all pages...")
            embeddings = {}
            
            # Create DataFrame for page contents
            df_pages = pd.DataFrame(columns=['Page', 'Title', 'Text'])
            for page_num, content in all_pages_content.items():
                if content.strip():  # Skip empty pages
                    # Add to DataFrame
                    df_pages = df_pages._append({
                        'Page': page_num,
                        'Title': f"page_{page_num}",
                        'Text': content
                    }, ignore_index=True)
                    
                    # Existing dictionary approach
                    try:
                        page_title = f"page_{page_num}"
                        result = embed_fn(page_title, content)
                        embeddings[page_num] = result
                        print(f"Created embedding for page {page_num} - Vector dimension: {len(result)}")
                    except Exception as e:
                        print(f"Error creating embedding for page {page_num}: {e}")
            
            # Apply embeddings to DataFrame
            print("Adding embeddings to DataFrame...")
            df_pages['Embeddings'] = df_pages.apply(lambda row: embed_fn(row['Title'], row['Text']), axis=1)
            print(f"DataFrame with embeddings created. Shape: {df_pages.shape}")
            
            print(f"Successfully created embeddings for {len(embeddings)} pages")
            
            # Example of how to use the first embedding
            if embeddings:
                first_page_num = list(embeddings.keys())[0]
                print(f"First page embedding : {embeddings[first_page_num]}...")
                
            # Start query interaction with user
            while True:
                user_input = input("\nDo you want to make a query? (yes/no): ").strip().lower()
                if user_input != 'yes':
                    break
                query_text = input("Enter your query: ")
                best_passage = find_best_passage(query_text, df_pages)
                print("\nBest matching passage:")
                print("-" * 80)
                print(best_passage)
                print("-" * 80)
    else:
        print("No PDF files found in current directory")


def query(query_text, dataframe):
    """
    Process a query and return the best matching passage.
    """
    return find_best_passage(query_text, dataframe)
    

def find_best_passage(query, dataframe):
    """
    Compute the distances between the query and each document in the dataframe
    using the dot product.
    """
    query_embedding = genai2.embed_content(model=model,
                                        content=query,
                                        task_type="retrieval_query")['embedding']
    dot_products = np.dot(np.stack(dataframe['Embeddings'].tolist()), query_embedding)
    idx = np.argmax(dot_products)
    return dataframe.iloc[idx]['Text'] # Return text from index with max value