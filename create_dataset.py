from customs.make_cml_dataset import create_dataset

'''
How should the data_dir be created?
Place the necessary audio files in data_dir.
Transcription, tokenization, etc. of the audio files are done by the create_dataset function.

data_dir
├── bpe_69.json
├── utt1.wav
├── utt2.wav
├── utt3.wav
......
└── utt{n}.wav
'''

data_dir = "/mnt/Projetos/DATASETS/cml_tts_dataset_portuguese_v0.2/"
metadata = 'train_sample.csv'
create_dataset(data_dir, metadata, dataloader_process_only=True)