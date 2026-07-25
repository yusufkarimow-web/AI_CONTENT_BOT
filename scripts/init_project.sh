#!/bin/bash
# scripts/init_project.sh

set -e

echo "🔧 Initializing TojikAI Project Structure..."
echo "=============================================="
echo ""

# Создание структуры папок
echo "📁 Creating directory structure..."

mkdir -p app/{core,db,services,api,bot,static/fonts,static/images}
mkdir -p scripts
mkdir -p generated
mkdir -p logs

echo "✅ Directories created"
echo ""

# Создание пустых __init__.py файлов
echo "📝 Creating Python module files..."

touch app/__init__.py
touch app/core/__init__.py
touch app/db/__init__.py
touch app/services/__init__.py
touch app/api/__init__.py
touch app/bot/__init__.py

echo "✅ Module files created"
echo ""

# Проверка зависимостей
echo "🔍 Checking Python version..."
python3 --version

if [ $? -eq 0 ]; then
    echo "✅ Python 3 is installed"
else
    echo "❌ Python 3 is required!"
    exit 1
fi

echo ""
echo "✅ Project initialization completed!"
echo ""
echo "📋 Next steps:"
echo "1. Copy .env.example to .env"
echo "2. Fill in your credentials"
echo "3. Run: docker-compose up -d"
echo ""
echo "🚀 Happy coding!"
