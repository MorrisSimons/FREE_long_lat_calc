import math
from geopy.distance import geodesic

def predict_future_distance(current_long, current_lat, target_long, target_lat, direction, speed, time) -> tuple:
    """
    Predicts your position after a set time, given current 
    and target coordinates, movement direction, and speed.

    Args:
        current_long (float): Current longitude.
        current_lat (float): Current latitude.
        target_long (float): Target longitude.
        target_lat (float): Target latitude.
        direction (float): Movement direction in degrees (0 = north, 90 = east).
        speed (float): Speed in km/second.
        time (float): Time interval in seconds.

    Returns:
        tuple: (future_longitude, future_latitude, distance_traveled, percent_complete)
            - future_longitude (float): Predicted longitude after 'time' seconds.
            - future_latitude (float): Predicted latitude after 'time' seconds.
            - distance_traveled (float): Distance moved in meters.
            - percent_complete (float): Trip completion percentage (0–100).
    """
    # Convert speed from km/s to m/s (assuming input is in km/s)
    speed_ms = speed * 1000  # Convert km/s to m/s
    
    # Calculate distance traveled in the given time
    distance_traveled = speed_ms * time
    
    # Convert direction to radians
    direction_rad = math.radians(direction)
    
    # Calculate change in coordinates
    # Using approximate conversion: 1 degree lat ≈ 111,111 meters
    # 1 degree lon ≈ 111,111 * cos(lat) meters
    lat_change = (distance_traveled * math.cos(direction_rad)) / 111111.0
    lon_change = (distance_traveled * math.sin(direction_rad)) / (111111.0 * math.cos(math.radians(current_lat)))
    
    # Calculate future position
    future_latitude = current_lat + lat_change
    future_longitude = current_long + lon_change
    
    # Calculate total distance from current to target using geodesic
    total_distance = geodesic((current_lat, current_long), (target_lat, target_long)).meters
    
    # Calculate distance from future position to target
    remaining_distance = geodesic((future_latitude, future_longitude), (target_lat, target_long)).meters
    
    # Calculate percentage complete
    if total_distance > 0:
        percent_complete = ((total_distance - remaining_distance) / total_distance) * 100
        # Ensure percentage doesn't exceed 100% or go below 0%
        percent_complete = max(0, min(100, percent_complete))
    else:
        percent_complete = 100.0  # Already at target
    
    return (future_longitude, future_latitude, distance_traveled, percent_complete)

# Example usage (only runs when file is executed directly)
if __name__ == "__main__":
    import pandas as pd

    # Read GNSS data from file
    df = pd.read_csv('gnss_data.csv')
    # Get the most recent position from the data
    current_long = df['longitude'].iloc[0]
    current_lat = df['latitude'].iloc[0]

    target_lat = df['latitude'].iloc[-1]
    target_long = df['longitude'].iloc[-1]
    direction = 43.99 
    speed = 0.01  # 0.01 km/s (10 m/s)
    time_interval = 60  # 60 seconds
    
    result = predict_future_distance(
        current_long, current_lat, target_long, target_lat, 
        direction, speed, time_interval
    )
    
    future_lon, future_lat, dist_traveled, percent_done = result
    
    print("Prediction Results:")
    print(f"Future Position: ({future_lat:.6f}, {future_lon:.6f})")
    print(f"Distance Traveled: {dist_traveled:.2f} meters")
    print(f"Trip Completion: {percent_done:.2f}%")
