#!/bin/bash
# Banking ETL Assessment - GitHub Setup Script
# This script automates the process of pushing the project to GitHub

echo "=================================="
echo "Banking ETL Assessment - Git Setup"
echo "=================================="
echo ""

# Initialize git repository
echo "[1/5] Initializing git repository..."
git init

# Add all files
echo "[2/5] Adding all files..."
git add .

# Create initial commit
echo "[3/5] Creating initial commit..."
git commit -m "Initial ETL project - Complete banking transaction processing pipeline"

# Rename branch to main
echo "[4/5] Renaming branch to main..."
git branch -M main

# Add remote repository (user needs to replace USERNAME)
echo "[5/5] Adding remote repository..."
echo ""
echo "IMPORTANT: Before proceeding, please:"
echo "1. Create a new repository on GitHub: https://github.com/new"
echo "2. Name it: banking_etl_assessment"
echo "3. Run the command below with your GitHub username:"
echo ""
echo "git remote add origin https://github.com/USERNAME/banking_etl_assessment.git"
echo "git push -u origin main"
echo ""
echo "=================================="
echo "Setup Instructions:"
echo "=================================="
echo ""
echo "Step 1: Create repository on GitHub"
echo "  - Go to https://github.com/new"
echo "  - Repository name: banking_etl_assessment"
echo "  - Description: Banking ETL Assessment - Complete Python ETL Pipeline"
echo "  - Choose 'Public' or 'Private'"
echo "  - Click 'Create repository'"
echo ""
echo "Step 2: Add remote and push"
echo "  Replace USERNAME with your GitHub username:"
echo "  $ git remote add origin https://github.com/USERNAME/banking_etl_assessment.git"
echo "  $ git push -u origin main"
echo ""
echo "Or use SSH:"
echo "  $ git remote add origin git@github.com:USERNAME/banking_etl_assessment.git"
echo "  $ git push -u origin main"
echo ""
