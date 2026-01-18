#!/bin/bash
# generate-files.sh
# Generate files.txt with raw.githubusercontent.com URLs

REPO_URL="https://raw.githubusercontent.com/Echopraxium/tscg/main/"

echo "Generating files.txt with raw GitHub URLs..."

# Remove old file if it exists
if [ -f "files.txt" ]; then
    rm -f files.txt
fi

# List all files with specified extensions
# excluding bin, obj, .vs, .git, packages, _archives

# Find all files with specified extensions
find . -type f \( \
    -name "*.cs" -o \
    -name "*.fs" -o \
    -name "*.md" -o \
    -name "*.csproj" -o \
    -name "*.fsproj" -o \
    -name "*.jsonld" \
\) | while read -r filepath; do
    
    # Flag to know if we should exclude this file
    exclude=0
    
    # Test for _archives
    if echo "$filepath" | grep -qi "_archives"; then
        exclude=1
    fi
    
    # Test for other excluded folders
    if echo "$filepath" | grep -qiE "(^|/)(bin|obj|\.vs|\.git|packages)/"; then
        exclude=1
    fi
    
    # If not excluded, add to file
    if [ $exclude -eq 0 ]; then
        # Remove leading './'
        filepath="${filepath#./}"
        
        # Replace spaces with %20 (URL encoding)
        filepath="${filepath// /%20}"
        
        # Write to files.txt
        echo "${REPO_URL}${filepath}" >> files.txt
    fi
done

echo ""
echo "Done! files.txt generated with raw GitHub URLs."
echo ""

# Count number of lines
if [ -f "files.txt" ]; then
    count=$(wc -l < files.txt)
    echo "Number of URLs generated: $count"
else
    echo "No files found matching criteria."
fi