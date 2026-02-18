import content_generator
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

def test_seo_analysis():
    topic = "SpaceX Starship Launch"
    print(f"Testing SEO analysis for topic: {topic}")
    
    # Check API Key
    if not os.getenv("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY not found.")
        return

    keywords = content_generator.analyze_keywords(topic)
    print(f"Resulting Keywords: {keywords}")
    
    if keywords and "," in keywords:
        print("SUCCESS: Keywords generation looks valid.")
    else:
        print("WARNING: Keywords generation might have failed or returned unexpected format.")

if __name__ == "__main__":
    test_seo_analysis()
