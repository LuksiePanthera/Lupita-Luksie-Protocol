#!/usr/bin/env python3
# rigel-zero.py
# Lupita-Luksie Protocol - Zenith Calibration Kit
# 
# What this does:
# Saves rookie astronomers 45 minutes of math.
# Calculates the exact time Rigel passes the Zenith (straight up)
# from your location, on any date you choose.

from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time
from astropy import units as u
import numpy as np

def main():
    print("=" * 50)
    print("  LUPITA-LUKSIE PROTOCOL")
    print("  Zenith Calibration Kit")
    print("  rigel-zero.py v1.0")
    print("=" * 50)
    
    # Default to Lupita's coordinates (you can change these!)
    default_lat = -7.5
    default_lon = 31.0  # Approximate. Replace with exact if you know it.
    
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
    
    # Rigel's fixed position (RA: 05h14m32.27s, Dec: -08°12'05.9")
    rigel = SkyCoord(ra=78.6345 * u.deg, dec=-8.2016 * u.deg, frame='icrs')
    
    # Observer's location
    observer = EarthLocation(lat=lat * u.deg, lon=lon * u.deg)
    
    # Generate timestamps for the entire day
    start = Time(f"{year}-{month:02d}-{day:02d} 00:00:00")
    end = Time(f"{year}-{month:02d}-{day:02d} 23:59:00")
    times = Time(np.arange(start.unix, end.unix, 60), format='unix')  # Check every minute
    
    # Calculate the altitude of Rigel for each minute
    altaz_frame = AltAz(location=observer, obstime=times)
    rigel_altaz = rigel.transform_to(altaz_frame)
    
    # Find the moment Rigel is highest (closest to Zenith)
    max_alt_index = np.argmax(rigel_altaz.alt)
    transit_time = times[max_alt_index]
    max_alt = rigel_altaz.alt[max_alt_index]
    zenith_distance = 90 - max_alt
    
    print("\n" + "=" * 50)
    print(f"RESULTS for {year}-{month:02d}-{day:02d}")
    print("=" * 50)
    print(f"Rigel is highest in the sky at: {transit_time.iso.split(' ')[1]} UTC")
    print(f"Altitude at that moment: {max_alt:.2f} degrees")
    print(f"Distance from Zenith: {zenith_distance:.2f} degrees")
    
    if zenith_distance < 1:
        print("\n>> PERFECT ALIGNMENT: Less than 1° from Zenith.")
        print(">> Point your telescope straight up at the time above.")
    else:
        print(f"\n>> Note: {zenith_distance:.2f}° from Zenith. Adjust your aim slightly.")
    
    print("\nProof of Work complete. Now go build something cool.")
    print("Lupita-Luksie Protocol - MIT License. No warranty. No support.")

if __name__ == "__main__":
    main()