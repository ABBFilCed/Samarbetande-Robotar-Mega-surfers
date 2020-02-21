import sensor, image, lcd, time
#import video
enable_lens_corr = True
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
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
roi= (0,0,160,120)
mittlinje = () #(x1, x2, y1, y2)
x=1
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
        if (min_degree <= l.theta()) and (l.theta() <= max_degree):
            if (l[0] > 30 and l[0] < 120 and l[4] > 100):
               mittlinje = l.line()
               print("Mittlinje:", mittlinje)
            #img.draw_line(l.line(), color = (255, 0, 0))
            #img.draw_rectangle(ro i, color = (255, 0, 0), thickness=1, fill=False)
            #print(l)
    #lcd.display(img)
#    img_len = v.record(img)
print("finish")
#v.record_finish()
lcd.clear()
