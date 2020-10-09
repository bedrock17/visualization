import cv2
import numpy as np
import glob
import videoProperty
import random

def createImage(width, height, rgb_color=(0, 0, 0)):
  """Create new image(numpy array) filled with certain color in RGB"""
  # Create black blank image
  image = np.zeros((height, width, 3), np.uint8)
  # Since OpenCV uses BGR, convert the color first
  color = tuple(reversed(rgb_color))
  # Fill image with color
  image[:] = color
  return image

colorTable = []
out = cv2.VideoWriter(videoProperty.VIDEO_PROP["filename"], cv2.VideoWriter_fourcc(*'MJPG'), videoProperty.VIDEO_PROP["frame"], (videoProperty.VIDEO_PROP["width"], videoProperty.VIDEO_PROP["height"]) )
# font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX  # hand-writing style font

lastimg = None
def step(lst):
  global lastimg

  maxHeight = videoProperty.VIDEO_PROP["height"]
  maxWidth  = videoProperty.VIDEO_PROP["width"]

  blockWidth = maxWidth // len(lst)
  blockHeight = maxHeight // max(lst)

  img = createImage(width=maxWidth, height=maxHeight, rgb_color=(0, 0, 0))
  # print(lst)
  for i in range(len(lst)):
    startx = blockWidth * i
    starty = 0
    stickWidth = blockWidth
    stickHeight = blockHeight * lst[i]
    cv2.rectangle(img, (startx, starty), (startx + stickWidth, starty + stickHeight), colorTable[i%colorTableLength], -1)

  out.write(img)
  lastimg = img

def cmp(a, b):
  return a > b

def bubbleSort(lst, cmp, step = None):
  lstLen = len(lst)
  for i in range(lstLen):
    for j in range(i+1, lstLen):
      if cmp(lst[i], lst[j]):
        lst[i], lst[j] = lst[j], lst[i]
        if step != None:
          step(lst)
        
    print(i)

test = []
# test = [5,4,3,2,1]
for i in range(50):
  test.append(random.randint(0, 500))

for i in range(len(test)):
  tmp = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
  colorTable.append(tmp)
colorTableLength = len(colorTable)

print(test)
bubbleSort(test, cmp, step)
print(test)

for i in range(30):
  out.write(lastimg)

out.release()