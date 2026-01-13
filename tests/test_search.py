import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock

class TestSearch:
    def test_search_post(self, client: TestClient, sample_book):
        """Test POST search"""
        response = client.post("/search?query=Test&limit=5")
        
        print(f"Search POST response: {response.status_code}")
        print(f"Response body: {response.json()}")
        
        assert response.status_code == 200
        assert response.json()["query"] == "Test"
        assert "results" in response.json()

    def test_search_get(self, client: TestClient, sample_book):
        """Test GET search"""
        response = client.get("/search?query=Test&limit=5")
        
        print(f"Search GET response: {response.status_code}")
        
        assert response.status_code == 200
        assert response.json()["query"] == "Test"

    def test_search_empty_query(self, client: TestClient):
        """Test search with empty query"""
        response = client.get("/search?query=&limit=5")
        
        print(f"Search empty query response: {response.status_code}")
        
        assert response.status_code == 200
        assert response.json()["query"] == ""

    def test_reindex_all(self, client: TestClient, sample_book):
        """Test reindexing all books"""
        with patch('app.main.rag_pipeline.index_book', new_callable=AsyncMock) as mock_index:
            response = client.post("/reindex-all")
            
            print(f"Reindex all response: {response.status_code}")
            
            assert response.status_code == 200
            assert "Reindexed" in response.json()["message"]

    def test_debug_embeddings(self, client: TestClient):
        """Test debug embeddings endpoint"""
        response = client.get("/debug/embeddings")
        
        print(f"Debug embeddings response: {response.status_code}")
        
        assert response.status_code == 200
        assert "total_books_indexed" in response.json()

class TestRecommendations:
    def test_recommendations(self, client: TestClient, sample_book, mock_db):
        """Test book recommendations"""
        response = client.get("/recommendations?genre=Fiction")
        
        print(f"Recommendations response: {response.status_code}")
        
        assert response.status_code == 200
        assert "recommendations" in response.json()

class TestSummaryGeneration:
    def test_generate_summary_from_content(self, client: TestClient):
        """Test generating summary from content"""
        with patch('app.main.generate_summary_llama3', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = "This is a generated summary"
            
            response = client.post("/generate-summary", json={
                "content": "This is a test book content for summary generation."
            })
            
            print(f"Generate summary response: {response.status_code}")
            
            assert response.status_code == 200
            assert response.json()["summary"] == "This is a generated summary"