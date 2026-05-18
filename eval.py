import os
import concurrent.futures
from collections import Counter
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
MODEL_ID = 'gemini-3.1-flash-lite'

def generate_reformulation(prompt_type, original_query):
    prompts = {
        "synonyms": f"Rewrite the following academic search query by using alternative academic synonyms and related terminology. Query: '{original_query}'. Return ONLY the new query string.",
        
        "hyde": f"Write a brief, ideal academic abstract (max 150 words) for a hypothetical paper that perfectly answers the following query: '{original_query}'.",
        
        "specific": f"Rewrite the following search query to focus strictly on the technical implementation, architecture, and granular methodology. Query: '{original_query}'. Return ONLY the new query string.",
        
        "broad": f"Rewrite the following search query to target broad review papers, literature surveys, and state-of-the-art summaries. Query: '{original_query}'. Return ONLY the new query string."
    }
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompts[prompt_type]
    )
    return response.text.strip()

def mock_search(query_string):
    print(f"Searching for: {query_string}")
    base_id = len(query_string) % 10
    return [f"paper_{base_id}", f"paper_{base_id + 1}", f"paper_{base_id + 2}", "paper_universal_1", "paper_universal_2"]

def pipeline_search(original_query):
    print(f"Initiating pipeline for query: '{original_query}'\n")
    reformulation_types = ["synonyms", "hyde", "specific", "broad"]
    queries = [original_query] 
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_type = {
            executor.submit(generate_reformulation, r_type, original_query): r_type 
            for r_type in reformulation_types
        }
        for future in concurrent.futures.as_completed(future_to_type):
            try:
                result = future.result()
                queries.append(result)
            except Exception as e:
                print(f"Error generating reformulation: {e}")
    print("\nAll Queries Generated:")
    all_retrieved_results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        search_futures = [executor.submit(mock_search, q) for q in queries]
        for future in concurrent.futures.as_completed(search_futures):
            all_retrieved_results.extend(future.result())
    paper_scores = Counter(all_retrieved_results)
    print("\nFinal Ranked Results:")
    ranked_papers = paper_scores.most_common()
    for rank, (paper_id, score) in enumerate(ranked_papers, 1):
        print(f"{rank}. {paper_id} (Found in {score}/5 searches)")
    return ranked_papers

if __name__ == "__main__":
    test = "long term memory in LLM agents"
    pipeline_search(test)