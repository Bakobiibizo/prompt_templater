# Prompt Templater

A simple and elegant desktop application that processes text input using OpenAI's API and customizable prompt templates. Built with Python and Tkinter, featuring a modern user interface with typewriter animations and loading indicators.

## Features

- Clean and intuitive user interface
- Real-time text processing using OpenAI's API
- Customizable prompt templates
- Typewriter-style response animation
- Loading indicator during API calls
- Keyboard shortcuts (Enter to submit)

## Prerequisites

- Python 3.6+
- OpenAI API access
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd prompt_templater
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API configuration:
```
API_KEY=your_openai_api_key
BASE_URL=your_api_base_url
MODEL=your_preferred_model
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Enter your text in the input box
3. Press Enter or click Submit to process
4. Watch as the response is typed out character by character

## Customizing Templates

Templates are stored in the `templates` directory. You can modify existing templates or create new ones to customize the prompts sent to the API.

## Project Structure

```
prompt_templater/
├── app.py              # Main application code
├── templates/          # Prompt template directory
│   └── rhymes.txt     # Example template
├── requirements.txt    # Python dependencies
└── .env               # API configuration
```

## Testing

Run the tests using:
```bash
python -m unittest discover tests
```

The test suite includes:
- Unit tests for app initialization
- Input validation tests
- API integration tests (with mocked responses)
- Template loading tests

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.