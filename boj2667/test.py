
import cv2
import numpy as np
import glob
from videoProperty import VIDEO_PROP 
import random


videoWidth, videoHeight = VIDEO_PROP["width"], VIDEO_PROP["height"]

out = cv2.VideoWriter(VIDEO_PROP["filename"], cv2.VideoWriter_fourcc(*'MPEG'), VIDEO_PROP["frame"], (videoWidth, videoHeight) )

font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX  # hand-writing style font

def createImage(width, height, rgb_color=(0, 0, 0)):
	"""Create new image(numpy array) filled with certain color in RGB"""
	# Create black blank image
	return np.zeros((height, width, 3), np.uint8)

lastimg = None

table = []
table.append((0x00, 0x00, 0x00))
table.append((0xff, 0xff, 0xff))
# table.append((0x00, 0xaa, 0xff))
# table.append((0xff, 0xaa, 0x00))

inputData = [
	"0110100011010001111100110100",
	"0110101011010101111110110101",
	"1110101111010111111111110101",
	"0000111000011100011110000111",
	"0100000010000001011100100001",
	"0111110011111001111100110111",
	"0111000011100001111100111001",
	"0110100011010001111100100001",
	"0110101011010101111110100001",
	"1110101111010111111111100001",
	"0100111000011100011110000001",
	"0100000010000001011100100001",
	"0111110011111001111100100001",
	"1111111011100001111100100001",
	"1111111011010001111100100001",
	"1111111011010101111110100001",
	"1111111111010111111111100001",
	"1111111000011100011110000111",
	"1111111010000001011100100000",
	"1111111011111001111100111110",
	"0111000011100001111100111000",
	"0110100011010001111100110100",
	"0110101011010101111110110101",
	"1110101111010111111111110101",
	"0000111000011100011110000111",
	"0100000010000001011100100000",
	"0111110011111001111100111110",
	"0111000011100001111100111000"
	]

inputDataLength = len(inputData)
arr = []
for i in range(inputDataLength):
	arr.append([])

	for j in inputData[i]:
		t = 0
		if j == "1":
			t = 1
		arr[i].append(t)

	# arr.append()

N = len(arr)
print(N)

blockLength = min(videoHeight / N, videoWidth / N)

print(blockLength)

result = []

  
# org 
org = (50, 50) 

# fontScale 
fontScale = 2
# Blue color in BGR 
color = (255, 255, 255)
# color = (255, 255, 255)
  
# Line thickness of 2 px 
thickness = 2
   
# Using cv2.putText() method 


leftmargin = 200
def makeFrame(arr, N: int):
	global lastimg
	img = createImage(videoWidth, videoHeight)


	for i in range(N):
		for j in range(N):
			
			startx = int(blockLength * j) + leftmargin
			starty = int(blockLength * i)
			length = int(blockLength)
			
			cv2.rectangle(img, (startx, starty), (startx + length, starty + length), table[arr[i][j]], -1)

	textStartx = min(videoHeight, videoWidth) + 10 +leftmargin

	cv2.putText(img, " " + str(len(result)), (textStartx, 60), font,  
								fontScale, color, thickness + 3, cv2.LINE_AA)


	lcount = 0
	for i,v in enumerate(result):
		if len(result) > 17 and i <= len(result) - 17:
			continue
		
		# if i <= len(result) - 16:
		# 	i -= len(result) - 16

		cv2.putText(img, "%2d"%(i+1)+": %3d"%v, (textStartx, 120 + int(60*lcount)), font,  
                  fontScale, color, thickness, cv2.LINE_AA)

		lcount+=1
	out.write(img)
	lastimg = img
	cv2.imshow('frame', img)
	cv2.waitKey(delay=1)

def f(i: int, j: int, count: int) -> int:
	if arr[i][j] != 1:
		return 0
	arr[i][j] = count
	size = 1
	makeFrame(arr, N)

	if i > 0 and arr[i - 1][j] == 1:
		size += f(i - 1, j, count)

	if j > 0 and arr[i][j - 1] == 1:
		size += f(i, j - 1, count)

	if i < N - 1 and arr[i + 1][j] ==1:
		size += f(i + 1, j, count)

	if j < N - 1 and arr[i][j + 1] == 1:
		size += f(i, j + 1, count)

	return size



def run():
	count = 1
	makeFrame(arr, N)
	# for i in arr:print(i)
	for i in range(inputDataLength):
		for j in range(inputDataLength):
			if arr[i][j] == 1:
				table.append( (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) )
				count += 1
				result.append(f(i, j, count))
				result.sort()
		
	for i in range(VIDEO_PROP["frame"] * 3):
		makeFrame(arr, N)

print("?????????????????????????")
print(table)

run()


randarr = []
tarr = [0, 0, 1, 1]
inputDataLength *= 2
for i in range(inputDataLength):
	randarr.append([])
	for j in range(inputDataLength):
		randarr[i].append(tarr[random.randint(0,len(tarr)-1)])
arr = randarr

N = len(arr)
blockLength = min(videoHeight / N, videoWidth / N)

result = []

run()
# count =1 
# for i in arr:print(i)


out.release()