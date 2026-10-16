# Lab 5: Static Code Analysis

## Issue Table

| No. | Issue | Type | Line(s) | Description | Fix Approach |
|---:|---|---|---|---|---|
| 1 | Use of `eval()` | Security | 47 | Evaluating a string as code can execute unsafe expressions. | Replaced the expression-based calculation with a numeric surcharge rate and input validation. |
| 2 | Hard-coded API secret | Security | 75 | A secret embedded directly in source code can be exposed. | Removed the hard-coded secret from the corrected implementation. |
| 3 | Use of `os.system()` | Security | 63 | Executing shell commands from application input can introduce command-injection risks. | Removed the shell command and used a normal Python print statement. |
| 4 | Mutable default argument | Code quality | 13 | A default list can be shared across function calls, causing unexpected results. | Used `None` as the default and created a new list inside the function. |
| 5 | Missing function docstrings | Code quality | Multiple | Functions without docstrings are harder to understand and maintain. | Added docstrings describing each function's purpose. |
| 6 | Incorrect naming style | Code quality | Multiple | CamelCase function names do not follow Pylint's recommended snake_case convention. | Renamed functions using snake_case. |
| 7 | Unused imports and variables | Code quality | Multiple | Unused items make code less clear and may indicate unnecessary operations. | Removed unused imports and variables. |
| 8 | Bare `except` clause | Code quality | 29 | Catching every exception can hide unexpected errors. | Replaced the broad exception handling with explicit input validation. |
| 9 | `open()` without encoding or context manager | Code quality | 60 | The file operation did not specify an encoding or guarantee closure if an error occurred. | Used a `with` statement and explicitly specified UTF-8 encoding. |
| 10 | Use of `== None` | Code quality | 38 | Direct comparison with `None` is not the recommended Python style. | Used an explicit `is None` check or a Boolean expression. |
| 11 | Unnecessary `if/else` | Code quality | 39 | A conditional could be simplified to make the function shorter and clearer. | Returned the Boolean condition directly. |
| 12 | Weak hash algorithm | Security | 52 | MD5 is not recommended when a stronger hash is appropriate. | Replaced MD5 with SHA-256 for the passenger identifier hash. |
| 13 | Predictable boarding PIN generation | Security | 56 | The standard random module is not intended for security-sensitive values. | Used the `secrets` module to generate the PIN. |

## Verification Results

- **Pylint:** Final score of 10.00/10.
- **Bandit:** No issues identified in the final scan.
- **Flake8:** Run the final check and confirm that it produces no output.