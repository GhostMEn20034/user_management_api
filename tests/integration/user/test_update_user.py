import pytest


class TestUpdateUser:
    def test_update_user_success(self, client, test_db_session, prepopulated_users):
        """Successfully updates a user"""
        user = prepopulated_users[0]
        updated_data = {"name": "Updated Name", "email": user.email}
        response = client.put(f"/api/v1/users/{user.id}", json=updated_data)

        assert response.status_code == 200
        data = response.get_json()
        assert data["id"] == user.id
        assert data["name"] == updated_data["name"]
        assert data["email"] == updated_data["email"]

    def test_update_user_not_found(self, client, test_db_session):
        """Returns 404 when trying to update a non-existent user"""
        updated_data = {"name": "New Name", "email": "new.email@example.com"}
        response = client.put("/api/v1/users/999999", json=updated_data)

        assert response.status_code == 404
        data = response.get_json()
        assert data == {"message": "User not found"}

    @pytest.mark.parametrize(
        "invalid_payload",
        [
            {},  # Empty payload
            {"name": "John"},  # Missing email
            {"email": "john.doe@example.com"},  # Missing name
            {"name": "", "email": "john.doe@example.com"},  # Empty name
            {"name": "John", "email": "invalid-email"},  # Invalid email
        ]
    )
    def test_update_user_invalid_data(self, client, test_db_session, prepopulated_users, invalid_payload):
        """Returns 400 when request body is invalid"""
        user = prepopulated_users[0]
        response = client.put(f"/api/v1/users/{user.id}", json=invalid_payload)

        assert response.status_code == 400
        data = response.get_json()
        assert "message" in data

    def test_update_user_email_already_taken(self, client, test_db_session, prepopulated_users):
        """Returns 400 when trying to update with an already existing email"""
        user = prepopulated_users[0]
        another_user = prepopulated_users[1]
        updated_data = {"name": "Updated Name", "email": another_user.email}
        response = client.put(f"/api/v1/users/{user.id}", json=updated_data)

        assert response.status_code == 400
        data = response.get_json()
        assert data == {"message": "User with this email already exists"}

    def test_update_user_same_email(self, client, test_db_session, prepopulated_users):
        """Returns 200 when user updates with the same email"""
        user = prepopulated_users[0]
        updated_data = {"name": "Updated Name", "email": user.email}
        response = client.put(f"/api/v1/users/{user.id}", json=updated_data)

        assert response.status_code == 200
        data = response.get_json()
        assert data["id"] == user.id
        assert data["name"] == updated_data["name"]
        assert data["email"] == updated_data["email"]
        