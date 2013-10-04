# Copyright (c) James Percent, Byron Galbraith and Unlock contributors.
# All rights reserved.
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#    
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#    3. Neither the name of Unlock nor the names of its contributors may be used
#       to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from optparse import OptionParser
import numpy as np
from unlock.util import Trigger

def map_cue(cue):
	if cue == Trigger.Up:
		return 'UP'
	elif cue == Trigger.Right:
		return 'RIGHT'
	elif cue == Trigger.Down:
		return 'DOWN'
	elif cue == Trigger.Left:
		return 'LEFT'
	else:
		raise Exception('Unsupported value')

class EightChannelSchema(object):
	DataStart = 0
	DataEnd = 7
	DeviceDelta = 8
	DeviceTimeHigh = 9
	DeviceTimeLow = 10
	MicroDelta = 11
	PythonReceiveTime = 12
	SequenceTrigger = 13
	SequenceTriggerTime = 14
	CueTrigger = 15
	CueTriggerTime = 1


class CueIndicateRestSampleParser(object):
	Cue=0
	Indicate=1
	Rest=2
	def __init__(self, file_path, channel_schema, cue_duration, rest_duration, indicate_duration, data_start,
				 data_end):
		self.file_path = file_path
		self.schema = channel_schema
		self.cue_duration = cue_duration
		self.rest_duration = rest_duration
		self.indicate_duration = indicate_duration
		self.data_start = data_start
		self.data_end = data_end
		self.parsed_samples = { Trigger.Cue:[], Trigger.Rest:[], Trigger.Up:[], Trigger.Right:[] ,
				Trigger.Down: [], Trigger.Left : []}
				
	def is_cue(self, sample):
		if sample[self.schema.CueTrigger] == Trigger.Up or \
			sample[self.schema.CueTrigger] == Trigger.Right or \
			sample[self.schema.CueTrigger] == Trigger.Down or \
			sample[self.schema.CueTrigger] == Trigger.Left:
			return True
		else:
			return False
			
	def is_indication(self, sample):
		if sample[self.schema.CueTrigger] == Trigger.Indicate:
			return True
		else:
			return False
			
	def is_rest(self, sample):
		if sample[self.schema.CueTrigger] == Trigger.Rest:
			return True
		else:
			return False
			
	def parse_samples(self):
		done = False
		mode = None
		new_cue = []
		new_indication = []
		new_rest = []
		
		file_ = open(self.file_path, 'r')
		
		while True:
			samplestr = file_.readline()
			if samplestr == '':
				break
			
			sample = np.array([float(datumstr.strip()) for datumstr in samplestr.split()])
		
			if mode == None:
				if self.is_cue(sample):
					trigger = sample[self.schema.CueTrigger]
					mode = self.Cue
					
			elif mode == self.Cue:
				if self.is_indication(sample):
					mode = self.Indicate
					self.parsed_samples[Trigger.Cue].append((trigger, new_cue))
					new_cue = []
				else:
					new_cue.append(sample)
					
			elif mode == self.Indicate:
				if self.is_rest(sample):
					mode = self.Rest
					self.parsed_samples[trigger].append(new_indication)
					new_indication = []
				else:
					new_indication.append(sample)
					
			elif mode == self.Rest:
				if self.is_cue(sample):
					mode = self.Cue
					trigger = sample[self.schema.CueTrigger]
					self.parsed_samples[Trigger.Rest].append(new_rest)
					new_rest = []
				else:
					new_rest.append(sample)
					
		file_.close()
		return self.parsed_samples

	def completed_trials(self, handler):
		handler("Completed trails = ", len(self.parsed_samples[Trigger.Rest]))

	def compute_samples_per_command(self, handler):
		[handler("Sampes/cue = ", len(cue[1]), ' cue value = ', map_cue(cue[0])) for cue in self.parsed_samples[Trigger.Cue]]
		[handler("Sampes/Up = ", len(indicate)) for indicate in self.parsed_samples[Trigger.Up]]
		[handler("Sampes/Right = ", len(indicate)) for indicate in self.parsed_samples[Trigger.Right]]
		[handler("Sampes/Down = ", len(indicate)) for indicate in self.parsed_samples[Trigger.Down]]
		[handler("Sampes/Left = ", len(indicate)) for indicate in self.parsed_samples[Trigger.Left]]		
		[handler("Sampes/Rest = ", len(rest)) for rest in self.parsed_samples[Trigger.Rest]]				

	@staticmethod
	def create_eight_channel_analyzer(file_path, cue_duration=.5, rest_duration=.5, indicate_duration=1.0,
									  data_start=0, data_end=3):
		return CueIndicateRestSampleParser(file_path, EightChannelSchema(), cue_duration, rest_duration,
									   indicate_duration, data_start, data_end)
									

if __name__ == '__main__':
	
	args = None
	options = None
	usage = "usage: %prog [options]"
	args_parser = OptionParser(version="%prog 1.0", usage=usage)
	file_help = 'file to parse'
	args_parser.add_option('-f', '--file', type=str, dest='file', default=None, metavar='FILE',
					  help=file_help)
	
	(options, args) = args_parser.parse_args()
	#print args
	#if options.file == None:
	#	args_parser.print_help()
	#	sys.exit(1)			
	for file_ in args:
		samples_parser = CueIndicateRestSampleParser.create_eight_channel_analyzer(file_)
		samples = samples_parser.parse_samples()
		samples_parser.completed_trials(print)
		samples_parser.compute_samples_per_command(print)
		print (80*'-')