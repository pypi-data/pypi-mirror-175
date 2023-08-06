"""Tests the integration test plugin
"""

import pytest

from pytest_cppython.mock.interface import MockInterface
from pytest_cppython.plugin import InterfaceIntegrationTests


class TestCPPythonInterface(InterfaceIntegrationTests[MockInterface]):
    """The tests for the Mock interface"""

    @pytest.fixture(name="plugin_type", scope="session")
    def fixture_plugin_type(self) -> type[MockInterface]:
        """A required testing hook that allows type generation

        Returns:
            An overridden interface type
        """
        return MockInterface
