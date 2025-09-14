import os
import shutil
import time
import json

def confirm():
    """
    Asks for user confirmation to move files. 

    Args:
        ---

    Returns:
        confirm.lower (str): user's confirmation    
    """

    confirm = input("Would you really like to move files? Type 'Y' + Enter to confirm: ")
    if not confirm.lower() == 'y':
        print("Canceled!")
    else:
        print("Organizing files...")
        time.sleep(wait)
    return confirm.lower()

def choose_premade_mapping():
    """
    Asks for user choice to use (or not) a premade mapping. 

    Args:
        ---

    Returns:
        premap.lower (str): user's choice    
    """

    premap = input("Would you like to use a premade file extension to destination directory mapping? Type 'Y' + Enter if yes: ")
    if not premap.lower() == 'y':
        print("Manual mapping chosen!")
    else:
        print("Premade mapping chosen!")
    return premap.lower()

def get_directory_names():
    """
    Gets list of directory names as specified by user 

    Args:
        ---

    Returns:
        dirs (list): list of specified directory names    
    """

    dirs_str = input("Input directory names in which you want to put your files, separated by ',' without spaces: ")
    dirs = dirs_str.split(",")
    return dirs

def get_extensions(dirs):
    """
    Gets list of specified file extensions for each directory as specified by user 

    Args:
        dirs (list): list of specified directory names

    Returns:
        exts (list): list of specified file extensions     
    """

    exts = []
    for i in range(len(dirs)):    
        exts_str = input(f"Input file extensions for directory \"{dirs[i]}\", separated by ',' without spaces: ")
        exts.append(exts_str.split(","))
    return exts

def move_files_to_new_directories(root, dst_dict):
    """
    Moves files to destination directories, creating them if needed.

    Args:
        root (str): root path
        dst_dict (dict): dictionary that specifies which files go in which directory (based on extension)
        
    Returns:
        ---     
    """

    files = os.listdir(root)
    files_moved = []
    dirs_moved_into = set()

    #iterate through all files in root, put them in the right directory as per the dict. Create directories if needed.
    for file in files:
        #check if file (os.path.join(root, file) == file in root)
        full_this_file_path = os.path.join(root, file)
        if not (os.path.isfile(full_this_file_path)):
            continue #skip file

        #else
        filename, ext = os.path.splitext(file)
        ext = ext[1:].lower() #cut .

        #moving
        dst_dir = dst_dict.get(ext) #extension determines destination directory using dict

        ##if extension isnt specified in dict
        if dst_dir is None:
            continue #skip file

        ##get full path
        full_dst_dir_path = os.path.join(root, dst_dir)
        
        ##make dir if doesnt exist!!!
        os.makedirs(full_dst_dir_path, exist_ok=True)

        ##move
        shutil.move(full_this_file_path, full_dst_dir_path)

        #accumulate directory count
        files_moved.append(file)
        dirs_moved_into.add(dst_dir)


    #print success
    print(f"Successfully moved {len(files_moved)} files into {len(dirs_moved_into)} directories!")    

if __name__ == "__main__":
    #stock parameters
    EXIT_COMMAND = "exit"
    wait = 1.5
    with open("extdir_filemap.json") as f:
        premap_exts_dirs = json.load(f)
    with open("dirext_filemap.json") as g:
        premap_dirs_exts = json.load(g)

    while True:
        #input
        dir = input("Input path to directory to organize (type exit to exit program): ").strip('""')

        #exit
        if dir == EXIT_COMMAND:
            print("Exiting program...")
            time.sleep(wait)
            break

        #check if directory exists
        if not os.path.isdir(dir):
            print("Couldn't find directory! Check if the directory exists or if you made a typo.")
            continue
    
        else:
            dir_list = os.listdir(dir)
            print(f"Found directory! ({len(dir_list)} files)")
            print(f"{dir_list}")
    
        #user can choose between manual mapping or use a predefined mapping
        exts_dirs = {} #mapping
        premap = choose_premade_mapping()
        if premap == 'y':
            exts_dirs = premap_exts_dirs
            dirs = list(premap_dirs_exts.keys())
            exts = list(premap_dirs_exts.values())
                
        else:
            #get user's desired directory names and file extensions
            dirs = get_directory_names()
            exts = get_extensions(dirs)
            count = len(exts)

            #get the file destination mapping
            for i in range(count):
                for ext in exts[i]:
                    exts_dirs[ext] = dirs[i] #get the corresponding key-value
    
        #print how the files will be moved
        for i in range(len(dirs)):
            print(f"Files with extensions {exts[i]} will be moved to directory \"{dirs[i]}\"")

        #CONFIRM!!!
        confirmation = confirm()
        if confirmation != 'y':
            continue 

        #move files
        move_files_to_new_directories(dir, exts_dirs)


