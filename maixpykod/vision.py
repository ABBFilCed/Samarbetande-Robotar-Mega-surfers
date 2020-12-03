import sensor
import image
import lcd
import time
import math
from fpioa_manager import fm
from board import board_info
from time import time
from machine import UART


class Midline():
    """Class that holds the latest midline props."""

    def __init__(self):
        self.l = ()
        self.line_props = ()
        self.theta = 0
        self.visible = False
        self.delta_theta = 0
        self.roi = (120, 0, 80, 240)

    def print_line(self):
        """Print line properties."""
        print(self.line_props)

    def update_line(self, l, delta_theta):
        """Update to the latest values."""
        self.l = l
        self.line_props = l.line()
        self.theta = convert_theta_val(l.theta())
        self.visible = True
        self.delta_theta = delta_theta

    def draw_line(self, img):
        """Draw line to screen."""
        img.draw_line(self.l.line(), color=(255, 0, 0))

    def reset_roi(self):
        """Reset midline, e.g. after turning"""
        self.roi = (120, 120, 80, 120)


class Robot():
    """Class to hold robot data."""

    def __init__(self):
        self.err = 0
        self.turning = False
        self.new_part = True
        self.update_midline = True

    def update_err(self, err):
        """Update to latest error values"""
        self.err = err


class Settings():
    """Class which holds global settings"""

    def __init__(self):
        # Different rois for crossings
        self.crossing_rois = [{"pos": "mid_bottom", "roi": (90, 120, 140, 120)},
                              {"pos": "left", "roi": (0, 40, 60, 160)},
                              {"pos": "mid_top", "roi": (90, 0, 140, 120)},
                              {"pos": "right", "roi": (250, 40, 70, 160)},
                              ]
        self.cam_width = 16  # Width of camera in cm
        # x-stride, y-stride, threshold, theta_margin, rho_margin
        self.v_crossing_settings = 2, 1, 1000, 10, 10
        self.h_crossing_settings = 2, 1, 1000, 5, 5
        self.midline_settings = 5, 300, 400, 25, 25
        self.h_line_settings = 10, 1, 800, 25, 25
        self.uart_timeout = 50
        self.sending_index = 0
        self.sending_labels = ["edi", "ome"]


def initialize(uart_timeout):
    """Initialize the camera and lcd."""
    lcd.init(freq=15000000)
    sensor.reset(freq=20000000, set_regs=True, dual_buff=True)
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_hmirror(False)
    sensor.set_vflip(False)
    sensor.skip_frames(time=2000)
    fm.register(board_info.PIN15, fm.fpioa.UART1_TX)
    uart_A = UART(UART.UART1, 115200, 8, 0, 0,
                  timeout=uart_timeout, read_buf_len=4096)
    last_time = time()
    return uart_A, last_time


def take_snapshot():
    """Turn on, take an image and then shut down the camera"""
    sensor.run(1)
    # Use grayscale for line detection
    img = sensor.snapshot().to_grayscale()
    sensor.run(0)
    return img


def convert_theta_val(theta):
    """Converts theta value to 90 > theta > -90"""
    if theta < 90:
        converted_theta = theta
    else:
        converted_theta = -(180 - theta)
    return converted_theta


def get_delta_theta(midline, l):
    """Calculates delta theta."""
    latest_theta = midline.theta
    current_theta = convert_theta_val(l.theta())
    return (current_theta-latest_theta)


def get_midline(lines, midline):
    """Picks a midline from possible line candidates."""
    for l in lines:
        if l.theta() < 20 or l.theta() > 160:
            #img.draw_line(l.line(), color=(255, 0, 0))
            delta_theta = get_delta_theta(midline, l)
            midline.update_line(l, delta_theta)
            break


def get_error(midline, cam_width, robot):
    """Calculates error based on distance from midline."""
    Error = (midline.l.x1()-160)*(cam_width/320)
    robot.update_err(Error)


def update_midline(img, settings, midline, robot):
    """Updates midline and error."""
    lines = img.find_lines(midline.roi, *
                           settings.midline_settings)
    get_midline(lines, midline)
    # Only do calculations if the midline is visible.
    if midline.visible:
        # Calculate error to regulate steering.
        get_error(midline, settings.cam_width, robot)
        # Update roi
        #print("x1: " + str(midline.l.x1()))
        #print("x2: " + str(midline.l.x2()))
        #print("diff: " + str(midline.l.x2() - midline.l.x1()))
        if midline.l.x1() < midline.l.x2():
            midline.roi = (midline.l.x1() - 30, 0, midline.l.x2() - midline.l.x1() + 60, 240)
        else:
            midline.roi = (midline.l.x2() - 30, 0, midline.l.x1() - midline.l.x2() + 60, 240)


def v_line(l):
    """Returns True if line is vertical"""
    if l.theta() < (10) or l.theta() > 170:
        return True
    else:
        return False


def h_line(l):
    """Return True if a line is horizontal"""
    if l.theta() > 35 and l.theta() < 145:
        return True
    else:
        return False


def find_crossings(crossing_rois, v_crossing_settings, h_crossing_settings):
    """Returns True if more than 4 vertical lines are found."""
    crossing_list = []
    n_lines = 0
    # Loops through all the given rois(possible crossings)
    for roi in crossing_rois:
        # Crossings in the middle has vertical lines; |||. Crossings on the sides are horizontal; =.
        if roi['pos'].startswith('mid'):
            lines = img.find_lines(roi['roi'], *v_crossing_settings)
        else:
            lines = img.find_lines(roi['roi'], *h_crossing_settings)
        for l in lines:
            if roi['pos'].startswith('mid') and v_line(l):
                n_lines += 1
            elif not roi['pos'].startswith('mid') and h_line(l):
                n_lines += 1
        if n_lines > 4:
            crossing_list.append(roi)
        n_lines = 0
    return crossing_list


def detect_junctions(crossings, img, h_line_settings):
    """Detects junctions by crossing- and img-data."""
    # 4 way-junctions have 4 crossings.
    junct = False
    if len(crossings) == 4:
        #print("4-way crossing ahead!")
        junct = "4_W"
    elif len(crossings) == 1:
        # A t-junction with <-- and --> has a crossing and a horizontal midline.
        if crossings[0]['pos'] == "mid_bottom":
            for l in img.find_lines((0, 0, 320, 120), *h_line_settings):
                if h_line(l):
                    #print("T-junction ahead!")
                    img.draw_line(l.line(), color=(255, 0, 0), thickness=3)
                    junct = "T_LR"
        elif crossings[0]['pos'] == "left":
            junct = "T_L"
        elif crossings[0]['pos'] == "right":
            junct = "T_R"
        else:
            junct = "Ahead"

    return junct


def check_for_curve(midline):
    """Detects a turn if line angle suddenly changes by more than a certain number."""
    crv = False
    img.draw_string(60, 100, str(midline.delta_theta), scale=2)
    if midline.delta_theta > 10:
        crv = "Curve -->"
    elif midline.delta_theta < -10:
        crv = "Curve <--"
    return crv


def update_pos(settings, img, midline, robot):
    """Returns roadtype ahead."""
    crossings = find_crossings(
        settings.crossing_rois, settings.v_crossing_settings, settings.h_crossing_settings)

    # Detect if junction ahead
    junction = detect_junctions(crossings, img, settings.h_line_settings)
    curve = check_for_curve(midline)
    robot.update_midline = True
    if junction:
        robot.update_midline = False
        midline.reset_roi()
        return junction
    elif curve:
        return curve
    else:
        return "Straight"


def draw_roi(img, roi, filled=False):
    """Draws out a rectangle by the same size and coordinates as the roi."""
    img.draw_rectangle(roi, color=(255, 0, 0),
                       thickness=3, fill=filled)


def draw_onscreen(midline, img, settings, pos, robot):
    """Draws relevant information on the screen."""
    if midline.visible and robot.update_midline:
        # Visualise midline and region of interest
        midline.draw_line(img)
        # Visualise error
        img.draw_line((int((midline.l.x1()+midline.l.x2())/2), 120, int((midline.l.x1() +
                                                                         midline.l.x2())/2+robot.err*20), 120), color=(255, 0, 0), thickness=5)
    # Draw out used rois
    draw_roi(img, midline.roi)
    img.draw_string(100, 100, pos, scale=2)
    img.draw_string(0, 120, "Fel: " + str(robot.err-1) +
                    "vinkel: " + str(midline.theta), scale=2)
    # for crossing in settings.crossing_rois:
    # Fill if a crossing is found in the roi.
    # if crossing in crossings:
    #draw_roi(img, crossing['roi'], True)
    # else:
    #draw_roi(img, crossing['roi'])
    lcd.display(img)


def send_error(robot, midline, settings, uart_A):
    index = settings.sending_index
    label = settings.sending_labels[index]
    if label == "edi":
        uart_A.write(label + ":" + str(robot.err-1.75))
        print(str(robot.err-1.75))
    elif label == "ome":
        uart_A.write(label + ":" + str(midline.theta))
    index = 1 - index
    settings.sending_index = index
    last_time = time()
    return last_time


midline = Midline()  # (x1, x2, y1, y2)
robot = Robot()
settings = Settings()
uart_A, last_time = initialize(settings.uart_timeout)


while(True):
    # Robot is blind while turning
    if not robot.turning:
        img = take_snapshot()
        #img = modify_img(take_snapshot(), settings)
        # Get current position and midline
        if robot.update_midline:
            update_midline(img, settings, midline, robot)
        if robot.new_part:
            pos = update_pos(settings, img, midline, robot)
        # Draw output to lcd
        draw_onscreen(midline, img, settings, pos, robot)
        delta_time = time() - last_time
        draw_roi(img, midline.roi)
        last_time = send_error(robot, midline, settings, uart_A)
        #print("Sending to arduino")
    else:
        robot.update_midline = False
print("finish")
lcd.clear()
