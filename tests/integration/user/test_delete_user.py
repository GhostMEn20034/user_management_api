class TestDeleteUser:
    def test_delete_user_success(self, client, test_db_session, prepopulated_users):
        """Successfully deletes a user"""
        user = prepopulated_users[0]
        response = client.delete(f"/api/v1/users/{user.id}")

        assert response.status_code == 204
        assert response.data == b''

    def test_delete_user_not_found(self, client, test_db_session):
        """Returns 404 when the user does not exist"""
        response = client.delete("/api/v1/users/999999")

        assert response.status_code == 404
        data = response.get_json()
        assert data == {"message": "User not found"}
