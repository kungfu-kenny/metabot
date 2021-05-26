import os
import exifread
from PIL import Image
from PIL.ExifTags import TAGS
from pprint import pprint
from datetime import datetime


class ImageMetadata:
    """
    class which is dedicated to work with a picture metadata
    and return all possible values for it
    """
    def __init__(self):
        self.folder_main = os.path.dirname(os.path.abspath(__file__))
        self.folder_img = os.path.join(self.folder_main, 'img')
        
    @staticmethod
    def get_list_metadate_pil(value_file_path:str) -> dict:
        """
        Static method to extract images metadata using Pillow
        Input:  value_file_path = full path to the image
        Output: dictionary 
        """
        value_image = Image.open(value_file_path)
        return {TAGS[tag]:value for tag, value in value_image.getexif().items() if tag in TAGS}

    @staticmethod
    def get_list_metadate_exifread(value_file_path:str) -> dict:
        """
        Static method to extract metadata using exifread
        Input:  value_file_path = full path to the image
        Output: dictionary with all possible metadata
        """
        value_image = open(value_file_path, 'rb')
        return {key:str(value) for key, value in exifread.process_file(value_image, details=False).items()}
            
    @staticmethod
    def replace_metadate(value_file_path:str, value_file_store:str) -> object:
        """
        Static method which replaces all possible metadata from the
        Input:  value_file_path = full path to the image
                value_file_store = place where to store the files
        Output: we successfully saved the  
        """
        pass

    def check_img(self) -> dict:
        """
        Method which looks on the tags and returns them in cases of the 
        Input:  containment inside the self.folder_img
        Output: dictionary with the folder
        """
        for value_file in os.listdir(self.folder_img):
            value_file_path = os.path.join(self.folder_img, value_file)
            value_pil = self.get_list_metadate_pil(value_file_path)
            print(value_pil)
            print('==========================================================')
            value_exif = self.get_list_metadate_exifread(value_file_path)
            pprint(value_exif)
            print('##################################################################')
            

if __name__ == '__main__':
    a = ImageMetadata()
    a.check_img()