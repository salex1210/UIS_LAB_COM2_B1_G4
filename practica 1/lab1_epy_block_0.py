import numpy as np
from gnuradio import gr

class StatsBlock(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='Stats_Block',
            in_sig=[np.float32],
            out_sig=[np.float32, np.float32, np.float32, np.float32, np.float32]
        )
        self.sum_x = 0
        self.sum_x2 = 0
        self.sum_x3 = 0
        self.N = 0

    def work(self, input_items, output_items):
        x = input_items[0]

        N = len(x)
        self.N += N

        # Calculating sum of x, x^2, x^3
        self.sum_x += np.sum(x)
        self.sum_x2 += np.sum(x ** 2)
        self.sum_x3 += np.sum(x ** 3)

        # Calculating mean
        mean = self.sum_x / self.N
        output_items[0][:] = mean

        # Calculating mean square
        mean_square = self.sum_x2 / self.N
        output_items[1][:] = mean_square

        # Calculating RMS
        rms = np.sqrt(mean_square)
        output_items[2][:] = rms

        # Calculating average power
        average_power = mean_square
        output_items[3][:] = average_power

        # Calculating standard deviation
        standard_deviation = np.sqrt((self.sum_x2 - 2 * mean * self.sum_x + self.N * mean ** 2) / self.N)
        output_items[4][:] = standard_deviation

        return len(x)
