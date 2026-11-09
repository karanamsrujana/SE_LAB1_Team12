# Lab 5 – Static Code Analysis and Issue Documentation

## Project Details

- **Project Name:** IT Helpdesk Ticket Management System
- **Source File:** `helpdesk_system.py`
- **Tools Used:** Pylint, Bandit, Flake8

## Identified Issues

The following table documents the issues identified through static code analysis using Pylint, Bandit, and Flake8. Findings from multiple tools have been consolidated wherever they refer to the same underlying problem.

| **No.** | **Issue** | **Tool / Error Code** | **Type / Severity** | **Original Line(s)** | **Description** | **Fix Approach** |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Long Lines | Pylint C0301 / Flake8 E501 | Code Quality – Low | 13, 14, 52 | Several statements exceeded the recommended line length, reducing readability. | Split long statements into multiple lines and improved formatting. |
| 2 | Missing Module Docstring | Pylint C0114 | Code Quality – Low | 1 | The Python module did not contain a module-level docstring describing its purpose. | Added a module-level docstring describing the helpdesk system. |
| 3 | Invalid Constant Naming | Pylint C0103 | Style – Low | 7 | The constant `ticket_counter` did not follow the recommended uppercase naming convention. | Changed the naming convention to uppercase for constants. |
| 4 | Missing Function Docstrings | Pylint C0116 | Code Quality – Low | 10, 17, 20, 26, 30, 37, 40, 45 | Several functions did not contain documentation explaining their purpose. | Added meaningful docstrings to functions. |
| 5 | Mutable Default Argument | Pylint W0102 | Bug – Medium | 10 | The default list argument `[]` could be shared across multiple function calls, causing unintended data retention. | Replaced the mutable default with `None` and initialized a new list inside the function. |
| 6 | Global Variable Usage | Pylint W0603 | Code Quality – Low | 11 | A function modified a global variable, increasing dependency on shared program state. | Reworked ticket ID management to avoid directly modifying global variables. |
| 7 | Unnecessary String Formatting | Pylint C0209 | Code Quality – Low | 14 | Regular string formatting was used where an f-string would be more readable. | Replaced regular string formatting with an f-string. |
| 8 | Bare Exception Handling | Pylint W0702 / Flake8 E722 | Bug / Code Quality – Medium | 23–24 | A bare `except` block caught all exceptions, potentially hiding unexpected errors. | Replaced bare exception handling with a specific `KeyError` exception. |
| 9 | Incorrect Function Naming | Pylint C0103 | Style – Low | 30 | The function `unresolvedHighPriority` did not follow Python's snake\_case naming convention. | Renamed it to `unresolved_high_priority`. |
| 10 | Inefficient Dictionary Iteration | Pylint C0206 | Code Quality – Low | 32 | The code iterated over dictionary keys and accessed values separately. | Used `.items()` to access dictionary keys and values together. |
| 11 | Incorrect None Comparison | Pylint C0121 / Flake8 E711 | Style – Low | 33 | The code used `== None` instead of the recommended identity comparison. | Replaced `== None` with `is None`. |
| 12 | Unspecified File Encoding | Pylint W1514 | Code Quality – Low | 41 | The file was opened without explicitly specifying an encoding, which could cause inconsistent behavior across systems. | Specified `encoding="utf-8"` in the file-opening statement. |
| 13 | Improper File Resource Management | Pylint R1732 | Code Quality – Low | 41 | The file resource was not managed using a context manager. | Used the `with open()` statement to ensure proper file closure. |
| 14 | Unused Variable | Pylint W0612 / Flake8 F841 | Code Quality – Low | 47 | A local variable named `t2` was assigned but never used. | Removed the unused variable. |
| 15 | Missing Blank Lines | Flake8 E302 / E305 | Style – Low | 10, 17, 20, 26, 30, 37, 40, 45, 58 | Function definitions did not have the recommended number of blank lines before or after them. | Added appropriate blank lines between function definitions. |
| 16 | Subprocess Module Import | Bandit B404 | Security – Low | 2 | Importing the subprocess module may introduce security risks when external commands are executed unsafely. | Validated input, resolved the executable path, used argument lists and disabled shell execution. Added a targeted `# nosec B404` annotation for the intentional import. |
| 17 | Hardcoded Password | Bandit B105 | Security – Low | 8 | The administrator password was directly stored in the source code, exposing sensitive credentials. | Retrieved the password from the `HELPDESK_ADMIN_PASSWORD` environment variable. |
| 18 | Silent Exception Handling | Bandit B110 | Code Quality / Security – Low | 23–24 | An exception was caught and silently ignored using `pass`, making errors difficult to identify. | Removed silent exception handling and handled missing ticket IDs using `KeyError`. |
| 19 | Insecure Subprocess Execution | Bandit B602 | Security – High | 38 | The ping command was constructed using string concatenation and executed with `shell=True`, creating a command-injection vulnerability. | Validated the hostname, resolved the ping executable using `shutil.which()`, passed arguments as a list and used `shell=False`. |

## Before-and-After Analysis

### 1. Pylint Analysis

**Before Correction:**

- Pylint identified multiple code-quality and style issues.
- Issues included missing docstrings, mutable default arguments, global variable usage, incorrect naming conventions, bare exception handling and unused variables.
- The initial code quality score was **5.53/10**.

**After Correction:**

- Added module-level and function-level docstrings.
- Corrected naming conventions and formatting.
- Removed mutable default arguments and unnecessary global state.
- Improved exception handling and file management.
- Final Pylint score: **10.00/10**.

### 2. Bandit Analysis

**Before Correction:**

Bandit identified four security-related findings:

| **Error Code** | **Issue** | **Severity** |
| --- | --- | --- |
| B404 | Subprocess module import | Low |
| B105 | Hardcoded password | Low |
| B110 | Try-Except-Pass | Low |
| B602 | Subprocess execution with shell=True | High |

The most critical issue was B602 because executing shell commands using dynamically constructed strings can expose the application to command injection.

**After Correction:**

- Removed the hardcoded administrator password.
- Validated hostnames before executing ping commands.
- Used a resolved executable path.
- Replaced shell-based execution with argument-list execution and `shell=False`.
- Replaced silent exception handling with specific exception handling.
- Added targeted `# nosec` annotations for the intentional subprocess import and execution.

**Final Bandit Result:** No issues identified.

### 3. Flake8 Analysis

**Before Correction:**

Flake8 identified several formatting and code-quality issues:

| **Error Code** | **Description** |
| --- | --- |
| E302 | Expected two blank lines before function definitions. |
| E305 | Expected two blank lines after function definitions. |
| E501 | Line exceeded the recommended length. |
| E711 | Incorrect comparison with None. |
| E722 | Bare exception handling. |
| F841 | Local variable assigned but never used. |

**After Correction:**

- Corrected blank-line formatting.
- Split long statements.
- Fixed None comparisons.
- Removed bare exception handling.
- Removed unused variables.

**Final Flake8 Result:** No violations reported.

## Summary of Results

| **Tool** | **Before Correction** | **After Correction** |
| --- | --- | --- |
| Pylint | 5.53/10 | 10.00/10 |
| Bandit | 4 findings | No issues identified |
| Flake8 | Multiple violations | No violations reported |

## Conclusion

The initial analysis identified several issues related to security, code quality, exception handling, naming conventions and formatting.

The final analysis demonstrated significant improvement in the code quality. Pylint achieved a score of 10.00/10, Bandit reported no issues, and Flake8 reported no remaining violations.

Thus, the static code analysis process helped improve the reliability, readability, maintainability and security of the helpdesk application.
