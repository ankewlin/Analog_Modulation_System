import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.fftpack import fft

# 说明：此项目为一个AM调制与解调的交互项目，运行时须配置好界面环境，然后点击相应的指令"生成余弦信号"等等界面就会出现相应的图像

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Signal Processing App")
        self.fig = plt.figure(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        self.signal = None
        self.signal_with_noise = None
        # 常量线性空间
        self.T = np.linspace(0, 10, 1000)
        # 常量载波
        self.carrier_freq = None
        # 已调信号
        self.shifted_signal = None

        self.generate_button = tk.Button(self.master, text="生成余弦信号", command=self.generate_signal)
        self.generate_button.pack(side="left")

        self.add_noise_button = tk.Button(self.master, text="加噪声", command=self.add_noise)
        self.add_noise_button.pack(side="left")

        self.to_freq_domain_button = tk.Button(self.master, text="to freq domain", command=self.to_freq_domain)
        self.to_freq_domain_button.pack(side="left")

        self.shift_freq_button = tk.Button(self.master, text="频谱搬移", command=self.shift_freq)
        self.shift_freq_button.pack(side="left")

        self.coherent_demodulation_button = tk.Button(self.master, text="相干解调频域", command=self.coherent_demodulation)
        self.coherent_demodulation_button.pack(side="left")

        self.LPF_button = tk.Button(self.master, text="通过LPF后时域的图像", command=self.LPF)
        self.LPF_button.pack(side="left")

    def generate_signal(self):
        t = self.T
        f = 1
        self.signal = np.cos(2 * np.pi * f * t)

        # 清除之前的图形
        self.fig.clear()

        ax = self.fig.add_subplot(111)
        ax.clear()
        ax.plot(t, self.signal)
        self.canvas.draw()

    def add_noise(self):
        if self.signal is None:
            return
        noise = np.random.normal(0, 1, len(self.signal))
        self.signal_with_noise = self.signal + noise

        # 清除之前的图形
        self.fig.clear()

        ax = self.fig.add_subplot(111)
        ax.clear()
        ax.plot(self.signal_with_noise)
        self.canvas.draw()

    def to_freq_domain(self):
        if self.signal_with_noise is None:
            return
        freq = fft(self.signal_with_noise)
        freq_mag = np.abs(freq)
        freq_mag = freq_mag[:int(len(freq_mag) / 2)]
        freq_scale = np.arange(len(freq_mag))
        freq_scale = freq_scale * 1.0 / len(self.signal)

        # 清除之前的图形
        self.fig.clear()

        ax = self.fig.add_subplot(111)
        ax.clear()
        ax.plot(freq_scale, freq_mag)
        self.canvas.draw()

    def shift_freq(self):
        if self.signal_with_noise is None:
            return

        carrier_freq = tk.simpledialog.askfloat("频谱搬移", "请输入载波的频率：")
        if carrier_freq is None:
            return
        self.carrier_freq = carrier_freq
        t = self.T
        carrier_signal = np.cos(2 * np.pi * carrier_freq * t)
        self.shifted_signal = self.signal_with_noise * carrier_signal

        freq = fft(self.shifted_signal)
        freq_mag = np.abs(freq)
        freq_mag = freq_mag[:int(len(freq_mag) / 2)]
        freq_scale = np.arange(len(freq_mag))
        freq_scale = freq_scale * 1.0 / len(self.signal)

        # 清除之前的图形
        self.fig.clear()

        ax = self.fig.add_subplot(111)
        ax.clear()
        ax.plot(freq_scale, freq_mag)
        self.canvas.draw()

    def coherent_demodulation(self):

        if self.shifted_signal is None:
            return

        # 引入常量空间
        t = self.T

        # 求出时域的相干解调信号
        carrier_signal = np.cos(2 * np.pi * self.carrier_freq * t)
        shifted_signal = self.signal_with_noise * carrier_signal
        coherent_demodulated_signal = shifted_signal * carrier_signal

        #转换到频域
        freq = fft(coherent_demodulated_signal)
        freq_mag = np.abs(freq)
        freq_mag = freq_mag[:int(len(freq_mag) / 2)]
        freq_scale = np.arange(len(freq_mag))
        freq_scale = freq_scale * 1.0 / len(self.signal)

        # 清除之前的图形
        self.fig.clear()

        #绘制图形
        ax = self.fig.add_subplot(111)
        ax.clear()
        ax.plot(freq_scale, freq_mag)
        self.canvas.draw()

    #滤波
    def LPF(self):

        #引入常量空间
        t = self.T

        # 求出时域的相干解调信号
        carrier_signal = np.cos(2 * np.pi * self.carrier_freq * t)
        shifted_signal = self.signal_with_noise * carrier_signal
        coherent_demodulated_signal = shifted_signal * carrier_signal

        #转换到频域
        y_freq_filtered = fft(coherent_demodulated_signal)
        freq_mag = np.abs(y_freq_filtered)
        freq_mag = freq_mag[:int(len(freq_mag))]
        freq_scale = np.arange(len(freq_mag))
        freq_scale = freq_scale * 1.0 / len(self.signal)


        # 将频率大于150Hz的频谱值设为0
        y_freq_filtered = np.abs(np.copy(y_freq_filtered))
        y_freq_filtered[np.abs(freq_scale) > 0.01] = 0

        # 进行傅立叶逆变换
        y_filtered = np.fft.ifft(y_freq_filtered)

        # 清除之前的图形
        self.fig.clear()

        #绘制图形
        ax = self.fig.add_subplot(111)
        ax.clear()
        ax.plot(t, y_filtered)
        self.canvas.draw()


root = tk.Tk()
app = App(root)
root.mainloop()
