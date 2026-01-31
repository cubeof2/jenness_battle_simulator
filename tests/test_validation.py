import pytest
from main import validate_scenario_config
from exceptions import ConfigurationError

def test_validate_valid_config():
    config = {
        "id": "valid",
        "description": "valid desc",
        "starting_momentum": "pcs",
        "pcs": [{"name": "PC1"}],
        "npcs": [{"name": "NPC1", "hp": 10, "dt": 12}]
    }
    # Should not raise any error
    validate_scenario_config(config)

def test_validate_missing_npcs():
    config = {
        "id": "invalid",
        "description": "missing npcs",
        "starting_momentum": "pcs",
        "pcs": [{"name": "PC1"}],
        "npcs": []
    }
    with pytest.raises(ConfigurationError, match="Scenario must have at least one NPC."):
        validate_scenario_config(config)

def test_validate_invalid_hp():
    config = {
        "id": "invalid",
        "description": "invalid hp",
        "starting_momentum": "pcs",
        "pcs": [{"name": "PC1"}],
        "npcs": [{"name": "NPC1", "hp": 0, "dt": 12}]
    }
    with pytest.raises(ConfigurationError, match="must have HP > 0"):
        validate_scenario_config(config)

def test_validate_missing_dt():
    config = {
        "id": "invalid",
        "description": "missing dt",
        "starting_momentum": "pcs",
        "pcs": [{"name": "PC1"}],
        "npcs": [{"name": "NPC1", "hp": 10}]
    }
    with pytest.raises(ConfigurationError, match="missing field 'dt'"):
        validate_scenario_config(config)
