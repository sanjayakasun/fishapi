#!/usr/bin/env python
"""
Test script to verify the fish classification and chatbot integration
"""
import requests
import json
import os
from PIL import Image
import numpy as np

def test_chatbot_api():
    """Test the chatbot API"""
    print("Testing Chatbot API...")
    
    # Test chat endpoint
    chat_url = "http://localhost:8000/chatbot/api/chat/"
    
    test_messages = [
        "Tell me about Bulath Hapaya",
        "What is the habitat of Lethiththaya?",
        "Tell me about all fish species"
    ]
    
    for message in test_messages:
        try:
            response = requests.post(chat_url, json={
                "message": message,
                "session_id": "test_session"
            })
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Query: {message}")
                print(f"   Response: {data['response'][:100]}...")
                print()
            else:
                print(f"❌ Query: {message} - Status: {response.status_code}")
                print(f"   Error: {response.text}")
                print()
                
        except Exception as e:
            print(f"❌ Query: {message} - Exception: {str(e)}")
            print()

def test_species_api():
    """Test the species API"""
    print("Testing Species API...")
    
    # Test species list
    species_url = "http://localhost:8000/chatbot/api/species/"
    
    try:
        response = requests.get(species_url)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Species list - Found {len(data)} species")
            for species in data[:3]:  # Show first 3
                print(f"   - {species['vernacular_name']} ({species['scientific_name']})")
            print()
        else:
            print(f"❌ Species list - Status: {response.status_code}")
            print()
    except Exception as e:
        print(f"❌ Species list - Exception: {str(e)}")
        print()

def test_classification_api():
    """Test the classification API with a dummy image"""
    print("Testing Classification API...")
    
    # Create a dummy image for testing
    dummy_image = Image.new('RGB', (224, 224), color='red')
    
    # Save to temporary file
    temp_image_path = "temp_test_image.jpg"
    dummy_image.save(temp_image_path)
    
    try:
        with open(temp_image_path, 'rb') as f:
            files = {'image': f}
            response = requests.post("http://localhost:8000/predict/", files=files)
            
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Classification - Prediction: {data['prediction']}")
            print(f"   Confidence: {data['confidence']}")
            if 'fish_info' in data:
                print(f"   Fish Info: {data['fish_info']['name']}")
                print(f"   Description: {data['fish_info']['description'][:100]}...")
            print()
        else:
            print(f"❌ Classification - Status: {response.status_code}")
            print(f"   Error: {response.text}")
            print()
            
    except Exception as e:
        print(f"❌ Classification - Exception: {str(e)}")
        print()
    finally:
        # Clean up
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)

def main():
    print("🐠 Testing Fish API Integration")
    print("=" * 50)
    
    # Wait a moment for server to start
    import time
    time.sleep(2)
    
    test_species_api()
    test_chatbot_api()
    test_classification_api()
    
    print("=" * 50)
    print("✅ Integration test completed!")

if __name__ == "__main__":
    main()
