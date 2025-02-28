import os
import torch
import logging
from data.dataset import create_dataloader
from macros import *
from data.tokenizer import (
    AudioTokenizer,
    tokenize_audio,
)
from data.collation import get_text_token_collater
from models.vallex import VALLE
if torch.cuda.is_available():
    device = torch.device("cuda", 0)
from vocos import Vocos

import pathlib
import platform

if platform.system() != "Windows":
    pathlib.WindowsPath = pathlib.PosixPath


def get_model(device):
    url = 'https://huggingface.co/Plachta/VALL-E-X/resolve/main/vallex-checkpoint.pt'

    checkpoints_dir = "./checkpoints"

    checkpoint_filepath = os.path.join("vallex-checkpoint.pt")
    if not os.path.exists(checkpoints_dir): os.mkdir(checkpoints_dir)
    if not os.path.exists(checkpoint_filepath):
        import wget
        try:
            logging.info(
                "Downloading model from https://huggingface.co/Plachta/VALL-E-X/resolve/main/vallex-checkpoint.pt ...")
            # download from https://huggingface.co/Plachta/VALL-E-X/resolve/main/vallex-checkpoint.pt to ./checkpoints/vallex-checkpoint.pt
            if not os.path.exists(checkpoint_filepath):
                wget.download("https://huggingface.co/Plachta/VALL-E-X/resolve/main/vallex-checkpoint.pt",
                          out=checkpoint_filepath, bar=wget.bar_adaptive)
        except Exception as e:
            logging.info(e)
            raise Exception(
                "\n Model weights download failed, please go to 'https://huggingface.co/Plachta/VALL-E-X/resolve/main/vallex-checkpoint.pt'"
                "\n manually download model weights and put it to {} .".format(os.getcwd() + "\checkpoints"))
    # VALL-E
    model = VALLE(
        N_DIM,
        NUM_HEAD,
        NUM_LAYERS,
        norm_first=True,
        add_prenet=False,
        prefix_mode=PREFIX_MODE,
        share_embedding=True,
        nar_scale_factor=1.0,
        prepend_bos=True,
        num_quantizers=NUM_QUANTIZERS,
    ).to(device)

    if os.path.exists(checkpoint_filepath):
        print(f"Loading checkpoint {checkpoint_filepath}.")
        checkpoint = torch.load(checkpoint_filepath, map_location='cpu')
        missing_keys, unexpected_keys = model.load_state_dict(
            checkpoint["model"], strict=True
        )
        assert not missing_keys
    else:
        print(f"Checkpoint file not found: {checkpoint_filepath}.")


    # Encodec
    codec = AudioTokenizer(device)
    
    vocos = Vocos.from_pretrained('charactr/vocos-encodec-24khz').to(device)
    
    return model, codec, vocos