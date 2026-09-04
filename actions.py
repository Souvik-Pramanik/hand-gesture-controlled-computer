import time

from pycaw.pycaw import AudioUtilities


# ============================================================
# AUDIO SETUP
# ============================================================

device = AudioUtilities.GetSpeakers()

volume = device.EndpointVolume


# ============================================================
# VOLUME FUNCTIONS
# ============================================================

def volume_up(step=0.05):

    current_volume = volume.GetMasterVolumeLevelScalar()

    new_volume = min(
        current_volume + step,
        1.0
    )

    volume.SetMasterVolumeLevelScalar(
        new_volume,
        None
    )

    print(
        f"Volume Up: {int(new_volume * 100)}%"
    )


def volume_down(step=0.05):

    current_volume = volume.GetMasterVolumeLevelScalar()

    new_volume = max(
        current_volume - step,
        0.0
    )

    volume.SetMasterVolumeLevelScalar(
        new_volume,
        None
    )

    print(
        f"Volume Down: {int(new_volume * 100)}%"
    )


# ============================================================
# ACTION MANAGER
# ============================================================

class ActionManager:

    def __init__(self):

        self.last_action_time = 0

        self.cooldown = 0.8


    def can_execute(self):

        current_time = time.time()

        if (
            current_time -
            self.last_action_time
            >= self.cooldown
        ):

            self.last_action_time = current_time

            return True

        return False


    def execute(self, gesture):

        if not self.can_execute():

            return None


        if gesture == "THUMB UP":

            volume_up()

            return "Volume Up"


        elif gesture == "THUMB DOWN":

            volume_down()

            return "Volume Down"


        return None


# ============================================================
# TEST
# ============================================================

# if __name__ == "__main__":

#     print("=" * 40)
#     print("AUDIO CONTROL TEST")
#     print("=" * 40)

#     current = volume.GetMasterVolumeLevelScalar()

#     print(
#         f"Current Volume: {int(current * 100)}%"
#     )

#     print("Increasing volume...")
#     volume_up()

#     time.sleep(2)

#     print("Decreasing volume...")
#     volume_down()

#     print("Test completed.")