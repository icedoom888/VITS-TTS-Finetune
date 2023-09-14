import argparse
import os
from math import floor
from tqdm import tqdm
import text
import json

def process_filelist(args, wav_filelist, json_filelist, split):

    filepaths_and_text = []

    for wav_path, json_path in tqdm(zip(wav_filelist, json_filelist), total=len(wav_list)):

        # Check language
        with open(json_path, "r") as json_file:
            trans = json.load(json_file)
            txt = trans["text"]
            cleaned_text = text._clean_text(txt, args.text_cleaners)
            filepaths_and_text.append([wav_path, cleaned_text])

    new_filelist = f'filelists/{args.dataset_name}_{split}_filelist.txt'
    with open(new_filelist, "w", encoding="utf-8") as f:
      f.writelines(["|".join(x) + "\n" for x in filepaths_and_text])

    return


def split_filelist(file_list, split=(0.7, 0.1, 0.2)):
    train_split, val_split, test_split = split

    train_split_index = floor(len(file_list) * train_split)
    train_split = file_list[:train_split_index]

    val_split_index = train_split_index + floor(len(file_list) * val_split)
    val_split = file_list[train_split_index:val_split_index]


    test_split = file_list[val_split_index:]

    return train_split, val_split, test_split

if __name__ == "__main__":

    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_name", type=str, default="./")
    parser.add_argument("--datapath", type=str, default="./")
    parser.add_argument("--lang", type=str, default="eng")
    args = parser.parse_args()

    # Choose cleaners
    if args.lang == "eng":
        args.text_cleaners = ["english_cleaners2"]
        
    else: 
        args.text_cleaners = ["basic_cleaners"]

    splits = ['train', 'val', 'test']

    # get all files in the dataset
    wav_list = [os.path.join(args.datapath, 'split_audio', f) for f in sorted(os.listdir(os.path.join(args.datapath, 'split_audio')))]
    json_list = [os.path.join(args.datapath, 'transcription/audio_transcriptions/', f) for f in sorted(os.listdir(os.path.join(args.datapath, 'transcription/audio_transcriptions/')))]

    # split into train val test
    wav_filelists = split_filelist(wav_list, split=(0.8, 0.1, 0.1))
    json_filelists = split_filelist(json_list, split=(0.8, 0.1, 0.1))

    for split, wav_filelist, json_filelist in zip(splits, wav_filelists, json_filelists):
        # process each split
        process_filelist(args, wav_filelist, json_filelist, split)
