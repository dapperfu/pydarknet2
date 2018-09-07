import pytest
import uuid
import tempfile
import socket
import shutil


# Figuring out Pytest fixtures, ignore.
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

@pytest.fixture(scope="session")
def darknet_root():
    """Darknet temporary directory."""
    root = tempfile.mkdtemp(prefix="darknet_", suffix="_"+socket.gethostname())
    try:
        shutil.rmtree(root)
    except FileNotFoundError:
        pass # yeah.
    except:
        raise
    yield str(root)
    try:
        shutil.rmtree(root)
    except FileNotFoundError:
        pass # yeah.
    except:
        raise

@pytest.fixture(scope="session")
def clone_url():
    """Clone URL"""
    clone_url = "https://github.com/jed-frey/darknet.git"
    yield str(clone_url)
