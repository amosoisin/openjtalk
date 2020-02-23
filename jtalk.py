import subprocess
import sys


class Talker:
    def save(self, t, speed=1.0, volume=0.0, half_tone=0.0 ,all_pass=None , weight_f0=1.0, output_file="open_jtalk.wav"):
        cmd = ['open_jtalk']
        cmd += ['-x','/var/lib/mecab/dic/open-jtalk/naist-jdic']    # mech
        cmd += ['-m','/usr/share/hts-voice/mei_normal.htsvoice']    # htsvoice
        #speed
        cmd += ['-r', str(speed)]
        # volume
        cmd += ['-g', str(volume)]
        if all_pass:
            cmd += ['-a', str(all_pass)]    # all_pass
        # add-half-rone
        cmd += ['-fm', str(half_tone)]
        # weight_f0
        cmd += ['-jf', str(weight_f0)]
        # output_filename
        cmd += ['-ow',output_file]
        c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
        c.stdin.write(t.encode())
        c.stdin.close()
        c.wait()

    def play_audio(self, filename="open_jtalk.wav"):
        cmd = ["aplay", "-q", filename]
        c = subprocess.Popen(cmd)

if __name__ == '__main__':
    talker = Talker()
    talker.save("こんにちは、オープンジェートークです")
    talker.play_audio()
