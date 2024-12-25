import os
import tkinter as tk
from tkinter import ttk
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv

"""
A Tkinter-based application that generates responses using OpenAI's API based on user input
and a predefined prompt template. Features include typewriter-style text animation and
loading indicators for better user experience.
"""

load_dotenv()

class PromptApp:
    """
    Main application class that handles the GUI and prompt processing.
    
    The app provides a simple interface where users can input text, which is then
    processed using a template and sent to OpenAI's API for completion. The response
    is displayed with a typewriter effect for better user experience.
    """
    
    def __init__(self, root):
        """
        Initialize the application window and all UI components.
        
        Args:
            root: The root Tkinter window
        """
        self.root = root
        self.root.title("Prompt Template App")
        
        # Configure the main window
        self.root.geometry("600x400")
        self.root.configure(padx=20, pady=20)
        
        # Create and configure the input frame
        input_frame = ttk.Frame(root)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Create input label and entry
        ttk.Label(input_frame, text="Enter word:").pack(side=tk.LEFT)
        self.word_entry = ttk.Entry(input_frame, width=40)
        self.word_entry.pack(side=tk.LEFT, padx=(10, 10))
        
        # Bind Enter key to submit
        self.word_entry.bind('<Return>', lambda e: self.process_prompt())
        
        # Create submit button with loading state
        self.submit_button = ttk.Button(input_frame, text="Submit", command=self.process_prompt)
        self.submit_button.pack(side=tk.LEFT)
        
        # Create response text area
        self.response_text = tk.Text(root, height=15, wrap=tk.WORD)
        self.response_text.pack(fill=tk.BOTH, expand=True)
        
        # Set focus to entry
        self.word_entry.focus_set()
        
        # Loading animation dots
        self.loading_dots = 0
        self.loading_after_id = None
        self.typewriter_after_id = None
        
        self.template_path = Path(
            "./templates"
        )
        self.prompt_template_path = self.template_path / "rhymes.txt"
        # Template for the prompt
        self.prompt_template = self.prompt_template_path.read_text()
        
    def process_prompt(self):
        """
        Process the user input, send it to OpenAI API, and display the response.
        
        This method:
        1. Validates the input
        2. Shows a loading animation
        3. Sends the request to OpenAI
        4. Displays the response with a typewriter effect
        """
        word = self.word_entry.get().strip()
        if not word:
            self.response_text.delete(1.0, tk.END)
            self.response_text.insert(tk.END, "Please enter a word first.")
            return
            
        # Show loading animation
        self.submit_button.configure(state='disabled')
        self.word_entry.configure(state='disabled')
        self.response_text.delete(1.0, tk.END)
        self.animate_loading()
        
        # Create custom OpenAI client
        client = OpenAI(
            api_key=os.getenv("API_KEY"),
            base_url=os.getenv("BASE_URL")
        )
        
        try:
            # Format the prompt with the user's word
            formatted_prompt = self.prompt_template.format(word=word)
            
            # Make the API request
            response = client.chat.completions.create(
                model=os.getenv("MODEL"),
                messages=[
                    {"role": "user", "content": formatted_prompt}
                ]
            )
            
            # Stop loading animation
            if self.loading_after_id:
                self.root.after_cancel(self.loading_after_id)
            
            # Display the response with typewriter effect
            self.response_text.delete(1.0, tk.END)
            self.typewriter_text(response.choices[0].message.content)
            
        except Exception as e:
            if self.loading_after_id:
                self.root.after_cancel(self.loading_after_id)
            self.response_text.delete(1.0, tk.END)
            self.response_text.insert(tk.END, f"Error: {str(e)}")
            
        # Re-enable controls
        self.submit_button.configure(state='normal')
        self.word_entry.configure(state='normal')
        self.word_entry.focus_set()

    def animate_loading(self):
        """
        Display and animate a loading indicator while waiting for the API response.
        Shows "Thinking" with animated dots (e.g., "Thinking...", "Thinking....", etc.)
        """
        self.loading_dots = (self.loading_dots + 1) % 4
        self.response_text.delete(1.0, tk.END)
        self.response_text.insert(tk.END, "Thinking" + "." * self.loading_dots)
        self.loading_after_id = self.root.after(500, self.animate_loading)
        
    def typewriter_text(self, text, index=0):
        """
        Display text with a typewriter effect, character by character.
        
        Args:
            text: The text to display
            index: Current character position in the text
        """
        if index < len(text):
            self.response_text.insert(tk.END, text[index])
            self.typewriter_after_id = self.root.after(20, lambda: self.typewriter_text(text, index + 1))

def main():
    """Initialize and start the application."""
    root = tk.Tk()
    app = PromptApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
