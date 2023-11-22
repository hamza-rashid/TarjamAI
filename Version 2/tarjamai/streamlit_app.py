import streamlit as st
import streamlit.components.v1 as components
from moviepy.editor import * #pip install moviepy
from moviepy.video.io.ffmpeg_reader import FFMPEG_VideoReader
from moviepy.editor import *
import base64
import openai
import os
import tempfile
from streamlit_image_select import image_select
from PIL import Image
from io import BytesIO 
from transloadit import client





#from moviepy.tools import cvsecs
#from moviepy.video.tools.subtitles import SubtitlesClip
#import arabic_reshaper # pip install arabic-reshaper
#from bidi.algorithm import get_display # pip install python-bidi


# Set OpenAI API Key's (hidden)
API_KEY = os.environ.get('API_KEY')
AUTH_KEY = os.environ.get('TRANSLOADIT_AUTH_KEY')
openai.api_key = API_KEY


image_dir = "./stock_images"
stock_images_list = [os.path.join(image_dir, file) for file in os.listdir(image_dir) if file.endswith('.jpg')]


# Load stock photos - cached
@st.cache_data(experimental_allow_widgets=True)
def load_stock_photos(image_dir):
    image_dir = image_dir
    stock_images_list = [os.path.join(image_dir, file) for file in os.listdir(image_dir) if file.endswith('.jpg')]
    return stock_images_list 


st.title('🚀 Tarjam.ai')

components.html("""



<link href="https://releases.transloadit.com/uppy/v3.6.1/uppy.min.css" rel="stylesheet" />
<button id="browse">Select Files</button>
<div id="player"></div>
<script type="module">
  import {
    Uppy,
    Dashboard,
    ImageEditor,
    RemoteSources,
    Transloadit,
  } from 'https://releases.transloadit.com/uppy/v3.6.1/uppy.min.mjs'

  const player = document.getElementById('player')
  const uppy = new Uppy()
    .use(Transloadit, {
      waitForEncoding: true,
      alwaysRunAssembly: true,
      params: {
        auth: {
          key: '%s',
        },
        steps: {
          ":original": {
            "robot": "/upload/handle"
          },
              "audio_from_video_extracted": {
              "use": ":original",
              "robot": "/video/encode",
              "result": true,
              "preset": "mp3",
              "ffmpeg_stack": "v3.3.3",
              "rotate": false,
              "ffmpeg": {
                "vn": true,
                "codec:v": "none",
                "map": [
                  "0",
                  "-0:d?",
                  "-0:s?",
                  "-0:v?"
                ]
              }
            }
        },
      },
    })
    .use(Dashboard, { trigger: '#browse' })
    .use(ImageEditor, { target: Dashboard })
    .use(RemoteSources, {
      companionUrl: 'https://api2.transloadit.com/companion',
    })
    .on('complete', ({ transloadit }) => {
      transloadit.forEach((assembly) => {
        const url = assembly.results.audio_from_video_extracted[0].ssl_url
        console.log(url)
        player.innerHTML = `<video width="320" height="240" controls><source src="${url}" type="video/mp4"></video>`
      })
    })
    .on('error', (error) => {
      console.error(error)
    })
    
</script>



"""%AUTH_KEY, width = 300, height = 300)