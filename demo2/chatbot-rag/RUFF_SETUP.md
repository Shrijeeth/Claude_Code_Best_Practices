# Ruff Setup Summary

Ruff has been successfully configured for this project! Ruff is a fast, all-in-one Python linter and formatter that replaces tools like flake8, isort, black, and more.

## What Was Installed

- **Ruff >= 0.8.4** added to dev-dependencies in `pyproject.toml`
- Comprehensive configuration in `pyproject.toml` including:
  - Code formatting rules
  - Import sorting (replaces isort)
  - Linting with auto-fix capabilities
  - Python 3.10+ modern syntax enforcement

## Usage

### Quick Commands

```bash
# Check for issues without fixing
./lint.sh check

# Auto-fix all fixable issues
./lint.sh fix

# Format code (includes import sorting)
./lint.sh format

# Run everything (recommended)
./lint.sh all
```

### Direct uv Commands

```bash
# Lint and auto-fix
uv run ruff check --fix backend/ frontend/

# Format code
uv run ruff format backend/ frontend/

# Just check (no changes)
uv run ruff check backend/ frontend/
```

## What Ruff Checks

- **E, W**: PEP 8 style errors and warnings
- **F**: Pyflakes (unused imports, undefined names, etc.)
- **I**: Import sorting (isort replacement)
- **N**: PEP 8 naming conventions
- **UP**: Python upgrade syntax (modern type hints, etc.)
- **B**: Bugbear (common bugs and design problems)
- **C4**: Comprehension improvements
- **SIM**: Code simplification suggestions
- **RUF**: Ruff-specific rules

## Configuration Details

See `pyproject.toml` for the full configuration:

- Line length: 100 characters
- Target: Python 3.10+
- Auto-fix enabled for all rules
- Import sorting configured with proper section ordering

## Resources

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Ruff Rules Reference](https://docs.astral.sh/ruff/rules/)
- [Configuration Options](https://docs.astral.sh/ruff/configuration/)
