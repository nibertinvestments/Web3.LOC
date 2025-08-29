#!/bin/bash
# Web3.LOC GitHub Setup Script
# Run this script to push to GitHub and enable Pages

echo "🚀 Web3.LOC GitHub Pages Setup"
echo "================================="
echo ""

# Check if we're in the right directory
if [ ! -f "docs/index.html" ]; then
    echo "❌ Error: Please run this script from the Web3.LOC directory"
    exit 1
fi

echo "📋 Setup Instructions:"
echo ""
echo "1. CREATE GITHUB REPOSITORY:"
echo "   - Go to https://github.com/new"
echo "   - Repository name: Web3.LOC"
echo "   - Set to PUBLIC (required for free GitHub Pages)"
echo "   - Do NOT initialize with README, .gitignore, or license"
echo "   - Click 'Create repository'"
echo ""

echo "2. COPY YOUR REPOSITORY URL:"
echo "   - After creating, copy the HTTPS URL"
echo "   - It looks like: https://github.com/YOUR_USERNAME/Web3.LOC.git"
echo ""

echo "3. ENTER YOUR REPOSITORY URL:"
read -p "Paste your GitHub repository URL here: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ Error: Repository URL is required"
    exit 1
fi

echo ""
echo "🔗 Adding remote repository..."
git remote add origin "$REPO_URL"

echo "📤 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! Code pushed to GitHub"
    echo ""
    echo "4. ENABLE GITHUB PAGES:"
    echo "   - Go to your repository on GitHub"
    echo "   - Click 'Settings' tab"
    echo "   - Scroll to 'Pages' in left sidebar"
    echo "   - Under 'Source' select 'GitHub Actions'"
    echo "   - Your site will deploy automatically!"
    echo ""
    echo "🌍 Your live site will be available at:"
    echo "   $(echo $REPO_URL | sed 's/\.git$//' | sed 's/github\.com\//github.io\//')/"
    echo ""
    echo "🎉 Deployment complete! Your Web3.LOC site is now live!"
else
    echo ""
    echo "❌ Error pushing to GitHub. Please check:"
    echo "   - Repository URL is correct"
    echo "   - You have push access to the repository"
    echo "   - Repository exists and is accessible"
fi
