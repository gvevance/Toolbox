# Script that can compress jpeg images to user specified file size

'''
1. Open image
2. Take argument from script - sys.argv
3. Quality of compression (size afterwards)
4. Display size of resultant image
5. Compressed image is saved to the directory where the image is at
6. Check whether format is correct
'''

import sys
import os
from PIL import Image
from PIL import UnidentifiedImageError

# file_name, file_extension = os.path.splitext("/Users/pankaj/abc.txt")
def main():
    
    if len(sys.argv) != 3 :
        print("Usage : python3 compress_jpeg.py <file> <compression percentage>")
        exit()
    
    FILE = sys.argv[1]
    if not os.path.exists(FILE) :
        print("ERROR : File does not exist.")
        exit()

    try :
        COMPRESS_BY = int(sys.argv[2])
        if COMPRESS_BY < 1 :
            print("ERROR : Cannot compress by more than 10%.")
            exit()
    
    except ValueError :
        print("ERROR : Invalid compression percent entered.")
        exit()
    
    except Exception as e:
        print(e)
        exit()

    try :
        img = Image.open(FILE).rotate(180)
        # img.show()
    except UnidentifiedImageError :
        print("Invalid image file entered. Exiting.")
        exit()
    
    file_stat = os.stat(FILE)
    print("Current file size is : ",file_stat.st_size>>10,"kB")

    _filename, _file_extension = os.path.splitext(FILE)
    NEW_FILE = _filename + "_min.JPG"
    img.save(NEW_FILE,"JPEG",optimize=True,quality=COMPRESS_BY)

    # img_min = Image.open(NEW_FILE).rotate(180)
    # # img_min.show()

    file_stat = os.stat(NEW_FILE)
    print("Compressed file size is : ",file_stat.st_size>>10,"kB")


if __name__ == "__main__" :
    main()