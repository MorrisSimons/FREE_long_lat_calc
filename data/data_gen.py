import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
import math
import csv

class GNSSDataGenerator:
    def __init__(self, base_lat=37.7749, base_lon=-122.4194, duration_minutes=10, sample_rate_hz=1):
        """
        Initialize GNSS data generator
        
        Args:
            base_lat: Base latitude (default: San Francisco)
            base_lon: Base longitude (default: San Francisco) 
            duration_minutes: Duration of data collection in minutes
            sample_rate_hz: Sampling rate in Hz (samples per second)
        """
        self.base_lat = base_lat
        self.base_lon = base_lon
        self.duration_minutes = duration_minutes
        self.sample_rate_hz = sample_rate_hz
        self.total_samples = int(duration_minutes * 60 * sample_rate_hz)
    
    def simulate_movement_pattern(self, time_index):
        """Simulate 1km straight line movement"""
        # Calculate total distance to cover (1000 meters)
        total_distance_m = 1000.0
        
        # Calculate distance per sample
        distance_per_sample = total_distance_m / self.total_samples
        
        # Fixed direction (heading north-east at 45 degrees)
        direction = math.pi / 4  # 45 degrees (north-east)
        
        # Convert distance to lat/lon movement
        lat_drift = (distance_per_sample * math.cos(direction)) / 111320.0
        lon_drift = (distance_per_sample * math.sin(direction)) / (111320.0 * math.cos(math.radians(self.base_lat)))
        
        # Add small random noise to make it more realistic (±1 meter)
        noise_factor = 1.0  # meters
        lat_noise = random.gauss(0, noise_factor / 111320.0)
        lon_noise = random.gauss(0, noise_factor / (111320.0 * math.cos(math.radians(self.base_lat))))
        
        return lat_drift + lat_noise, lon_drift + lon_noise
    
    def generate_gnss_data(self):
        """Generate the complete GNSS dataset"""
        print(f"Generating GNSS data for {self.duration_minutes} minutes...")
        print(f"Base position: {self.base_lat:.6f}, {self.base_lon:.6f}")
        print(f"Sample rate: {self.sample_rate_hz} Hz")
        print(f"Total samples: {self.total_samples}")
        
        # Initialize data storage
        timestamps = []
        latitudes = []
        longitudes = []
        
        # Starting position
        current_lat = self.base_lat
        current_lon = self.base_lon
        start_time = datetime.now()
        
        for i in range(self.total_samples):
            # Calculate timestamp
            timestamp = start_time + timedelta(seconds=i / self.sample_rate_hz)
            
            # Add movement
            lat_movement, lon_movement = self.simulate_movement_pattern(i)
            current_lat += lat_movement
            current_lon += lon_movement
            
            # Store data
            timestamps.append(timestamp)
            latitudes.append(current_lat)
            longitudes.append(current_lon)
            
            # Progress indicator
            if i % (self.total_samples // 10) == 0:
                progress = (i / self.total_samples) * 100
                print(f"Progress: {progress:.1f}%")
        
        # Create DataFrame
        data = pd.DataFrame({
            'timestamp': timestamps,
            'latitude': latitudes,
            'longitude': longitudes
        })
        
        return data
    
    def save_data(self, data, filename='gnss_data.csv'):
        """Save data to CSV file"""
        filepath = f"/home/morrisubuntu/Desktop/long_lat_calc/{filename}"
        data.to_csv(filepath, index=False)
        print(f"\nData saved to: {filepath}")
        print(f"Total records: {len(data)}")
        
        # Print statistics
        print("\nData Statistics:")
        print(f"Latitude range: {data['latitude'].min():.6f} to {data['latitude'].max():.6f}")
        print(f"Longitude range: {data['longitude'].min():.6f} to {data['longitude'].max():.6f}")
        
        return filepath

def main():
    """Main function to run the GNSS data generator"""
    print("GNSS Data Generator")
    print("==================")
    
    # Configuration
    base_latitude = 37.7749  # San Francisco
    base_longitude = -122.4194
    duration_minutes = 5
    sample_rate = 1  # 1 Hz (1 sample per second)
    
    # Allow user to customize parameters
    print(f"\nDefault configuration:")
    print(f"Base location: {base_latitude}, {base_longitude} (San Francisco)")
    print(f"Duration: {duration_minutes} minutes")
    print(f"Sample rate: {sample_rate} Hz")
    
    # Create generator
    generator = GNSSDataGenerator(
        base_lat=base_latitude,
        base_lon=base_longitude,
        duration_minutes=duration_minutes,
        sample_rate_hz=sample_rate
    )
    
    # Generate data
    gnss_data = generator.generate_gnss_data()
    
    # Save data
    output_file = generator.save_data(gnss_data, 'gnss_dataset.csv')
    
    print(f"\nGNSS dataset generation complete!")
    print(f"File location: {output_file}")

if __name__ == "__main__":
    main()
