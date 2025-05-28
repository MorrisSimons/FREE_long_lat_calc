import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
import math
import csv

class GNSSDataGenerator:
    def __init__(self, base_lat=37.7749, base_lon=-122.4194, duration_minutes=20, sample_rate_hz=1):
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
        
        # GNSS accuracy parameters (meters)
        self.base_accuracy = 3.0  # Base GPS accuracy in open sky
        self.max_accuracy_degradation = 15.0  # Maximum accuracy degradation
        
    def simulate_satellite_visibility(self, time_index):
        """Simulate satellite visibility effects on accuracy"""
        # Simulate periodic satellite visibility changes
        cycle1 = math.sin(time_index * 0.01) * 2.0  # Slow cycle
        cycle2 = math.sin(time_index * 0.05) * 1.0  # Medium cycle
        cycle3 = math.sin(time_index * 0.1) * 0.5   # Fast cycle
        
        visibility_factor = 1.0 + (cycle1 + cycle2 + cycle3) / 3.0
        return max(0.3, min(2.0, visibility_factor))  # Clamp between 0.3 and 2.0
    
    def simulate_multipath_effects(self, time_index):
        """Simulate multipath interference effects"""
        # Random multipath events
        if random.random() < 0.05:  # 5% chance of multipath event
            return random.uniform(2.0, 8.0)
        
        # Background multipath noise
        return 1.0 + random.uniform(-0.2, 0.3)
    
    def simulate_atmospheric_effects(self, time_index):
        """Simulate atmospheric interference (ionospheric/tropospheric delays)"""
        # Slow atmospheric changes
        base_effect = math.sin(time_index * 0.001) * 0.5 + 1.0
        # Add random variations
        random_effect = random.gauss(0, 0.1)
        return max(0.5, base_effect + random_effect)
    
    def calculate_position_error(self, accuracy_meters):
        """Convert accuracy to lat/lon error in degrees"""
        # Approximate conversion: 1 degree ≈ 111,320 meters at equator
        lat_error = (random.gauss(0, accuracy_meters) / 111320.0)
        lon_error = (random.gauss(0, accuracy_meters) / (111320.0 * math.cos(math.radians(self.base_lat))))
        return lat_error, lon_error
    
    def simulate_movement_pattern(self, time_index):
        """Simulate 1km straight line movement"""
        # Calculate total distance to cover (1000 meters)
        total_distance_m = 1000.0
        
        # Calculate distance per sample
        distance_per_sample = total_distance_m / self.total_samples
        
        # Fixed direction (heading north-east at 45 degrees)
        # You can change this direction: 0=North, π/2=East, π=South, 3π/2=West
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
        accuracies = []
        satellite_counts = []
        hdops = []  # Horizontal Dilution of Precision
        
        # Starting position
        current_lat = self.base_lat
        current_lon = self.base_lon
        start_time = datetime.now()
        
        for i in range(self.total_samples):
            # Calculate timestamp
            timestamp = start_time + timedelta(seconds=i / self.sample_rate_hz)
            
            # Simulate various GNSS effects
            sat_visibility = self.simulate_satellite_visibility(i)
            multipath = self.simulate_multipath_effects(i)
            atmospheric = self.simulate_atmospheric_effects(i)
            
            # Calculate current accuracy
            accuracy = self.base_accuracy * sat_visibility * multipath * atmospheric
            accuracy = min(accuracy, self.max_accuracy_degradation)
            
            # Simulate satellite count (4-12 satellites typical)
            base_sat_count = 8
            sat_count = max(4, min(12, int(base_sat_count * sat_visibility + random.gauss(0, 1))))
            
            # Calculate HDOP based on satellite count and geometry
            hdop = max(0.8, 3.0 / math.sqrt(sat_count) + random.uniform(-0.2, 0.3))
            
            # Add movement
            lat_movement, lon_movement = self.simulate_movement_pattern(i)
            current_lat += lat_movement
            current_lon += lon_movement
            
            # Add position error based on accuracy
            lat_error, lon_error = self.calculate_position_error(accuracy)
            
            # Final position with error
            final_lat = current_lat + lat_error
            final_lon = current_lon + lon_error
            
            # Store data
            timestamps.append(timestamp)
            latitudes.append(final_lat)
            longitudes.append(final_lon)
            accuracies.append(accuracy)
            satellite_counts.append(sat_count)
            hdops.append(hdop)
            
            # Progress indicator
            if i % (self.total_samples // 10) == 0:
                progress = (i / self.total_samples) * 100
                print(f"Progress: {progress:.1f}%")
        
        # Create DataFrame
        data = pd.DataFrame({
            'timestamp': timestamps,
            'latitude': latitudes,
            'longitude': longitudes,
            'accuracy_meters': accuracies,
            'satellite_count': satellite_counts,
            'hdop': hdops
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
        print(f"Accuracy range: {data['accuracy_meters'].min():.2f}m to {data['accuracy_meters'].max():.2f}m")
        print(f"Average accuracy: {data['accuracy_meters'].mean():.2f}m")
        print(f"Satellite count range: {data['satellite_count'].min()} to {data['satellite_count'].max()}")
        print(f"HDOP range: {data['hdop'].min():.2f} to {data['hdop'].max():.2f}")
        
        return filepath

def main():
    """Main function to run the GNSS data generator"""
    print("GNSS Data Generator")
    print("==================")
    
    # Configuration
    base_latitude = 37.7749  # San Francisco
    base_longitude = -122.4194
    duration_minutes = 20
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