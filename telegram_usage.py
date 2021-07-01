import os
import io
import py7zr
import tarfile
import zipfile
from PIL import Image
from uuid import uuid4
from image_parser import ImageParser
from config import (txt_sent,
                    list_image_ext,
                    list_archive_ext,
                    callback_data_show,
                    callback_data_update,
                    callback_data_delete,
                    callback_data_show_f,
                    callback_data_update_f,
                    callback_data_delete_f,
                    callback_data_show_un,
                    callback_data_update_un,
                    callback_data_delete_un,
                    folder_tmp,
                    folder_config,
                    folder_arc_input,
                    folder_arc_extract,
                    folder_arc_output,
                    folder_tmp_uncompressed)


class TelegramUsage:
    """
    class which is dedicated to work with telegram files
    """
    def __init__(self) -> None:
        self.image_parser = ImageParser()
        self.folder_current = os.getcwd()
        self.folder_tmp = os.path.join(self.folder_current, folder_tmp)
        self.folder_config = os.path.join(self.folder_current, folder_config)
        self.folder_arc_input = os.path.join(self.folder_current, folder_arc_input)
        self.folder_arc_output = os.path.join(self.folder_current, folder_arc_output)
        self.folder_arc_extract = os.path.join(self.folder_current, folder_arc_extract)
        self.folder_tmp_unc = os.path.join(self.folder_current, folder_tmp_uncompressed)
        self.create_folder = lambda x: os.path.exists(x) or os.mkdir(x)
        self.create_name_tmp = lambda: f"{uuid4()}.jpg"
        self.create_name_unc = lambda x: f"{uuid4()}{x}"

    def store_info_file(self, value_id:int, value_name:str, value_id_message:int) -> None:
        """
        Method which is dedicated to stro file values in case of the 
        Input:  value_id = id of the user
                value_name = name which is required to send
                value_id_message = id of the message which is used here
        Output: we saved all neccessary values to the
        """
        self.create_folder(self.folder_config)
        file_location = os.path.join(self.folder_config, txt_sent)
        with open(file_location, "a+") as file_values:
            file_values.write(f"{value_id},{value_name},{value_id_message}\n")

    def make_file_output(self, file_path:str, file_name:str, file_name_output:str) -> set:
        """
        Method which is dedicated to create the zip file and sending to the client
        Input:  file_path = path to the image file which is required to sent
                file_name = name which was renamed
                file_name_output = name of output names
        Output: we created compressed archive with the pictures 
        """
        zip_name = f'{os.path.splitext(file_name_output)[0]}.zip'
        with zipfile.ZipFile(os.path.join(self.folder_config, zip_name), 'w') as zp:
            path_write = os.path.join(file_path, file_name)
            zp.write(path_write, os.path.basename(path_write))
        return zip_name, self.folder_config

    def delete_stored_info(self, value_id:int, value_name:str, value_id_message:int) -> None:
        """
        Method which is dedicated to delete from the file required values
        Input:  value_id = id of the user
                value_name = name of the file which was sent
                value_id_message = id of the message
        Output: neccessary value was removed from it
        """
        self.create_folder(self.folder_config)
        file_location = os.path.join(self.folder_config, txt_sent)
        if not os.path.exists(file_location):
            return
        with open(file_location) as value_file:
            lines_wrote = value_file.readlines()
        with open(file_location, "w") as value_file:
            for line in lines_wrote:
                if line.strip("\n") != f"{value_id},{value_name},{value_id_message}":
                    value_file.write(line)

    def detect_less_compressed(self, file_list:list) -> str:
        """
        Method which is dedicated to detect less compressed file out of them and
        Input:  file_list = list with the files
        Output: string of the least compressed file
        """
        value_lists = []
        for file_name in file_list:
            file_location = os.path.join(self.folder_tmp, file_name) 
            value_lists.append((os.stat(file_location).st_size, file_name, file_location))
        _, used_name, used_location = sorted(value_lists, key=lambda x: x[0])[-1]
        for _, file_name, file_location in value_lists:
            if file_name != used_name and file_location != used_location:
                os.remove(file_location)
        return used_name

    @staticmethod
    def detect_image_ext(value_name:str) -> bool:
        """
        Static method which is dedicated to work with the extention of the files
        Input:  value_name = name of selected files
        Output: True if it has image extention else False
        """
        return value_name.lower().endswith(list_image_ext)

    @staticmethod
    def detect_image_value(bytes_io:object) -> bool:
        """
        Method which is dedicated to detect the mage from the inserted bytes of the text
        Input:  bytes_io = bytes from the telegram which were sent via message
        Output: True if it is image else False
        """
        try:
            im = Image.open(io.BytesIO(bytes_io))
            im.verify()
            im.close()
            return True
        except Exception as e:
            return False

    @staticmethod
    def detect_image_archive(folder_file:str) -> bool:
        """
        Method which is dedicated to detect the mage from the inserted bytes of the text
        Input:  folder_file = full path to the file
        Output: True if it is image else False
        """
        try:
            im = Image.open(folder_file)
            im.verify()
            im.close()
            return True
        except Exception as e:
            return False

    @staticmethod
    def detect_archive_ext(value_name:str) -> bool:
        """
        Static method which is dedicated to check that inserted value can be an archieve
        Input:  value_name = name of the file which uer have been
        Output: boolean value which signifies archieve
        """
        return value_name.lower().endswith(list_archive_ext)

    def detect_archive_value(self, bytes_io:bytes, bytes_name:str) -> bool:
        """
        Method which is dedicated to check that 
        Input:  bytes_io = bytes of the file which is sent to the values
        Output: True if it is value
        """
        self.create_folder(self.folder_arc_input)
        file_loc = os.path.join(self.folder_arc_input, bytes_name)
        with open(file_loc, 'wb') as tst_bytes_io:
            tst_bytes_io.write(bytes_io)
        value_check = zipfile.is_zipfile(file_loc) or tarfile.is_tarfile(file_loc) or self.is_7zip(file_loc)
        os.remove(file_loc)
        return value_check

    @staticmethod
    def is_7zip(file_loc:str) -> bool:
        """
        Static method which is dedicated to work with a 
        Input:  file_loc = location to the file
        Output: True if it is a 7zip file or False if it is not
        """
        try:
            py7zr.SevenZipFile(file_loc, 'r')
            return True
        except Exception as e:
            return False

    def detect_compability_archive(self, value_file_name:str) -> set:
        """
        Method which is dedicated to compare archives
        Input:  value_file_name = name of the file which is dedicated
        Output: boolean value which signifies that wee ned to use everything and path to the file
        """
        def extract_zip(file_extract:str, file_loc:str):
            """
            Function to extract zip archive
            Input:  file_extract = path where to store the 
                    file_loc = path to the file of the
            Output: we extracted values
            """
            with zipfile.ZipFile(file_loc) as archive:
                archive.extractall(file_extract)

        def extract_rar(file_extract:str, file_loc:str):
            """
            Function to extract rar archive
            Input:  file_extract = path where to store the 
                    file_loc = path to the file of the
            Output: we extracted values
            """
            with tarfile.TarFile(file_loc) as archive:
                archive.extractall(file_extract)

        def extract_7z(file_extract:str, file_loc:str):
            """
            Function to extract 7z archive
            Input:  file_extract = path where to store the 
                    file_loc = path to the file of the
            Output: we extracted values
            """
            with py7zr.SevenZipFile(file_loc) as archive:
                archive.extractall(file_extract)

        self.create_folder(self.folder_arc_input)
        self.create_folder(self.folder_arc_extract)

        file_folder = [f for f in os.listdir(self.folder_arc_input) if os.path.splitext(f)[0]==value_file_name][0]
        file_loc = os.path.join(self.folder_arc_input, file_folder)
        file_extract = os.path.join(self.folder_arc_extract, value_file_name)
        try:
            if zipfile.is_zipfile(file_loc):
                extract_zip(file_extract, file_loc)
            elif tarfile.is_tarfile(file_loc):
                extract_rar(file_extract, file_loc)
            elif self.is_7zip(file_loc):
                extract_7z(file_extract, file_loc)
            return True, value_file_name
        except Exception as e:
            return False, ''
        return False, ''

    def remove_unnecessary(self, folder_value:str) -> list:
        """
        Method which is dedicated to remove unneccessary values
        Input:  folder_value = folder which is required to see
        Output: we removed unnecessary values and returned list with the values
        """
        folder_required = []
        self.create_folder(self.folder_arc_extract)
        folder_check = os.path.join(self.folder_arc_extract, folder_value)
        for folder_values, _, folder_files in os.walk(folder_check):
            for folder_file in folder_files:
                folder_loop = os.path.join(folder_values, folder_file)
                if not (self.detect_image_ext(folder_loop) and self.detect_image_archive(folder_loop)):
                    os.remove(folder_loop)
                else:
                    folder_required.append(folder_loop)
        return folder_required

    def detect_usage_location(self, value_name_ext:str, value_type:str) -> set:
        """
        Method which is dedicated to return set with name and its folder
        Input:  value_name_ext = name of the temporary value without ext
                value_type = type of the inserted value
        Output: returned name and it's path
        """
        if value_type in [callback_data_show, callback_data_update, callback_data_delete]:
            for value_name in os.listdir(self.folder_tmp):
                if os.path.splitext(value_name)[0] == value_name_ext:
                    return value_name, self.folder_tmp
        if value_type in [callback_data_show_un, callback_data_update_un, callback_data_delete_un]:
            for value_name in os.listdir(self.folder_tmp_unc):
                if os.path.splitext(value_name)[0] == value_name_ext:
                    return value_name, self.folder_tmp_unc
    
    def produce_message_photo_text(self, value_type:str) -> str:
        """
        Method which is dedicated to create the output text and 
        Input:  value_type = type value of the inserted by user command
        Output: text which is required to be returned
        """
        if value_type == callback_data_update:
            return "We've updated values of the picture which was sent and compressed"
        if value_type == callback_data_delete:
            return "We checked the image and removed the metatags in additional cases"
        if value_type == callback_data_show:
            return "Let's see the values of the metatags of the analysed image"
        if value_type == callback_data_update_un:
            return "We've updated values to a unencrypted values of the images and sent you back"
        if value_type == callback_data_delete_un:
            return "We checked the uncompressed image and removed the metatags in additional cases"
        if value_type == callback_data_show_un:
            return "Let's see the values of the metatags of the analysed uncompressed image"
        return "Check values"
        
    def produce_file_update(self, image_folder_path:str, image_name:str) -> str:
        """
        Method which is dedicated to update file with selected metatags
        Input:  image_folder_path = folder where this file is located
                image_name = name of the file
        Output: name of the selected 
        """
        value_ext = os.path.splitext(image_name)[-1]
        new_name = self.create_name_unc(value_ext)
        self.image_parser.produce_file_update(image_name, image_folder_path, image_folder_path, new_name)
        print(f"Deleting {image_name}")
        os.remove(os.path.join(image_folder_path, image_name))
        return new_name

    def produce_file_showings(self, image_folder_path:str, image_name:str) -> str:
        """
        Method which is dedicated to check the file and to return the string to the printing
        Input:  image_folder_path = path to the selected images
                image_name = nema of the image to open
        Output: string which is dedicated to print
        """
        value_json = self.image_parser.produce_analysis(image_name, image_folder_path)
        value_showings = '\n'.join([f"{key} ----------> {value}" for key, value in value_json.items()])
        if value_showings:
            return value_showings
        return 'Unfortunatelly, file cannot provide any metatags'

    def produce_file_delete(self, image_folder_path:str, image_name:str) -> str:
        """
        Method which is dedicated to delete metatags
        Input:  image_folder_path = folder where image was stored
                image_name = name of the file
        Output: name of the new file
        """
        value_ext = os.path.splitext(image_name)[-1]
        new_name = self.create_name_unc(value_ext)
        self.image_parser.produce_file_delete(image_name, image_folder_path, image_folder_path, new_name)
        print(f"Deleting {image_name}")
        os.remove(os.path.join(image_folder_path, image_name))
        return new_name

    def save_tmp_archive(self, bytes_io:bytes, value_ext:str='') -> str:
        """
        Method which is dedicated to save temporal archive to the server part
        Input:  bytes_io = bytes of the sent file inside
                value_ext= file extention of the inserted file
        Output: we successfully saved the archive to the directory and returned file name of it
        """
        value_name_new = f"{self.create_name_unc('')}{value_ext}"
        value_location = os.path.join(self.folder_arc_input, value_name_new)
        with open(value_location, 'wb') as bytes_arc:
            bytes_arc.write(bytes_io)
        return value_name_new

    def save_tmp_file(self, bytes_io:bytes, value_compressed:bool=True, value_ext:str='') -> str:
        """
        Method which is dedicated to save the compressed picture from the telegram
        Input:  bytes_io = byte value of the sent picture
                value_compressed = boolaen variable which signifies that 
        Output: we successfully saved temporary image and returned name of it
        """
        new_image = Image.open(io.BytesIO(bytes_io))
        folder_used = self.folder_tmp if value_compressed else self.folder_tmp_unc
        if value_compressed and not value_ext: 
            value_name = self.create_name_tmp()
        else: 
            value_name = self.create_name_unc(value_ext)
        self.create_folder(folder_used)
        new_image.save(os.path.join(folder_used, value_name))
        return value_name


if __name__ == '__main__':
    a = TelegramUsage()
    a.make_file_output('E:\Projects\\folder_metadata\img_input', 'photo_2021-06-25_13-27-25.jpg', 'tst')