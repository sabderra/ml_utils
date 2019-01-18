import numpy as np


class LRDecay:

    def __init__(self, initial_lrate=1e-3, decay_multiple=0.5, epochs_step=25, patience_multiple=3):
        self.initial_lrate = initial_lrate
        self.decay_multiple = decay_multiple
        self.epochs_step = epochs_step
        self.patience_multiple = patience_multiple
        self.patience = self.epochs_step * self.patience_multiple
        self.history_lr = []
        self.r_epoch = 0

    def linear_decay(self, x):
        return self.decay_multiple - (x / 1500)

    def reset(self, r_epoch=0):
        self.r_epoch = r_epoch

    # learning rate schedule
    def step_decay(self, epoch, current_lr):
        lrate = current_lr

        if self.r_epoch == 0:
            lrate = self.initial_lrate

        elif (1 + self.r_epoch) % self.epochs_step == 0:
            lrate = current_lr * self.linear_decay(self.r_epoch)

        lrate = np.around(lrate, 8)

        # Use the actual epoch to track history rather then
        # this runs epoch
        self.history_lr.append((epoch, current_lr, lrate))

        self.r_epoch += 1

        return lrate
