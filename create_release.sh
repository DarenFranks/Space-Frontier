#!/bin/bash
# Quick script to create a versioned release

VERSION="2.0.0"
RELEASE_NAME="Space-Frontier-v${VERSION}"

# Create release directory
mkdir -p releases
mkdir -p "releases/${RELEASE_NAME}"

# Copy all necessary files
cp *.py "releases/${RELEASE_NAME}/"
cp *.md "releases/${RELEASE_NAME}/"
cp *.txt "releases/${RELEASE_NAME}/"
cp *.bat "releases/${RELEASE_NAME}/"
cp *.sh "releases/${RELEASE_NAME}/"

# Create zip
cd releases
zip -r "${RELEASE_NAME}.zip" "${RELEASE_NAME}"
cd ..

echo "Release created: releases/${RELEASE_NAME}.zip"
echo ""
echo "Now create a GitHub release:"
echo "1. Go to: https://github.com/DarenFranks/Space-Frontier/releases/new"
echo "2. Tag: v${VERSION}"
echo "3. Title: Space Frontier ${VERSION}"
echo "4. Upload: releases/${RELEASE_NAME}.zip"
