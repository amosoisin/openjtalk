from jtalk import Talker
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QApplication,
                             QFileDialog, QTextEdit,
                             QPushButton, QSlider,
                             QLabel, QCheckBox,
                             QHBoxLayout, QVBoxLayout)
import sys
import subprocess
import pickle

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.speed = 1.0
        self.volume = 0.0
        self.half_tone = 0.0
        self.weight_f0 = 1.0
        self.all_pass = None
        self.init_UI()

    def init_UI(self):
        vbox_main = QVBoxLayout()

        hbox_upper = QHBoxLayout()
        vbox_text_edit = QVBoxLayout()
        self.text_edit = QTextEdit()
        vbox_text_edit.addWidget(QLabel("Please input text", self))
        vbox_text_edit.addWidget(self.text_edit)
        hbox_upper.addLayout(vbox_text_edit)

        vbox_sliders = QVBoxLayout()

        vbox_volume = QVBoxLayout()
        self.volume_label = QLabel("volume : {}".format(self.volume), self)
        volume_reset_btn = QPushButton("reset", self)
        volume_reset_btn.clicked.connect(self.reset_volume)
        self.volume_slider = self.qt_slider(-10, 10, 0)
        self.volume_slider.valueChanged[int].connect(self.change_volume)
        hbox_volume = QHBoxLayout()
        hbox_volume.addWidget(self.volume_label)
        hbox_volume.addWidget(volume_reset_btn)
        vbox_volume.addLayout(hbox_volume)
        vbox_volume.addWidget(self.volume_slider)

        vbox_speed = QVBoxLayout()
        self.speed_label = QLabel("speed : {}".format(self.speed), self) 
        speed_reset_btn = QPushButton("reset", self)
        speed_reset_btn.clicked.connect(self.reset_speed)
        self.speed_slider = self.qt_slider(1, 200, 100)
        self.speed_slider.valueChanged[int].connect(self.change_speed)
        hbox_speed = QHBoxLayout()
        hbox_speed.addWidget(self.speed_label)
        hbox_speed.addWidget(speed_reset_btn)
        vbox_speed.addLayout(hbox_speed)
        vbox_speed.addWidget(self.speed_slider)

        vbox_all_pass = QVBoxLayout()
        self.all_pass_label = QLabel("all-pass : {}".format(self.all_pass), self) 
        all_pass_reset_btn = QPushButton("reset", self)
        all_pass_reset_btn.clicked.connect(self.reset_all_pass)
        self.all_pass_chk = QCheckBox("None", self)
        self.all_pass_chk.toggle()
        self.all_pass_chk.stateChanged.connect(self.switch_all_pass_none)
        self.all_pass_slider = self.qt_slider(0, 100, 0)
        self.all_pass_slider.valueChanged[int].connect(self.change_all_pass)
        hbox_all_pass_1 = QHBoxLayout()
        hbox_all_pass_1.addWidget(self.all_pass_label)
        hbox_all_pass_1.addWidget(all_pass_reset_btn)
        hbox_all_pass_2 = QHBoxLayout()
        hbox_all_pass_2.addWidget(self.all_pass_chk)
        hbox_all_pass_2.addWidget(self.all_pass_slider)
        vbox_all_pass.addLayout(hbox_all_pass_1)
        vbox_all_pass.addLayout(hbox_all_pass_2)

        vbox_half_tone = QVBoxLayout()
        self.half_tone_label = QLabel("add-half-tone : {}".format(self.half_tone), self) 
        half_tone_reset_btn = QPushButton("reset", self)
        half_tone_reset_btn.clicked.connect(self.reset_half_tone)
        self.half_tone_slider = self.qt_slider(0, 100, 0)
        self.half_tone_slider.valueChanged[int].connect(self.change_half_tone)
        hbox_half_tone = QHBoxLayout()
        hbox_half_tone.addWidget(self.half_tone_label)
        hbox_half_tone.addWidget(half_tone_reset_btn)
        vbox_half_tone.addLayout(hbox_half_tone)
        vbox_half_tone.addWidget(self.half_tone_slider)

        vbox_weight_f0 = QVBoxLayout()
        self.weight_f0_label = QLabel("weight-f0 : {}".format(self.weight_f0), self) 
        weight_f0_reset_btn = QPushButton("reset", self)
        weight_f0_reset_btn.clicked.connect(self.reset_weight_f0)
        self.weight_f0_slider = self.qt_slider(0, 50, 10)
        self.weight_f0_slider.valueChanged[int].connect(self.change_weight_f0)
        hbox_weight_f0 = QHBoxLayout()
        hbox_weight_f0.addWidget(self.weight_f0_label)
        hbox_weight_f0.addWidget(weight_f0_reset_btn)
        vbox_weight_f0.addLayout(hbox_weight_f0)
        vbox_weight_f0.addWidget(self.weight_f0_slider)

        vbox_sliders.addLayout(vbox_volume)
        vbox_sliders.addLayout(vbox_speed)
        vbox_sliders.addLayout(vbox_all_pass)
        vbox_sliders.addLayout(vbox_half_tone)
        vbox_sliders.addLayout(vbox_weight_f0)
        hbox_upper.addLayout(vbox_sliders)

        hbox_btn = QHBoxLayout()
        open_file_btn = QPushButton("Open File", self)
        open_file_btn.clicked.connect(self.show_dialog)
        play_btn = QPushButton("Play", self)
        play_btn.clicked.connect(self.play_audio)
        save_btn = QPushButton("Save audio", self)
        load_voice_btn = QPushButton("load voice", self)
        load_voice_btn.clicked.connect(self.load_voice_settings)
        save_btn.clicked.connect(self.save_wav_file)
        save_voice_btn = QPushButton("save voice", self)
        save_voice_btn.clicked.connect(self.save_voice_settings)
        hbox_btn.addWidget(open_file_btn)
        hbox_btn.addWidget(play_btn)
        hbox_btn.addWidget(save_btn)
        hbox_btn.addWidget(load_voice_btn)
        hbox_btn.addWidget(save_voice_btn)

        vbox_main.addLayout(hbox_upper)
        vbox_main.addLayout(hbox_btn)
        self.setLayout(vbox_main)

        self.resize(1000, 600)

    def qt_slider(self, min_v, max_v, default_v, direction=Qt.Horizontal, focus_policy=Qt.NoFocus):
        slider = QSlider(direction, self)
        slider.setFocusPolicy(focus_policy)
        slider.setMinimum(min_v)
        slider.setMaximum(max_v)
        slider.setValue(default_v)
        return slider

    def change_speed(self, value):
        self.speed = value / 100 
        self.speed_label.setText("speed : {}".format(self.speed))

    def reset_speed(self):
        self.speed = 1.0
        self.speed_slider.setValue(1.0*100)

    def change_volume(self, value):
        self.volume = value
        self.volume_label.setText("volume : {}".format(self.volume))

    def reset_volume(self):
        self.volume = 0.0
        self.volume_slider.setValue(0.0)

    def change_all_pass(self, value):
        if self.all_pass_chk.isChecked():
            self.all_pass = None
            self.all_pass_slider.setValue(0)
        else:
            self.all_pass = value / 100
            self.all_pass_label.setText("all-pass : {}".format(self.all_pass))

    def reset_all_pass(self):
        self.all_pass = 0
        self.all_pass_slider.setValue(0)

    def switch_all_pass_none(self, state):
        if state == Qt.Checked:
            self.all_pass = None
            self.all_pass_label.setText("all-pass : {}".format(self.all_pass))
            self.all_pass_slider.setValue(0)

    def change_half_tone(self, value):
        self.half_tone = value/10
        self.half_tone_label.setText("add-half-tone : {}".format(self.half_tone))

    def reset_half_tone(self):
        self.half_tone = 0
        self.half_tone_slider.setValue(0)

    def change_weight_f0(self, value):
        self.weight_f0 = value / 10
        self.weight_f0_label.setText("weight-f0 : {}".format(self.weight_f0))

    def reset_weight_f0(self):
        self.weight_f0 = 1.0
        self.weight_f0_slider.setValue(10)
    
    def show_dialog(self):
        fname = QFileDialog.getOpenFileName(self,
                "Open file",
                "/home/szbhitoshikiizaya/",
                "Text (*.txt)")
        if fname[0]:
            f = open(fname[0], "r")
            with f:
                data = f.read()
                self.text_edit.setText(data)

    def play_audio(self):
        read_text = self.text_edit.toPlainText().replace("\n", "、")
        talker = Talker()
        talker.save(read_text,
                    speed=self.speed,
                    volume=self.volume,
                    all_pass=self.all_pass,
                    half_tone=self.half_tone,
                    weight_f0=self.weight_f0,
                    output_file=".tmp.wav")
        talker.play_audio(filename=".tmp.wav")

    def save_wav_file(self):
        read_text = self.text_edit.toPlainText().replace("\n", "、")
        fname = QFileDialog.getSaveFileName(self,
                "Save file",
                "/home/szbhitoshikiizaya/",
                "Audio (*.wav)")[0]
        if not fname:
            return
        ex = fname.split(".")[-1]
        if ex != "wav":
            fname += ".wav"
        talker = Talker()
        talker.save(read_text,
                    volume=self.volume,
                    speed=self.speed,
                    half_tone=self.half_tone,
                    all_pass=self.all_pass,
                    weight_f0=self.weight_f0,
                    output_file=fname)

    def load_voice_settings(self):
        fname = QFileDialog.getOpenFileName(self,
                "Open voice file",
                "/home/szbhitoshikiizaya/",
                "Voice Settings (*.voice)")[0]
        if not fname:
            return
        with open(fname, "rb") as f:
            settings = pickle.load(f)
        self.speed = settings["speed"]
        self.volume = settings["volume"]
        self.all_pass = settings["all_pass"]
        self.half_tone = settings["half_tone"]
        self.weight_f0 = settings["weight_f0"]
        self.speed_slider.setValue(self.speed*100)
        self.volume_slider.setValue(self.volume)
        if self.all_pass:
            if self.all_pass_chk.isChecked():
                self.all_pass_chk.toggle()
            self.all_pass_slider.setValue(self.all_pass*100)
        else:
            if not self.all_pass_chk.isChecked:
                self.all_pass_chk.toggle()
            self.all_pass_slider.setValue(0)
        self.half_tone_slider.setValue(self.half_tone*10)
        self.weight_f0_slider.setValue(self.weight_f0*10)

    def save_voice_settings(self):
        settings = {
                "speed":self.speed, "volume": self.volume,
                "all_pass":self.all_pass, "half_tone": self.half_tone,
                "weight_f0":self.weight_f0
        }
        fname = QFileDialog.getSaveFileName(self,
                "Save voice file",
                "/home/szbhitoshikiizaya/",
                "Voice Settings (*.voice)")[0]
        if not fname:
            return
        ex = fname.split(".")[-1]
        if ex != "voice":
            fname += ".voice"
        with open(fname, "wb") as f:
            pickle.dump(settings, f)

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
