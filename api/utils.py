import subprocess
from .models import User, Video, Nerf, NerfModel, NerfObject
from celery import shared_task

@shared_task
def generate_nerf_model(nerf: Nerf, video: Video, user: User, nerf_model_id: int) -> None:
    
    try:
        
        # run command
        result = subprocess.run(['python', 'ruta/a/tu/otro_script.py', modelo.archivo.path])
        
        # get nerf_model after result
        nerf_model = NerfModel.objects.get(id=nerf_model_id)

        if result.returncode == 0:
            nerf_model.status = 'complete'
        else:
            nerf_model.status = 'failed'
            print("[GENERATE_MODEL_TASK]: RETCODE ERROR (not 0)")
        
        nerf_model.save_endtime()

    except Exception as e:

        nerf_model = NerfModel.objects.get(id=nerf_model_id)
        nerf_model.status = 'failed'
        nerf_model.save_endtime()
        print("[GENERATE_MODEL_TASK]: ERROR")
        print('-- GENERATE_NERF_MODEL EXCEPTION START --')
        print(err)
        print('-- GENERATE_NERF_MODEL EXCEPTION END --')

@shared_task
def generate_nerf_object(nerf_model: NerfModel, user: User, nerf_object_id: int, method: str = 'TSDF') -> None:

    try:
        
        # run command
        result = subprocess.run(['python', 'ruta/a/tu/otro_script.py', modelo.archivo.path])
        
        # get nerf_object after result
        nerf_object = NerfObject.objects.get(id=nerf_object_id)

        if result.returncode == 0:
            nerf_object.status = 'complete'
        else:
            nerf_object.status = 'failed'
            print("[GENERATE_OBJECT_TASK]: RETCODE ERROR (not 0)")
        
        nerf_object.save_endtime()

    except Exception as e:

        nerf_object = NerfObject.objects.get(id=nerf_object_id)
        nerf_object.status = 'failed'
        nerf_model.save_endtime()
        print("[GENERATE_OBJECT_TASK]: ERROR")
        print('-- GENERATE_NERF_OBJECT EXCEPTION START --')
        print(err)
        print('-- GENERATE_NERF_OBJECT EXCEPTION END --')

import requests
from bs4 import BeautifulSoup
import json

METHODS_URL = 'https://docs.nerf.studio/nerfology/methods/'

def get_nerfs() -> [dict]:

    response = requests.get(METHODS_URL)
    if response.status_code == 200:

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        methods = soup.select('div.toctree-wrapper ul li')
        nerfs = []

        for method in methods:

            method_a_tag = method.find('a')
            method_url = METHODS_URL + method_a_tag['href']

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

        print("Success")
        return nerfs

    else:
        print(f"Error while scrapping, code: {response.status_code}")
        return {}