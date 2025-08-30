#!/usr/bin/env python3
"""
Test script to verify API connections
"""
import os
from dotenv import load_dotenv
from openai import OpenAI
import requests

load_dotenv()

def test_openai():
    """Test OpenAI API connection"""
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), timeout=30.0)
        response = client.embeddings.create(
            input=["test"],
            model="text-embedding-ada-002"
        )
        print("✅ OpenAI API: Connected successfully")
        return True
    except Exception as e:
        print(f"❌ OpenAI API: {e}")
        return False

def test_internet():
    """Test internet connectivity"""
    try:
        response = requests.get("https://api.openai.com", timeout=10)
        print("✅ Internet: Connected")
        return True
    except Exception as e:
        print(f"❌ Internet: {e}")
        return False

def test_env_vars():
    """Test environment variables"""
    required_vars = ["OPENAI_API_KEY", "PINECONE_API_KEY", "COHERE_API_KEY", "MONGODB_URI"]
    missing = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"❌ Missing environment variables: {missing}")
        return False
    else:
        print("✅ All environment variables set")
        return True

if __name__ == "__main__":
    print("Testing API connections...\n")
    
    test_env_vars()
    test_internet()
    test_openai()
    
    print("\nTest complete!")