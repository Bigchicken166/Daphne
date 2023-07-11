import os
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import json
import requests
import random
import replicate
from flask import Flask, request, jsonify, render_template
from flask import Flask
from werkzeug.utils import secure_filename

from flask_cors import CORS

modelText = replicate.models.get("openai/whisper")
versionText = modelText.versions.get("30414ee7c4fffc37e260fcab7842b5be470b9b840f2b608f5baa9bbef9a259ed")

modelImage = replicate.models.get("stability-ai/stable-diffusion-img2img")
version = modelImage.versions.get("15a3689ee13b0d2616e98820eca31d4c3abcd36672df6afce5cb6feb1d66087d")


# Our Host URL should not be prepended with "https" nor should it have a trailing slash.
os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

# Sign up for an account at the following link to get an API Key.
# https://beta.dreamstudio.ai/membership

# Click on the following link once you have created an account to be taken to your API Key.
# https://beta.dreamstudio.ai/membership?tab=apiKeys

# Paste your API Key below.

os.environ['STABILITY_KEY'] = 'sk-fbGJkF5x2MHX3l6no1A5qCoDOoFC46Lz16mP2YIv2IUjDI3O'

# Set up our connection to the API.
stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'], # API Key reference.
    verbose=True, # Print debug messages.
    engine="stable-diffusion-768-v2-0", # Set the engine to use for generation.
)

def generaImg(texto):
	# Set up our initial generation parameters.
	seed=random.randint(1,1000000000)
	##seed=3376651455
	img=Image.open("/home/jlopez/salida/img2.png")
	answers = stability_api.generate(
	    prompt=texto,
	    init_image=img,
	    seed=seed, # If a seed is provided, the resulting generated image will be deterministic.
	                    # What this means is that as long as all generation parameters remain the same, you can always recall the same image simply by generating it again.
	                    # Note: This isn't quite the case for Clip Guided generations, which we'll tackle in a future example notebook.
	    steps=50, # Step Count defaults to 50 if not specified here.
	    cfg_scale=7.0, # Influences how strongly your generation is guided to match your prompt.
	                   # Setting this value higher increases the strength in which it tries to match your prompt.
	                   # Defaults to 7.0 if not specified.
	    width=512, # Generation width, defaults to 512 if not included.
	    height=512, # Generation height, defaults to 512 if not included.
        ##sampler=generation.SAMPLER_K_DPM_2_ANCESTRAL,
        start_schedule=0.8, 
        ### guidance_strength=0.8,
            ###sampler = 'k_euler' ,
	    samples=1, # Number of images to generate, defaults to 1 if not included.
	    ##sampler=generation.K_LMS # Choose which sampler we want to denoise our generation with.
	                                                 # Defaults to k_lms if not specified. Clip Guidance only supports ancestral samplers.
	                                                 # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_lms)
	)

	# Set up our warning to print to the console if the adult content classifier is tripped.
	# If adult content classifier is not tripped, save generated images.
	for resp in answers:
	    for artifact in resp.artifacts:
	        if artifact.finish_reason == generation.FILTER:
	            warnings.warn(
	                "Your request activated the API's safety filters and could not be processed."
	                "Please modify the prompt and try again.")
	        if artifact.type == generation.ARTIFACT_IMAGE:
	            img = Image.open(io.BytesIO(artifact.binary))
	            img.save("/var/www/html/resultados/"+str(artifact.seed)+ ".png") # Save our generated images with their seed number as the filename

	return "/resultados/"+str(artifact.seed)+ ".png"

app = Flask(__name__)
cors = CORS(app)

app.config['UPLOAD_FOLDER']="/var/www/html/audios"


@app.route('/upload')
def upfile():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save("/var/www/html/audios/"+secure_filename(f.filename))
      url="http://137.184.177.230/audios/"+secure_filename(f.filename)
      output = versionText.predict(audio=url)
      return json.dumps(output)


@app.route('/api/genimg', methods=['GET', 'POST'])
def add_message():
    content = request.json
    ##json_object = json.loads(content)
    print(content)
    texto=content['frase']
    ##path = generaImg(texto)
    ##output = version.predict(prompt=texto)
    output = version.predict(prompt=texto,image="http://137.184.177.230/img2.png")
    ##return '{"path":"'+path+'"}'
    print(json.dumps(output))
    return('{"path":"'+output[0]+'"}')
    

@app.route('/api/gentext', methods=['GET', 'POST'])
def add_text():
    content = request.json
    ##json_object = json.loads(content)
    print(content)
    url=content['url']
    output = versionText.predict(audio=url)
    return json.dumps(output)

@app.route('/api/fileupload', methods = ['GET','POST'])  
def trasncribe():  
    if request.method == 'POST':  
        f = request.files['file']
        f.save("/var/www/html/audios/"+f.filename)
        output = versionText.predict(audio="http://137.184.177.230/audio/"+ f.filename)
        return json.dumps(output)


app.run(host='0.0.0.0', port=8080)

