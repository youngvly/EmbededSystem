
from __future__ import division

import RPi.GPIO as GPIO
import time
import thread

import re
import sys

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue
from Word import wordExtract
from threading import Timer

#time bool

TIMEOUTVAL = False
# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

def timeout(txtfile) :
    try :
        print("Google Speech Time out")
        
        if True:
            raise Exception ("Timeout")
    finally :
        global TIMEOUTVAL
        TIMEOUTVAL = True
        #print(TIMEOUTVAL)
        txtfile.close()
    
    
class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)


def listen_print_loop(responses,txtfile):
    
    num_chars_printed = 0
    try : 
        for response in responses:
            #print(TIMEOUTVAL)
            if TIMEOUTVAL :
                break
            if not response.results:
                continue

            # The `results` list is consecutive. For streaming, we only care about
            # the first result being considered, since once it's `is_final`, it
            # moves on to considering the next utterance.
            result = response.results[0]
            if not result.alternatives:
                continue

            # Display the transcription of the top alternative.
            transcript = result.alternatives[0].transcript

            # Display interim results, but with a carriage return at the end of the
            # line, so subsequent lines will overwrite them.
            #
            # If the previous result was longer than this one, we need to print
            # some extra spaces to overwrite the previous result
            overwrite_chars = ' ' * (num_chars_printed - len(transcript))

            if not result.is_final:
                sys.stdout.write(transcript + overwrite_chars + '\r')
                sys.stdout.flush()

                num_chars_printed = len(transcript)
                


            else:
                
                
                print(transcript + overwrite_chars)
                txtfile.write((transcript + overwrite_chars).encode('utf-8'))
                # Exit recognition if any of the transcribed phrases could be
                # one of our keywords.
                
                if re.search(r'\b(finish)\b', transcript, re.I):
                    print('Exiting..')
                    txtfile.close()
                    break

            num_chars_printed = 0
    except Exception as e:
        print(e)
        afterTimeout()
        return
    
def afterTimeout() :
    filename = "Resources/speech.txt"
    top3 = wordExtract(filename)
    for top in top3 :
        print(top[0] , ":" , top[1])
        
def detectSpeech():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = 'ko-KR'  # a BCP-47 language tag
    #ko-KR

    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)
    filename = "speech.txt"
    txtfile = open(filename,'w')
    t = Timer(10,timeout,[txtfile,])
    t.start()
    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)
        
        # Now, put the transcription responses to use.
        listen_print_loop(responses,txtfile)
    t.join()
    


if __name__ == '__main__':
    
    detectSpeech()
# [END speech_transcribe_streaming_mic]


