#!/usr/bin/env python

"""Tests for `kepler_quickvis` package."""


import unittest
from click.testing import CliRunner

from kepler_quickvis import kepler_quickvis
from kepler_quickvis import cli


class TestKepler_quickvis(unittest.TestCase):
    """Tests for `kepler_quickvis` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'kepler_quickvis.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
