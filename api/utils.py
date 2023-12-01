import subprocess
from .models import Video, Nerf, NerfModel, NerfObject
from celery import shared_task

@shared_task
def generate_nerf_model(nerf: NerfModel, video: Video) -> None:
    """
    given a nerf and a video, generate a model with nerfstudio
    """
    nerf = Nerf.objects.get(id=nerf_id)
    if nerf:
        

    try:
        # revisar y extraer nombre del nerf
        video = Video.objects.get(id=video_id)
        subprocess.run(['python', 'ruta/a/tu/script.py', nerf, video.archivo.path])
        Modelo.objects.create(video=video, archivo='ruta/al/modelo_generado.obj')
    except Exception as e:
        print(f"Error al generar el modelo: {e}")

@shared_task
def generate_nerf_object(nerf_model_id: int) -> None:
    try:

        modelo = NerfModel.objects.get(id=nerf_model_id)
        subprocess.run(['python', 'ruta/a/tu/otro_script.py', modelo.archivo.path])
        Objeto.objects.create(modelo=modelo, archivo='ruta/al/objeto_generado.obj')
    except Exception as e:
        print(f"Error al generar el objeto: {e}")
        return None

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