import pytest
import uuid

@pytest.fixture(scope="session")
def uuid_session():
    """UUID with a session scope."""
    print("Session!")
    yield str(uuid.uuid4())

@pytest.fixture(scope="module")
def uuid_module():
    """UUID with a module scope."""
    print("Module!")
    yield str(uuid.uuid4())

@pytest.fixture(scope="function")
def uuid_function():
    """UUID with a function scope."""
    print("Function!")
    yield str(uuid.uuid4())

