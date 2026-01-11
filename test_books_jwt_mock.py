#!/usr/bin/env python
"""
Test books with JWT decode mocked
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from jose import jwt
from app.main import app
from app.database import get_db

def test_books_with_jwt_mock():
    """Mock JWT decode directly"""
    
    print("🔐 Testing Books with JWT Mock")
    
    # Mock database
    mock_db_session = AsyncMock()
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    
    class MockBook:
        def __init__(self):
            self.id = 1
            self.title = "Test Book"
            self.author = "Test Author"
    
    mock_book = MockBook()
    mock_scalars.all.return_value = [mock_book]
    mock_result.scalars.return_value = mock_scalars
    mock_result.scalar_one_or_none.return_value = mock_book
    mock_db_session.execute.return_value = mock_result
    mock_db_session.commit = AsyncMock()
    mock_db_session.refresh = AsyncMock()
    
    def override_get_db():
        yield mock_db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Mock JWT decode in the jose module
    with patch('jose.jwt.decode') as mock_decode:
        # Make decode return a valid payload
        mock_decode.return_value = {"sub": "testuser", "roles": ["user"]}
        
        # Mock external services
        with patch('app.main.rag_pipeline') as mock_rag:
            mock_rag.index_book = AsyncMock()
            
            with patch('app.main.generate_summary_llama3', AsyncMock(return_value="Summary")):
                with TestClient(app) as client:
                    
                    print("\n1. Testing authenticated PUT")
                    response = client.put(
                        "/books/1",
                        json={"title": "Updated"},
                        headers={"Authorization": "Bearer valid_token"}
                    )
                    print(f"   Status: {response.status_code}")
                    assert response.status_code == 200
                    
                    print("\n2. Testing authenticated DELETE")
                    response = client.delete(
                        "/books/1",
                        headers={"Authorization": "Bearer valid_token"}
                    )
                    print(f"   Status: {response.status_code}")
                    assert response.status_code == 204
                    
                    print("\n3. Testing authenticated summary")
                    response = client.post(
                        "/books/1/generate-summary",
                        headers={"Authorization": "Bearer valid_token"}
                    )
                    print(f"   Status: {response.status_code}")
                    assert response.status_code == 200
    
    app.dependency_overrides.clear()
    print("\n✅ All JWT mock tests passed!")

if __name__ == "__main__":
    test_books_with_jwt_mock()