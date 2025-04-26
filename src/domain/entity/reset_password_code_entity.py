from datetime import datetime

class ResetPasswordCodeEntity:
    id: int
    user_id: int
    code: str
    created_at: datetime

    def __init__(self, user_id: int, code: str, id: int, created_at: datetime):
        self.id = id
        self.user_id = user_id
        self.code = code
        self.created_at = created_at
