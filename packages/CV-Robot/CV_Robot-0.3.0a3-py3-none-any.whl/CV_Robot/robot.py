try:
    # noinspection PyShadowingBuiltins
    from printlog import printlog as print
except ImportError:
    pass

#from CV_Robot import is_Server, is_Robot

target_drive_speed = 75

def forward():
    """
    Moves robot forward at speed set by speed command.

    Runs emulated code if GPIO backend not found.
    """
    print("Driving forward...")

def backward():
    """
    Moves robot backward at speed set by speed command.

    Runs emulated code if GPIO backend not found.
    """
    print("Driving backward...")

def left():
    """
    Turns robot left at speed set by speed command.

    Runs emulated code if GPIO backend not found.
    """
    print("Turning left...")

def right():
    """
    Turns robot right at speed set by speed command.

    Runs emulated code if GPIO backend not found.
    """
    print("Turning right...")

def stop():
    """
    Sets speed of all motors to 0.

    Runs emulated code if GPIO backend not found.
    """
    print("Stopping robot...")

def speed(val):
    """
    Sets driving speed to value specified
    """
    global target_drive_speed
    target_drive_speed = val