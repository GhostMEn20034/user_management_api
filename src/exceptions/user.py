class UserNotFoundError(Exception):
    """Exception raised when a user is not found."""
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.message = f"User with ID {user_id} not found"
        super().__init__(self.message)
