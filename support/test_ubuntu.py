

if __name__ == "__main__":
    import os, glob
    files = glob.glob ( '*.py' )
    for file in files :
        print os.path.isfile(file),file
