"""Global conftest for pytest."""
import pytest
import os


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "timeout(duration): mark test with timeout in seconds")
    config.addinivalue_line("markers", "sandbox: sandbox-related tests")


def pytest_collection_modifyitems(config, items):
    """Skip Docker tests if Docker is not available."""
    docker_socket = os.environ.get("DOCKER_HOST", "/var/run/docker.sock")
    docker_available = os.path.exists(docker_socket)
    
    if not docker_available:
        skip_sandbox = pytest.mark.skip(reason="Docker socket not available")
        for item in items:
            if "sandbox" in item.fspath.strpath:
                item.add_marker(skip_sandbox)


@pytest.fixture
def mock_docker_client():
    """Mock Docker client for tests that need it."""
    from unittest.mock import MagicMock
    return MagicMock()
