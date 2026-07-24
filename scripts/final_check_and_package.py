"""
Финальная проверка проекта и создание ZIP пакета
"""

import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

class ProjectPackager:
    def __init__(self, project_root="."):
        self.root = Path(project_root)
        self.version = "3.0.0"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def print_header(self, text):
        print(f"\n{'='*70}")
        print(f"  {text}")
        print(f"{'='*70}\n")

    def check_all_files(self):
        """Проверка наличия всех критичных файлов"""
        self.print_header("📋 CHECKING REQUIRED FILES")

        required_files = [
            'app/__init__.py',
            'app/main.py',
            'app/core/config.py',
            'app/core/errors.py',
            'app/db/models.py',
            'app/db/session.py',
            'app/db/connection.py',
            'app/services/generation_service.py',
            'app/services/pdf_generator.py',
            'app/services/billing_service.py',
            'app/services/whatsapp_service.py',
            'app/services/gamification_service.py',
            'app/api/routes.py',
            'app/api/payments.py',
            'app/bot/handlers.py',
            'app/static/index.html',
            'app/static/app.js',
            'requirements.txt',
            '.env.example',
            'Dockerfile',
            'docker-compose.yml',
            'nginx.conf',
            'init.sql',
            'deploy.sh',
            'README.md',
        ]

        missing = []
        found = 0

        for file_path in required_files:
            if (self.root / file_path).exists():
                print(f"✅ {file_path}")
                found += 1
            else:
                print(f"❌ {file_path}")
                missing.append(file_path)

        print(f"\n✅ Found: {found}/{len(required_files)}")

        if missing:
            print(f"❌ Missing: {len(missing)}")
            return False

        return True

    def create_project_structure(self):
        """Создание необходимых директорий"""
        self.print_header("📁 CREATING PROJECT STRUCTURE")

        dirs_to_create = [
            'app/__pycache__',
            'app/db',
            'app/services',
            'app/api',
            'app/bot',
            'app/core',
            'app/static/images',
            'app/static/fonts',
            'scripts',
            'generated',
            'logs',
        ]

        for dir_path in dirs_to_create:
            full_path = self.root / dir_path
            if not full_path.exists():
                full_path.mkdir(parents=True, exist_ok=True)
                print(f"✅ Created: {dir_path}")
            else:
                print(f"ℹ️  Exists: {dir_path}")

    def create_zip_package(self):
        """Создание ZIP пакета"""
        self.print_header("📦 CREATING ZIP PACKAGE")

        zip_name = f"tojikai-smm-platform-v{self.version}.zip"
        zip_path = self.root / zip_name

        # Remove if already exists
        if zip_path.exists():
            zip_path.unlink()

        exclude_patterns = [
            '__pycache__',
            '.pyc',
            '.git',
            '.env',
            '.pytest_cache',
            '.venv',
            'venv',
            'node_modules',
            'generated/',  # Исключить сгенерированные PDF
            '*.log',
            '*.sqlite',
            '*.db',
            '.DS_Store',
            zip_name
        ]

        def should_exclude(file_path):
            for pattern in exclude_patterns:
                if pattern in str(file_path):
                    return True
            return False

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            files_added = 0

            for root, dirs, files in os.walk(self.root):
                # Пропустить исключенные директории
                dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d))]

                for file in files:
                    file_path = Path(root) / file

                    if not should_exclude(file_path):
                        arcname = file_path.relative_to(self.root)
                        zipf.write(file_path, arcname)
                        files_added += 1

                        if files_added % 50 == 0:
                            print(f"  Processing... {files_added} files")

        size_mb = zip_path.stat().st_size / (1024 * 1024)
        print(f"✅ Created: {zip_name}")
        print(f"   Size: {size_mb:.2f} MB")
        print(f"   Files: {files_added}")

        return zip_path

    def generate_deployment_guide(self):
        """Генерация краткого гайда для развертывания"""
        self.print_header("📝 GENERATING DEPLOYMENT GUIDE")

        guide = """
╔══════════════════════════════════════════════════════════════════════════╗
║                    TOJIKAI SMM PLATFORM v3.0                            ║
║                    QUICK DEPLOYMENT GUIDE                               ║
╚══════════════════════════════════════════════════════════════════════════╝

📦 PACKAGE CONTENTS:
✅ Complete FastAPI application
✅ Database models (PostgreSQL)
✅ Telegram Bot with Mini App
✅ Payment integration (Click, Payme, Alif)
✅ AI Content generation (OpenAI GPT-4o-mini)
✅ PDF export functionality
✅ WhatsApp integration (Green-API)
✅ Business simulator (TojikAI Empire)
✅ Docker & Docker Compose setup
✅ Nginx reverse proxy config

═══════════════════════════════════════════════════════════════════════════

🚀 QUICK START (5 MINUTES):

1. EXTRACT THE ARCHIVE
   $ unzip tojikai-smm-platform-v3.0.zip

2. ENTER DIRECTORY
   $ cd tojikai-smm-platform-v3.0

3. PREPARE ENVIRONMENT
   $ cp .env.example .env

4. FILL IN YOUR CREDENTIALS IN .env
   - BOT_TOKEN (from @BotFather)
   - OPENAI_API_KEY (from OpenAI)
   - CLICK_SECRET_KEY (or PAYME or ALIF)
   - WHATSAPP_API_TOKEN (from Green-API)

5. RUN DEPLOYMENT
   $ chmod +x deploy.sh
   $ ./deploy.sh

6. VERIFY
   $ docker-compose logs -f app
   (Wait for "Application started" message)

7. TEST
   $ curl https://YOUR_URL/health

═══════════════════════════════════════════════════════════════════════════

🔐 SECURITY CHECKLIST:

Before deploying to production:
✅ Change all default passwords
✅ Enable HTTPS/SSL (use Let's Encrypt)
✅ Configure firewall (only allow ports 80, 443)
✅ Set SECRET_KEY to strong random string (32+ chars)
✅ Review .env for test values
✅ Enable database backups
✅ Configure log rotation
✅ Set up monitoring/alerting
✅ Test payment callbacks
✅ Verify webhook signatures

═══════════════════════════════════════════════════════════════════════════

📞 SUPPORT:

For issues or questions:
- Email: support@tojikai.app
- Telegram: @tojikai_support
- Documentation: https://docs.tojikai.app

═══════════════════════════════════════════════════════════════════════════

Congratulations! Your TojikAI Platform is ready to serve users!

Happy deploying! 🚀

═══════════════════════════════════════════════════════════════════════════
"""

        guide_path = self.root / "DEPLOYMENT_GUIDE.txt"
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide)

        print("✅ Generated: DEPLOYMENT_GUIDE.txt")

    def create_manifest(self):
        """Создание манифеста проекта"""
        self.print_header("📄 CREATING PROJECT MANIFEST")

        manifest = {
            "project": "TojikAI SMM Platform",
            "version": self.version,
            "release_date": datetime.now().isoformat(),
            "components": {
                "backend": "FastAPI 0.104.1",
                "database": "PostgreSQL 16",
                "cache": "Redis 7",
                "bot": "aiogram 3.3.0",
                "ai": "OpenAI GPT-4o-mini",
                "payments": ["Click", "Payme", "Alif"],
                "messaging": "Green-API (WhatsApp)",
            },
            "features": [
                "Smart Steps (4-step content generator)",
                "TojikAI Empire (business simulator)",
                "AI Consultant",
                "Multi-language support (TJ, UZ, RU)",
                "Payment integration",
                "Telegram Mini App",
                "PDF export",
                "WhatsApp messaging",
                "Analytics & reporting",
            ],
            "deployment": {
                "method": "Docker Compose",
                "min_requirements": {
                    "cpu": "2 cores",
                    "ram": "4 GB",
                    "disk": "50 GB",
                    "os": "Linux/Mac/Windows"
                }
            },
            "security": {
                "encryption": "TLS 1.2+",
                "authentication": "Telegram Bot API",
                "api_security": "Bearer tokens",
                "payment_security": "Webhook signatures"
            }
        }

        import json
        manifest_path = self.root / "MANIFEST.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        print("✅ Generated: MANIFEST.json")

    def run_all(self):
        """Запустить всю процедуру"""
        print("\n")
        print("╔" + "="*68 + "╗")
        print("║" + " "*68 + "║")
        print("║" + "  🚀 TOJIKAI PROJECT FINAL PACKAGING STARTED".center(68) + "║")
        print("║" + " "*68 + "║")
        print("╚" + "="*68 + "╝")

        # Проверка файлов
        if not self.check_all_files():
            print("\n❌ Some required files are missing!")
            print("❌ Cannot create package.")
            return False

        # Создание структуры
        self.create_project_structure()

        # Создание гайда
        self.generate_deployment_guide()

        # Создание манифеста
        self.create_manifest()

        # Создание ZIP
        zip_path = self.create_zip_package()

        # Финальное сообщение
        self.print_header("✅ PACKAGING COMPLETED SUCCESSFULLY")

        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║  ✅ Your TojikAI Platform is ready for deployment!                      ║
║                                                                          ║
║  📦 Package: tojikai-smm-platform-v3.0.zip                              ║
║  📋 Guide:   DEPLOYMENT_GUIDE.txt                                       ║
║  📄 Manifest: MANIFEST.json                                             ║
║                                                                          ║
║  🚀 NEXT STEPS:                                                         ║
║                                                                          ║
║  1. Extract ZIP on your server                                          ║
║  2. Copy .env.example to .env                                           ║
║  3. Fill in your API keys and credentials                               ║
║  4. Run: docker-compose up -d                                           ║
║  5. Check: docker-compose logs -f app                                   ║
║                                                                          ║
║  🔐 REMEMBER:                                                           ║
║  - Never commit .env to version control                                 ║
║  - Use strong passwords for databases                                   ║
║  - Enable HTTPS/SSL in production                                       ║
║  - Set up monitoring and backups                                        ║
║                                                                          ║
║  📞 Need help? support@tojikai.app                                      ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
        """)

        return True

if __name__ == "__main__":
    import sys
    packager = ProjectPackager()
    success = packager.run_all()
    sys.exit(0 if success else 1)
