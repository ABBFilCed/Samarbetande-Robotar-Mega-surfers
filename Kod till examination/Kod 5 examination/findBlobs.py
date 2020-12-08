import sensor
import image
import lcd
import time

lcd.init(freq=15000000)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)

# color thresholds
green_threshold   = (0,   80,  -70,   -10,   -0,   30)
darkBlue_threshold = (0, 64, 3, 24, -63, -20)
red_threshold = (0, 100, 6, 49, -61, 127)
yellow_threshold = (15, 86, -96, 105, 13, 39)

while True:
    img=sensor.snapshot()
    darkBlueBlobs = img.find_blobs([darkBlue_threshold], area_threshold = 200)
    greenBlobs = img.find_blobs([green_threshold], area_threshold = 200) #  adjust area_threshold to change blob size.
    redBlobs = img.find_blobs([red_threshold], area_threshold = 200)
    yellowBlobs = img.find_blobs([yellow_threshold], area_threshold = 200)

    # statements to find different blobs
    #if darkBlueBlobs:
        #for b in darkBlueBlobs:
            #tmp=img.draw_rectangle(b[0:4])
            #tmp=img.draw_cross(b[5], b[6])
            #c=img.get_pixel(b[5], b[6])
            #print("darkBlue blob found")

    if greenBlobs:
        for b in greenBlobs:
            tmp=img.draw_rectangle(b[0:4])
            tmp=img.draw_cross(b[5], b[6])
            c=img.get_pixel(b[5], b[6])
            print("Green blob found")

    #if redBlobs:
        #for b in redBlobs:
            #tmp=img.draw_rectangle(b[0:4])
            #tmp=img.draw_cross(b[5], b[6])
            #c=img.get_pixel(b[5], b[6])
            #print("Red blob found")

    #if yellowBlobs:
        #for b in yellowBlobs:
            #tmp=img.draw_rectangle(b[0:4])
            #tmp=img.draw_cross(b[5], b[6])
            #c=img.get_pixel(b[5], b[6])
            #print("Yellow blob found")

    lcd.display(img)
