import os
import piexif

bot_key = 'a'

ifd_zeroth = {
            piexif.ImageIFD.Make: u"Our daddy told us not to be ashamed of our dicks",
            piexif.ImageIFD.XResolution: (300, 1),
            piexif.ImageIFD.YResolution: (300, 1), 
            piexif.ImageIFD.Software: u"Sorry for what?"
            }

ifd_exif = {
            piexif.ExifIFD.DateTimeOriginal: u"2077:99:99 44:44:00",
            piexif.ExifIFD.LensMake: u"I'm sorry",
            piexif.ExifIFD.Sharpness: 300,
            piexif.ExifIFD.LensSpecification: ((1, 1), (1, 1), (1, 1), (1, 1)),
            }
ifd_gps = {
           piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
           piexif.GPSIFD.GPSAltitudeRef: 1,
           piexif.GPSIFD.GPSDateStamp: u"2000:99:99 44:44:00",
           }
ifd_first = {
             piexif.ImageIFD.Make: u"I rip the skin",
             piexif.ImageIFD.XResolution: (300, 1),
             piexif.ImageIFD.YResolution: (300, 1),
             piexif.ImageIFD.Software: u"Hhhhmmmm"
             }

json_name = 'settings.json'
json_keys_default = {"0th": ifd_zeroth, "Exif": ifd_exif, "GPS": ifd_gps, "1st": ifd_first, "thumbnail": None}

folder_config = 'config'
folder_img = 'img_input'
folder_out = 'img_output'

description = 'This is a module to deal with the images and their metadata'
args_deletion_necessary = ('-n', '--necessary', 'argument which is dedicated to delete original images after the work with them', 'store_true', False)
args_update_json = ('-u', '--update', 'argument which is dedicated to update the json value from the config', 'store_true', False)
args_analyse_pictures = ('-a', '--analyse', 'argument which is dedicated to analyse pictures of the inserted and return values to the file', 'store_true', False)
args_change_meta = ('-c', '--change', 'argument which is dedicated to remove the metadata and change to json values', 'store_true', False)
args_delete_meta = ('-d', '--delete', 'argument which is dedicated to remove all metadata', 'store_true', False)
args_use_selected = ('-s', '--selected', 'argument which is dedicated to use only selected', str, False, '')