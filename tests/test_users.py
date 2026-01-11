import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

class TestUserManagement:
    def test_create_user(self, client: TestClient, auth_headers):
        """Test creating a new user with admin privileges"""
        with patch('app.routes.users.verify_admin', return_value="admin"):
            response = client.post("/admin/users/", 
                json={
                    "username": "newuser",
                    "password": "password123",
                    "role_names": []
                },
                headers=auth_headers
            )
            
            print(f"Create user response: {response.status_code}")
            
            assert response.status_code == 200
            assert "successfully" in response.json()["message"]

    def test_create_user_unauthorized(self, client: TestClient):
        """Test creating user without authentication"""
        response = client.post("/admin/users/", json={
            "username": "newuser",
            "password": "password123"
        })
        
        print(f"Create user unauthorized response: {response.status_code}")
        
        assert response.status_code == 401

    def test_list_users(self, client: TestClient, auth_headers, admin_user, mock_db):
        """Test listing all users"""
        with patch('app.routes.users.verify_admin', return_value="admin"):
            response = client.get("/admin/users/", headers=auth_headers)
            
            print(f"List users response: {response.status_code}")
            print(f"Response body: {response.json()}")
            
            assert response.status_code == 200
            assert isinstance(response.json(), list)

    def test_list_users_unauthorized(self, client: TestClient):
        """Test listing users without authentication"""
        response = client.get("/admin/users/")
        
        print(f"List users unauthorized response: {response.status_code}")
        
        assert response.status_code == 401

    def test_update_user(self, client: TestClient, auth_headers, admin_user, mock_db):
        """Test updating a user"""
        with patch('app.routes.users.verify_admin', return_value="admin"):
            response = client.put(
                f"/admin/users/{admin_user.id}",
                json={"username": "updated_admin"},
                headers=auth_headers
            )
            
            print(f"Update user response: {response.status_code}")
            
            assert response.status_code == 200
            assert "successfully" in response.json()["message"]

    def test_delete_user(self, client: TestClient, auth_headers, mock_db):
        """Test deleting a user"""
        with patch('app.routes.users.verify_admin', return_value="admin"):
            # Create a test user in mock data
            from app.models import User
            test_user = User(
                id=999,
                username="deleteuser",
                password_hash="hashedpassword",
                is_active=True
            )
            mock_db.data['users'].append(test_user)
            
            # Delete the user
            response = client.delete(f"/admin/users/{test_user.id}", headers=auth_headers)
            
            print(f"Delete user response: {response.status_code}")
            
            assert response.status_code == 204

    def test_list_roles(self, client: TestClient, auth_headers, mock_db):
        """Test listing all roles"""
        with patch('app.routes.users.verify_admin', return_value="admin"):
            response = client.get("/admin/users/roles", headers=auth_headers)
            
            print(f"List roles response: {response.status_code}")
            
            assert response.status_code == 200
            assert isinstance(response.json(), list)

    def test_create_role(self, client: TestClient, auth_headers, mock_db):
        """Test creating a new role"""
        with patch('app.routes.users.verify_admin', return_value="admin"):
            response = client.post(
                "/admin/users/roles?role_name=editor", 
                headers=auth_headers
            )
            
            print(f"Create role response: {response.status_code}")
            
            assert response.status_code == 200
            assert "successfully" in response.json()["message"]