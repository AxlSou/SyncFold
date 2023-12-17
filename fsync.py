import os
import hashlib
import time
import argparse

# =================
# = Color logs    =
# =================

class bcolors:
    HEADER = '\033[95m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'

class counters:
    files_created = 0
    folders_created = 0
    files_updated = 0
    folders_updated = 0
    files_deleted = 0
    folders_deleted = 0
    
# ====================
# = Define functions =
# ====================

def create_parser():
    parser = argparse.ArgumentParser(description='Synconize files between two directories.')
    parser.add_argument('src', metavar='src', type=str, help='source directory')
    parser.add_argument('dst', metavar='dst', type=str, help='destination directory')
    parser.add_argument('sync_interval', metavar='sync_interval', type=int, help='sync interval in seconds')
    parser.add_argument('log', metavar='log', type=str, help='log file')
    return parser

def log(log_file, message, color=bcolors.OKGREEN):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    with open(log_file, 'a') as f:
        f.write('[' + timestamp + ']' + message + '\n')
    print(color + '[' + timestamp + ']' + message)

def get_file_md5(file_path):
    with open(file_path, 'rb') as f:
        md5 = hashlib.md5(f.read()).hexdigest()
    return md5

def compare_files(src_file, dst_file):
    src_md5 = get_file_md5(src_file)
    dst_md5 = get_file_md5(dst_file)
    return src_md5 == dst_md5

def compare_folders(src_folder, dst_folder):
    src_list = os.listdir(src_folder)
    dst_list = os.listdir(dst_folder)
    if len(src_list) != len(dst_list):
        return False
    for src_file in src_list:
        if src_file in dst_list:
            if os.path.isfile(src_folder+'/'+src_file):
                if not compare_files(src_folder+'/'+src_file, dst_folder+'/'+src_file):
                    return False
            else:
                if not compare_folders(src_folder+'/'+src_file, dst_folder+'/'+src_file):
                    return False
        else:
            return False
    return True

def sync_files(src_file, dst_file):
    src_content = os.listdir(src_file)
    dst_content = os.listdir(dst_file)
    for src_item in src_content:
        full_src_path = os.path.join(src_file, src_item)
        full_dst_path = os.path.join(dst_file, src_item)
        if os.path.isfile(full_src_path):
            if src_item in dst_content:
                if not compare_files(full_src_path, full_dst_path):
                    log(args.log, 'Updating ' + full_dst_path)
                    os.system('cp ' + full_src_path + ' ' + full_dst_path)
                    log(args.log, 'File ' + full_src_path + ' is updated.')
                    counters.files_updated += 1
            else:
                log(args.log, 'File ' + full_src_path + ' has not been found in destination directory.', bcolors.WARNING)
                os.system('cp ' + full_src_path + ' ' + full_dst_path)
                log(args.log, 'File ' + full_src_path + ' has been copied.')
                counters.files_created += 1
        else:
            if src_item in dst_content:
                if not compare_folders(full_src_path, full_dst_path):
                    sync_files(full_src_path, full_dst_path)
                    counters.folders_updated += 1
            else:
                log(args.log, 'Folder ' + full_src_path + ' has not been found in destination directory.', bcolors.WARNING)
                os.system('mkdir ' + full_dst_path)
                log(args.log, 'Folder ' + full_src_path + ' created in destination directory.')
                sync_files(full_src_path, full_dst_path)
                counters.folders_created += 1
                    
# ================
# = Main program =
# ================

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    if not os.path.isdir(args.src):
        log(args.log, '[ERROR] - Source directory does not exist.', bcolors.ERROR)
        exit(-1)
    if not os.path.isdir(args.dst):
        log(args.log, '[ERROR] - Destination directory does not exist.', bcolors.ERROR)
        exit(-1)
    if not os.path.isfile(args.log):
        log(args.log, '[ERROR] - Log file does not exist.', bcolors.ERROR)
        exit(-1)

    log(args.log, 'Starting synchronization.', bcolors.HEADER)
    while True:
            
        if compare_folders(args.src, args.dst):
            log(args.log, 'Folders are up to date.')
            time.sleep(args.sync_interval)
            continue
        
        sync_files(args.src, args.dst)
        
        src_content = os.listdir(args.src)
        dst_content = os.listdir(args.dst)
        for dst_item in dst_content:
            if os.path.isfile(dst_item):
                if dst_item not in src_content:
                    log(args.log, 'File ' + dst_item + ' has not been found in source directory.', bcolors.WARNING)
                    os.system('rm ' + args.dst + '/' + dst_item)
                    log(args.log, 'File ' + dst_item + ' has been deleted.')
                    counters.files_deleted += 1
            else:
                if dst_item not in src_content:
                    log(args.log, 'Folder ' + dst_item + ' has not been found in source directory.', bcolors.WARNING)
                    os.system('rm -r ' + args.dst + '/' + dst_item)
                    log(args.log, 'Folder ' + dst_item + ' has been deleted.')
                    counters.folders_deleted += 1
                
        log(args.log, 'Folders are up to date.')
        log(args.log, 'Files created: ' + str(counters.files_created) + ', folders created: ' + str(counters.folders_created) + ',', bcolors.OKCYAN)
        log(args.log, 'files updated: ' + str(counters.files_updated) + ', folders updated: ' + str(counters.folders_updated) + '.', bcolors.OKCYAN)
        log(args.log, 'files deleted: ' + str(counters.files_deleted) + ', folders deleted: ' + str(counters.folders_deleted) + '.', bcolors.OKCYAN)
        time.sleep(args.sync_interval)