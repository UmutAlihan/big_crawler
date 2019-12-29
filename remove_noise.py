import numpy as np
import wave
import math
import contextlib



class noise_remover:
    def __init__(self,fname,outname):
        self.cutOffFrequency = 400.0

        self.fname = fname
        self.outname = outname

    def running_mean(self,x, windowSize):
      cumsum = np.cumsum(np.insert(x, 0, 0))
      return (cumsum[windowSize:] - cumsum[:-windowSize]) / windowSize

    # from http://stackoverflow.com/questions/2226853/interpreting-wav-data/2227174#2227174
    def interpret_wav(self,raw_bytes, n_frames, n_channels, sample_width, interleaved = True):

        if sample_width == 1:
            dtype = np.uint8 # unsigned char
        elif sample_width == 2:
            dtype = np.int16 # signed 2-byte short
        else:
            raise ValueError("Only supports 8 and 16 bit audio formats.")

        channels = np.fromstring(raw_bytes, dtype=dtype)

        if interleaved:
            # channels are interleaved, i.e. sample N of channel M follows sample N of channel M-1 in raw data
            channels.shape = (n_frames, n_channels)
            channels = channels.T
        else:
            # channels are not interleaved. All samples from channel M occur before all samples from channel M-1
            channels.shape = (n_channels, n_frames)

        return channels

    def run(self):
        with contextlib.closing(wave.open(self.fname,'rb')) as spf:
            sampleRate = spf.getframerate()
            ampWidth = spf.getsampwidth()
            nChannels = spf.getnchannels()
            nFrames = spf.getnframes()

            # Extract Raw Audio from multi-channel Wav File
            signal = spf.readframes(nFrames*nChannels)
            spf.close()
            channels = self.interpret_wav(signal, nFrames, nChannels, ampWidth, True)

            # get window size
            # from http://dsp.stackexchange.com/questions/9966/what-is-the-cut-off-frequency-of-a-moving-average-filter
            freqRatio = (self.cutOffFrequency/sampleRate)
            N = int(math.sqrt(0.196196 + freqRatio**2)/freqRatio)

            # Use moviung average (only on first channel)
            filtered = self.running_mean(channels[0], N).astype(channels.dtype)

            wav_file = wave.open(self.outname, "w")
            wav_file.setparams((1, ampWidth, sampleRate, nFrames, spf.getcomptype(), spf.getcompname()))
            wav_file.writeframes(filtered.tobytes('C'))
            wav_file.close()