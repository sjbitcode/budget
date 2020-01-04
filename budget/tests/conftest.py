import pytest


@pytest.fixture
def test_envs(monkeypatch):
    monkeypatch.setenv('DATA_PATH', 'accounts_data.example.json')
