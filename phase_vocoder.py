import marsyas

oscbank_ = False
N = 512
Nw = 512
D = 64
I = 64
P = 1.0
unconvertmode_ = "classic"
convertmode_ = "sorted"
multires_ = False
multiresMode_ = "transient_switch"
bopt = 128
sopt = 80
music_file = ""
options = {'music_file':music_file, 'N':N, 'Nw':Nw, 'D':D, 'I':I, 'P':P, 'unconvertmode_':unconvertmode_, 'convertmode_':convertmode_, 'multires_':multires_, 'multiresMode_':multiresMode_, 'bopt':bopt, 'sopt':sopt, 'oscbank_':oscbank_}

def time_shift(**args):

	for arg in args:
		options[arg] = args[arg]

	print options

	mng = marsyas.MarSystemManager()
	pvseries = marsyas.system_from_script_file("./marsystems/time-shift.mrs")

	pvseries.updControl("mrs_string/file", options['music_file'])
	pvseries.updControl("mrs_string/outfile", "./pv/pv_output_phaselock.wav")


  	pvseries.updControl("mrs_real/israte", 44100.0)
	pvseries.updControl("mrs_real/osrate", 44100.0)
	pvseries.updControl("mrs_natural/inSamples", options['D'])
	pvseries.updControl("mrs_natural/onSamples", options['I'])


  	
  	
  	pvseries.updControl("SoundFileSource/src/mrs_natural/onSamples", options['D'])
  	pvseries.updControl("mrs_natural/inObservations", 1)



	pvseries.updControl("ShiftInput/si/mrs_natural/winSize", options['Nw'])

	pvseries.updControl("PvFold/fo/mrs_natural/FFTSize", options['N'])

	pvseries.updControl("PvConvert/conv/mrs_natural/Decimation", options['D'])
	pvseries.updControl("PvConvert/conv/mrs_natural/Sinusoids", options['sopt'])
	pvseries.updControl("PvConvert/conv/mrs_string/mode", options['convertmode_'])

	pvseries.updControl("mrs_natural/onStabilizingDelay", 63)

	pvseries.updControl("SoundFileSource/src/mrs_natural/onObservations", 2)
	pvseries.updControl("SoundFileSource/src/mrs_natural/inSamples", options['D'])
	pvseries.updControl("SoundFileSource/src/mrs_natural/onSamples", options['D'])

	pvseries.updControl("ShiftInput/si/mrs_natural/onSamples", options['Nw'])
	pvseries.updControl("ShiftInput/si/mrs_real/israte", 44100.0)
	pvseries.updControl("ShiftInput/si/mrs_real/osrate", 44100.0)

	pvseries.updControl("ShiftInput/si/mrs_natural/onObservations", 1)

	pvseries.updControl("PvConvert/conv/mrs_natural/inSamples", 1)
	pvseries.updControl("PvConvert/conv/mrs_natural/onSamples", 1)
	pvseries.updControl("PvConvert/conv/mrs_real/osrate", 44100.0)


	pvseries.updControl("PvUnconvert/uconv/mrs_natural/inObservations", options['Nw'])
	pvseries.updControl("PvUnconvert/uconv/mrs_natural/onObservations", options['Nw'])
	pvseries.updControl("PvUnconvert/uconv/mrs_natural/Interpolation", options['I'])
	pvseries.updControl("PvUnconvert/uconv/mrs_natural/Decimation", options['D'])
	
	pvseries.updControl("PvUnconvert/uconv/mrs_string/mode",options['unconvertmode_'])

	pvseries.updControl("InvSpectrum/ispectrum/mrs_natural/onObservations", 1)
	pvseries.updControl("InvSpectrum/ispectrum/mrs_natural/onSamples", 1024)

	pvseries.updControl("PvOverlapadd/pover/mrs_natural/FFTSize", options['N'])
	pvseries.updControl("PvOverlapadd/pover/mrs_natural/winSize", options['Nw'])
	pvseries.updControl("PvOverlapadd/pover/mrs_natural/Interpolation", options['I'])
	pvseries.updControl("PvOverlapadd/pover/mrs_natural/Decimation", options['D'])

	pvseries.updControl("ShiftOutput/so/mrs_natural/Interpolation", options['I'])

	pvseries.linkControl("PvConvert/conv/mrs_realvec/phases", "PvUnconvert/uconv/mrs_realvec/analysisphases")
	pvseries.linkControl("PvUnconvert/uconv/mrs_realvec/regions", "PvConvert/conv/mrs_realvec/regions")

	ticks = 0

	notempty = pvseries.getControl("SoundFileSource/src/mrs_bool/hasData")

	while (notempty.to_bool()):
		if(ticks == 0):
			pvseries.updControl("PvUnconvert/uconv/mrs_bool/phaselock", marsyas.MarControlPtr.from_bool(True))
		
		pvseries.tick()
		print ticks
		ticks = ticks + 1
		print ticks*(options['D']/44100.0)

	return "pv_output.wav"




if __name__ == "__main__":

	speed = 2
	ipol = int(16*speed)
	infile = "../../phasevocoding/nolove.wav"
	print "Output file will be at", speed, "times original speed."
	outputfile = time_shift(N=1024, Nw=1024, D=16, I=ipol, music_file=infile)
	print("Done!")

