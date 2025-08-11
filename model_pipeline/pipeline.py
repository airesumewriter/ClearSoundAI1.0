# pipeline.py - orchestrator stub
# Run with: python pipeline.py --input sample.wav --output out.wav
import argparse
from models.denoise import Denoiser
from models.fingerprint import Fingerprinter
from utils.audio_io import load_wav, save_wav

def main(input_path, output_path):
    audio, sr = load_wav(input_path)
    denoiser = Denoiser()
    clean_audio = denoiser.process(audio, sr)
    fingerprinter = Fingerprinter()
    fingerprint = fingerprinter.fingerprint(clean_audio, sr)
    save_wav(output_path, clean_audio, sr)
    print("Processed. fingerprint:", fingerprint[:16])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    main(args.input, args.output)
