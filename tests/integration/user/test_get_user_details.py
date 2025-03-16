class TestGetUserDetails:
    def test_get_user_details_success(self, client, test_db_session, prepopulated_users):
        """Successfully retrieves user details"""
        user = prepopulated_users[0]
        response = client.get(f"/api/v1/users/{user.id}")

        assert response.status_code == 200
        data = response.get_json()
        assert data["id"] == user.id
        assert data["name"] == user.name
        assert data["email"] == user.email
        assert "created_at" in data

    def test_get_user_details_not_found(self, client, test_db_session):
        """Returns 404 when the user does not exist"""
        response = client.get("/api/v1/users/999999")

        assert response.status_code == 404
        data = response.get_json()
        assert data == {"message": "User not found"}
