#!/bin/zsh

# Create videos directory if it doesn't exist
mkdir -p videos

# Read the JSON file and download each video
jq -r '.[]' videos.json | while read url; do
    # Extract the UUID from the URL (the part before .mp4)
    filename=$(echo "$url" | sed -n 's/.*\/\([^\/]*\)\.mp4.*/\1/p')

    echo "Downloading: $filename.mp4"
    wget -O "videos/$filename.mp4" "$url"

    if [ $? -eq 0 ]; then
        echo "✓ Successfully downloaded: $filename.mp4"
    else
        echo "✗ Failed to download: $filename.mp4"
    fi
    echo ""
done

echo "Download complete!"
