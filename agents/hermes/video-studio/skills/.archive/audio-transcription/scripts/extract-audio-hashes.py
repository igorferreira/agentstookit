#!/usr/bin/env python3
"""
Extract SHA-256 hashes and ffprobe metadata from all audio files in a directory.
Output: tab-separated table for INDICE-PROVAS.md.
Usage: python3 extract-audio-hashes.py /path/to/case/folder/
"""
import hashlib, subprocess, json, sys
from pathlib import Path

AUDIO_EXTS = {'.ogg', '.mp3', '.m4a', '.oga', '.wav', '.flac', '.aac', '.opus'}

def main():
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    
    print("Arquivo|SHA-256|Duração|Codec|Tamanho|Bitrate|Canais")
    print("---|:---:|---:|:---:|---:|---:|---:")
    
    for f in sorted(folder.iterdir()):
        if f.suffix.lower() not in AUDIO_EXTS:
            continue
        
        # SHA-256
        sha = hashlib.sha256()
        with open(f, 'rb') as fh:
            for chunk in iter(lambda: fh.read(65536), b''):
                sha.update(chunk)
        
        # Metadata via ffprobe
        r = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-print_format', 'json',
             '-show_format', '-show_streams', str(f)],
            capture_output=True, text=True, timeout=30
        )
        meta = json.loads(r.stdout) if r.stdout else {}
        fmt = meta.get('format', {})
        streams = meta.get('streams', [])
        audio = next((s for s in streams if s.get('codec_type') == 'audio'), {})
        
        dur = float(fmt.get('duration', 0))
        mins = int(dur // 60)
        secs = int(dur % 60)
        duration = f"{mins}min{secs}s" if mins else f"{secs}s"
        
        print(f"{f.name}|`{sha.hexdigest()[:16]}…`|"
              f"{duration}|{audio.get('codec_name','?')}|"
              f"{fmt.get('size','?')}|{fmt.get('bit_rate','?')}|"
              f"{audio.get('channels','?')}")

if __name__ == '__main__':
    main()
