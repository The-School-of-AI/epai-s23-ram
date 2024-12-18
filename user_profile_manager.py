from datetime import datetime
from typing import Any, Callable
import weakref


class ValidatedProperty:
    def __init__(self, validator: Callable[[Any], bool]):
        self.validator = validator
        self.name = None  # Will be set by __set_name__

    def __set_name__(self, owner: Any, name: str):
        self.name = name

    def __get__(self, instance: Any, owner: Any) -> Any:
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance: Any, value: Any):
        if not self.validator(value):
            raise ValueError(f"Invalid value for {self.name}: {value}")
        instance.__dict__[self.name] = value


class UserProfileManager:
    # Change the cache to use object IDs as keys
    _profile_cache = weakref.WeakValueDictionary()

    # Class-level default for last_login
    default_last_login = datetime(2000, 1, 1)  # Example default date

    @staticmethod
    def validate_username(username: str) -> bool:
        return isinstance(username, str) and len(username.strip()) > 0

    @staticmethod
    def validate_email(email: str) -> bool:
        return isinstance(email, str) and "@" in email and "." in email

    @staticmethod
    def validate_last_login(date: datetime | None) -> bool:
        return isinstance(date, (datetime, type(None)))

    username = ValidatedProperty(validate_username)
    email = ValidatedProperty(validate_email)
    last_login = ValidatedProperty(validate_last_login)

    def __init__(
        self,
        username: str | None = None,
        email: str | None = None,
        last_login: datetime | None = None,
    ):
        # Initialize with None values if not provided
        self._username = None
        self._email = None
        self.last_login = last_login

        # Only set values and add to cache if username is provided
        if username is not None:
            self.username = username
            if email is not None:
                self.email = email
            # Add to cache only if we have a username
            UserProfileManager._profile_cache[username] = self

    @property
    def last_login_with_default(self) -> datetime:
        """Returns the last_login value or class default if None"""
        return self.last_login or self.default_last_login

    @classmethod
    def get_cached_profile(cls, username: str) -> "UserProfileManager | None":
        """Retrieve a profile from cache if it exists"""
        return cls._profile_cache.get(username)

    @classmethod
    def create_profile(
        cls, username: str, email: str, last_login: datetime | None = None
    ) -> "UserProfileManager":
        """Factory method that checks cache before creating new profile"""
        if existing := cls.get_cached_profile(username):
            return existing
        return cls(username, email, last_login)

    @classmethod
    def add_to_cache(cls, profile: "UserProfileManager") -> None:
        """Add a profile to the cache using its object ID as key"""
        cls._profile_cache[id(profile)] = profile

    @classmethod
    def get_from_cache(cls, uid: int) -> "UserProfileManager | None":
        """Retrieve a profile from cache by its object ID"""
        return cls._profile_cache.get(uid)
