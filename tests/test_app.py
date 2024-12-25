import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from pathlib import Path
import sys
import os

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import PromptApp

class TestPromptApp(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.root = tk.Tk()
        self.app = PromptApp(self.root)
        
    def tearDown(self):
        """Clean up after each test"""
        self.root.destroy()

    def test_init(self):
        """Test initialization of the app"""
        self.assertEqual(self.app.root.title(), "Prompt Template App")
        self.assertIsInstance(self.app.word_entry, tk.ttk.Entry)
        self.assertIsInstance(self.app.response_text, tk.Text)

    def test_empty_input(self):
        """Test behavior with empty input"""
        self.app.word_entry.delete(0, tk.END)
        self.app.process_prompt()
        response_text = self.app.response_text.get("1.0", tk.END).strip()
        self.assertEqual(response_text, "Please enter a word first.")

    @patch('app.OpenAI')
    def test_process_prompt(self, mock_openai):
        """Test prompt processing with mocked OpenAI API"""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Test response"))]

        # Create mock client
        mock_chat = MagicMock()
        mock_chat.completions.create.return_value = mock_response
        
        mock_client = MagicMock()
        mock_client.chat = mock_chat
        
        mock_openai.return_value = mock_client

        # Set up environment variables
        with patch.dict('os.environ', {'API_KEY': 'test_key', 'BASE_URL': 'test_url', 'MODEL': 'test_model'}):
            # Test prompt processing
            self.app.word_entry.insert(0, "test")
            self.app.process_prompt()
            
            # Process pending events
            while self.root.dooneevent(tk._tkinter.ALL_EVENTS | tk._tkinter.DONT_WAIT):
                pass
            
            # Verify API was called with correct parameters
            mock_chat.completions.create.assert_called_once()
            call_args = mock_chat.completions.create.call_args[1]
            self.assertEqual(call_args['model'], 'test_model')
            self.assertIsInstance(call_args['messages'], list)

    def test_template_loading(self):
        """Test template file loading"""
        self.assertTrue(Path(self.app.prompt_template_path).exists())
        self.assertIsInstance(self.app.prompt_template, str)
        self.assertNotEqual(self.app.prompt_template, "")

if __name__ == '__main__':
    unittest.main()
