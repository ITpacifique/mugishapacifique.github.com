# Assignment 3 DevOps Test Plan

| Test ID | Test case | URL / target | Expected result | Evidence |
|---|---|---|---|---|
| TEST-001 | Main content container | `index.html#main-content` | Main content container is present and visible | `INFO`, PASS result, duration |
| TEST-002 | About section | `index.html#about` | About section is present and visible | `INFO`, PASS result, duration |
| TEST-003 | Projects section | `index.html#projects` | Projects section is present and visible | `INFO`, PASS result, duration |
| TEST-004 | Contact section | `index.html#contact` | Contact section is present and visible | `INFO`, PASS result, duration |
| TEST-005 | Missing-section failure handling | `index.html#skills` | Missing Skills section is reported as a failure | `ERROR`, FAIL result, error, failure URL, duration |

## Execution details

- Test runner: `run_website_tests.py`
- Browser automation: Selenium WebDriver with headless Chrome
- Logging library: Python `logging`
- Log directory: `/logs/`
- Log format: `timestamp - level - message`
- The runner continues after failures and writes a final `RUN_SUMMARY` entry.
