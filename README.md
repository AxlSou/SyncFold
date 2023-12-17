# Directory Synchronization Script

## Overview

This Python script synchronizes files between two directories. It compares the contents of the source and destination directories, updates files that have changed, creates new files and folders, and deletes files and folders that no longer exist in the source directory.

## Features

- File synchronization based on MD5 hash comparison.
- Incremental synchronization with a specified interval.
- Logging of synchronization activities to a specified log file.
- Color-coded console logs for better visibility.

## Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/AxlSou/SyncFold.git
    ```

2. Navigate to the project directory:

    ```bash
    cd SyncFold
    ```

3. Run the script with the following command:

    ```bash
    python fsync.py <src_directory> <dst_directory> <sync_interval_seconds> <log_file>
    ```

    - `<src_directory>`: Source directory to synchronize.
    - `<dst_directory>`: Destination directory to synchronize.
    - `<sync_interval_seconds>`: Sync interval in seconds (e.g., 60 for every minute).
    - `<log_file>`: Path to the log file.

4. Monitor synchronization activities in the console and log file.

## Requirements

- Python 3.x
- No additional Python packages are required.

## Example

```bash
python fsync.py /path/to/source /path/to/destination 60 synchronization.log
```

## NOTES
- Make sure to set appropriate permissions for reading, writing, and executing on the specified directories.