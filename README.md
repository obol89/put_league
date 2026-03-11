# PUT League

A web application for organizing sports tournaments. Enter team names, split them into groups, and export tournament brackets as CSV.

## Features

- Support for multiple sports disciplines
- Flexible team count (4 to 64 teams)
- Configurable group sizes (choose number of groups)
- Automatic random group assignment
- Tournament bracket generation with knockout rounds
- CSV export of full tournament structure

## Prerequisites

- Python 3.10+

## Installation

```bash
git clone https://github.com/obol89/put_league_2.git
cd put_league_2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Copy the example environment file and adjust as needed:

```bash
cp .env.example .env
```

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask session signing key | Random (generated at startup) |
| `FLASK_DEBUG` | Enable debug mode | `false` |

## Usage

```bash
source venv/bin/activate
python app.py
```

Open `http://localhost:5000` in your browser.

1. Select a sports discipline
2. Choose the number of teams and groups
3. Enter team names
4. Click "Split into groups" to generate the draw
5. Export the tournament bracket as CSV

## Running tests

```bash
pip install pytest
python -m pytest tests/ -v
```

## Roadmap

- [ ] Match results — enter scores for group stage and knockout matches
- [ ] Full tournament view — display standings table and knockout bracket in the browser
- [ ] Tournament mode selection — choose between knockout tournament (group stage + elimination) or league format (round-robin, everyone plays everyone)

## License

MIT - see [LICENSE](LICENSE) for details.
