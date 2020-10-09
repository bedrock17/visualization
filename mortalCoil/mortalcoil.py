import cv2
import numpy as np
import glob
from videoProperty import VIDEO_PROP 
import random
from colour import Color
import copy

videoWidth, videoHeight = VIDEO_PROP["width"], VIDEO_PROP["height"]

out = cv2.VideoWriter(VIDEO_PROP["filename"], cv2.VideoWriter_fourcc(*'MPEG'), VIDEO_PROP["frame"], (videoWidth, videoHeight) )

def createImage(width, height, rgb_color=(0, 0, 0)):
  """Create new image(numpy array) filled with certain color in RGB"""
  # Create black blank image
  image = np.zeros((height, width, 3), np.uint8)

  # Since OpenCV uses BGR, convert the color first
  color = tuple(reversed(rgb_color))
  # Fill image with color
  image[:] = color

  return image

# lastimg = None
maxHeight = VIDEO_PROP["height"]
maxWidth  = VIDEO_PROP["width"]

table = []
table.append((0xff, 0xff, 0xff))
table.append((0x00, 0x00, 0x00))
colors = list(Color("red").range_to(Color("blue"), 512))
# for i in range(105):
#   table.append( (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) )
font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX  # hand-writing style font


colorTable = []
for i in colors:
  r,g,b = i.rgb
  t = [r,g,b]
  t = list(map(lambda x: int(x*255), t))
  colorTable.append(t)

colorTableLength = len(colorTable)

gCount = 0
lastArray = None
img = None

lastWidth, lastHeigth = 0,0

def makeFrame(arr, width, height, colorTabelParam = None, level="", path=""):
  global lastArray
  global img
  global lastHeigth
  global lastWidth
  blockLength = min(maxHeight / height, maxWidth / width)
  if lastArray == None or lastWidth != width or lastHeigth != height:
    img = createImage(maxWidth, maxHeight)
    lastHeigth = height
    lastWidth = width
    lastArray = None
  
  # print("STEP 1")

  # print(maxWidth, maxHeight)
  for i in range(height):
    for j in range(width):
      
      startx = int(blockLength * j) +3
      starty = int(blockLength * i) +3
      length = int(blockLength) -3

      # if lastArray != None:
      #   print(lastArray, len(lastArray))
      if lastArray == None or lastArray[i][j] != arr[i][j]:
        if arr[i][j] < 2:
          cv2.rectangle(img, (startx, starty), (startx + length, starty + length), table[arr[i][j] % 2], -1)
        else:
          cv2.rectangle(img, (startx, starty), (startx + length, starty + length), colorTable[arr[i][j] % colorTableLength], -1)

  # startx = int(blockLength * width + 20)
  # cv2.putText(img, level, (startx, 50), font, 2, (0xff,0xff,0xff), 5, cv2.LINE_AA)
  # print("STEP 2")

  # print(img)
  lastArray = copy.deepcopy(arr)
  if VIDEO_PROP["writeVideo"]:
    out.write(img)

    tmparr = sum(arr, [])
    # print(tmparr)
    if (0 in tmparr) == False:
      for i in range(VIDEO_PROP["frame"] * 5):
        out.write(img)
      lastArray = None
      print ("END")

  global gCount
  gCount += 1
  # print(gCount)

  cv2.imshow('frame', img)
  cv2.waitKey(delay=1)
