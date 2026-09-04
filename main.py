import cv2
import mediapipe as mp
import pyautogui
import os
import math
import time
import ctypes


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "models",
    "hand_landmarker.task"
)

CAMERA_INDEX = 0

# Gesture must remain stable for this many seconds
GESTURE_STABILITY_TIME = 0.08

# Windows lock requires a longer intentional hold
LOCK_HOLD_TIME = 0.5

# Prevent repeated actions
ACTION_COOLDOWN = 0.25


# ============================================================
# LANDMARK INDICES
# ============================================================

WRIST = 0

THUMB_MCP = 2
THUMB_IP = 3
THUMB_TIP = 4

INDEX_MCP = 5
INDEX_PIP = 6
INDEX_TIP = 8

MIDDLE_MCP = 9
MIDDLE_PIP = 10
MIDDLE_TIP = 12

RING_MCP = 13
RING_PIP = 14
RING_TIP = 16

PINKY_MCP = 17
PINKY_PIP = 18
PINKY_TIP = 20


# ============================================================
# DISTANCE
# ============================================================

def distance(p1, p2):

    return math.sqrt(
        (p2.x - p1.x) ** 2 +
        (p2.y - p1.y) ** 2
    )


# ============================================================
# FINGER DETECTION
# ============================================================

def finger_extended(hand, tip, pip):

    return hand[tip].y < hand[pip].y


def get_fingers(hand):

    index = finger_extended(
        hand,
        INDEX_TIP,
        INDEX_PIP
    )

    middle = finger_extended(
        hand,
        MIDDLE_TIP,
        MIDDLE_PIP
    )

    ring = finger_extended(
        hand,
        RING_TIP,
        RING_PIP
    )

    pinky = finger_extended(
        hand,
        PINKY_TIP,
        PINKY_PIP
    )

    return index, middle, ring, pinky


# ============================================================
# THUMB UP
# ============================================================

def is_thumb_up(hand):

    index, middle, ring, pinky = get_fingers(hand)

    # All other fingers should be folded
    if index or middle or ring or pinky:
        return False

    thumb_tip_y = hand[THUMB_TIP].y
    thumb_ip_y = hand[THUMB_IP].y
    thumb_mcp_y = hand[THUMB_MCP].y
    wrist_y = hand[WRIST].y

    return (
        thumb_tip_y < thumb_ip_y
        and
        thumb_ip_y < thumb_mcp_y
        and
        thumb_tip_y < wrist_y - 0.04
    )


# ============================================================
# THUMB DOWN
# ============================================================

def is_thumb_down(hand):

    index, middle, ring, pinky = get_fingers(hand)

    # All other fingers should be folded
    if index or middle or ring or pinky:
        return False

    thumb_tip_y = hand[THUMB_TIP].y
    thumb_ip_y = hand[THUMB_IP].y
    thumb_mcp_y = hand[THUMB_MCP].y
    wrist_y = hand[WRIST].y

    return (
        thumb_tip_y > thumb_ip_y
        and
        thumb_ip_y > thumb_mcp_y
        and
        thumb_tip_y > wrist_y + 0.04
    )


# ============================================================
# PINCH
# ============================================================

def is_pinch(hand):

    d = distance(
        hand[THUMB_TIP],
        hand[INDEX_TIP]
    )

    return d < 0.06


# ============================================================
# FIST
# ============================================================

def is_fist(hand):

    # Calculate palm size
    palm_size = distance(
        hand[WRIST],
        hand[MIDDLE_MCP]
    )

    if palm_size == 0:
        return False

    # Finger tip distances from wrist
    index_distance = distance(
        hand[INDEX_TIP],
        hand[WRIST]
    ) / palm_size

    middle_distance = distance(
        hand[MIDDLE_TIP],
        hand[WRIST]
    ) / palm_size

    ring_distance = distance(
        hand[RING_TIP],
        hand[WRIST]
    ) / palm_size

    pinky_distance = distance(
        hand[PINKY_TIP],
        hand[WRIST]
    ) / palm_size

    # A curled finger should be relatively close
    # to the palm.
    threshold = 1.65

    curled = [
        index_distance < threshold,
        middle_distance < threshold,
        ring_distance < threshold,
        pinky_distance < threshold
    ]

    return sum(curled) >= 3


# ============================================================
# GESTURE RECOGNITION
# ============================================================

def recognize_gesture(hand):

    # IMPORTANT:
    # Thumb detection is checked first and kept independent.

    if is_thumb_up(hand):
        return "THUMB UP"

    if is_thumb_down(hand):
        return "THUMB DOWN"

    if is_pinch(hand):
        return "PINCH"

    if is_fist(hand):
        return "FIST"

    index, middle, ring, pinky = get_fingers(hand)

    count = sum([
        index,
        middle,
        ring,
        pinky
    ])

    if count == 4:
        return "OPEN PALM"

    if count == 1 and index:
        return "ONE FINGER"

    if count == 2 and index and middle:
        return "TWO FINGERS"

    if count == 3 and index and middle and ring:
        return "THREE FINGERS"

    return "UNKNOWN"


# ============================================================
# WINDOWS VOLUME
# ============================================================

from pycaw.pycaw import AudioUtilities

audio_device = AudioUtilities.GetSpeakers()
volume_control = audio_device.EndpointVolume


def volume_up():

    current = volume_control.GetMasterVolumeLevelScalar()

    new_value = min(
        current + 0.05,
        1.0
    )

    volume_control.SetMasterVolumeLevelScalar(
        new_value,
        None
    )

    print(
        f"🔊 Volume: {int(new_value * 100)}%"
    )


def volume_down():

    current = volume_control.GetMasterVolumeLevelScalar()

    new_value = max(
        current - 0.05,
        0.0
    )

    volume_control.SetMasterVolumeLevelScalar(
        new_value,
        None
    )

    print(
        f"🔉 Volume: {int(new_value * 100)}%"
    )


# ============================================================
# SCREENSHOT
# ============================================================

def take_screenshot():

    filename = time.strftime(
        "screenshot_%Y%m%d_%H%M%S.png"
    )

    path = os.path.join(
        os.path.expanduser("~/Pictures"),
        filename
    )

    os.makedirs(
        os.path.dirname(path),
        exist_ok=True
    )

    screenshot = pyautogui.screenshot()

    screenshot.save(path)

    print(
        f"📸 Screenshot saved: {path}"
    )


# ============================================================
# PLAY / PAUSE
# ============================================================

def play_pause():

    pyautogui.press("playpause")

    print("▶️ Play/Pause")


# ============================================================
# WINDOWS LOCK
# ============================================================

def lock_windows():

    print("🔒 Locking Windows...")

    ctypes.windll.user32.LockWorkStation()


# ============================================================
# ACTION EXECUTION
# ============================================================

def execute_action(gesture):

    if gesture == "THUMB UP":

        volume_up()

        return "Volume Up"

    elif gesture == "THUMB DOWN":

        volume_down()

        return "Volume Down"

    elif gesture == "TWO FINGERS":

        take_screenshot()

        return "Screenshot"

    elif gesture == "PINCH":

        play_pause()

        return "Play/Pause"

    return None


# ============================================================
# DRAW LANDMARKS
# ============================================================

def draw_hand(frame, hand):

    height, width, _ = frame.shape

    connections = [

        # Palm
        (0, 1),
        (1, 5),
        (5, 9),
        (9, 13),
        (13, 17),
        (17, 0),

        # Thumb
        (1, 2),
        (2, 3),
        (3, 4),

        # Index
        (5, 6),
        (6, 7),
        (7, 8),

        # Middle
        (9, 10),
        (10, 11),
        (11, 12),

        # Ring
        (13, 14),
        (14, 15),
        (15, 16),

        # Pinky
        (17, 18),
        (18, 19),
        (19, 20)
    ]

    for start, end in connections:

        x1 = int(hand[start].x * width)
        y1 = int(hand[start].y * height)

        x2 = int(hand[end].x * width)
        y2 = int(hand[end].y * height)

        cv2.line(
            frame,
            (x1, y1),
            (x2, y2),
            (255, 0, 0),
            2
        )

    for point in hand:

        x = int(point.x * width)
        y = int(point.y * height)

        cv2.circle(
            frame,
            (x, y),
            5,
            (0, 255, 0),
            -1
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("🖐️ HAND GESTURE CONTROL SYSTEM")
    print("=" * 60)

    print()
    print("Controls:")
    print("👍  Volume Up")
    print("👎  Volume Down")
    print("✌️  Screenshot")
    print("👌  Play/Pause")
    print("✊  Hold to Lock Windows")
    print()
    print("Press Q to quit.")
    print("=" * 60)


    # --------------------------------------------------------
    # CAMERA
    # --------------------------------------------------------

    camera = cv2.VideoCapture(
        CAMERA_INDEX
    )

    if not camera.isOpened():

        print("ERROR: Camera could not be opened.")

        return


    # --------------------------------------------------------
    # MEDIAPIPE
    # --------------------------------------------------------

    BaseOptions = mp.tasks.BaseOptions

    HandLandmarker = (
        mp.tasks.vision.HandLandmarker
    )

    HandLandmarkerOptions = (
        mp.tasks.vision.HandLandmarkerOptions
    )

    RunningMode = (
        mp.tasks.vision.RunningMode
    )


    options = HandLandmarkerOptions(

        base_options=BaseOptions(
            model_asset_path=MODEL_PATH
        ),

        running_mode=RunningMode.VIDEO,

        num_hands=1,

        min_hand_detection_confidence=0.5,

        min_hand_presence_confidence=0.5,

        min_tracking_confidence=0.5
    )


    # --------------------------------------------------------
    # GESTURE STATE
    # --------------------------------------------------------

    current_gesture = "NONE"

    gesture_start_time = 0

    last_action_time = 0

    lock_triggered = False


    # --------------------------------------------------------
    # DETECTOR
    # --------------------------------------------------------

    with HandLandmarker.create_from_options(
        options
    ) as detector:

        timestamp = 0


        while True:

            success, frame = camera.read()

            if not success:

                print(
                    "ERROR: Could not read camera."
                )

                break


            # Mirror
            frame = cv2.flip(
                frame,
                1
            )


            # RGB
            rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )


            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb
            )


            # Detect
            result = detector.detect_for_video(
                mp_image,
                timestamp
            )

            timestamp += 33


            gesture = "NO HAND"

            action = None


            # ------------------------------------------------
            # HAND DETECTED
            # ------------------------------------------------

            if result.hand_landmarks:

                hand = result.hand_landmarks[0]

                draw_hand(
                    frame,
                    hand
                )

                gesture = recognize_gesture(
                    hand
                )


                # --------------------------------------------
                # GESTURE CHANGED
                # --------------------------------------------

                if gesture != current_gesture:

                    current_gesture = gesture

                    gesture_start_time = time.time()

                    lock_triggered = False


                # --------------------------------------------
                # HOW LONG GESTURE IS HELD
                # --------------------------------------------

                held_time = (
                    time.time()
                    -
                    gesture_start_time
                )


                # --------------------------------------------
                # LOCK WINDOWS
                # --------------------------------------------

                if (
                    gesture == "FIST"
                    and
                    held_time >= LOCK_HOLD_TIME
                    and
                    not lock_triggered
                ):

                    lock_windows()

                    lock_triggered = True


                # --------------------------------------------
                # NORMAL ACTIONS
                # --------------------------------------------

                elif (
                    gesture != "FIST"
                    and
                    gesture != "UNKNOWN"
                    and
                    held_time >= GESTURE_STABILITY_TIME
                    and
                    time.time() - last_action_time
                    >= ACTION_COOLDOWN
                ):

                    action = execute_action(
                        gesture
                    )

                    if action:

                        last_action_time = time.time()


            else:

                current_gesture = "NO HAND"

                gesture_start_time = time.time()

                lock_triggered = False


            # =================================================
            # UI
            # =================================================

            cv2.putText(
                frame,
                "HAND GESTURE CONTROLLER",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 255),
                2
            )


            cv2.putText(
                frame,
                f"Gesture: {gesture}",
                (20, 85),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )


            if result.hand_landmarks:

                held = (
                    time.time()
                    -
                    gesture_start_time
                )

                cv2.putText(
                    frame,
                    f"Held: {held:.1f}s",
                    (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2
                )


            if action:

                cv2.putText(
                    frame,
                    f"Action: {action}",
                    (20, 160),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 255),
                    2
                )


            cv2.putText(
                frame,
                "Q = Quit",
                (20, 200),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )


            # Show
            cv2.imshow(
                "Hand Gesture Controller",
                frame
            )


            # Quit
            if cv2.waitKey(1) & 0xFF == ord("q"):

                break


    camera.release()

    cv2.destroyAllWindows()

    print("Program closed.")


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()