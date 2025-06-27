#!/usr/bin/python

# switches the power profile of your GPU on and off.
# you need to run as root for it to work!

import os
import sys

GPU_PROFILE_DEFAULT=0

# the name of your GPU in /sys/class/drm/. this is usually either card0 or card1! but double check, just to be safe.
# card0 is usually the internal GPU, card1 is usually the dedicated GPU.
GPU_ID="card1"

# normally this script automatically finds the VR power profile number,
# but you can override it by setting this. leave it blank to use autodetect
GPU_VR_PROFILE_OVERRIDE = None

if len(sys.argv) <= 1:
    print("please specify either 'on' or 'off'")
    sys.exit(1)

if sys.argv[1].lower() == "on":
   # Enable manual override
    with open(f"/sys/class/drm/{GPU_ID}/device/power_dpm_force_performance_level", 'w') as f:
        f.write("manual")

    # Translate "VR" into profile number
    if not GPU_VR_PROFILE_OVERRIDE:
      vr_profile = 0
      with open(f"/sys/class/drm/{GPU_ID}/device/pp_power_profile_mode", 'r') as f:
          vr_profiles_raw = f.read()
  
      vr_profiles = vr_profiles_raw.split("\n")
      vr_profile = 0
      for line in vr_profiles:
          if line.find("VR") != -1:
              vr_profile = line.split()[0]
  
      if vr_profile == 0:
          sys.exit(1)
    else:
      vr_profile = GPU_VR_PROFILE_OVERRIDE

    # Set profile to VR
    with open(f"/sys/class/drm/{GPU_ID}/device/pp_power_profile_mode", 'w') as f:
        f.write(vr_profile)

    print("VR power profile enabled")
else:
    # Disable manual override
    with open(f"/sys/class/drm/{GPU_ID}/device/power_dpm_force_performance_level", 'w') as f:
        f.write("auto")

    # Set profile to DEFAULT
    with open(f"/sys/class/drm/{GPU_ID}/device/pp_power_profile_mode", 'w') as f:
        f.write(str(GPU_PROFILE_DEFAULT))

    print("VR power profile disabled")
