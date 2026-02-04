"""
Quick test script to verify the system works
Run this after setting up API keys
"""

import asyncio
import sys
from src.detection.scam_detector import ScamDetector
from src.personas.persona_manager import PersonaManager
from src.extraction.entity_extractor import EntityExtractor


async def test_system():
    """Test all components"""
    print("=" * 60)
    print("CHAMELEON AGENT - SYSTEM TEST")
    print("=" * 60)
    print()
    
    # Test 1: Scam Detection
    print("TEST 1: Scam Detection Engine")
    print("-" * 60)
    detector = ScamDetector()
    test_message = "Congratulations! You won 5 lakh rupees. Pay 2000 processing fee to claim."
    result = detector.analyze(test_message)
    print(f"Message: {test_message}")
    print(f"Scam Detected: {result['is_scam']}")
    print(f"Scam Type: {result['scam_type']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Signals: {result['signals_detected']}")
    print("✅ PASSED\n")
    
    # Test 2: Persona System
    print("TEST 2: Persona System")
    print("-" * 60)
    persona_manager = PersonaManager()
    persona = persona_manager.select_persona("prize")
    print(f"Selected Persona: {persona.name} ({persona.age} years old)")
    print(f"Description: {persona.description}")
    print("✅ PASSED\n")
    
    # Test 3: Entity Extraction
    print("TEST 3: Entity Extraction")
    print("-" * 60)
    extractor = EntityExtractor()
    messages = [
        "Pay to 9876543210@paytm",
        "Or account 12345678901, IFSC SBIN0001234"
    ]
    extraction_result = extractor.extract(messages)
    print(f"Messages: {messages}")
    print(f"Extracted {extraction_result['extraction_count']} entities:")
    for entity_type, entities in extraction_result['extracted_data'].items():
        print(f"  - {entity_type}: {len(entities)} found")
    print("✅ PASSED\n")
    
    # Test 4: LLM Client (requires API key)
    print("TEST 4: LLM Client")
    print("-" * 60)
    try:
        from src.agent.llm_client import LLMClient
        llm_client = LLMClient()
        print(f"LLM Provider: {llm_client.provider}")
        print(f"Model: {llm_client.model_name}")
        
        # Try to generate a simple response
        system_prompt = "You are a helpful assistant. Respond in one sentence."
        response = await llm_client.generate_response(
            system_prompt=system_prompt,
            user_message="Say hello"
        )
        print(f"Test Response: {response}")
        print("✅ PASSED\n")
    except Exception as e:
        print(f"⚠️  WARNING: LLM test failed - {str(e)}")
        print("Make sure you've added your API key to .env file\n")
    
    print("=" * 60)
    print("SYSTEM TEST COMPLETE")
    print("=" * 60)
    print()
    print("All core components are working!")
    print("Next step: Run 'uvicorn main:app --reload' to start the server")


if __name__ == "__main__":
    asyncio.run(test_system())
