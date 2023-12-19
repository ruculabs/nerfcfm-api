import subprocess
from .models import User, Data, ProcessedData, ExportMethod, Nerf, NerfModel, NerfObject
from celery import shared_task
import os
from dotenv import load_dotenv

from django.core.files import File

load_dotenv()

ACTIVATE_NERF_STUDIO_COMMAND = "conda activate nerfstudio"
# ACTIVATE_FFMPEG = 'export PATH="$HOME/ffmpeg_build/bin:$PATH"'

@shared_task
def generate_processed_data(data: dict, processed_data_id: int) -> None:

    print(data)
    user_id = data.get('user')
    data_id = data.get('data')

    user = User.objects.get(id=user_id)
    data = Data.objects.get(id=data_id)

    processed_data = ProcessedData.objects.get(id=processed_data_id)
    
    try:

        process_command = None
        if(os.getenv("USE_TEST_SCRIPT")):
            process_command = ['python', 'api/scripts/test_process_data.py', os.getenv("MAX_TIME_SCRIPT"), os.getenv("MIN_TIME_SCRIPT"), str(processed_data.id)]
        else:
            data_path = data.data_file.name
            data_name = data_path.split("/")[-1]
            ns_process_data_command = f"ns-process-data video --data media/data/{data_name}/ --output-dir media/processed_data/{processed_data_id}/"
            process_command = f"{ACTIVATE_NERF_STUDIO_COMMAND} && {ns_process_data_command}"
        
        process_data_result = subprocess.run(process_command)
        
        if process_data_result.returncode == 0:
                processed_data.status = 'complete'
                print("[PROCESS_DATA_TASK]: SUCCESS")
        else:
                processed_data.status = 'failed'
                print("[PROCESS_DATA_TASK]: RETCODE ERROR (not 0)")
            
        processed_data.save_endtime()

    except Exception as e:

        processed_data.status = 'failed'
        processed_data.save_endtime()
        print("[PROCESS_DATA_TASK]: ERROR")
        print('-- PROCESS_DATA EXCEPTION START --')
        print(e)
        print('-- PROCESS_DATA EXCEPTION END --')

@shared_task
def generate_nerf_model(data: dict, nerf_model_id: int) -> None:

    print(data)
    processed_data_id = data.get('processed_data')
    nerf_id = data.get('nerf')
    user_id = data.get('user')

    user = User.objects.get(id=user_id)
    nerf = Nerf.objects.get(id=nerf_id)
    processed_data = ProcessedData.objects.get(id=processed_data_id)

    nerf_model = NerfModel.objects.get(id=nerf_model_id)
    
    try:

        train_command = None
        if(os.getenv("USE_TEST_SCRIPT")):
            train_command = ['python', 'api/scripts/test_nerf_model.py', os.getenv("MAX_TIME_SCRIPT"), os.getenv("MIN_TIME_SCRIPT"), str(nerf_model.id)]
        else:
            ns_train_command = f"ns-train nerfacto --data media/processed_data/{processed_data_id}/ --output-dir media/nerf_models/{nerf_model_id}/ --viewer.quit-on-train-completion True"          
            train_command = f"{ACTIVATE_NERF_STUDIO_COMMAND} && {ns_train_command}"

        train_result = subprocess.run(train_command)
        
        if train_result.returncode == 0:
            nerf_model.status = 'complete'
            print("[GENERATE_MODEL_TASK]: SUCCESS")
        else:
            nerf_model.status = 'failed'
            print("[GENERATE_MODEL_TASK]: RETCODE ERROR (not 0)")
    
        nerf_model.save_endtime()

    except Exception as e:

        nerf_model.status = 'failed'
        nerf_model.save_endtime()
        print("[GENERATE_MODEL_TASK]: ERROR")
        print('-- GENERATE_NERF_MODEL EXCEPTION START --')
        print(e)
        print('-- GENERATE_NERF_MODEL EXCEPTION END --')

@shared_task
def generate_nerf_object(data: dict, nerf_object_id: int) -> None:

    print(data)
    nerf_model_id = data.get('nerf_model')
    export_method_id = data.get('export_method')
    user_id = data.get('user')

    user = User.objects.get(id=user_id)
    export_method = ExportMethod.objects.get(id=export_method_id)
    nerf_model = NerfModel.objects.get(id=nerf_model_id)

    nerf_object = NerfObject.objects.get(id=nerf_object_id)
    
    try:

        export_command = None
        if(os.getenv("USE_TEST_SCRIPT")):
            export_command = ['python', 'api/scripts/test_nerf_object.py', os.getenv("MAX_TIME_SCRIPT"), os.getenv("MIN_TIME_SCRIPT"), str(nerf_object.id)]
        else:
            ns_export_command = f"ns-export {export_method.name} --data media/nerf_models/{nerf_model_id}/{nerf_model.nerf.name}/{nerf}/ --output-dir media/nerf_objects/{nerf_object_id}/"
            export_command = f"{ACTIVATE_NERF_STUDIO_COMMAND} && {ns_export_command}"
        
        export_result = subprocess.run(export_command)
            
        if export_result.returncode == 0:
            nerf_object.object_file.save('mesh.obj', 
                                File(open(f'media/nerf_objects/{nerf_object_id}/mesh.obj', 'rb')), 
                                save=True)
            nerf_object.texture_file.save('material_0.png', 
                                File(open(f'media/nerf_objects/{nerf_object_id}/material_0.png', 'rb')), 
                                save=True)
            nerf_object.material_file.save(f'material_0.mtl', 
                                File(open(f'media/nerf_objects/{nerf_object_id}/material_0.mtl', 'rb')), 
                                save=True)
            nerf_object.status = 'complete'
            print("[GENERATE_OBJECT_TASK]: SUCCESS")
        else:
            nerf_object.status = 'failed'
            print("[GENERATE_OBJECT_TASK]: RETCODE ERROR (not 0)")
            
        nerf_object.save_endtime()
            
    except Exception as e:

        nerf_object.status = 'failed'
        nerf_object.save_endtime()
        print("[GENERATE_OBJECT_TASK]: ERROR")
        print('-- GENERATE_NERF_OBJECT EXCEPTION START --')
        print(e)
        print('-- GENERATE_NERF_OBJECT EXCEPTION END --')

import requests
from bs4 import BeautifulSoup
import json

NERF_METHODS_URL = 'https://docs.nerf.studio/nerfology/methods/'

def get_nerfs() -> [dict]:

    response = requests.get(NERF_METHODS_URL)
    if response.status_code == 200:

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        methods = soup.select('div.toctree-wrapper ul li')
        nerfs = []

        for method in methods:

            method_a_tag = method.find('a')
            method_url = NERF_METHODS_URL + method_a_tag['href']

            method_url_response = requests.get(method_url)
            if method_url_response.status_code == 200:

                method_html = method_url_response.text
                method_soup = BeautifulSoup(method_html, 'html.parser')

                long_name_tag = method_soup.find('h4')
                if long_name_tag:

                    nerf_info = {
                        'name': method.text.strip(),
                        'long_name': long_name_tag.text.strip(),
                        'url': method_url
                    }
                    nerfs.append(nerf_info)

        print(json.dumps(nerfs, indent=4, ensure_ascii=True))
        return nerfs

    else:
        print(f"Error while scrapping, code: {response.status_code}")
        return []

DATA_TYPES_URL = 'https://docs.nerf.studio/quickstart/custom_dataset.html'

def get_data_types() -> [dict]:

    response = requests.get(DATA_TYPES_URL)
    if response.status_code == 200:

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        data_types = soup.select('table.docutils tbody tr')

        data_types_list = []

        for data_type in data_types:

            columns = data_type.find_all('td')

            if len(columns) >= 4:
                name = columns[0].text.strip()
                capture_device = columns[1].text.strip()
                requirements = columns[2].text.strip()
                ns_process_data_speed = columns[3].text.strip()

                data_type_info = {
                    'name': name,
                    'capture_device': capture_device,
                    'requirements': requirements,
                    'ns_process_data_speed': ns_process_data_speed,
                }

                data_types_list.append(data_type_info)

        print(json.dumps(data_types_list, indent=4, ensure_ascii=True))
        return data_types_list

    else:
        print(f"Error while scrapping, code: {response.status_code}")
        return []
