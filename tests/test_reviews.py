import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from app.models import Review

class TestReviews:
    def test_add_review(self, client: TestClient, sample_book):
        """Test adding a review to a book"""
        with patch('app.main.rag_pipeline.index_book', new_callable=AsyncMock) as mock_index:
            response = client.post(f"/books/{sample_book.id}/reviews", json={
                "user_id": 1,
                "review_text": "Great book!",
                "rating": 4.5
            })
            
            print(f"Add review response: {response.status_code}")
            print(f"Response body: {response.json()}")
            
            assert response.status_code == 201
            assert response.json()["review_text"] == "Great book!"
            assert response.json()["rating"] == 4.5

    def test_add_review_book_not_found(self, client: TestClient):
        """Test adding review to non-existent book"""
        response = client.post("/books/999/reviews", json={
            "user_id": 1,
            "review_text": "Great book!",
            "rating": 4.5
        })
        
        print(f"Add review to non-existent book response: {response.status_code}")
        
        assert response.status_code == 404
        assert "Book not found" in response.json()["detail"]

    def test_get_reviews(self, client: TestClient, sample_book, mock_db):
        """Test getting reviews for a book"""
        # Add a test review to mock data
        test_review = Review(
            id=1,
            book_id=sample_book.id,
            user_id=1,
            review_text="Great book!",
            rating=4.5
        )
        mock_db.data['reviews'] = [test_review]
        
        response = client.get(f"/books/{sample_book.id}/reviews")
        
        print(f"Get reviews response: {response.status_code}")
        print(f"Response body: {response.json()}")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) >= 1
        assert response.json()[0]["review_text"] == "Great book!"

    def test_get_reviews_book_not_found(self, client: TestClient):
        """Test getting reviews for non-existent book"""
        response = client.get("/books/999/reviews")
        
        print(f"Get reviews for non-existent book response: {response.status_code}")
        
        assert response.status_code == 404
        assert "Book not found" in response.json()["detail"]

    def test_book_summary(self, client: TestClient, sample_book, mock_db):
        """Test getting book summary"""
        # Add a test review
        test_review = Review(
            id=1,
            book_id=sample_book.id,
            user_id=1,
            review_text="Great book!",
            rating=4.5
        )
        mock_db.data['reviews'] = [test_review]
        
        response = client.get(f"/books/{sample_book.id}/summary")
        
        print(f"Book summary response: {response.status_code}")
        print(f"Response body: {response.json()}")
        
        assert response.status_code == 200
        assert "rating" in response.json()
        assert response.json()["rating"] == 4.5

    def test_book_summary_no_reviews(self, client: TestClient, sample_book):
        """Test getting summary for book with no reviews"""
        response = client.get(f"/books/{sample_book.id}/summary")
        
        print(f"Book summary with no reviews response: {response.status_code}")
        print(f"Response body: {response.json()}")
        
        assert response.status_code == 200
        assert response.json()["rating"] == 0
        assert "No reviews" in response.json()["review_summary"]