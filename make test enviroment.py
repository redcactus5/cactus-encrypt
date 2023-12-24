import shutil
import os
#got from chat gpt
import shutil
import os

def copy_files_from_subdirectories(src_subdirectory1, src_subdirectory2, dest_subdirectory):
    try:
        # Remove the existing destination directory if it exists
        if os.path.exists(dest_subdirectory):
            shutil.rmtree(dest_subdirectory)

        # Create the destination directory
        os.makedirs(dest_subdirectory)

        # Get the list of files in the first source subdirectory
        files_subdirectory1 = os.listdir(src_subdirectory1)
        # Copy each file to the destination directory
        for filename in files_subdirectory1:
            src_path = os.path.join(src_subdirectory1, filename)
            dest_path = os.path.join(dest_subdirectory, filename)
            shutil.copy(src_path, dest_path)

        # Get the list of files in the second source subdirectory
        files_subdirectory2 = os.listdir(src_subdirectory2)
        # Copy each file to the destination directory
        for filename in files_subdirectory2:
            src_path = os.path.join(src_subdirectory2, filename)
            dest_path = os.path.join(dest_subdirectory, filename)
            shutil.copy(src_path, dest_path)
        print("test enviroment successfully created")
        print(f"Files copied successfully from '{src_subdirectory1}' and '{src_subdirectory2}' to '{dest_subdirectory}'.")
        input("press enter to finish")
    except Exception as e:
        print(f"Error: {e}")

# Example usage:
# Specify the source subdirectories and the destination subdirectory
source_subdirectory1 = "source_code"
source_subdirectory2 = "txt_dependancies"
destination_subdirectory = "test_build"

# Call the function
copy_files_from_subdirectories(source_subdirectory1, source_subdirectory2, destination_subdirectory)

