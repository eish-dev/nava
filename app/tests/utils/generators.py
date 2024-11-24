from typing import Dict, Any
from datetime import datetime

def generate_user_data() -> Dict[str, Any]:
    return {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "password123"
    }

def generate_organization_data() -> Dict[str, Any]:
    return {
        "name": "Test Organization",
    }

def generate_admin_login_data() -> Dict[str, Any]:
    return {
        "email": "admin@example.com",
        "password": "password123"
    } 