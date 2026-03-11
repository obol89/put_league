import math
import random
import pandas as pd
import string


def get_team_groups(teams, n):
    """Shuffle teams and split into groups of size n.

    Yields tuples of n teams. Teams that don't fill a complete group are dropped.
    """
    random.shuffle(teams)
    for i in range(0, len(teams), n):
        val = teams[i:i+n]
        if len(val) == n:
            yield tuple(val)


def csv_data(groups):
    """Convert a list of group tuples into a DataFrame with Group_A, Group_B, etc. columns."""
    columns = ['Group_' + string.ascii_uppercase[i] for i in range(len(groups))]
    data = pd.DataFrame(columns=columns)
    for group, column in zip(groups, data):
        data[column] = group
    return data


def _build_group_stage_column(data):
    """Build the group stage column from group data DataFrame."""
    # Insert column headers as the first row
    data.loc[-1] = data.columns
    data.index = data.index + 1
    data.sort_index(inplace=True)

    # Flatten column by column
    flat_values = pd.Series(data.values.ravel('F')).tolist()

    # Break into chunks (header + teams per group) with blank separators
    num_groups = len(data.columns)
    teams_per_group = len(data) - 1  # subtract the header row we added
    chunk_size = teams_per_group + 1  # +1 for group name header

    group_stage_rows = []
    for i in range(0, len(flat_values), chunk_size):
        chunk = flat_values[i:i + chunk_size]
        group_stage_rows.extend(chunk)
        if i + chunk_size < len(flat_values):
            group_stage_rows.append('')

    return ['Group stage', ''] + group_stage_rows


def _generate_knockout_rounds(num_groups):
    """Generate knockout round matchups dynamically based on number of groups.

    Returns a list of knockout rounds, each being a list of (label, matchups) tuples.
    Matchups are pairs of team labels like ('A1', 'B2').
    """
    letters = list(string.ascii_uppercase[:num_groups])
    rounds = []

    # First knockout round: group winners vs runners-up from adjacent groups
    first_round = []
    for i in range(0, num_groups, 2):
        if i + 1 < num_groups:
            first_round.append((f'{letters[i]}1', f'{letters[i+1]}2'))
            first_round.append((f'{letters[i+1]}1', f'{letters[i]}2'))
        else:
            # Odd number of groups - last group winner gets a bye
            first_round.append((f'{letters[i]}1', 'BYE'))
    rounds.append(first_round)

    # Subsequent rounds: pair up winners from previous round
    prev_labels = [f'{m[0]}/{m[1]}' for m in first_round]
    while len(prev_labels) > 1:
        current_round = []
        for i in range(0, len(prev_labels), 2):
            if i + 1 < len(prev_labels):
                current_round.append((prev_labels[i], prev_labels[i+1]))
            else:
                current_round.append((prev_labels[i], 'BYE'))
        rounds.append(current_round)
        prev_labels = [f'{m[0]} - {m[1]}' for m in current_round]

    return rounds


def _round_name(num_matches, is_final=False):
    """Get the conventional name for a knockout round based on number of matches."""
    if is_final or num_matches == 1:
        return 'Final'
    if num_matches == 2:
        return 'Semifinals'
    if num_matches == 4:
        return 'Quarterfinals'
    if num_matches == 8:
        return 'Round of 16'
    return f'Round of {num_matches * 2}'


def get_data_structure(data):
    """Build a tournament bracket CSV structure from group data.

    Takes a DataFrame from csv_data() and produces a bracket layout with:
    - Group stage column
    - Knockout round columns (dynamically generated based on number of groups)
    - Blank separator columns between each round

    Supports any number of groups (2+).
    """
    num_groups = len(data.columns)
    group_column = _build_group_stage_column(data.copy())
    total_rows = len(group_column)

    result = {'Group stage': group_column}

    knockout_rounds = _generate_knockout_rounds(num_groups)

    for round_idx, matchups in enumerate(knockout_rounds):
        is_final = (round_idx == len(knockout_rounds) - 1)
        name = _round_name(len(matchups), is_final)

        col = [''] * total_rows
        # Place round header
        header_row = min(1 + round_idx * 2, total_rows - 1)
        if header_row < total_rows:
            col[header_row] = name

        # Space matchups evenly in the column
        available_start = header_row + 2
        entries = []
        for m in matchups:
            entries.append(m[0])
            entries.append(m[1])
            entries.append('')  # separator between matchups

        if entries and entries[-1] == '':
            entries.pop()

        # Place entries starting after the header
        for i, entry in enumerate(entries):
            row = available_start + i
            if row < total_rows:
                col[row] = entry

        # Add blank separator and round column
        blank_key = f'break{round_idx + 1}'
        result[blank_key] = [''] * total_rows
        result[name] = col

    return pd.DataFrame(result)
