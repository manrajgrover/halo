"""Test notebook widget initialization and cleanup registration."""
import io
import unittest
from unittest.mock import MagicMock, patch

from halo import HaloNotebook


class TestHaloNotebookInitialization(unittest.TestCase):
    def test_widget_failure_does_not_register_cleanup(self):
        error = ImportError('widget dependency unavailable')
        with patch('halo.halo.get_environment', return_value='terminal'), \
                patch('halo.halo.atexit.register') as register, \
                patch.object(HaloNotebook, '_make_output_widget', side_effect=error):
            with self.assertRaises(ImportError) as caught:
                HaloNotebook()

        self.assertIs(caught.exception, error)
        register.assert_not_called()

    def test_widget_exists_before_cleanup_is_registered(self):
        calls = []
        widget = MagicMock()
        with patch('halo.halo.get_environment', return_value='terminal'), \
                patch('halo.halo.atexit.register', side_effect=lambda callback: calls.append('cleanup')), \
                patch.object(HaloNotebook, '_make_output_widget',
                             side_effect=lambda: calls.append('widget') or widget):
            HaloNotebook(stream=io.StringIO())

        self.assertEqual(calls, ['widget', 'cleanup'])

    def test_base_initialization_failure_closes_widget(self):
        widget = MagicMock()
        with patch('halo.halo.atexit.register') as register, \
                patch.object(HaloNotebook, '_make_output_widget', return_value=widget):
            with self.assertRaises(ValueError):
                HaloNotebook(placement='invalid')

        widget.close.assert_called_once_with()
        register.assert_not_called()

    def test_registered_cleanup_still_clears_a_ready_widget(self):
        widget = MagicMock()
        widget.outputs = ()
        with patch('halo.halo.get_environment', return_value='terminal'), \
                patch('halo.halo.atexit.register') as register, \
                patch.object(HaloNotebook, '_make_output_widget', return_value=widget):
            spinner = HaloNotebook(stream=io.StringIO())

        callback = register.call_args[0][0]
        callback(None)

        self.assertEqual(widget.outputs, spinner._output())
        widget.close.assert_called_once_with()

    def test_disabled_cleanup_keeps_existing_behavior(self):
        widget = MagicMock()
        with patch('halo.halo.get_environment', return_value='terminal'), \
                patch('halo.halo.atexit.register') as register, \
                patch.object(HaloNotebook, '_make_output_widget', return_value=widget):
            HaloNotebook(enabled=False, stream=io.StringIO())

        callback = register.call_args[0][0]
        callback(None)

        widget.close.assert_not_called()
