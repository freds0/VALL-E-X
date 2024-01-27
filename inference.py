from utils.prompt_making import make_prompt
from utils.generation import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav

### Use given transcript
# save to ./customs/paimon.npz
#make_prompt(name="paimon", audio_prompt_path="5677_sample.wav",
#                transcript="Just, what was that? Paimon thought we were gonna get eaten.")

### Alternatively, use whisper
#make_prompt(name="paimon", audio_prompt_path="5677_sample.wav")




# download and load all models
preload_models()

# generate audio from text
text_prompt = """
Hello, my name is Nose. And uh, and I like hamburger. Hahaha... But I also have other interests such as playing tactic toast.
"""
audio_array = generate_audio(text_prompt)

# save audio to disk
write_wav("vallex_generation.wav", SAMPLE_RATE, audio_array)