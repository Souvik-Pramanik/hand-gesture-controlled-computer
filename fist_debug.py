import cv2
import mediapipe as mp
import os
import math


# ============================================================
# MODEL
# ============================================================

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "models",
    "hand_landmarker.task"
)


# ============================================================
# LANDMARKS
# ============================================================

WRIST = 0

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
# ANGLE
# ============================================================

def angle(a, b, c):

    ba_x = a.x - b.x
    ba_y = a.y - b.y

    bc_x = c.x - b.x
    bc_y = c.y - b.y

    dot = (
        ba_x * bc_x +
        ba_y * bc_y
    )

    mag_ba = math.sqrt(
        ba_x ** 2 +
        ba_y ** 2
    )

    mag_bc = math.sqrt(
        bc_x ** 2 +
        bc_y ** 2
    )

    if mag_ba == 0 or mag_bc == 0:
        return 0

    cosine = dot / (
        mag_ba * mag_bc
    )

    cosine = max(-1, min(1, cosine))

    return math.degrees(
        math.acos(cosine)
    )


# ============================================================
# MEDIAPIPE
# ============================================================

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode


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


# ============================================================
# CAMERA
# ============================================================

camera = cv2.VideoCapture(0)

if not camera.isOpened():

    print("Could not open camera.")
    exit()


# ============================================================
# MAIN
# ============================================================

with HandLandmarker.create_from_options(options) as detector:

    timestamp = 0

    while True:

        success, frame = camera.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        result = detector.detect_for_video(
            mp_image,
            timestamp
        )

        timestamp += 33


        # ====================================================
        # DETECTION
        # ====================================================

        if result.hand_landmarks:

            hand = result.hand_landmarks[0]

            # -----------------------------------------------
            # ANGLES
            # -----------------------------------------------

            index_angle = angle(
                hand[INDEX_MCP],
                hand[INDEX_PIP],
                hand[INDEX_TIP]
            )

            middle_angle = angle(
                hand[MIDDLE_MCP],
                hand[MIDDLE_PIP],
                hand[MIDDLE_TIP]
            )

            ring_angle = angle(
                hand[RING_MCP],
                hand[RING_PIP],
                hand[RING_TIP]
            )

            pinky_angle = angle(
                hand[PINKY_MCP],
                hand[PINKY_PIP],
                hand[PINKY_TIP]
            )


            # -----------------------------------------------
            # WRIST DISTANCES
            # -----------------------------------------------

            index_dist = distance(
                hand[INDEX_TIP],
                hand[WRIST]
            )

            middle_dist = distance(
                hand[MIDDLE_TIP],
                hand[WRIST]
            )

            ring_dist = distance(
                hand[RING_TIP],
                hand[WRIST]
            )

            pinky_dist = distance(
                hand[PINKY_TIP],
                hand[WRIST]
            )


            # -----------------------------------------------
            # DISPLAY
            # -----------------------------------------------

            y = 40

            values = [
                f"INDEX angle : {index_angle:.1f}",
                f"MIDDLE angle: {middle_angle:.1f}",
                f"RING angle  : {ring_angle:.1f}",
                f"PINKY angle : {pinky_angle:.1f}",
                "",
                f"INDEX wrist : {index_dist:.3f}",
                f"MIDDLE wrist: {middle_dist:.3f}",
                f"RING wrist  : {ring_dist:.3f}",
                f"PINKY wrist : {pinky_dist:.3f}",
            ]

            for text in values:

                cv2.putText(
                    frame,
                    text,
                    (20, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 255),
                    2
                )

                y += 30


        # ====================================================
        # SHOW
        # ====================================================

        cv2.imshow(
            "Fist Diagnostic",
            frame
        )


        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


camera.release()

cv2.destroyAllWindows()