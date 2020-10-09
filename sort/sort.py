import cv2
import numpy as np
import glob
import videoProperty
import random
from colour import Color

def createImage(width, height, rgb_color=(0, 0, 0)):
	"""Create new image(numpy array) filled with certain color in RGB"""
	# Create black blank image
	image = np.zeros((height, width, 3), np.uint8)

	# Since OpenCV uses BGR, convert the color first
	color = tuple(reversed(rgb_color))
	# Fill image with color
	image[:] = color

	return image

lastimg = None

maxHeight = videoProperty.VIDEO_PROP["height"]
maxWidth  = videoProperty.VIDEO_PROP["width"]

def makeFrame(lst, colorTabelParam = None):
  global lastimg

  table = colorTable
  if colorTabelParam != None:
    table = colorTabelParam
  colorTableLength = len(table)

  blockWidth = maxWidth / len(lst)
  blockHeight = maxHeight / max(lst)

  img = np.zeros((maxHeight, maxWidth, 3), np.uint8)
  # img[:] = black

  # print(lst)
  for i in range(len(lst)):
    stickWidth = int(blockWidth)
    stickHeight = int(blockHeight * lst[i])
    startx = int(blockWidth * i)
    starty = maxHeight - stickHeight

    cv2.rectangle(img, (startx, starty), (startx + stickWidth, starty + stickHeight), table[lst[i]-1], -1)

  out.write(img)
  lastimg = img

  cv2.imshow('frame', img)
  cv2.waitKey(delay=1)

def cmp(a, b):
  return a > b

def bubbleSort(lst, cmp, makeFrame = None, colorTable = None):
  lstLen = len(lst)
  for i in range(lstLen):
    for j in range(0, lstLen-1-i):
      if cmp(lst[j], lst[j+1]):
        lst[j], lst[j+1] = lst[j+1], lst[j]
        # if colorTable != None:
        #   colorTable[j], colorTable[j+1] = colorTable[j+1], colorTable[j]
        if makeFrame != None:
          makeFrame(lst, colorTable)
        
    print(i)

def quick_sort(arr, makeFrame = None, colorTable = None):
  def sort(low, high):
    if high <= low:
      return
    mid = partition(low, high)
    sort(low, mid - 1)
    sort(mid, high)
  def partition(low, high):
    pivot = arr[(low + high) // 2]
    while low <= high:
      while arr[low] < pivot:
        low += 1
      while arr[high] > pivot:
        high -= 1
      if low <= high:
        arr[low], arr[high] = arr[high], arr[low]
        # if colorTable != None:
        #   colorTable[low], colorTable[high] = colorTable[high], colorTable[low]
        if makeFrame != None:
          makeFrame(arr, colorTable)
        low, high = low + 1, high - 1
    return low
  return sort(0, len(arr) - 1)



out = cv2.VideoWriter(videoProperty.VIDEO_PROP["filename"], cv2.VideoWriter_fourcc(*'MPEG'), videoProperty.VIDEO_PROP["frame"], (videoProperty.VIDEO_PROP["width"], videoProperty.VIDEO_PROP["height"]) )

# VIDEOWRITER_PROP_QUALITY 
out.set(cv2.VIDEOWRITER_PROP_QUALITY , 0)
# font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX  # hand-writing style font

test = []
for i in range(100):
  test.append(i+1)
random.shuffle(test)
colorTable = []
colors = list(Color("red").range_to(Color("blue"), len(test)))

for i in colors:
  r,g,b = i.rgb
  t = [r,g,b]
  t = list(map(lambda x: int(x*255), t))
  colorTable.append(t)
print(colorTable)
colorTableLength = len(colorTable)

arr1 = test[:]
color1 = colorTable[:]
bubbleSort(arr1, cmp, makeFrame = makeFrame, colorTable = color1)
for i in range(120):
  out.write(lastimg)
arr2 = test[:]
color2 = colorTable[:]
quick_sort(arr2, makeFrame, color2)
for i in range(120):
  out.write(lastimg)

test = []
for i in range(1000):
  test.append(i+1)
random.shuffle(test)
colorTable = []
colors = list(Color("red").range_to(Color("blue"), len(test)))

for i in colors:
  r,g,b = i.rgb
  t = [r,g,b]
  t = list(map(lambda x: int(x*255), t))
  colorTable.append(t)
print(colorTable)
colorTableLength = len(colorTable)

quick_sort(test, makeFrame, colorTable)

out.release()

# cv2.displayAllWindows()