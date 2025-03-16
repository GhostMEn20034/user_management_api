import pytest


class TestGetUserList:

    def test_get_user_list_success(self, client, test_db_session, prepopulated_users):
        """Users are successfully retrieved with pagination"""
        response = client.get("/api/v1/users/", query_string={"page": 1, "page_size": 2})
        assert response.status_code == 200

        data = response.get_json()
        assert "items" in data
        assert "pagination" in data
        assert len(data["items"]) == 2  # Should return 2 users as per pagination

        # Validate user data
        expected_users = sorted(prepopulated_users, key=lambda u: u.created_at, reverse=True)[:2]
        for i, user in enumerate(expected_users):
            assert data["items"][i]["id"] == user.id
            assert data["items"][i]["name"] == user.name
            assert data["items"][i]["email"] == user.email

    def test_get_user_list_no_pagination(self, client, test_db_session, prepopulated_users):
        """Users are successfully retrieved without specifying pagination params"""
        response = client.get("/api/v1/users/")
        assert response.status_code == 200

        data = response.get_json()
        assert "items" in data
        assert "pagination" in data
        assert len(data["items"]) > 0  # Should return users as per default pagination

        expected_users = sorted(prepopulated_users, key=lambda u: u.created_at, reverse=True)
        for i, user in enumerate(expected_users[:len(data["items"])]):
            assert data["items"][i]["id"] == user.id
            assert data["items"][i]["name"] == user.name
            assert data["items"][i]["email"] == user.email

    @pytest.mark.parametrize("page, page_size", [
        (-1, 10),   # Negative page number
        (0, 10),    # Zero page number
        (1, -5),    # Negative page size
        (1, 0),     # Zero page size
        ("abc", 10),  # Non-numeric page
        (1, "xyz")   # Non-numeric page_size
    ])
    def test_get_user_list_invalid_pagination(self, client, page, page_size):
        """Test case where invalid pagination params should return HTTP 400"""
        response = client.get("/api/v1/users/", query_string={"page": page, "page_size": page_size})
        assert response.status_code == 400

        data = response.get_json()
        assert "message" in data  # Ensure error message exists