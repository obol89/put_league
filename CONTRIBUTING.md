# Contributing to PUT League

## Setup

1. Clone the repository
2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install pytest
   ```
3. Copy `.env.example` to `.env` and adjust values if needed

## Running the app

```bash
source venv/bin/activate
python app.py
```

The app will be available at `http://localhost:5000`.

## Running tests

```bash
source venv/bin/activate
python -m pytest tests/ -v
```

## Submitting changes

1. Create a feature branch from `master`
2. Make your changes
3. Ensure all tests pass
4. Submit a pull request with a clear description of your changes
