import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import HTTPException

class TestBooks:
    
    def test_create_book_success(self, client: TestClient, mock_db_session):
        """Test creating a new book"""
        print("\n📚 Test 1: Create Book")
        
        # Mock the Book model to return proper object
        with patch('app.models.Book') as MockBookClass:
            mock_book_instance = MagicMock()
            mock_book_instance.id = 1
            mock_book_instance.title = "New Test Book"
            mock_book_instance.author = "New Test Author"
            mock_book_instance.genre = "Sci-Fi"
            mock_book_instance.year_published = 2024
            mock_book_instance.summary = None
            
            # Make it serializable
            mock_book_instance.dict = MagicMock(return_value={
                'id': 1,
                'title': 'New Test Book',
                'author': 'New Test Author',
                'genre': 'Sci-Fi',
                'year_published': 2024,
                'summary': None
            })
            
            MockBookClass.return_value = mock_book_instance
            
            response = client.post("/books", json={
                "title": "New Test Book",
                "author": "New Test Author",
                "genre": "Sci-Fi",
                "year_published": 2024
            })
            
            print(f"   Status: {response.status_code}")
            print(f"   Response keys: {list(response.json().keys())}")
            
            assert response.status_code == 200
            assert "title" in response.json()

    def test_get_books(self, client: TestClient, setup_book_found):
        """Test getting all books"""
        print("\n📚 Test 2: Get All Books")
        
        response = client.get("/books")
        
        print(f"   Status: {response.status_code}")
        print(f"   Books count: {len(response.json())}")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_book_by_id_found(self, client: TestClient, setup_book_found):
        """Test getting a book by ID (found)"""
        print("\n📚 Test 3: Get Book By ID (Found)")
        
        response = client.get("/books/1")
        
        print(f"   Status: {response.status_code}")
        
        assert response.status_code == 200
        assert "title" in response.json()

    def test_get_book_by_id_not_found(self, client: TestClient, setup_book_not_found):
        """Test getting a book by ID (not found)"""
        print("\n📚 Test 4: Get Book By ID (Not Found)")
        
        response = client.get("/books/999")
        
        print(f"   Status: {response.status_code}")
        
        assert response.status_code == 404

    def test_update_book_success(self, client: TestClient, setup_book_found):
        """Test updating a book with auth"""
        print("\n📚 Test 5: Update Book (Authenticated)")
        
        response = client.put(
            "/books/1",
            json={"title": "Updated Book Title"},
            headers={"Authorization": "Bearer token"}
        )
        
        print(f"   Status: {response.status_code}")
        
        # Should succeed because verify_user is mocked
        assert response.status_code == 200

    def test_update_book_unauthorized(self, client: TestClient, setup_book_found):
        """Test updating without auth"""
        print("\n📚 Test 6: Update Book (Unauthorized)")
        
        # Temporarily patch verify_user to fail
        with patch('app.main.verify_user', side_effect=HTTPException(401, "Unauthorized")):
            response = client.put(
                "/books/1",
                json={"title": "Updated Book"}
            )
            
            print(f"   Status: {response.status_code}")
            
            assert response.status_code == 401

    def test_delete_book_success(self, client: TestClient, setup_book_found):
        """Test deleting a book with auth"""
        print("\n📚 Test 7: Delete Book (Authenticated)")
        
        response = client.delete(
            "/books/1",
            headers={"Authorization": "Bearer token"}
        )
        
        print(f"   Status: {response.status_code}")
        
        assert response.status_code == 204

    def test_delete_book_unauthorized(self, client: TestClient, setup_book_found):
        """Test deleting without auth"""
        print("\n📚 Test 8: Delete Book (Unauthorized)")
        
        # Temporarily patch verify_user to fail
        with patch('app.main.verify_user', side_effect=HTTPException(401, "Unauthorized")):
            response = client.delete("/books/1")
            
            print(f"   Status: {response.status_code}")
            
            assert response.status_code == 401

    def test_generate_summary(self, client: TestClient, setup_book_found):
        """Test generating summary with auth"""
        print("\n📚 Test 9: Generate Summary")
        
        response = client.post(
            "/books/1/generate-summary",
            headers={"Authorization": "Bearer token"}
        )
        
        print(f"   Status: {response.status_code}")
        
        assert response.status_code == 200
        assert "summary" in response.json()

    def test_reindex_book(self, client: TestClient, setup_book_found):
        """Test reindexing a book"""
        print("\n📚 Test 10: Reindex Book")
        
        response = client.post("/books/1/reindex")
        
        print(f"   Status: {response.status_code}")
        
        assert response.status_code == 200