import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime, timedelta
from src.core.auth import BStockAuthenticator, AuthenticationError

# Test data
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "password123"

@pytest.fixture
async def auth():
    """Create an authenticator with mocked session"""
    # Create mock session
    mock_session = AsyncMock()
    mock_session.closed = False
    
    # Mock successful responses
    mock_session.get = AsyncMock(return_value=AsyncMock(
        status=200,
        text=AsyncMock(return_value='<input name="form_key" value="test_key"/>'),
        raise_for_status=AsyncMock(),
        __aenter__=AsyncMock(),
        __aexit__=AsyncMock(),
    ))
    
    mock_session.post = AsyncMock(return_value=AsyncMock(
        status=200,
        url="https://bstock.com/amazon/account",
        cookies={"frontend": "test_token"},
        text=AsyncMock(return_value="success"),
        raise_for_status=AsyncMock(),
        __aenter__=AsyncMock(),
        __aexit__=AsyncMock(),
    ))
    
    with patch('aiohttp.ClientSession', return_value=mock_session):
        auth = BStockAuthenticator(TEST_EMAIL, TEST_PASSWORD)
        auth.session = mock_session
        yield auth
        await auth.close()

@pytest.mark.asyncio
async def test_basic_auth_flow(auth):
    """Test the complete authentication flow"""
    await auth.login()
    assert auth.is_authenticated()
    assert auth.auth_token == "test_token"

@pytest.mark.asyncio
async def test_auth_failure(auth):
    """Test authentication failure"""
    # Mock failed login response
    auth.session.post = AsyncMock(return_value=AsyncMock(
        status=200,
        url="https://bstock.com/amazon/customer/account/login",
        raise_for_status=AsyncMock(),
        __aenter__=AsyncMock(),
        __aexit__=AsyncMock(),
    ))
    
    with pytest.raises(AuthenticationError):
        await auth.login()

@pytest.mark.asyncio
async def test_auth_expiration(auth):
    """Test authentication expiration"""
    await auth.login()
    assert auth.is_authenticated()
    
    auth.last_auth = datetime.now() - timedelta(hours=2)
    assert not auth.is_authenticated()

@pytest.mark.asyncio
async def test_marketplace_validation():
    """Test marketplace validation"""
    with pytest.raises(ValueError):
        BStockAuthenticator(TEST_EMAIL, TEST_PASSWORD, "invalid")