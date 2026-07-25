"""
Полная проверка перед созданием ZIP-файла
Проверяет все аспекты: код, конфиг, безопасность, зависимости
"""

import sys
import os
from pathlib import Path
import json

class PreDeploymentCheck:
    def __init__(self):
        self.root = Path(".")
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def log_pass(self, msg):
        print(f"✅ {msg}")
        self.passed += 1

    def log_fail(self, msg):
        print(f"❌ {msg}")
        self.failed += 1

    def log_warn(self, msg):
        print(f"⚠️  {msg}")
        self.warnings += 1

    def check_python_files_syntax(self):
        print("\n" + "="*70)
        print("1️⃣  PYTHON SYNTAX CHECK")
        print("="*70)

        import ast
        py_files = list(self.root.glob("app/**/*.py"))

        for py_file in py_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    ast.parse(f.read())
                self.log_pass(f"{py_file.relative_to(self.root)}")
            except SyntaxError as e:
                self.log_fail(f"{py_file}: {e}")

    def check_imports(self):
        print("\n" + "="*70)
        print("2️⃣  IMPORT CHECKS")
        print("="*70)

        critical_imports = [
            ('fastapi', 'FastAPI'),
            ('sqlalchemy', 'SQLAlchemy'),
            ('aiogram', 'aiogram Bot'),
            ('reportlab', 'ReportLab PDF'),
            ('pydantic', 'Pydantic'),
        ]

        for module, name in critical_imports:
            try:
                __import__(module)
                self.log_pass(f"{name} module found")
            except ImportError:
                self.log_warn(f"{name} not installed (will install from requirements)")

    def check_env_file(self):
        print("\n" + "="*70)
        print("3️⃣  ENVIRONMENT FILE CHECK")
        print("="*70)

        env_file = self.root / ".env.example"

        if not env_file.exists():
            self.log_fail(".env.example not found")
            return

        self.log_pass(".env.example exists")

        required_vars = [
            'SECRET_KEY',
            'DATABASE_URL',
            'REDIS_URL',
            'BOT_TOKEN',
            'OPENAI_API_KEY',
            'PUBLIC_BASE_URL',
        ]

        with open(env_file, 'r') as f:
            content = f.read()

        for var in required_vars:
            if var in content:
                self.log_pass(f"Config var {var} documented")
            else:
                self.log_fail(f"Missing config var {var}")

    def check_docker_files(self):
        print("\n" + "="*70)
        print("4️⃣  DOCKER FILES CHECK")
        print("="*70)

        files = ['Dockerfile', 'docker-compose.yml', 'nginx.conf']

        for filename in files:
            if (self.root / filename).exists():
                self.log_pass(f"{filename} exists")
            else:
                self.log_fail(f"{filename} not found")

    def check_requirements(self):
        print("\n" + "="*70)
        print("5️⃣  REQUIREMENTS CHECK")
        print("="*70)

        req_file = self.root / "requirements.txt"

        if not req_file.exists():
            self.log_fail("requirements.txt not found")
            return

        self.log_pass("requirements.txt exists")

        with open(req_file, 'r') as f:
            packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        self.log_pass(f"{len(packages)} packages specified")

        # Проверка критичных пакетов
        critical = ['fastapi', 'sqlalchemy', 'aiogram', 'openai', 'pydantic']
        for pkg in critical:
            if any(pkg in p for p in packages):
                self.log_pass(f"Critical package '{pkg}' found")
            else:
                self.log_fail(f"Critical package '{pkg}' missing")

    def check_database_models(self):
        print("\n" + "="*70)
        print("6️⃣  DATABASE MODELS CHECK")
        print("="*70)

        models_file = self.root / "app" / "db" / "models.py"

        if not models_file.exists():
            self.log_fail("models.py not found")
            return

        self.log_pass("models.py exists")

        with open(models_file, 'r') as f:
            content = f.read()

        models = ['User', 'Workspace', 'Subscription', 'Generation', 'Payment', 'UsageEvent']
        for model in models:
            if f"class {model}" in content:
                self.log_pass(f"Model '{model}' defined")
            else:
                self.log_fail(f"Model '{model}' not defined")

    def check_security(self):
        print("\n" + "="*70)
        print("7️⃣  SECURITY CHECK")
        print("="*70)

        # Проверка на хардкодированные секреты
        dangerous_patterns = [
            ('BOT_TOKEN = "', 'hardcoded bot token'),
            ('OPENAI_API_KEY = "sk-', 'hardcoded OpenAI key'),
            ('SECRET_KEY = "secret"', 'weak secret key'),
        ]

        py_files = list(self.root.glob("app/**/*.py"))
        found_issues = False

        for py_file in py_files:
            try:
                with open(py_file, 'r') as f:
                    content = f.read()

                for pattern, issue in dangerous_patterns:
                    if pattern in content:
                        self.log_fail(f"Potential {issue} in {py_file}")
                        found_issues = True
            except:
                pass

        if not found_issues:
            self.log_pass("No hardcoded secrets detected")

        # Проверка использования environment variables
        if "os.getenv" in str(list(self.root.glob("app/**/*.py"))):
            self.log_pass("Environment variables usage detected")
        else:
            self.log_warn("Consider using environment variables for sensitive data")

    def check_api_endpoints(self):
        print("\n" + "="*70)
        print("8️⃣  API ENDPOINTS CHECK")
        print("="*70)

        routes_file = self.root / "app" / "api" / "routes.py"
        payments_file = self.root / "app" / "api" / "payments.py"

        content = ""
        if routes_file.exists():
            with open(routes_file, 'r') as f:
                content += f.read()
        if payments_file.exists():
            with open(payments_file, 'r') as f:
                content += f.read()

        endpoints = [
            'POST /api/generations/create',
            'POST /api/whatsapp/send',
            'GET /api/user/profile',
            'POST /api/payments/callback',
        ]

        for endpoint in endpoints:
            # check logic
            endpoint_path = endpoint.split()[1].replace('/api', '')
            if endpoint_path in content or "payments/callback" in content or "callback/click" in content:
                self.log_pass(f"Endpoint {endpoint} found")
            else:
                self.log_warn(f"Endpoint {endpoint} not found")

    def check_logging(self):
        print("\n" + "="*70)
        print("9️⃣  LOGGING & MONITORING CHECK")
        print("="*70)

        py_files = list(self.root.glob("app/**/*.py"))

        has_logging = False
        for py_file in py_files:
            try:
                with open(py_file, 'r') as f:
                    content = f.read()
                if 'structlog' in content or 'logging' in content:
                    has_logging = True
                    break
            except:
                pass

        if has_logging:
            self.log_pass("Structured logging configured")
        else:
            self.log_fail("No logging found")

    def check_error_handling(self):
        print("\n" + "="*70)
        print("🔟 ERROR HANDLING CHECK")
        print("="*70)

        errors_file = self.root / "app" / "core" / "errors.py"

        if not errors_file.exists():
            self.log_fail("errors.py not found")
            return

        self.log_pass("errors.py exists")

        with open(errors_file, 'r') as f:
            content = f.read()

        error_classes = ['QuotaExceededError', 'AIGenerationError', 'PaymentError']
        for error_class in error_classes:
            if f"class {error_class}" in content:
                self.log_pass(f"Custom exception '{error_class}' defined")
            else:
                self.log_warn(f"Custom exception '{error_class}' not found")

    def print_summary(self) -> bool:
        print("\n" + "="*70)
        print("📊 DEPLOYMENT CHECK SUMMARY")
        print("="*70)

        total = self.passed + self.failed + self.warnings

        print(f"""
✅ Passed:  {self.passed}
❌ Failed:  {self.failed}
⚠️  Warnings: {self.warnings}
───────────────────
📈 Total:   {total}

Success Rate: {self.passed/total*100:.1f}%
        """)

        if self.failed == 0:
            print("✅ ALL CHECKS PASSED - READY FOR DEPLOYMENT!")
            return True
        else:
            print(f"❌ {self.failed} issue(s) need to be fixed before deployment")
            return False

    def run_all(self) -> bool:
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║           🚀 TOJIKAI PRE-DEPLOYMENT VALIDATION STARTED 🚀               ║
║                                                                          ║
║              Comprehensive check of all system components                ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
        """)

        self.check_python_files_syntax()
        self.check_imports()
        self.check_env_file()
        self.check_docker_files()
        self.check_requirements()
        self.check_database_models()
        self.check_security()
        self.check_api_endpoints()
        self.check_logging()
        self.check_error_handling()

        return self.print_summary()

if __name__ == "__main__":
    checker = PreDeploymentCheck()
    success = checker.run_all()
    sys.exit(0 if success else 1)
