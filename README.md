# User Profile Manager

A Python library for managing user profiles with validation and caching capabilities. This library provides a robust way to handle user profile data with built-in validation for common fields like username and email.

## Features

- Validated properties for username, email, and last login
- Weak reference caching system to prevent duplicate profile instances
- Type hints and static typing support
- Custom property validation framework
- Default value handling for optional fields

## Usage
```python
from user_profile_manager import UserProfileManager
from datetime import datetime
Create a new user profile
profile = UserProfileManager.create_profile(
username="john_doe",
email="john@example.com",
last_login=datetime.now()
)
Access validated properties
print(profile.username) # "john_doe"
print(profile.email) # "john@example.com"
Get cached profile
cached_profile = UserProfileManager.get_cached_profile("john_doe")
```
## Validation Rules

- Username: Must be a non-empty string
- Email: Must be a string containing '@' and '.'
- Last Login: Must be a datetime object or None

## Caching

The library uses a weak reference cache to prevent memory leaks and ensure that profiles are not retained unnecessarily. The cache is automatically cleared when a profile is deleted.
