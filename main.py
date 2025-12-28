import speech_recognition as sr
from pydub import AudioSegment
import os
import sys

def convert_mp3_to_wav(mp3_path):
    """
    Convert MP3 file to WAV format for speech recognition
    """
    try:
        print(f"Converting {mp3_path} to WAV format...")
        audio = AudioSegment.from_mp3(mp3_path)
        
        # Create temporary WAV file
        wav_path = mp3_path.rsplit('.', 1)[0] + '_temp.wav'
        audio.export(wav_path, format='wav')
        print(f"Conversion complete: {wav_path}")
        return wav_path
    except Exception as e:
        print(f"Error converting MP3 to WAV: {e}")
        return None

def transcribe_audio(audio_path):
    """
    Transcribe audio file to text using offline speech recognition
    """
    recognizer = sr.Recognizer()
    
    # Check if file is MP3, convert to WAV if needed
    if audio_path.lower().endswith('.mp3'):
        wav_path = convert_mp3_to_wav(audio_path)
        if not wav_path:
            return None
        is_temp = True
    else:
        wav_path = audio_path
        is_temp = False
    
    try:
        print(f"Loading audio file: {wav_path}")
        with sr.AudioFile(wav_path) as source:
            # Adjust for ambient noise
            print("Analyzing audio...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # Record the audio
            print("Processing audio data...")
            audio_data = recognizer.record(source)
            
            # Perform speech recognition using offline Sphinx
            print("Transcribing audio (this may take a while)...")
            text = recognizer.recognize_sphinx(audio_data)
            
            return text
            
    except sr.UnknownValueError:
        print("Speech recognition could not understand the audio")
        return None
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        return None
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None
    finally:
        # Clean up temporary WAV file
        if is_temp and os.path.exists(wav_path):
            os.remove(wav_path)
            print(f"Cleaned up temporary file: {wav_path}")

def main():
    """
    Main function to handle command line arguments and transcription
    """
    if len(sys.argv) < 2:
        print("Usage: python script.py <audio_file_path>")
        print("Example: python script.py /path/to/audio.mp3")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(audio_path):
        print(f"Error: File not found - {audio_path}")
        sys.exit(1)
    
    # Check file extension
    valid_extensions = ['.mp3', '.wav', '.flac', '.aiff']
    if not any(audio_path.lower().endswith(ext) for ext in valid_extensions):
        print(f"Error: Unsupported file format. Supported formats: {', '.join(valid_extensions)}")
        sys.exit(1)
    
    print("=" * 50)
    print("Audio Transcription Tool")
    print("=" * 50)
    print(f"Input file: {audio_path}")
    print()
    
    # Perform transcription
    transcription = transcribe_audio(audio_path)
    
    if transcription:
        print()
        print("=" * 50)
        print("TRANSCRIPTION RESULT:")
        print("=" * 50)
        print(transcription)
        print()
        
        # Save transcription to file
        output_file = audio_path.rsplit('.', 1)[0] + '_transcription.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(transcription)
        print(f"Transcription saved to: {output_file}")
    else:
        print("Transcription failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
