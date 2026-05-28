import time
import sys
import random

class Colors:
    # Bright/Light shades requested by user
    LIGHT_RED = '\033[91m'      # Bright Red
    LIGHT_VIOLET = '\033[95m'   # Bright Magenta / Violet
    LIGHT_PURPLE = '\033[38;5;141m' # Light Purple (256 color)
    LIGHT_GREEN = '\033[92m'    # Bright Green
    LIGHT_BLUE = '\033[96m'     # Bright Cyan / Light Blue
    
    # Keeping original names for backwards compatibility if needed
    HEADER = '\033[38;5;141m'   # Light Purple
    OKBLUE = '\033[96m'         # Light Blue
    OKCYAN = '\033[96m'         # Light Blue
    OKGREEN = '\033[92m'        # Light Green
    WARNING = '\033[93m'        # Bright Yellow
    FAIL = '\033[91m'           # Light Red
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_slow(text, delay=0.01, color=Colors.ENDC, end='\n'):
    """Prints text slowly with a specified color."""
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(Colors.ENDC)
    sys.stdout.write(end)
    sys.stdout.flush()

def animate_typing_human(text, delay_base=0.015, color=Colors.ENDC, end='\n'):
    """Types out text with random delays to simulate human typing."""
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(max(0.002, delay_base + random.uniform(-0.005, 0.02)))
    sys.stdout.write(Colors.ENDC)
    sys.stdout.write(end)
    sys.stdout.flush()

def print_color(text, color=Colors.ENDC, end='\n'):
    """Prints text instantly with a specified color."""
    sys.stdout.write(color + text + Colors.ENDC + end)
    sys.stdout.flush()

def animate_spinner(message, duration=0.8):
    """Shows a spinner animation for a short duration."""
    spinner_chars = ['|', '/', '-', '\\']
    end_time = time.time() + duration
    sys.stdout.write(Colors.OKCYAN + message + " ")
    i = 0
    while time.time() < end_time:
        sys.stdout.write(spinner_chars[i % len(spinner_chars)])
        sys.stdout.flush()
        time.sleep(0.05)
        sys.stdout.write('\b')
        i += 1
    sys.stdout.write(Colors.OKGREEN + "Done!" + Colors.ENDC + "\n")
    sys.stdout.flush()

def animate_progress_bar(message, duration=0.8, length=30, color=Colors.OKCYAN):
    """Shows a filling progress bar."""
    sys.stdout.write(color + message + " [" + Colors.ENDC)
    steps = length
    sleep_time = duration / steps
    for i in range(steps):
        sys.stdout.write(color + "█" + Colors.ENDC)
        sys.stdout.flush()
        time.sleep(sleep_time)
    sys.stdout.write(color + "] " + Colors.OKGREEN + "Complete!\n" + Colors.ENDC)
    sys.stdout.flush()
