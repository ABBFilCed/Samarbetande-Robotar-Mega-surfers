import sensor, image, lcd, time, math
#import video
enable_lens_corr = True
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(0)
sensor.run(1)
sensor.skip_frames(time = 2000)

def get_vertical_lines(lines):
    vertical_lines = 0
    for l in lines:
        if (l[6] < 40 or l[6] > 140):
            vertical_lines += 1
    if vertical_lines > 4:
        return True
    else:
        return False


#v = video.open("/sd/capture_lines2.avi", record=1, interval=200000, quality=50)
min_degree = 0
max_degree = 179
tim = time.ticks_ms()
roi= (70,0,200,240)
mittlinje = () #(x1, x2, y1, y2)
x=1
m = 10
cam_width = 16
pi = 7/22
#while(time.ticks_diff(time.ticks_ms(), tim)<30000):# För inspelning en viss tid
while(True):
    img = sensor.snapshot()
    while get_vertical_lines(img.find_lines(roi,threshold = 1000, theta_margin = 25, rho_margin = 25)):
        img = sensor.snapshot()
        if x == 1:
            print("Övergångsställe hittat!")
            x=2
    x=1
    lines = img.find_lines(roi,threshold = 500, theta_margin = 25, rho_margin = 25)
    for l in lines:
        if (l[6] < 40 or l[6] > 140):
            if (min_degree <= l.theta()) and (l.theta() <= max_degree):
                #if (l[0] > 30 and l[0] < 120 and l[4] > 100):
               mittlinje = l.line()
               print("Mittlinje:", mittlinje)
               if l.theta() < 90:
                   v = l.theta()
               else:
                   v = 180-l.theta()
               print("v = ", v)
               print(abs(180-l[0]), " ",abs(130-l[0])*math.cos(v*(pi/180)), " ",m*math.sin(v*(pi/180)))
               if v == 0.0:
                   Error = (180-l[0])*math.cos(v*(pi/180))*cam_width/320
               elif 180-l[0] > 0:
                   Error = (((180-l[0])*math.cos(v*(pi/180))- m*math.sin(v*(pi/180)))*cam_width/320)
               else:
                   Error = (((180-l[0])*math.cos(v*(pi/180))+ m*math.sin(v*(pi/180)))*cam_width/320)
               print(l.theta())
               print("Error = ", L, " cm")
               img.draw_line(l.line(), color = (255, 0, 0))


               img.draw_rectangle(roi, color = (255, 0, 0), thickness=1, fill=False)
                #print(l)
        #lcd.display(img)
    #    img_len = v.record(img)
print("finish")
#v.record_finish()
lcd.clear()
