import os
import json
import string
from flask import Flask, request, render_template, jsonify, Response, session, redirect, flash
import tournament

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))


@app.template_global()
def group_letter(index):
    """Convert 0-based index to group letter (0->A, 1->B, etc.)."""
    return string.ascii_uppercase[index]


@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', error_code=404, message='Page not found.'), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('error.html', error_code=500, message='Something went wrong. Please try again.'), 500


@app.route('/')
def my_form():
    session.pop('teams', None)
    session.pop('groups', None)
    return render_template('index.html')


@app.route('/', methods=['POST'])
def my_form_post():
    teams_raw = request.form.get('teams')
    group_count_raw = request.form.get('group_count')

    if not teams_raw:
        return jsonify(error='No teams provided'), 400

    try:
        teams = json.loads(teams_raw)
    except (json.JSONDecodeError, TypeError):
        return jsonify(error='Invalid data format'), 400

    # Remove empty first element (header row from table)
    if teams and teams[0] == '':
        teams.pop(0)

    # Validate team names: list of non-empty strings, max 32 chars each
    if not isinstance(teams, list) or len(teams) < 2:
        return jsonify(error='At least 2 teams required'), 400
    if len(teams) > 64:
        return jsonify(error='Maximum 64 teams allowed'), 400
    for team in teams:
        if not isinstance(team, str) or len(team.strip()) == 0 or len(team) > 32:
            return jsonify(error=f'Invalid team name: {team}'), 400

    # Validate group count
    try:
        group_count = int(group_count_raw) if group_count_raw else None
    except (ValueError, TypeError):
        return jsonify(error='Invalid group count'), 400

    if group_count:
        if len(teams) % group_count != 0:
            return jsonify(error='Team count must be evenly divisible by group count'), 400
        group_size = len(teams) // group_count
        if group_size < 2:
            return jsonify(error='Each group must have at least 2 teams'), 400
    else:
        group_size = 4  # default

    session['teams'] = teams
    session['group_size'] = group_size
    return jsonify(result={'status': 200})


@app.route('/teams')
def team_sender():
    try:
        teams = session.get('teams')
        group_size = session.get('group_size', 4)
    except Exception:
        session.clear()
        teams = None
        group_size = 4

    if not teams:
        flash('No teams found. Please enter teams first.')
        return redirect('/')

    groups = list(tournament.get_team_groups(teams, group_size))
    session['groups'] = groups

    return render_template('teams.html', groups=groups)


@app.route('/summary')
def get_structure():
    try:
        groups = session.get('groups')
    except Exception:
        session.clear()
        groups = None

    if not groups:
        flash('No groups found. Please create a tournament first.')
        return redirect('/')

    excel = tournament.csv_data(groups)
    excel = tournament.get_data_structure(excel)

    return Response(
        excel.to_csv(index=False, header=False),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=PUT-table_group.csv"}
    )


if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true')
