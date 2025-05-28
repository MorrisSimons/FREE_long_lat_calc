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
        tuple: (Predicted_longitude, Predicted_latitude, distance_traveled, percent_complete)
            - Predicted_longitude (float): Predicted longitude after 'time' seconds.
            - Predicted_latitude (float): Predicted latitude after 'time' seconds.
            - distance_traveled (float): Distance moved in meters.
            - percent_complete (float): Trip completion percentage (0–100).
    """
   
    distance_traveled = ((speed * 1000)/3600) * time
    
    # Calculate change in coordinates # https://www.sciencing.com/convert-distances-degrees-meters-7858322/
    lat_change = (distance_traveled * math.cos(math.radians(direction))) / 111111.0
    lon_change = (distance_traveled * math.sin(math.radians(direction))) / (111111.0 * math.cos(math.radians(current_lat)))
    
    # Calculate predicted position
    Predicted_latitude = current_lat + lat_change
    Predicted_longitude = current_long + lon_change
    
    # Calculate total distance from current to target using geodesic
    total_distance = geodesic((current_lat, current_long), (target_lat, target_long)).meters
    remaining_distance = geodesic((Predicted_latitude, Predicted_longitude), (target_lat, target_long)).meters
    
    # Calculate percentage complete
    if total_distance > 0:
        percent_complete = ((total_distance - remaining_distance) / total_distance) * 100
        # Ensure percentage doesn't exceed 100% or go below 0%
        percent_complete = max(0, min(100, percent_complete))
    else:
        percent_complete = 100.0  # Already at target
    
    return (Predicted_longitude, Predicted_latitude, distance_traveled, percent_complete)


