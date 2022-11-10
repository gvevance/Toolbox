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

def main():
    
    if len(sys.argv) != 3 :
        print("Usage : python3 compress_jpeg.py <file> <compression percentage>")
        exit()
    
    FILE = sys.argv[1]
    if not os.path.exists(FILE) :
        print("ERROR : File does not exist.")
        exit()

    try :
        COMPRESS_TO = int(sys.argv[2])
        if COMPRESS_TO < 1 :
            print("ERROR : Cannot compress by more than 1%.")
            exit()
    
    except ValueError :
        print("ERROR : Invalid compression percent entered.")
        exit()
    
    # except Exception as e:
    #     print(e)
    #     exit()

    try :
        img = Image.open(FILE).rotate(180)

    except UnidentifiedImageError :
        print("Invalid image file entered. Exiting.")
        exit()
    
    # except Exception as err:
    #     print(f"{type(err).__name__} was raised: {err}")
    #     exit()

    # print file size
    file_stat = os.stat(FILE)
    print("Current file size is : ",file_stat.st_size>>10,"kB")

    _filename, _ = os.path.splitext(FILE)
    NEW_FILE = _filename + "_min.JPG"

    # format = format you wanna save the compressed image as
    # NEW_FILE = filename you wanna save the compressed image as 
    img.save(NEW_FILE,format="JPEG",optimize=True,quality=COMPRESS_TO)

    # print new file size
    file_stat = os.stat(NEW_FILE)
    print("Compressed file size is : ",file_stat.st_size>>10,"kB")


if __name__ == "__main__" :
    main()