#!/usr/bin/env python3
# rigel-visualizer.py
# Lupita-Luksie Protocol - Zenith Calibration Kit
# 
# What this does:
# Shows Rigel's path across the sky on any date from any location.
# No hardware required. Just a laptop and curiosity.

from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time
from astropy import units as u
import numpy as np
import matplotlib.pyplot as plt

def main():
    print("=" * 50)
    print("  LUPITA-LUKSIE PROTOCOL")
    print("  Zenith Calibration Kit")
    print("  rigel-visualizer.py v1.0")
    print("=" * 50)
    print("\nNo hardware needed. Just a screen and curiosity.")

    # Default to Lupita
    default_lat = -7.5
    default_lon = 31.0

    print(f"\nDefault location: Lupita Island (Lat: {default_lat}°, Lon: {default_lon}°)")
    use_default = input("Use these coordinates? (y/n): ").strip().lower()

    if use_default == 'n':
        lat = float(input("Enter your Latitude (e.g., -7.5): "))
        lon = float(input("Enter your Longitude (e.g., 31.0): "))
    else:
        lat = default_lat
        lon = default_lon

    # Get the date
    year = int(input("Enter Year (e.g., 2026): "))
    month = int(input("Enter Month (e.g., 9): "))
    day = int(input("Enter Day (e.g., 15): "))

    # Rigel
    rigel = SkyCoord(ra=78.6345 * u.deg, dec=-8.2016 * u.deg, frame='icrs')
    observer = EarthLocation(lat=lat * u.deg, lon=lon * u.deg)

    # Generate timestamps every 10 minutes
    start = Time(f"{year}-{month:02d}-{day:02d} 00:00:00")
    end = Time(f"{year}-{month:02d}-{day:02d} 23:59:00")
    times = Time(np.arange(start.unix, end.unix, 600), format='unix')

    # Calculate altitude and azimuth
    altaz_frame = AltAz(location=observer, obstime=times)
    rigel_altaz = rigel.transform_to(altaz_frame)
    altitudes = rigel_altaz.alt.deg
    azimuths = rigel_altaz.az.deg

    # Plot altitude over time
    plt.figure(figsize=(12, 5))
    plt.plot(times.datetime, altitudes, label='Rigel Altitude', color='blue', linewidth=2)
    plt.axhline(90, color='red', linestyle='--', label='Zenith (90°)', linewidth=1.5)
    plt.axhline(0, color='gray', linestyle=':', label='Horizon (0°)', linewidth=1)

    # Highlight the Zenith transit
    max_idx = np.argmax(altitudes)
    max_time = times[max_idx].datetime
    max_alt = altitudes[max_idx]
    plt.scatter(max_time, max_alt, color='red', s=100, zorder=5, label=f'Zenith Pass at {max_time.strftime("%H:%M")}')

    plt.xlabel('Time of Day (UTC)')
    plt.ylabel('Altitude (degrees)')
    plt.title(f'Rigel\'s Path Across the Sky – {year}-{month:02d}-{day:02d}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(-5, 95)
    plt.tight_layout()
    plt.show()

    print("\n" + "=" * 50)
    print(f"Rigel reached its highest point at {max_time.strftime('%H:%M:%S')} UTC.")
    print(f"Altitude at that moment: {max_alt:.2f} degrees.")
    print("The red dashed line is the Zenith (straight up).")
    print("The closer the blue line gets to it, the better the alignment.")
    print("\nNow you understand the geometry. No hardware needed.")

if __name__ == "__main__":
    main()