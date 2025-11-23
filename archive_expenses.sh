#!/bin/bash

# archive_expenses.sh
# Move expense file to archives and log the operation

ARCHIVE_DIR="archives"
LOG_FILE="archive_log.txt"

# Check if archives directory exists, create if not
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR"
    echo "Created archives directory."
fi

echo "Enter the date of the expense file to archive (YYYY-MM-DD):"
read DATE

FILE="expenses_$DATE.txt"

if [ ! -f "$FILE" ]; then
    echo "No expense file found for $DATE."
    exit 1
fi

# Move file to archives
mv "$FILE" "$ARCHIVE_DIR/"

# Log the operation with timestamp
echo "Archived $FILE at $(date)" >> "$LOG_FILE"

echo "File $FILE has been archived successfully."

# Optional: search for a file in archive by date
echo "Do you want to search an archived expense file by date? (y/n)"
read SEARCH
if [ "$SEARCH" = "y" ]; then
    echo "Enter date to search (YYYY-MM-DD):"
    read SEARCH_DATE
    ARCH_FILE="$ARCHIVE_DIR/expenses_$SEARCH_DATE.txt"
    if [ -f "$ARCH_FILE" ]; then
        echo "Displaying $ARCH_FILE contents:"
        cat "$ARCH_FILE"
    else
        echo "No archived expense file found for $SEARCH_DATE."
    fi
fi
