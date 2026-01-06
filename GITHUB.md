# 🚀 GitHub Deployment Guide

Panduan lengkap untuk push project Banking ETL Assessment ke GitHub.

## Prerequisites

- Git installed on your system
- GitHub account
- GitHub repository created (or will create one)

## Step 1: Initialize Local Repository

Jika belum dilakukan, initialize repository lokal:

```bash
cd banking_etl_assessment
git init
git pull origin main
```

## Step 2: Add All Files

```bash
git add .
```

Verifikasi files yang akan di-commit:

```bash
git status
```

## Step 3: Create Initial Commit

```bash
git commit -m "Initial ETL project - Complete banking transaction processing pipeline

- Implemented full ETL pipeline for banking transactions
- Includes loader, validator, cleaner, and transformer modules
- Comprehensive unit tests with 100+ test cases
- Async API utilities with retry logic
- Complete documentation and example usage"
```

## Step 4: Create Repository on GitHub

1. Go to https://github.com/new
2. Fill in the details:
   - **Repository name**: `banking_etl_assessment`
   - **Description**: "Banking ETL Assessment - Complete Python ETL Pipeline for processing banking transactions with validation, cleaning, and transformation"
   - **Visibility**: Select "Public" (or "Private" for your own use)
   - **Initialize with**: Leave unchecked (we have our own files)
3. Click "Create repository"

## Step 5: Connect Local Repository to GitHub

Replace `USERNAME` with your GitHub username:

### Option A: HTTPS (Recommended for beginners)

```bash
git remote add origin https://github.com/USERNAME/banking_etl_assessment.git
git branch -M main
git push -u origin main
```

### Option B: SSH (Recommended for advanced users)

First, ensure you have SSH keys set up: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

Then:

```bash
git remote add origin git@github.com:USERNAME/banking_etl_assessment.git
git branch -M main
git push -u origin main
```

## Step 6: Verify Push Success

Check your GitHub repository in the browser:
```
https://github.com/USERNAME/banking_etl_assessment
```

You should see all your files there.

## Step 7: (Optional) Add Repository Shield

Add this to your README for visual appeal:

```markdown
[![GitHub license](https://img.shields.io/github/license/USERNAME/banking_etl_assessment)](https://github.com/USERNAME/banking_etl_assessment/blob/main/LICENSE)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
```

## Common Issues & Solutions

### Issue: "fatal: remote origin already exists"

**Solution**: Remove existing remote and add new one:

```bash
git remote remove origin
git remote add origin https://github.com/USERNAME/banking_etl_assessment.git
```

### Issue: "fatal: 'origin' does not appear to be a 'git' repository"

**Solution**: Ensure you're in the correct directory and have initialized git:

```bash
cd banking_etl_assessment
git init
git remote add origin https://github.com/USERNAME/banking_etl_assessment.git
```

### Issue: "Your branch is ahead of 'origin/main' by X commits"

**Solution**: Push your commits:

```bash
git push origin main
```

### Issue: "Permission denied (publickey)"

**Solution**: SSH key not configured. Either:
- Use HTTPS instead: `https://github.com/USERNAME/banking_etl_assessment.git`
- OR set up SSH keys: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

## Updating Repository

After making changes locally:

```bash
# Stage changes
git add .

# Commit changes
git commit -m "Describe your changes here"

# Push to GitHub
git push origin main
```

## Collaboration

To allow others to contribute:

1. Go to your repository Settings
2. Click "Collaborators" (or "Manage access")
3. Click "Add people"
4. Enter their GitHub username and send invitation

## Creating a Release

To create a release for your project:

```bash
# Create an annotated tag
git tag -a v1.0.0 -m "Initial release - Banking ETL Assessment v1.0.0"

# Push tag to GitHub
git push origin v1.0.0
```

Then on GitHub:
1. Go to "Releases"
2. Click "Create a new release"
3. Select your tag
4. Add release notes
5. Publish release

## Project URL

After pushing successfully, your project will be available at:

```
https://github.com/USERNAME/banking_etl_assessment
```

Replace `USERNAME` with your GitHub username.

## Additional Resources

- [GitHub Quick Start](https://docs.github.com/en/get-started)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Docs](https://docs.github.com)

---

**Need help?** Check the [Banking ETL Assessment README](README.md) for project information.


# kalau sudah di cloning ( ada perubahan )
git pull origin main ( kalau ada repo online ) 
git add .
git commit -m "fix: correct vector search bug"
git push 

# Cara menjalankan test
python example.py ( untuk coba coba )
pytest tests/ -q  ( untuk test semuanya )
pytest tests/ -v ( untuk lihat spesifik )
