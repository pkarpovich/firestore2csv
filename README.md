# Firestore to CSV Converter

This project contains a Python script for exporting data from Firebase Firestore into CSV format, managed using Poetry.

## Description

This Python script allows you to export all documents from specified collections within your Firebase Firestore database into CSV files. The files are then compressed into a tar.gz file for convenience.

## Features

- Exports all documents from Firestore collections into CSV files
- Can exclude specified collections
- Automatically archives all CSV files into a tar.gz file

## Requirements

You will need the following Python packages installed:

- `firebase_admin`
- `google-cloud-firestore`

These dependencies are specified in the `pyproject.toml` file and will be automatically managed by Poetry.

## Installation

1. Clone the repository:
2. Navigate to the project directory 
3. Install Poetry if it isn't installed
4. Install the project's dependencies


## Usage

You can run the script using Poetry:

```bash
poetry run python main.py --cred-file <firebase-privateKey.json> --exclude <comma separated collection names to exclude> --output-dir <output directory>
```

Where:

- `cred-file` is the path to your Firebase private key JSON file. Default is firebase-privateKey.json.
- `exclude` is a comma-separated list of collections to exclude from the backup. By default, no collections are excluded.
- `output-dir` is the path to the directory where the output tar.gz file will be saved. By default, files are saved in the backups directory in the current working directory

Example:

```bash
poetry run python main.py --cred-file firebase-privateKey.json --exclude users,logs --output-dir backups
```

## License
This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE) file for details.