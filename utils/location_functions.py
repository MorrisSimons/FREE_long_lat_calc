import math
from geopy.distance import geodesic
from datetime import datetime

def predict_future_dist_with_dir_and_speed(current_long, current_lat, target_long, target_lat, direction, speed, time) -> tuple:
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



def _bearing(p1, p2):
    """Initial bearing (deg from true north) p1→p2."""
    lat1, lon1, lat2, lon2 = map(math.radians, (*p1, *p2))
    dlon = lon2 - lon1
    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dlon)
    brng = math.degrees(math.atan2(x, y))
    return (brng + 360) % 360

def predict_future_dist_with_history(history, target_long, target_lat, time) -> tuple:
    """
    Predicts your position after a set time, given current 
    and target coordinates, movement direction, and speed.

    Args:
        history (list) with timestamps, direction and coordinates:
        target_long (float): Target longitude.
        target_lat (float): Target latitude.
        time (float): Time interval in seconds.

    Returns:
        tuple: (Predicted_longitude, Predicted_latitude, distance_traveled, percent_complete)
            - Predicted_longitude (float): Predicted longitude after 'time' seconds.
            - Predicted_latitude (float): Predicted latitude after 'time' seconds.
            - distance_traveled (float): Distance moved in meters.
            - percent_complete (float): Trip completion percentage (0–100).
    """

    lat1 = history[0][1]
    lon1 = history[0][2]
    lat2 = history[-1][1]
    lon2 = history[-1][2]
    current_lat = history[-1][1]
    current_long = history[-1][2]

    # direction based on first and last history entries
    direction = _bearing((lat1, lon1), (lat2, lon2))
    
    # start time and end time based on first and last history entries
    historytime = (datetime.fromisoformat(history[-1][0]) - datetime.fromisoformat(history[0][0])).total_seconds()  

    # speed based on first and last history entries
    speed = geodesic((lat1, lon1), (lat2, lon2)).meters / historytime

    distance_traveled = speed * time  # in meters

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


if __name__ == "__main__":
    print("location funtions module loaded successfully.")