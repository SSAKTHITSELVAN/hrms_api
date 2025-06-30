# your_app/exceptions/base.py

class AppException(Exception):
    def __init__(self, message_key: str, details: str = None, status_code: int = 400):
        self.message_key = message_key  # e.g., "COMPANY_DUPLICATE"
        self.details = details          # e.g., "company_code: ABC123"
        self.status_code = status_code  # e.g., 409
