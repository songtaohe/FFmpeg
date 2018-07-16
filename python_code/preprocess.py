# python preprocessing code
# simulate noise 
# random drop slice 


import sys
import os 
from subprocess import Popen
from time import time 

from PIL import Image 
import scipy.ndimage as nd 
import scipy.misc

import numpy as np 
import os.path



def process_single_video(filename, output_folder):
	strip_filename = filename.split('/')[-1].replace('.','_')
	output_sub_folder = output_folder+"/"+strip_filename


	Popen("mkdir -p %s" % output_sub_folder, shell=True)
	#os.mkdir(output_sub_folder)

	video_preprocessed = output_sub_folder+"_2000k_8_360p.h264"
	video_simulated = output_sub_folder+"_2000k_8_360p_sim.h264"





	# slice the input video, also resize the video 
	cmd1 = "ffmpeg  -i %s -vcodec h264 -slices 8 -b:v 2000k -vf scale=640:360 -bf 0 -y %s" % (filename, video_preprocessed)
	Popen(cmd1, shell=True).wait()

	# generate reference frames
	cmd2 = "ffmpeg  -i %s -r 30 -y \"%s\"" % (video_preprocessed, output_sub_folder+"/frame_ref_%05d.bmp")
	Popen(cmd2, shell=True).wait()


	# generate simulated frames
	cmd3 = "../ffmpeg  -i %s -r 30 -y \"%s\"" % (video_preprocessed, output_sub_folder+"/frame_sim_%05d.bmp")
	Popen(cmd3, shell=True).wait()


	# generate simulated videos
	# cmd4 = "../ffmpeg  -i %s -vcodec h264 -y %s" % video_simulated
	# Popen(cmd4, shell=True).wait()

	for i in xrange(100000):
		if os.path.isfile(output_sub_folder+"/frame_ref_%05d.bmp" % i) :
			img_ref = scipy.misc.imread(output_sub_folder+"/frame_ref_%05d.bmp" % i)
			img_sim = scipy.misc.imread(output_sub_folder+"/frame_sim_%05d.bmp" % i)

			img_mask = np.zeros_like(img_ref)

			img_mask[np.where(img_ref != img_sim)] = 1

			img_result = np.zeros((np.shape(img_mask)[0],np.shape(img_mask)[1]), dtype=np.uint8)

			img_result[:,:] = img_mask[:,:,0] + img_mask[:,:,1] + img_mask[:,:,2]

			img_result[np.where(img_result>0)] = 255 

			img_result = 255 - img_result


			Image.fromarray(img_result).save(output_sub_folder+"/frame_mask_%05d.png" % i) 

		else:
			if i > 0:
				break



if __name__== "__main__":
	output_folder = sys.argv[1]
	input_file_list = sys.argv[2:]	


	for filename in input_file_list:
		ts0 = time()
		process_single_video(filename, output_folder)
		print("#########  Time for one video %.2f ##############\n" % (time()-ts0))




