# File Synchronization Script

A Python script for file and folder synchronization between a source and backup folders.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Usage](#usage)

## Introduction

The File Synchronization Script is a Python utility that synchronises files and folders between a source directory (`folder`) and a backup directory (`backup`). It ensures that both directories have identical files and folder structures.

## Features

- Synchronize files and folders between `folder` and `backup`.
- Create a log of synchronization activities.
- Configurable synchronization interval.
- Handles file updates, deletions, and new file additions.

## Usage

python main.py: This is the command to run the Python script.
--config config.txt: Specifies the path to the configuration file.
--interval 300: Sets the synchronization interval to 300 seconds.
--log sync_log.log: Specifies the path to the log file.
--folder /path/to/source: Sets the source folder path for synchronization.
--backup /path/to/backup: Sets the backup folder path.

Example:
```python
python main.py --config config.txt --interval 300 --log sync_log.log --folder /path/to/source --backup /path/to/backup
