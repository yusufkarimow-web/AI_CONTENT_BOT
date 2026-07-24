#!/bin/bash
# deploy.sh

set -e

echo "🔍 Starting TojikAI Project Validation..."
echo "========================================"

# Run validation
python3 scripts/validate_project.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All validations passed!"
    echo ""
    echo "📦 Creating deployment package..."

    # Create ZIP file
    python3 scripts/final_check_and_package.py

    echo "✅ Deployment package created!"
    echo ""
    echo "🚀 Ready for deployment!"
    echo ""
    echo "📝 Next steps:"
    echo "1. Extract ZIP file to your server"
    echo "2. Copy .env.example to .env and fill in your credentials"
    echo "3. Run: docker-compose up -d"
    echo "4. Check: docker-compose logs -f app"

else
    echo ""
    echo "❌ Validation failed! Fix the issues above before deploying."
    exit 1
fi
