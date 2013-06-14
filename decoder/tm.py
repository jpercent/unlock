import numpy as np


class TemplateMatch():
    """
    Template matching method for code-VEP methods.

    the spuler method has three parts
    1) leave-one-out cross validation to pick the best channel
    2) CCA analysis using the best channel to build a spatial filter
    3) One class SVM training to create the template

    first pass: generate a single template from a stream of data,
    single channel, no trigger markers
    """
    def __init__(self, templates, length, trials, electrodes, filters=None):
        self.nTemplates = templates
        self.length = length
        self.nTrials = trials
        self.overflow = 16
        self.templates = np.zeros((length, templates))
        self.buffer = np.zeros((length + self.overflow, electrodes))
        self.cursor = 0
        self.filters = filters

        self.training = True
        self.training_buffer = np.zeros((trials, length, electrodes))
        self.training_template = 0
        self.trial = 0

    def loocv(self):
        """
        Leave one out cross validation to find the best channel for use in CCA

        k trials are obtained
        """
        pass


    def process(self, samples):
        s = samples.shape[0]
        self.buffer[self.cursor:self.cursor+s, :] = samples
        self.cursor += s

        if self.cursor >= self.length:
            self.cursor = 0
            x = self.buffer[0:self.length, :]
            if self.filters is not None:
                x = self.filters.apply(x)

            if self.training:
                self.training_buffer[self.trial, :, :] = x
                self.trial += 1
                if self.trial >= self.nTrials:
                    template = np.median(
                        np.median(self.training_buffer, axis=2), axis=0)
                    self.templates[:, self.training_template] = template
                    self.trial = 0
                    self.training_template += 1
                    if self.training_template >= self.nTemplates:
                        self.training = False
            else:
                print np.mean(
                    np.median(x, axis=1).reshape((self.length,1)) - \
                        self.templates, axis=0)