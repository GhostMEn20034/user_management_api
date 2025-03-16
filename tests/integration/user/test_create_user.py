import pytest


class TestCreateUser:
    def test_create_user_success(self, client, test_db_session):
        """Successfully creates a user"""
        user_data = {"name": "John Doe", "email": "john.doe@example.com"}
        response = client.post("/api/v1/users/", json=user_data)

        assert response.status_code == 201
        data = response.get_json()
        assert data["name"] == user_data["name"]
        assert data["email"] == user_data["email"]

    def test_create_user_duplicate_email(self, client, test_db_session, prepopulated_users):
        """Returns 400 when trying to create a user with an existing email"""
        existing_user = prepopulated_users[0]
        user_data = {"name": "New Name", "email": existing_user.email}
        response = client.post("/api/v1/users/", json=user_data)

        assert response.status_code == 400
        data = response.get_json()
        assert "email" in data["message"]

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
    def test_create_user_invalid_payload(self, client, test_db_session, invalid_payload):
        """Returns 400 when request body is invalid"""
        response = client.post("/api/v1/users/", json=invalid_payload)

        assert response.status_code == 400
        data = response.get_json()
        assert "message" in data