import os
# from doten

bot_key = 'a'

json_name = 'settings.json'
json_keys_default = {'Location': 'Pizda', 'Truth': 'Da', 'Width': 300, 'Height': -300}

folder_config = 'config'
folder_img = 'img_input'
folder_out = 'img_output'

description = 'This is a module to deal with the images and their metadata'
args_deletion_necessary = ('-n', '--necessary', 'argument which is dedicated to delete original images after the work with them', 'store_true', False)
args_update_json = ('-u', '--update', 'argument which is dedicated to update the ', 'store_true', False)
args_analyse_pictures = ('-a', '--analyse', 'argument which is dedicated to analyse pictures of the inserted and return values to the file', 'store_true', False)
args_change_meta = ('-c', '--change', 'argument which is dedicated to remove the metadata and change to selected values', 'store_true', False)
args_delete_meta = ('-d', '--delete', 'argument which is dedicated to remove all metadata', 'store_true', False)
args_use_selected = ('-s', '--selected', 'argument which is dedicated to use only selected', str, False, '')