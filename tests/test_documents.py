import pytest
from fastapi.testclient import TestClient
from io import BytesIO
from unittest.mock import patch, MagicMock
from app.models import Document

class TestDocuments:
    def test_upload_document(self, client: TestClient):
        """Test uploading a document"""
        file_content = b"This is a test document"
        files = {"file": ("test.txt", BytesIO(file_content), "text/plain")}
        
        response = client.post("/documents/upload", files=files)
        
        print(f"Upload document response: {response.status_code}")
        print(f"Response: {response.json()}")
        
        assert response.status_code == 200
        assert "successfully" in response.json()["message"]
        assert "document_id" in response.json()

    def test_list_documents(self, client: TestClient, sample_document):
        """Test listing all documents"""
        response = client.get("/documents/")
        
        print(f"List documents response: {response.status_code}")
        print(f"Response: {response.json()}")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) >= 1
        assert response.json()[0]["filename"] == "test.txt"

    def test_delete_document(self, client: TestClient, auth_headers):
        """Test deleting a document with authentication"""
        # Create a test document
        doc = Document(
            id=2,
            filename="delete_test.txt",
            file_size=50,
            uploaded_by=1,
            status="uploaded"
        )
        
        # Mock verify_user
        with patch('app.routes.documents.verify_user', return_value="admin"):
            # First add to test data
            from app.conftest import TEST_DATA
            TEST_DATA['documents'].append(doc)
            
            # Then delete
            response = client.delete(
                f"/documents/{doc.id}",
                headers=auth_headers
            )
            
            print(f"Delete document response: {response.status_code}")
            
            assert response.status_code == 204

    def test_delete_document_unauthorized(self, client: TestClient):
        """Test deleting a document without authentication"""
        response = client.delete("/documents/1")
        
        print(f"Delete unauthorized response: {response.status_code}")
        
        assert response.status_code == 401

    def test_delete_document_not_found(self, client: TestClient, auth_headers):
        """Test deleting a non-existent document"""
        with patch('app.routes.documents.verify_user', return_value="admin"):
            response = client.delete("/documents/999", headers=auth_headers)
            
            print(f"Delete non-existent response: {response.status_code}")
            
            assert response.status_code == 404
            assert "Document not found" in response.json()["detail"]