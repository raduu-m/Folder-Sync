import os
import time
import argparse
import hashlib
import shutil 

def compareHashFolder(folder, backup):
    files = os.listdir(folder)
    files_backup = os.listdir(backup)
    if len(files) != len(files_backup):
        return False

    for item in files:
        item_path = os.path.join(folder, item)
        item_backup_path = os.path.join(backup, item)

        if os.path.isdir(item_path):
            if not compareHashFolder(item_path, item_backup_path):
                return False
        else:
            if item not in files_backup:
                return False
            if not compare2file(item_path, item_backup_path):
                return False
    return True

def compare2file(file1, file2):
    with open(file1, 'rb') as file1:
        with open(file2, 'rb') as file2:
            if hashlib.md5(file1.read()).hexdigest() == hashlib.md5(file2.read()).hexdigest():
                return True
            else:
                return False

def log(message, log_file, to_console=True):
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_message = f'[{now}] {message}\n'

    with open(log_file, 'a') as log_f:
        log_f.write(log_message)

    if to_console:
        print(log_message)

def copy_folder(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst) 

    shutil.copytree(src, dst) 

def main(config_file, sync_interval, log_file, folder, backup):
    log('Start', log_file)

    if os.path.isfile(config_file):
        log('config file: OK', log_file)
    else:
        log('config file: NOT FOUND', log_file)
        print("config file: NOT FOUND")
        with open(config_file, 'w') as f:
            f.write('folder:' + folder)
            f.write('\n')
            f.write('backup:' + backup)
        log('config file: CREATED', log_file)

    while True:
        if compareHashFolder(folder, backup):
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            log('file is up to date', log_file)
            time.sleep(sync_interval)
            continue

        if os.path.isdir(folder):
            log('folder: ONLINE', log_file)
        else:
            log('folder doesn''t exist', log_file)
            print('please check the config file at ' + config_file)
            break

        if os.path.isdir(backup):
            log('backup: ONLINE', log_file)
        else:
            log('backup doesn''t  exist', log_file)
            print('please check the config file at ' + config_file)
            break

        countSync = 0
        updateFile = 0
        deleteFile = 0

        for item in os.listdir(folder):
            item_path = os.path.join(folder, item)
            item_backup_path = os.path.join(backup, item)

            if os.path.isdir(item_path):
                copy_folder(item_path, item_backup_path)
                log(f'{item} folder is copied', log_file)
            else:
                if item in os.listdir(backup):
                    if compare2file(item_path, item_backup_path):
                        log(f'{item} is up to date', log_file)
                        countSync += 1
                    else:
                        updateFile += 1
                        os.remove(item_backup_path)
                        shutil.copy(item_path, item_backup_path)
                        log(f'{item} is updated', log_file)
                else:
                    log(f'{item} is copied', log_file)
                    shutil.copy(item_path, item_backup_path)

        for item in os.listdir(backup):
            item_path = os.path.join(backup, item)
            item_backup_path = os.path.join(folder, item)

            if item not in os.listdir(folder):
                deleteFile += 1
                log(f'{item} is deleted', log_file)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)

        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f'[{now}] sync: {countSync}; update: {updateFile}; delete: {deleteFile};')

        time.sleep(sync_interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='File Synchronization Script')
    parser.add_argument('--config', type=str, required=True, help='Path to the config file')
    parser.add_argument('--interval', type=int, required=True, help='Synchronization interval in seconds')
    parser.add_argument('--log', type=str, required=True, help='Path to the log file')
    parser.add_argument('--folder', type=str, required=True, help='Path to the source folder')
    parser.add_argument('--backup', type=str, required=True, help='Path to the backup folder')
    args = parser.parse_args()
    main(args.config, args.interval, args.log, args.folder, args.backup)
