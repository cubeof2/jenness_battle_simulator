"""Custom exceptions for the Jenness Battle Simulator."""

class SimulatorError(Exception):
    """Base class for all simulator exceptions."""
    pass

class ConfigurationError(SimulatorError):
    """Raised when the scenario configuration is invalid or missing required data."""
    pass

class BattleError(SimulatorError):
    """Raised when an error occurs during the battle simulation."""
    pass
