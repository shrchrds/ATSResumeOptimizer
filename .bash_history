black --check .
flake8 . --max-line-length=127
pip install bandit
bandit -r . -ll
pip install detect-secrets
detect-secrets scan
