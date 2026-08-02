"""Tests for Authentication module."""

import pytest
from solutions.solution_01_jwt import JWTAuth, RBAC


class TestJWTAuth:
    """Test JWT authentication."""

    @pytest.fixture
    def auth(self):
        """Create auth instance."""
        return JWTAuth()

    def test_create_access_token(self, auth):
        """Test access token creation."""
        token = auth.create_access_token("user123", ["user"])
        assert isinstance(token, str)
        assert len(token) > 0

    def test_verify_valid_token(self, auth):
        """Test verifying a valid token."""
        token = auth.create_access_token("user123", ["user"])
        payload = auth.verify_token(token)
        assert payload is not None
        assert payload["sub"] == "user123"
        assert "user" in payload["roles"]

    def test_verify_invalid_token(self, auth):
        """Test verifying an invalid token."""
        payload = auth.verify_token("invalid.token.here")
        assert payload is None

    def test_refresh_token_flow(self, auth):
        """Test refresh token to get new access token."""
        refresh = auth.create_refresh_token("user123")
        new_access = auth.refresh_access_token(refresh)
        assert new_access is not None

        # Verify the new access token
        payload = auth.verify_token(new_access)
        assert payload["sub"] == "user123"


class TestRBAC:
    """Test Role-Based Access Control."""

    def test_admin_has_all_permissions(self):
        """Test that admin has all permissions."""
        assert RBAC.has_permission(["admin"], "read") is True
        assert RBAC.has_permission(["admin"], "write") is True
        assert RBAC.has_permission(["admin"], "delete") is True
        assert RBAC.has_permission(["admin"], "admin") is True

    def test_user_has_basic_permissions(self):
        """Test that user has read and write permissions."""
        assert RBAC.has_permission(["user"], "read") is True
        assert RBAC.has_permission(["user"], "write") is True
        assert RBAC.has_permission(["user"], "delete") is False

    def test_guest_has_read_only(self):
        """Test that guest has read-only permissions."""
        assert RBAC.has_permission(["guest"], "read") is True
        assert RBAC.has_permission(["guest"], "write") is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
