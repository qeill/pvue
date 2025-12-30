# Pvue - Python + Vue 3 Framework

Pvue is a modern framework that combines Vue 3 frontend with Python WebSocket backend, allowing developers to create desktop applications with ease. It provides a seamless integration between Python business logic and Vue 3 UI, supporting both web and desktop deployment.

## Features

- **Vue 3 + Python WebSocket**: Modern frontend with responsive design and real-time communication
- **Multiple Deployment Modes**: Web server, Eel desktop app, and PyWebView desktop app
- **Plugin System**: Extensible architecture for adding new features
- **Easy Packaging**: Support for PyInstaller to create standalone EXE files
- **Responsive Design**: Modern UI that works on different screen sizes
- **Scientific Calculator**: Built-in example with standard and scientific modes
- **Notepad Application**: Example of a simple text editor

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Install from PyPI

```bash
pip install pvue
```

### Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/pvue.git
cd pvue

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

## Quick Start

### Create a Simple Pvue Application

```python
from pvue.main import PvueApp

# Initialize Pvue app
app = PvueApp()

# Define a Python function that can be called from Vue
def hello(name):
    return f"Hello, {name}!"

# Register the function
app.register_function(hello)

# Start the app
app.run()
```

### Access the Application

After running the script, open your browser and navigate to:
```
http://localhost:8000
```

## Usage

### Web Mode

```python
from pvue.main import PvueApp

app = PvueApp()
app.run(mode='web')  # Default mode
```

### Eel Desktop Mode

```python
from pvue.eel import PvueEelApp

app = PvueEelApp()
app.run()
```

### PyWebView Desktop Mode

```python
from pvue.webview import PvueWebViewApp

app = PvueWebViewApp()
app.run()
```

## Examples

### Scientific Calculator

The project includes a fully functional scientific calculator with both standard and scientific modes:

```bash
cd test
python scientific_calculator.py
```

### Todo App with Eel

```bash
cd examples/eel-todo
python main.py
```

### Todo App with PyWebView

```bash
cd examples/webview-todo
python main.py
```

## Project Structure

```
pvue/
├── backend/           # Python WebSocket server
│   ├── __init__.py
│   └── server.py
├── frontend/          # Vue 3 frontend
│   ├── src/
│   │   ├── components/
│   │   ├── plugins/
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── style.css
│   ├── index.html
│   └── package.json
├── pvue/              # Main package code
│   ├── __init__.py
│   ├── main.py
│   ├── eel.py
│   ├── webview.py
│   └── static/        # Compiled frontend files
├── examples/          # Example applications
│   ├── eel-todo/
│   └── webview-todo/
├── test/              # Test applications
│   └── scientific_calculator.py
├── setup.py           # Package setup
└── README.md          # This file
```

## Architecture

### Frontend

- **Vue 3**: Modern reactive framework with Composition API
- **WebSocket**: Real-time communication with Python backend
- **Plugin System**: Extensible architecture for adding features
- **Responsive Design**: CSS Grid and Flexbox for layout

### Backend

- **Python 3**: Business logic implementation
- **WebSocket Server**: Using websockets library for real-time communication
- **Multiple Modes**: Web server, Eel, and PyWebView integration
- **Function Registration**: Easy registration of Python functions to be called from Vue

## Plugin Development

Pvue includes a plugin system that allows you to extend the framework functionality. Refer to the [PLUGIN_DEVELOPMENT.md](PLUGIN_DEVELOPMENT.md) for more information.

## Packaging Applications

### Create a Standalone EXE with PyInstaller

```bash
pyinstaller --onefile --windowed your_app.py
```

For more detailed packaging instructions, refer to the [PACKAGING_GUIDE.md](PACKAGING_GUIDE.md).

## Configuration

### Server Configuration

```python
app = PvueApp(
    host='localhost',
    port=8000,
    static_dir='path/to/static/files'
)
```

### Frontend Configuration

Modify the Vue app in `frontend/src/App.vue` to customize the UI and functionality.

## Development

### Build the Frontend

```bash
cd frontend
npm install
npm run build
```

### Run Development Server

```bash
cd frontend
npm run dev
```

### Run Tests

```bash
# Run backend tests
python -m pytest

# Run frontend tests
cd frontend
npm test
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

## Acknowledgments

- Vue 3 for the modern frontend framework
- Python for the powerful backend language
- Eel and PyWebView for desktop integration
- websockets library for real-time communication

## Support

If you have any questions or issues, please open an issue on GitHub or contact the maintainers.

---

**Happy Coding!** 🚀
