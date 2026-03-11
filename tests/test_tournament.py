import pytest
import tournament


def test_get_team_groups_16_teams_4_per_group():
    teams = [f"Team{i}" for i in range(16)]
    groups = list(tournament.get_team_groups(teams, 4))
    assert len(groups) == 4
    for group in groups:
        assert len(group) == 4


def test_get_team_groups_8_teams_4_per_group():
    teams = [f"Team{i}" for i in range(8)]
    groups = list(tournament.get_team_groups(teams, 4))
    assert len(groups) == 2
    for group in groups:
        assert len(group) == 4


def test_get_team_groups_12_teams_4_per_group():
    teams = [f"Team{i}" for i in range(12)]
    groups = list(tournament.get_team_groups(teams, 4))
    assert len(groups) == 3


def test_get_team_groups_32_teams_4_per_group():
    teams = [f"Team{i}" for i in range(32)]
    groups = list(tournament.get_team_groups(teams, 4))
    assert len(groups) == 8


def test_get_team_groups_6_teams_3_per_group():
    teams = [f"Team{i}" for i in range(6)]
    groups = list(tournament.get_team_groups(teams, 3))
    assert len(groups) == 2
    for group in groups:
        assert len(group) == 3


def test_get_team_groups_all_teams_assigned():
    teams = [f"Team{i}" for i in range(16)]
    groups = list(tournament.get_team_groups(teams, 4))
    all_teams = [t for g in groups for t in g]
    assert sorted(all_teams) == sorted(teams)


def test_csv_data_correct_columns():
    groups = [
        ("A1", "A2", "A3", "A4"),
        ("B1", "B2", "B3", "B4"),
    ]
    df = tournament.csv_data(groups)
    assert list(df.columns) == ["Group_A", "Group_B"]
    assert list(df["Group_A"]) == ["A1", "A2", "A3", "A4"]
    assert list(df["Group_B"]) == ["B1", "B2", "B3", "B4"]


def test_csv_data_many_groups():
    groups = [tuple(f"T{g}{i}" for i in range(3)) for g in range(6)]
    df = tournament.csv_data(groups)
    assert len(df.columns) == 6
    assert df.columns[0] == "Group_A"
    assert df.columns[5] == "Group_F"


@pytest.mark.parametrize("num_groups", [2, 3, 4, 6, 8])
def test_get_data_structure_various_group_counts(num_groups):
    groups = [tuple(f"T{g}{i}" for i in range(4)) for g in range(num_groups)]
    df = tournament.csv_data(groups)
    result = tournament.get_data_structure(df)
    assert "Group stage" in result.columns
    assert len(result) > 0


def test_get_data_structure_has_final():
    groups = [
        ("A1", "A2", "A3", "A4"),
        ("B1", "B2", "B3", "B4"),
        ("C1", "C2", "C3", "C4"),
        ("D1", "D2", "D3", "D4"),
    ]
    df = tournament.csv_data(groups)
    result = tournament.get_data_structure(df)
    assert "Final" in result.columns
