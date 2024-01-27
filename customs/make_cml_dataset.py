import h5py
import glob
import torch
import numpy as np
from tqdm import tqdm
import os
import torchaudio
import soundfile as sf
from utils.g2p.symbols import symbols
from utils.g2p import PhonemeBpeTokenizer
from utils.prompt_making import make_prompt, make_transcript
from data.collation import get_text_token_collater
from data.dataset import create_dataloader

# Mappings from symbol to numeric ID and vice versa:
_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}
from data.tokenizer import (
    AudioTokenizer,
    tokenize_audio,
)

tokenizer_path = "./utils/g2p/bpe_69.json"
tokenizer = PhonemeBpeTokenizer(tokenizer_path)
device = 'cuda' if torch.cuda.is_available() else 'cpu'

def make_prompts(name, audio_prompt_path, transcript=None):
    text_tokenizer = PhonemeBpeTokenizer(tokenizer_path="./utils/g2p/bpe_69.json")
    text_collater = get_text_token_collater()
    codec = AudioTokenizer(device)

    if not os.path.exists(audio_prompt_path):
        print(f"Audio file not found {audio_prompt_path}.")
        return False   
    
    wav_pr, sr = torchaudio.load(audio_prompt_path)

    # check length
    if wav_pr.size(-1) / sr > 15:
        print(f"Prompt too long, expect length below 15 seconds, got {wav_pr / sr} seconds.")
        return False
    
    if wav_pr.size(0) == 2:
        wav_pr = wav_pr.mean(0, keepdim=True)

    text_pr, lang_pr = make_transcript(name, wav_pr, sr, transcript)

    # tokenize audio
    encoded_frames = tokenize_audio(codec, (wav_pr, sr))
    audio_tokens = encoded_frames[0][0].transpose(2, 1).cpu().numpy()

    # tokenize text
    phonemes, langs = text_tokenizer.tokenize(text=f"{text_pr}".strip())

    text_tokens, enroll_x_lens = text_collater(
        [
            phonemes
        ]
    )

    return audio_tokens, text_tokens, langs, text_pr
    

def create_dataset(data_dir, metadata, dataloader_process_only):
    if dataloader_process_only:
        h5_output_path=f"{data_dir}/audio_sum.hdf5"
        ann_output_path=f"{data_dir}/audio_ann_sum.txt"

        metadata_filepath = os.path.join(data_dir, metadata)
        with open(metadata_filepath, "r") as ifile:
            metadata_content = ifile.readlines()[1:]

        # Create or open an HDF5 file
        with h5py.File(h5_output_path, 'w') as h5_file:
            # Loop through each audio and text file, assuming they have the same stem
            for line in tqdm(metadata_content):
                wav_filename,_,transcript,_,_,duration,_,_ = line.split("|")
                if not transcript.strip():
                    continue
                stem = os.path.splitext(os.path.basename(wav_filename))[0]
                wav_filepath = os.path.join(data_dir, wav_filename)
                result_prompt = make_prompts(name=stem, audio_prompt_path=wav_filepath, transcript=transcript)

                audio_tokens, text_tokens, langs, text = None, None, None, None
                if not result_prompt:
                    continue
                else:
                    audio_tokens, text_tokens, langs, text = result_prompt
                
                text_tokens = text_tokens.squeeze(0)
                # Create a group for each stem
                grp = h5_file.create_group(stem)
                # Add audio and text tokens as datasets to the group
                grp.create_dataset('audio', data=audio_tokens)
                #grp.create_dataset('text', data=text_tokens)
                
                with open(ann_output_path, 'a', encoding='utf-8') as ann_file:
                    try:
                        audio, sample_rate = sf.read(wav_filepath)
                        duration = len(audio) / sample_rate
                        ann_file.write(f'{stem}|{duration}|{langs[0]}|{text}\n')  # 改行を追加
                        print(f"Successfully wrote to {ann_output_path}")
                    except Exception as e:
                        print(f"An error occurred: {e}")
    else:
        dataloader = create_dataloader(data_dir=data_dir)
        return dataloader