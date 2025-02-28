# Coding Standards and Best Practices

## Python Version
- Python 3.11+ is required
- Use type hints for all function parameters and return values
- Use latest language features when appropriate

## Code Style
- Follow PEP 8 guidelines
- Maximum line length: 88 characters (Black default)
- Use Black for code formatting
- Use isort for import sorting
- Use ruff for linting

## Naming Conventions
- Classes: PascalCase
- Functions and variables: snake_case
- Constants: UPPER_SNAKE_CASE
- Private attributes/methods: _leading_underscore
- Protected attributes/methods: __double_underscore

## Documentation
- All modules must have docstrings
- All public functions must have docstrings
- Use Google style docstrings
- Include type hints in docstrings
- Document exceptions that may be raised

## Code Organization
- One class per file (with rare exceptions)
- Related functionality grouped in modules
- Clear separation of concerns
- Maximum function length: 50 lines
- Maximum class length: 300 lines

## Error Handling
- Use custom exceptions for domain-specific errors
- Always catch specific exceptions
- Log exceptions appropriately
- Provide meaningful error messages
- Use context managers (with statements) where appropriate

## Security Practices
- Never store secrets in code
- Use environment variables for configuration
- Validate all input data
- Use secure random number generation
- Follow principle of least privilege

## Testing
- Write tests before code (TDD)
- 100% test coverage for critical paths
- Use pytest fixtures
- Mock external dependencies
- Test edge cases and error conditions

## Version Control
- Meaningful commit messages
- One feature/fix per commit
- Branch naming: feature/, bugfix/, hotfix/
- Pull request required for all changes
- Code review required for all changes

## Dependencies
- Pin all dependency versions
- Use uv for package management
- Regular dependency updates
- Security audit of dependencies

## Logging
- Use structured logging
- Include context in log messages
- Appropriate log levels
- No sensitive data in logs

## Performance
- Profile code when necessary
- Use appropriate data structures
- Avoid premature optimization
- Document performance considerations

## Comments
- Comments explain why, not what
- Keep comments up to date
- Remove commented-out code
- Use TODO comments sparingly

## Type Checking
- Use mypy for static type checking
- No `type: ignore` without explanation
- Use Protocol for duck typing
- Use TypeVar for generic types

## Async Code
- Use async/await consistently
- Handle cancellation properly
- Use appropriate event loop
- Document async behavior

## Updates
This document should be reviewed and updated regularly as new best practices emerge or requirements change. 