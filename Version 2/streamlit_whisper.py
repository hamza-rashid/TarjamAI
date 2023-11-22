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

# Set OpenAI API Key's (hidden)
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

# upload audio and srt file with streamlit
video_file = st.file_uploader("Upload Video", type=["mp4", "m4a"])

placeholder = st.empty()
with placeholder.container():
    stock_images_list = load_stock_photos("./stock_images")
    img = image_select("Choose your video background", stock_images_list)

if video_file is not None:
    if video_file.name.endswith('mp4'):
        #placeholder.empty()

        # Open the file-like object as bytes and read it with BytesIO
        input_video = BytesIO(video_file.read())

        # Get the bytes of the video to display it
        display_video = input_video.read()

        # Display the video using st.video
        st.video(display_video)

    
if st.button("Create subtitles"):
    if video_file is not None and video_file.name.endswith('mp4'):
        # Update progress bar
        my_bar = st.progress(0, text="Lets go! 🚀 ")

        video_content = BytesIO(video_file.read())

        my_bar.progress(20, text="Transcribing your video!")

        my_bar.progress(30, text="Transcribing your video! 🚀")

        my_bar.progress(40, text="Transcribing your video! 🚀")

        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
            f.write(display_video)
            f.flush()

            with open(f.name, 'rb') as file:
            
            # Call openai API to transcribe the file
                response = openai.Audio.transcribe(
                        model='whisper-1',
                        file=file,
                        response_format='vtt',
                        language='ar',
                        prompt='This is a quran recitation in arabic'
                        )
                my_bar.progress(50, text="Transcribing your video! 🚀")

                vtt_content = response

                    # Save the API output string as a VTT file
                with open('transcription.vtt', 'w') as v:
                    v.write(vtt_content)

                    my_bar.progress(60, text="Transcription done✅ Now adding subtitles to your video!⏳ ")
                        # Start transloadit adding subtitles
                    tl = client.Transloadit('0d8f65ea184648c69a259928afab7c80', '0b3a3e5b3717429cbf390e2a1885e12bcd505716')
                    assembly = tl.new_assembly({
                        'template_id': 'd011d4497b034b9eb759f4e6662417e1'
                        })

                        # Add files to upload
                    assembly.add_file(file)
                    assembly.add_file(open(img, "rb"))
                    assembly.add_file(v)

                    my_bar.progress(65, text="Transcription done✅ Now adding subtitles to your video!⏳ ")    

                        # Start the Assembly
                    assembly_response = assembly.create(retries=5, wait=True)

                    my_bar.progress(70, text="Almost there!🥳")   
                    

                    st.video(assembly_response.data.get('assembly_ssl_url'))
                    st.text(assembly_response.data.get('assembly_ssl_url'))
                    
                    my_bar.progress(100, text="Enjoy 😊🤲🏼 ")   

                        # Delete temporary file
                    os.unlink(f.name)

    elif video_file is not None and video_file.name.endswith('mp4') == False:
        # Make Temporary file to store the video in 
        with tempfile.NamedTemporaryFile(suffix='.m4a', delete=False) as f:
            f.write(video_file.read())
            f.flush()

            my_bar = st.progress(0, text="Lets go! 🚀 ")
            
            # Open the temporary file 
            with open(f.name, 'rb') as file:

                # Load the audio file
                audio_clip = AudioFileClip(file.name)

                # Load the static image
                image_clip = ImageClip(img)

                # Use set_audio method from image clip to combine the audio with the image
                video_clip = image_clip.set_audio(audio_clip)

                # Set the duration of the video to be the same as the audio duration
                video_clip.duration = audio_clip.duration

                # Set FPS to 1
                video_clip.fps = 1

                # Create a temporary file to save the result
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file_combined:
                    
                    # Get the file path string
                    temp_file_combined_path = temp_file_combined.name
                    
                    my_bar.progress(20, text="Creating a video background!")

                    # Write the result to the temporary file
                    video_clip.write_videofile(temp_file_combined_path, codec='mpeg4', audio_codec='aac', bitrate='100k')

                    display_file = open(temp_file_combined_path, 'rb')
                    display_bytes = display_file.read()
                    video_content = display_bytes




                    # Delete temporary file
                    os.unlink(f.name)
                    my_bar.progress(30, text="Transcribing your audio!")

                # Make Temporary file to store the video in 
                with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as s:
                    s.write(video_content)
                    s.flush()
                
                    my_bar.progress(40, text="Transcribing your audio! 🚀")

                    # Open the temporary file 
                    with open(s.name, 'rb') as fileio:

                        # Call the moviepy package to get the height and width of the video
                        clip = VideoFileClip(fileio.name)

                        # So we don't resize the video too small
                        if clip.w/2 or clip.h/2 < 500:
                            width = clip.w
                            height = clip.h
                            
                        else:
                            width = clip.w/2
                            height = clip.h/2
                        
                        my_bar.progress(50, text="Transcribing your audio! 🚀")

                        # Call openai API to transcribe the file
                        response = openai.Audio.transcribe(
                            model='whisper-1',
                            file=fileio,
                            response_format='vtt',
                            language='ar',
                            prompt='This is a quran recitation in arabic'
                            )
                    vtt_content = response
                    st.text(vtt_content)
                    st.text(video_content)
                    
                    # Delete temporary file
                    os.unlink(s.name)

                    my_bar.progress(60, text="Adding subtitles to your video! Almost there...")
                
                    # Encode the API output string into bytes    
                    vtt_bytes = vtt_content.encode()

                    # css styling to center the div
                    st.markdown(
                        """
                        <style>
                        .center {
                        display: flex;
                        justify-content: center;
                        }
                        </style>
                        """, unsafe_allow_html=True
                    )

                    my_bar.progress(80, text="Adding subtitles to your video! 🎬 🖍️ Almost there...")    

                    # html video player that adds VTT file to video file
                    components.html(f"""
                        <div class="center">
                        <video id="transcribed_video" width="{width}" height="{height}" controls>
                        <source src="data:video/mp4;base64,{base64.b64encode(video_content).decode()}" type="video/mp4">
                        <track label="Arabic" kind="subtitles" srclang="ar" src="data:text/vtt;base64,{base64.b64encode(vtt_bytes).decode()}" default>
                        </video>    
                        </div>
                    """, width=width, height=height)

                    my_bar.progress(100, text="Enjoy 😊🤲🏼 ")  
else:
    st.stop()

