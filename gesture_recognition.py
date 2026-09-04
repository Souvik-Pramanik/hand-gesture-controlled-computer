import math


# ============================================================
# LANDMARK INDICES
# ============================================================

WRIST = 0

THUMB_MCP = 2
THUMB_IP = 3
THUMB_TIP = 4

INDEX_MCP = 5
INDEX_PIP = 6
INDEX_DIP = 7
INDEX_TIP = 8

MIDDLE_MCP = 9
MIDDLE_PIP = 10
MIDDLE_DIP = 11
MIDDLE_TIP = 12

RING_MCP = 13
RING_PIP = 14
RING_DIP = 15
RING_TIP = 16

PINKY_MCP = 17
PINKY_PIP = 18
PINKY_DIP = 19
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
# ANGLE BETWEEN THREE POINTS
# ============================================================

def angle(a, b, c):

    """
    Calculates angle ABC in degrees.

    a ---- b ---- c

    Straight finger ≈ 180°
    Curled finger  < 150°
    """

    ba_x = a.x - b.x
    ba_y = a.y - b.y

    bc_x = c.x - b.x
    bc_y = c.y - b.y

    dot_product = (
        ba_x * bc_x +
        ba_y * bc_y
    )

    magnitude_ba = math.sqrt(
        ba_x ** 2 +
        ba_y ** 2
    )

    magnitude_bc = math.sqrt(
        bc_x ** 2 +
        bc_y ** 2
    )

    if magnitude_ba == 0 or magnitude_bc == 0:
        return 0

    cosine = dot_product / (
        magnitude_ba * magnitude_bc
    )

    # Prevent floating-point errors
    cosine = max(-1.0, min(1.0, cosine))

    return math.degrees(
        math.acos(cosine)
    )


# ============================================================
# FINGER ANGLES
# ============================================================

def get_finger_angles(hand):

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

    return (
        index_angle,
        middle_angle,
        ring_angle,
        pinky_angle
    )


# ============================================================
# FINGER EXTENSION
# ============================================================

def get_finger_states(hand):

    angles = get_finger_angles(hand)

    index = angles[0] > 155
    middle = angles[1] > 155
    ring = angles[2] > 155
    pinky = angles[3] > 155

    return index, middle, ring, pinky


# ============================================================
# FIST DETECTION
# ============================================================

def is_fist(hand):

    # --------------------------------------------------------
    # Hand size reference
    # --------------------------------------------------------

    hand_size = distance(
        hand[WRIST],
        hand[MIDDLE_MCP]
    )

    if hand_size == 0:
        return False


    # --------------------------------------------------------
    # Fingertip distances from wrist
    # --------------------------------------------------------

    index_distance = distance(
        hand[INDEX_TIP],
        hand[WRIST]
    ) / hand_size

    middle_distance = distance(
        hand[MIDDLE_TIP],
        hand[WRIST]
    ) / hand_size

    ring_distance = distance(
        hand[RING_TIP],
        hand[WRIST]
    ) / hand_size

    pinky_distance = distance(
        hand[PINKY_TIP],
        hand[WRIST]
    ) / hand_size


    # --------------------------------------------------------
    # Determine whether fingers are curled
    # --------------------------------------------------------

    index_curled = index_distance < 1.45
    middle_curled = middle_distance < 1.45
    ring_curled = ring_distance < 1.45
    pinky_curled = pinky_distance < 1.45


    curled_count = sum([
        index_curled,
        middle_curled,
        ring_curled,
        pinky_curled
    ])


    # At least 3 of the 4 fingers must be curled
    return curled_count >= 3


# ============================================================
# OTHER FINGERS CURLED
# ============================================================

def other_fingers_curled(hand):

    return is_fist(hand)


# ============================================================
# THUMB UP
# ============================================================

def is_thumb_up(hand):

    if not other_fingers_curled(hand):
        return False

    thumb_tip = hand[THUMB_TIP]
    thumb_ip = hand[THUMB_IP]
    thumb_mcp = hand[THUMB_MCP]
    wrist = hand[WRIST]

    # Thumb points upward
    return (
        thumb_tip.y < thumb_ip.y
        and
        thumb_ip.y < thumb_mcp.y
        and
        thumb_tip.y < wrist.y - 0.04
    )


# ============================================================
# THUMB DOWN
# ============================================================

def is_thumb_down(hand):

    if not other_fingers_curled(hand):
        return False

    thumb_tip = hand[THUMB_TIP]
    thumb_ip = hand[THUMB_IP]
    thumb_mcp = hand[THUMB_MCP]
    wrist = hand[WRIST]

    # Thumb points downward
    return (
        thumb_tip.y > thumb_ip.y
        and
        thumb_ip.y > thumb_mcp.y
        and
        thumb_tip.y > wrist.y + 0.04
    )


# ============================================================
# PINCH
# ============================================================

def is_pinch(hand):

    thumb_index_distance = distance(
        hand[THUMB_TIP],
        hand[INDEX_TIP]
    )

    return thumb_index_distance < 0.06


# ============================================================
# MAIN GESTURE RECOGNITION
# ============================================================

def recognize_gesture(hand):

    # --------------------------------------------------------
    # PINCH
    # --------------------------------------------------------

    if is_pinch(hand):
        return "PINCH"


    # --------------------------------------------------------
    # THUMB UP
    # --------------------------------------------------------

    if is_thumb_up(hand):
        return "THUMB UP"


    # --------------------------------------------------------
    # THUMB DOWN
    # --------------------------------------------------------

    if is_thumb_down(hand):
        return "THUMB DOWN"


    # --------------------------------------------------------
    # FIST
    # --------------------------------------------------------

    if is_fist(hand):
        return "FIST"


    # --------------------------------------------------------
    # FINGER STATES
    # --------------------------------------------------------

    index, middle, ring, pinky = get_finger_states(hand)

    finger_count = sum([
        index,
        middle,
        ring,
        pinky
    ])


    # --------------------------------------------------------
    # OPEN PALM
    # --------------------------------------------------------

    if finger_count == 4:
        return "OPEN PALM"


    # --------------------------------------------------------
    # ONE FINGER
    # --------------------------------------------------------

    if (
        finger_count == 1
        and index
    ):
        return "ONE FINGER"


    # --------------------------------------------------------
    # TWO FINGERS
    # --------------------------------------------------------

    if (
        finger_count == 2
        and index
        and middle
    ):
        return "TWO FINGERS"


    # --------------------------------------------------------
    # THREE FINGERS
    # --------------------------------------------------------

    if (
        finger_count == 3
        and index
        and middle
        and ring
    ):
        return "THREE FINGERS"


    return "UNKNOWN"