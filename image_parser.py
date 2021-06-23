import os
import json
import piexif
import exifread
import argparse
from PIL import Image
from PIL.ExifTags import TAGS
from pprint import pprint
from config import (description,
                    folder_img,
                    folder_out,
                    folder_config,
                    json_name,
                    json_name_translate,
                    json_keys_default,
                    json_keys_translate,
                    args_deletion_necessary,
                    args_analyse_pictures,
                    args_change_meta,
                    args_delete_meta,
                    args_recheck_upd,
                    args_recheck_rem,
                    args_update_json,
                    args_use_selected)


class ImageParser:
    """
    class which is dedicated to the parsing of the input values and the dedication
    """
    def __init__(self) -> None:
        self.argparse = self.parse_arguments()
        self.folder_current = os.getcwd()
        self.folder_input = os.path.join(self.folder_current, folder_img)
        self.folder_config = os.path.join(self.folder_current, folder_config)
        self.folder_output = os.path.join(self.folder_current, folder_out)
        self.create_folder = lambda x: os.path.exists(x) or os.mkdir(x)
        self.folder_development()
        
    def folder_development(self) -> None:
        """
        Method which is for creation of the battles
        Input:  nothing
        Output: we checked all folders
        """
        for v in [self.folder_input, self.folder_config, self.folder_output]:
            self.create_folder(v)
        self.produce_json()

    def produce_json(self) -> None:
        """
        Method which is dedicated to produce config json file with the
        Input:  Basic values
        Output: json file was created
        """
        for v, key in zip([json_name, json_name_translate], [json_keys_default, json_keys_translate]):
            value_name = os.path.join(self.folder_config, v)
            if not os.path.exists(value_name):
                with open(value_name, 'w') as outfile:
                    outfile.write(json.dumps(key, indent=4))
            
    @classmethod
    def parse_arguments(cls) -> object:
        """
        Classmethod which are dedicated to parse arguments which were inserted
        Input:  everything which was inserted by user
        Output: we successfully parsed arguments
        """
        dn, dn_name, dn_help, dn_act, dn_req = args_deletion_necessary
        ap, ap_name, ap_help, ap_act, ap_req = args_analyse_pictures
        cm, cm_name, cm_help, cm_act, cm_req = args_change_meta
        dm, dm_name, dm_help, dm_act, dm_req = args_delete_meta
        ru, ru_name, ru_help, ru_act, ru_req = args_recheck_upd
        rr, rr_name, rr_help, rr_act, rr_req = args_recheck_rem
        uj, uj_name, uj_help, uj_act, uj_req = args_update_json
        us, us_name, us_help, us_type, us_req, us_def = args_use_selected
        
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument(dn, dn_name, action=dn_act, help=dn_help, required=dn_req)
        parser.add_argument(ap, ap_name, action=ap_act, help=ap_help, required=ap_req)
        parser.add_argument(cm, cm_name, action=cm_act, help=cm_help, required=cm_req)
        parser.add_argument(dm, dm_name, action=dm_act, help=dm_help, required=dm_req)
        parser.add_argument(ru, ru_name, action=ru_act, help=ru_help, required=ru_req) 
        parser.add_argument(rr, rr_name, action=rr_act, help=rr_help, required=rr_req) 
        parser.add_argument(uj, uj_name, action=uj_act, help=uj_help, required=uj_req) 
        parser.add_argument(us, us_name, type=us_type, help=us_help, required=us_req, default=us_def)
        
        return parser.parse_args()

    @staticmethod
    def is_img(file_img:str) -> bool:
        """
        Static method which is dedicated to check that file is an image
        Input:  file_img = full path to the file
        Output: boolean value which signifies tha 
        """
        try:
            im = Image.open(file_img)
            im.verify()
            im.close() 
            return True
        except Exception as e:
            return False

    def list_file_selection(self) -> list:
        """
        Method which is dedicated to work with 
        Input:  value args
        Output: list of the files which 
        """
        value_list_selected = self.argparse.selected.split(',')
        value_list_return = []
        value_listdir = [f for f in os.listdir(self.folder_input) if os.path.isfile(os.path.join(self.folder_input,f))]
        value_dict = {os.path.splitext(f)[0]:f for f in value_listdir}
        value_listdir_ext = [os.path.splitext(f)[0] for f in os.listdir(self.folder_input) 
                                                                if os.path.isfile(os.path.join(self.folder_input,f))]
        
        for value_name in value_list_selected:
            if value_name in value_listdir:
                value_list_return.append(value_name)
            elif value_name in value_listdir_ext:
                value_list_return.append(value_dict.get(value_name))
        
        return [f for f in value_list_return if self.is_img(os.path.join(self.folder_input, f))]

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

    def produce_analysis(self, value_file:str, value_path:str) -> None:
        """
        Method which is dedicated 
        Input:  value_file = name of the selected file
                value_path = path to the files for see the output
        Output: dictionary values with the 
        """
        file_path = os.path.join(value_path, value_file)
        value_exif = self.get_list_metadate_exifread(file_path)
        value_pil = self.get_list_metadate_pil(file_path)
        for key_exif in list(value_exif.keys()):
            if 'EXIF ' in key_exif:
                val_exif = value_exif.pop(key_exif)
                value_exif[key_exif.replace('EXIF ', '')] = val_exif
            if 'Image ' in key_exif:
                val_exif = value_exif.pop(key_exif)
                value_exif[key_exif.replace('Image ', '')] = val_exif
            if 'Thumbnail ' in key_exif:
                value_exif.pop(key_exif)
        value_pil.update(value_exif)
        return value_pil

    @staticmethod
    def parse_json_update(value_location:str) -> dict:
        """
        Static which is dedicated to return new dictionary for the insertion of the metadata
        Input:  value_location = location to the json file to create the new one
        Output: dictionary to insert as new exif
        """
        def parse_lists(value_element:list) -> tuple:
            """
            Function which is dedicated to work with the elements and to make them as lists
            Input:  value_element = element which is to transform
            Output: all lists were changed to the tuples
            """
            if isinstance(value_element, list):
                value_element = tuple([parse_lists(f) for f in value_element])
            return value_element 

        value_dict = json.load(open(value_location))
        value_return = {}
        for keys, values in value_dict.items():
            if values:
                values_new = {int(key):parse_lists(value) for key, value in values.items()}
            else:
                values_new = values
            value_return[keys] = values_new
        return value_return

    def produce_file_update(self, value_file:str) -> None:
        """
        Method which is dedicated to update required metadata
        Input:  value_file = file name of the input
        Output: saved image without any exif values to the output
        """
        exif_dict = self.parse_json_update(os.path.join(self.folder_config, json_name))
        exif_bytes = piexif.dump(exif_dict)
        
        im = Image.open(os.path.join(self.folder_input, value_file))
        im.save(os.path.join(self.folder_output, value_file), exif=exif_bytes)

    def produce_file_delete(self, value_file:str) -> None:
        """
        Method which is dedicated to delete all metadata
        Input:  value_file = file name of the input file
        Output: saved image without any exif values to the output
        """
        image = Image.open(os.path.join(self.folder_input, value_file))
        image.save(os.path.join(self.folder_output, value_file))

    def produce_print(self, value_file:str, value_folder:str) -> None:
        """
        Method which is dedicated to use the print of the selected values
        Input:  value_file = string to the file
                value_folder = folder where to look at some files
        Output: we've printed values for it
        """
        print(value_file)
        print('---------------------------------')
        pprint(self.produce_analysis(value_file, value_folder))
        print()

    def main_usage(self) -> None:
        """
        Main method which is dedicated to work with
        Input:  inserted arguments
        Output: program finished worked
        """
        if self.argparse.update:
            os.remove(os.path.join(self.folder_config, json_name))
            self.produce_json()
        if self.argparse.selected:
            value_files = self.list_file_selection()
        else:
            value_files = [f for f in os.listdir(self.folder_input) if self.is_img(os.path.join(self.folder_input, f))]
        for value_file in value_files:
            #TODO think what to do with the analysed data, does it required to store?
            if self.argparse.analyse:
                self.produce_print(value_file, self.folder_input)

            if self.argparse.change:
                self.produce_file_update(value_file)

            if self.argparse.recheck:
                self.produce_print(value_file, self.folder_output)

            if self.argparse.delete:
                self.produce_file_delete(value_file)

            if self.argparse.observe:
                self.produce_print(value_file, self.folder_output)

            if self.argparse.necessary:
                os.remove(os.path.join(self.folder_input, value_file))
                print(f"We successfully removed {value_file} from our folder: {self.folder_input}")


if __name__ == '__main__':
    a = ImageParser()
    a.main_usage()