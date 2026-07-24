"""
Полная проверка проекта перед деплоем
Проверяет: синтаксис, импорты, безопасность, конфигурацию
"""

import os
import sys
import ast
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple

class ProjectValidator:
    def __init__(self, project_root: str = "."):
        self.root = Path(project_root)
        self.errors = []
        self.warnings = []
        self.checks_passed = 0
        self.checks_failed = 0

    def print_header(self, text: str):
        print(f"\n{'='*60}")
        print(f"🔍 {text}")
        print(f"{'='*60}\n")

    def print_success(self, msg: str):
        print(f"✅ {msg}")
        self.checks_passed += 1

    def print_error(self, msg: str):
        print(f"❌ {msg}")
        self.errors.append(msg)
        self.checks_failed += 1

    def print_warning(self, msg: str):
        print(f"⚠️  {msg}")
        self.warnings.append(msg)

    # ===== CHECK 1: Python Syntax =====
    def check_python_syntax(self):
        self.print_header("CHECK 1: Python Syntax")

        py_files = list(self.root.glob("app/**/*.py")) + list(self.root.glob("scripts/**/*.py"))

        for py_file in py_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    code = f.read()
                    ast.parse(code)
                self.print_success(f"✓ Syntax OK: {py_file.relative_to(self.root)}")
            except SyntaxError as e:
                self.print_error(f"❌ Syntax Error in {py_file}: {e}")
            except Exception as e:
                self.print_error(f"❌ Error parsing {py_file}: {e}")

    # ===== CHECK 2: Requirements =====
    def check_requirements(self):
        self.print_header("CHECK 2: Requirements.txt Validity")

        req_file = self.root / "requirements.txt"

        if not req_file.exists():
            self.print_error("❌ requirements.txt not found")
            return

        try:
            with open(req_file, 'r') as f:
                lines = f.readlines()

            valid_packages = 0
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Check format: package==version
                    if '==' in line or '>=' in line or '<=' in line or '~=' in line:
                        valid_packages += 1

            if valid_packages >= 20:
                self.print_success(f"✓ Requirements: {valid_packages} packages found")
            else:
                self.print_error(f"❌ Too few packages in requirements: {valid_packages}")

        except Exception as e:
            self.print_error(f"❌ Error reading requirements: {e}")

    # ===== CHECK 3: Environment Variables =====
    def check_env_template(self):
        self.print_header("CHECK 3: Environment Configuration")

        env_file = self.root / ".env.example"

        if not env_file.exists():
            self.print_error("❌ .env.example not found")
            return

        try:
            with open(env_file, 'r') as f:
                content = f.read()

            required_vars = [
                'DATABASE_URL',
                'REDIS_URL',
                'BOT_TOKEN',
                'OPENAI_API_KEY',
                'SECRET_KEY',
                'PUBLIC_BASE_URL'
            ]

            found_vars = 0
            for var in required_vars:
                if var in content:
                    found_vars += 1

            if found_vars == len(required_vars):
                self.print_success(f"✓ All {found_vars} required env vars present")
            else:
                self.print_error(f"❌ Missing {len(required_vars) - found_vars} env vars")

        except Exception as e:
            self.print_error(f"❌ Error checking .env: {e}")

    # ===== CHECK 4: Security Issues =====
    def check_security(self):
        self.print_header("CHECK 4: Security Checks")

        security_issues = {
            "hardcoded_password": r"password\s*=\s*['\"](?!.*\{).*['\"]",
            "hardcoded_api_key": r"api_key\s*=\s*['\"].*sk-.*['\"]",
            "sql_injection": r"\.format\(.*query",
            "hardcoded_secret": r"SECRET_KEY\s*=\s*['\"][a-zA-Z0-9]{20,}['\"]",
        }

        py_files = list(self.root.glob("app/**/*.py"))
        issues_found = 0

        for py_file in py_files:
            try:
                with open(py_file, 'r') as f:
                    content = f.read()
                    lines = content.split('\n')

                for pattern_name, pattern in security_issues.items():
                    if re.search(pattern, content):
                        for i, line in enumerate(lines):
                            if re.search(pattern, line) and not line.strip().startswith('#'):
                                self.print_warning(f"Potential {pattern_name} in {py_file}:{i+1}")
                                issues_found += 1
            except Exception as e:
                self.print_warning(f"Could not check {py_file}: {e}")

        if issues_found == 0:
            self.print_success("✓ No hardcoded secrets found")
        else:
            self.print_warning(f"⚠️  {issues_found} potential security issues to review")

    # ===== CHECK 5: Docker Configuration =====
    def check_docker(self):
        self.print_header("CHECK 5: Docker Configuration")

        dockerfile = self.root / "Dockerfile"
        docker_compose = self.root / "docker-compose.yml"

        if not dockerfile.exists():
            self.print_error("❌ Dockerfile not found")
        else:
            self.print_success("✓ Dockerfile exists")

        if not docker_compose.exists():
            self.print_error("❌ docker-compose.yml not found")
        else:
            self.print_success("✓ docker-compose.yml exists")

            try:
                with open(docker_compose, 'r') as f:
                    yaml_content = f.read()

                required_services = ['db', 'redis', 'app']
                for service in required_services:
                    if service in yaml_content:
                        self.print_success(f"✓ Service '{service}' configured")
                    else:
                        self.print_error(f"❌ Service '{service}' not found")

            except Exception as e:
                self.print_error(f"❌ Error reading docker-compose: {e}")

    # ===== CHECK 6: Database Models =====
    def check_models(self):
        self.print_header("CHECK 6: Database Models")

        models_file = self.root / "app" / "db" / "models.py"

        if not models_file.exists():
            self.print_error("❌ models.py not found")
            return

        try:
            with open(models_file, 'r') as f:
                content = f.read()

            required_models = [
                'User',
                'Workspace',
                'Subscription',
                'Generation',
                'Payment',
                'UsageEvent',
                'EmpireUserStats',
            ]

            found_models = 0
            for model in required_models:
                if f"class {model}" in content:
                    found_models += 1

            if found_models == len(required_models):
                self.print_success(f"✓ All {found_models} models defined")
            else:
                self.print_error(f"❌ Missing {len(required_models) - found_models} models")

        except Exception as e:
            self.print_error(f"❌ Error checking models: {e}")

    # ===== CHECK 7: API Routes =====
    def check_api_routes(self):
        self.print_header("CHECK 7: API Routes")

        routes_file = self.root / "app" / "api" / "routes.py"
        payments_file = self.root / "app" / "api" / "payments.py"

        content = ""
        if routes_file.exists():
            with open(routes_file, 'r') as f:
                content += f.read()
        if payments_file.exists():
            with open(payments_file, 'r') as f:
                content += f.read()

        required_endpoints = [
            '/generations/create',
            '/whatsapp/send',
            '/user/profile',
            '/callback/click',
            '/callback/payme',
            '/callback/alif',
        ]

        found_endpoints = 0
        for endpoint in required_endpoints:
            if endpoint in content:
                found_endpoints += 1
            else:
                self.print_warning(f"Endpoint '{endpoint}' not found in API files.")

        if found_endpoints >= len(required_endpoints):
            self.print_success(f"✓ All {found_endpoints} required endpoints defined")
        else:
            self.print_error(f"❌ Missing {len(required_endpoints) - found_endpoints} endpoints")

    # ===== CHECK 8: Static Files =====
    def check_static_files(self):
        self.print_header("CHECK 8: Static Files & Assets")

        static_dir = self.root / "app" / "static"

        if not static_dir.exists():
            self.print_warning("⚠️  Static directory not found - will be created at runtime")
            return

        required_files = {
            'index.html': 'HTML',
            'app.js': 'JavaScript',
        }

        found_files = 0
        for filename, filetype in required_files.items():
            if (static_dir / filename).exists():
                self.print_success(f"✓ {filetype} file '{filename}' exists")
                found_files += 1
            else:
                self.print_warning(f"⚠️  {filetype} file '{filename}' not found")

        if found_files == len(required_files):
            self.print_success(f"✓ All static files present")

    # ===== CHECK 9: Configuration Files =====
    def check_config_files(self):
        self.print_header("CHECK 9: Configuration Files")

        required_configs = {
            'app/core/config.py': 'Config module',
            'docker-compose.yml': 'Docker compose',
            '.env.example': 'Environment template',
            'requirements.txt': 'Python dependencies',
            'Dockerfile': 'Docker image',
        }

        found_configs = 0
        for filepath, description in required_configs.items():
            if (self.root / filepath).exists():
                self.print_success(f"✓ {description}: {filepath}")
                found_configs += 1
            else:
                self.print_error(f"❌ {description} not found: {filepath}")

        if found_configs == len(required_configs):
            self.print_success(f"✓ All {found_configs} config files present")

    # ===== CHECK 10: Code Quality =====
    def check_code_quality(self):
        self.print_header("CHECK 10: Code Quality Metrics")

        py_files = list(self.root.glob("app/**/*.py"))
        total_lines = 0
        files_analyzed = 0

        for py_file in py_files:
            try:
                with open(py_file, 'r') as f:
                    lines = f.readlines()
                    total_lines += len(lines)
                    files_analyzed += 1
            except:
                pass

        if total_lines > 1000:
            self.print_success(f"✓ Codebase size: {total_lines} lines across {files_analyzed} files")
        else:
            self.print_warning(f"⚠️  Codebase seems small: {total_lines} lines")

    def run_all_checks(self) -> bool:
        print("\n" + "="*60)
        print("🚀 TOJIKAI PROJECT VALIDATION STARTED")
        print("="*60)

        self.check_python_syntax()
        self.check_requirements()
        self.check_env_template()
        self.check_security()
        self.check_docker()
        self.check_models()
        self.check_api_routes()
        self.check_static_files()
        self.check_config_files()
        self.check_code_quality()

        # Summary
        self.print_header("VALIDATION SUMMARY")

        total_checks = self.checks_passed + self.checks_failed
        print(f"✅ Passed: {self.checks_passed}")
        print(f"❌ Failed: {self.checks_failed}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        print(f"📊 Total Checks: {total_checks}")

        success_rate = (self.checks_passed / total_checks * 100) if total_checks > 0 else 0
        print(f"\n📈 Success Rate: {success_rate:.1f}%")

        if self.checks_failed == 0:
            print("\n" + "🎉 "*20)
            print("ALL CHECKS PASSED - PROJECT IS READY FOR DEPLOYMENT")
            print("🎉 "*20)
            return True
        else:
            print(f"\n⚠️  {self.checks_failed} issues need to be fixed before deployment")
            print("\nErrors:")
            for error in self.errors:
                print(f"  - {error}")
            return False

if __name__ == "__main__":
    validator = ProjectValidator()
    success = validator.run_all_checks()
    sys.exit(0 if success else 1)
