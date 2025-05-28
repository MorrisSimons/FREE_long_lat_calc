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

