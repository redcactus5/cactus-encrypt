import os
import shutil

def create_folder(folder_name):
    try:
        os.mkdir(folder_name)
        print(f"Created folder '{folder_name}'")
    except FileExistsError:
        print(f"Folder '{folder_name}' already exists")

def copy_folder_contents(source_folder, destination_folder):
    try:
        # Get all files and directories in the source folder
        contents = os.listdir(source_folder)
        
        # Copy each file/directory to the destination folder
        for item in contents:
            source_path = os.path.join(source_folder, item)
            destination_path = os.path.join(destination_folder, item)
            
            if os.path.isdir(source_path):
                shutil.copytree(source_path, destination_path)
            else:
                shutil.copy2(source_path, destination_path)
        
        print(f"Copied contents from '{source_folder}' to '{destination_folder}'")
    except FileNotFoundError:
        print("error!")
        print("build creation failed")
        print(f"Source folder '{source_folder}' not found")
        input("press enter to exit")
        exit()


def createBuild():
    print("starting build creation...")
    # Create a new folder
    new_folder = "debug build"
    create_folder(new_folder)
    
    # Specify folders to be copied
    folder2 = "txt_dependancies"
    folder1 = "source_code"
    folder3 = "build_modes/debug"
    
    # Copy contents of each folder to the new folder
    copy_folder_contents(folder1, new_folder)
    copy_folder_contents(folder2, new_folder)
    copy_folder_contents(folder3, new_folder)
    print("build created successfully!")
    input("press enter to finish")

createBuild()
