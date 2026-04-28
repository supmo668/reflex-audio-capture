```markdown
# reflex-audio-capture Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill covers the core development patterns and conventions used in the `reflex-audio-capture` Python codebase. You'll learn how to structure files, write imports and exports, follow commit message conventions, and organize tests. This guide is ideal for contributors aiming for consistency and maintainability in this repository.

## Coding Conventions

### File Naming
- Use **snake_case** for all Python files.
  - Example: `audio_capture.py`, `utils_test.py`

### Import Style
- Use **relative imports** within the package.
  - Example:
    ```python
    from .audio_capture import AudioRecorder
    from . import utils
    ```

### Export Style
- Use **named exports** (i.e., explicitly listing what is exported).
  - Example:
    ```python
    __all__ = ["AudioRecorder", "capture_audio"]
    ```

### Commit Messages
- Use **conventional commits** with the `feat` prefix for new features.
  - Example:
    ```
    feat: add support for stereo audio capture
    ```

## Workflows

### Adding a New Feature
**Trigger:** When implementing a new capability or improvement  
**Command:** `/add-feature`

1. Create a new Python file using snake_case if needed.
2. Implement the feature using relative imports for internal modules.
3. Export new classes or functions using the `__all__` variable.
4. Write or update tests in a corresponding `*.test.*` file.
5. Commit changes with a message starting with `feat:` and a concise description.

### Writing Tests
**Trigger:** When adding or updating functionality  
**Command:** `/write-test`

1. Create a test file named with the pattern `*.test.*` (e.g., `audio_capture.test.py`).
2. Write tests for new or modified functions/classes.
3. Use the same import conventions as the main codebase.
4. Run tests using the project's preferred method (framework unknown; use standard Python test runners if unsure).

## Testing Patterns

- Test files follow the `*.test.*` naming pattern (e.g., `utils.test.py`).
- The specific testing framework is not detected, but tests are likely written as standard Python test functions or classes.
- Example test file structure:
  ```python
  from .audio_capture import AudioRecorder

  def test_audio_recorder_initialization():
      recorder = AudioRecorder()
      assert recorder is not None
  ```

## Commands
| Command        | Purpose                                         |
|----------------|-------------------------------------------------|
| /add-feature   | Scaffold and commit a new feature               |
| /write-test    | Create and update test files for your changes   |
```
