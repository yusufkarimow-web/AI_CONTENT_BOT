#!/bin/bash
# final_build.sh - ПОЛНЫЙ СКРИПТ ДЛЯ СОЗДАНИЯ ZIP И ПРОВЕРКИ

set -e

clear

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                            ║"
echo "║         🚀 TOJIKAI SMM PLATFORM v3.0 - FINAL BUILD SCRIPT 🚀              ║"
echo "║                                                                            ║"
echo "║              Professional Production-Ready Package Creation                ║"
echo "║                                                                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# ============================================================================
# STEP 1: PRE-DEPLOYMENT CHECKS
# ============================================================================

echo "📋 STEP 1: Running Pre-Deployment Checks..."
echo "────────────────────────────────────────────────────────────────────────────"
echo ""

python3 scripts/pre_deployment_check.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Pre-deployment checks failed!"
    echo "Please fix the issues above before proceeding."
    exit 1
fi

echo ""

# ============================================================================
# STEP 2: VALIDATE PROJECT STRUCTURE
# ============================================================================

echo "🔍 STEP 2: Validating Project Structure..."
echo "────────────────────────────────────────────────────────────────────────────"
echo ""

python3 scripts/validate_project.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Project validation failed!"
    exit 1
fi

echo ""

# ============================================================================
# STEP 3: CREATE ZIP PACKAGE
# ============================================================================

echo "📦 STEP 3: Creating Deployment Package..."
echo "────────────────────────────────────────────────────────────────────────────"
echo ""

python3 scripts/final_check_and_package.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Package creation failed!"
    exit 1
fi

echo ""

# ============================================================================
# FINAL SUMMARY
# ============================================================================

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                            ║"
echo "║                   ✅ BUILD COMPLETED SUCCESSFULLY! ✅                      ║"
echo "║                                                                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

echo "📦 Your Deployment Package is Ready:"
echo ""
ls -lh tojikai-smm-platform-v3.0.zip 2>/dev/null | awk '{print "   Size: " $5 " | File: " $9}'

echo ""
echo "📋 Package includes:"
echo "   ✅ Complete FastAPI application"
echo "   ✅ Database models & migrations"
echo "   ✅ Telegram Bot with Mini App"
echo "   ✅ Payment gateway integrations"
echo "   ✅ AI content generation engine"
echo "   ✅ WhatsApp messaging integration"
echo "   ✅ Business simulator (TojikAI Empire)"
echo "   ✅ Docker & Docker Compose setup"
echo "   ✅ Nginx reverse proxy configuration"
echo "   ✅ Complete documentation"
echo ""

echo "🚀 NEXT STEPS:"
echo "───────────────────────────────────────────────────────────────────────────"
echo ""
echo "1. Transfer ZIP file to your production server:"
echo "   scp tojikai-smm-platform-v3.0.zip user@server:/home/user/"
echo ""
echo "2. SSH into the server:"
echo "   ssh user@server"
echo ""
echo "3. Extract the archive:"
echo "   unzip tojikai-smm-platform-v3.0.zip"
echo "   cd tojikai-smm-platform-v3.0"
echo ""
echo "4. Prepare environment configuration:"
echo "   cp .env.example .env"
echo "   nano .env  # Edit and fill in your credentials"
echo ""
echo "5. Required credentials to fill in .env:"
echo "   • BOT_TOKEN (from @BotFather on Telegram)"
echo "   • OPENAI_API_KEY (from https://platform.openai.com)"
echo "   • CLICK_SECRET_KEY or PAYME_SECRET_KEY or ALIF_SECRET_KEY"
echo "   • WHATSAPP_API_TOKEN (from https://green-api.com)"
echo "   • SECRET_KEY (generate random 32+ character string)"
echo "   • PUBLIC_BASE_URL (your domain with HTTPS)"
echo ""
echo "6. Start the application:"
echo "   docker-compose up -d"
echo ""
echo "7. Monitor startup:"
echo "   docker-compose logs -f app"
echo "   (Wait for 'Application started' message)"
echo ""
echo "8. Verify deployment:"
echo "   curl https://YOUR_DOMAIN/health"
echo "   (Should return 200 OK with status: 'healthy')"
echo ""
echo "9. Access Telegram Bot:"
echo "   Search for your bot in Telegram"
echo "   Send /start"
echo "   Click '🚀 Open Mini App'"
echo ""

echo ""
echo "🔒 SECURITY REMINDERS:"
echo "───────────────────────────────────────────────────────────────────────────"
echo "✅ Never commit .env file to version control"
echo "✅ Use strong, random passwords for databases"
echo "✅ Enable HTTPS/SSL with valid certificates (use Let's Encrypt)"
echo "✅ Configure firewall to only allow ports 80, 443"
echo "✅ Set up database backups (daily minimum)"
echo "✅ Configure log rotation"
echo "✅ Enable monitoring and alerting"
echo "✅ Test payment callbacks thoroughly"
echo "✅ Keep all dependencies updated"
echo "✅ Review security logs regularly"
echo ""

echo "📞 SUPPORT:"
echo "───────────────────────────────────────────────────────────────────────────"
echo "If you encounter issues:"
echo ""
echo "1. Check the logs:"
echo "   docker-compose logs -f app | grep -i error"
echo ""
echo "2. Review the documentation:"
echo "   cat DEPLOYMENT_GUIDE.txt"
echo ""
echo "3. Check the manifest:"
echo "   cat MANIFEST.json"
echo ""
echo "4. Contact support:"
echo "   📧 Email: support@tojikai.app"
echo "   💬 Telegram: @tojikai_support"
echo "   🌐 Website: https://tojikai.app"
echo ""

echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                            ║"
echo "║                    🎉 Thank you for choosing TojikAI! 🎉                   ║"
echo "║                                                                            ║"
echo "║        Your platform is ready to serve users across Central Asia!          ║"
echo "║                                                                            ║"
echo "║                        Good luck with your project! 🚀                     ║"
echo "║                                                                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"

exit 0
