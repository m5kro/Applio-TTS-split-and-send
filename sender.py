import os
from gradio_client import Client
import wave

# Function to read text from a file
def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to process each text file in the folder
def process_text_files(folder_path, output_folder_path, tts_voice, tts_rate, f0_up_key, filter_radius, index_rate, rms_mix_rate, protect, hop_length, f0_method, pth_path, index_path, split_audio, f0_autotune, clean_audio, clean_strength, export_format, embedder_model, embedder_model_custom, upscale_audio, f0_file, api_name):
    # Initialize the client
    client = Client("http://127.0.0.1:6969/")
    
    # List all text files in the specified folder
    text_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    output_wav_files = []
    
    for text_file in text_files:
        text_file_path = os.path.join(folder_path, text_file)
        
        # Read the text from the file
        tts_text = read_text_from_file(text_file_path)
        
        # Set output file paths
        base_name = os.path.splitext(text_file)[0]
        output_tts_path = os.path.join(output_folder_path, f"{base_name}_tts_output.wav")
        output_rvc_path = os.path.join(output_folder_path, f"{base_name}.wav")
        output_wav_files.append(output_rvc_path)
        
        # Call the predict function with the text read from the file
        client.predict(
          tts_text=tts_text,
          tts_voice=tts_voice,
          tts_rate=tts_rate,
          f0_up_key=f0_up_key,
          filter_radius=filter_radius,
          index_rate=index_rate,
          rms_mix_rate=rms_mix_rate,
          protect=protect,
          hop_length=hop_length,
          f0_method=f0_method,
          output_tts_path=output_tts_path,
          output_rvc_path=output_rvc_path,
          pth_path=pth_path,
          index_path=index_path,
          split_audio=split_audio,
          f0_autotune=f0_autotune,
          clean_audio=clean_audio,
          clean_strength=clean_strength,
          export_format=export_format,
          embedder_model=embedder_model,
          embedder_model_custom=embedder_model_custom,
          upscale_audio=upscale_audio,
          f0_file=f0_file,
          api_name=api_name
        )
    
    # Join all WAV files in order
    join_wav_files(output_wav_files, os.path.join(output_folder_path, "final_output.wav"))

# Function to join multiple WAV files
def join_wav_files(wav_files, output_path):
    with wave.open(output_path, 'wb') as outfile:
        for wav_file in wav_files:
            with wave.open(wav_file, 'rb') as infile:
                if wav_file == wav_files[0]:
                    outfile.setparams(infile.getparams())
                outfile.writeframes(infile.readframes(infile.getnframes()))

# Function to prompt the user for inputs
def get_user_input(prompt):
    return input(prompt)

# Define the folder containing the text files and the output folder
chunks_folder_path = "./chunks"
output_folder_path = get_user_input("Enter the output folder path: ")

# Get user inputs
tts_voice = get_user_input("Enter TTS voice: ")
tts_rate = int(get_user_input("Enter TTS rate: "))
f0_up_key = int(get_user_input("Enter f0 up key: "))
filter_radius = int(get_user_input("Enter filter radius: "))
index_rate = int(get_user_input("Enter index rate: "))
rms_mix_rate = int(get_user_input("Enter RMS mix rate: "))
protect = float(get_user_input("Enter protect value: "))
hop_length = int(get_user_input("Enter hop length: "))
f0_method = get_user_input("Enter f0 method: ")
pth_path = get_user_input("Enter pth path: ")
index_path = get_user_input("Enter index path: ")
split_audio = get_user_input("Split audio (True/False): ") == 'True'
f0_autotune = get_user_input("f0 autotune (True/False): ") == 'True'
clean_audio = get_user_input("Clean audio (True/False): ") == 'True'
clean_strength = float(get_user_input("Enter clean strength: "))
export_format = get_user_input("Enter export format: ")
embedder_model = get_user_input("Enter embedder model: ")
embedder_model_custom = get_user_input("Enter embedder model custom (or leave empty): ")
if embedder_model_custom == '':
    embedder_model_custom = None
upscale_audio = get_user_input("Upscale audio (True/False): ") == 'True'
f0_file = get_user_input("Enter f0 file path (or leave empty): ")
if f0_file == '':
    f0_file = None
api_name = get_user_input("Enter API name: ")

# Process the text files
process_text_files(chunks_folder_path, output_folder_path, tts_voice, tts_rate, f0_up_key, filter_radius, index_rate, rms_mix_rate, protect, hop_length, f0_method, pth_path, index_path, split_audio, f0_autotune, clean_audio, clean_strength, export_format, embedder_model, embedder_model_custom, upscale_audio, f0_file, api_name)
