import json
import os
import math
import urllib.request
import urllib.parse
from datetime import datetime
import socket

# Constants
EARTH_RADIUS = 6371000  # in meters
CELL_SIZE = 100  # cell size in meters

def encode_geohash(latitude, longitude, cell_size):
    """
    Simple geohash function to divide the Earth's surface into a grid of cell_size x cell_size meters.
    """
    lat_cell = int((latitude + 90) * (EARTH_RADIUS * 2 * math.pi / 360) / cell_size)
    lon_cell = int((longitude + 180) * (EARTH_RADIUS * 2 * math.pi / 360 * math.cos(math.radians(latitude))) / cell_size)
    return lat_cell, f"{lat_cell}_{lon_cell}"

def lambda_handler(event, context):
    # Extracting body from the event
    body = json.loads(event['body'])
    
    if 'action' in body and body['action'] == 'request_for_quote':
        dispatch_endpoint = body['dispatch_endpoint']
        payload = {
            'action': 'quote',
            'uuid': body['uuid'],
            'token': body['token'],
            'contract_value': body['contract_value'],
            'ride_matching_service_endpoints': os.environ['RIDE_MATCHING_SERVICE_ENDPOINTS']
        }
        
        # Encode the payload for the request
        data = urllib.parse.urlencode(payload).encode()
        
        # Create the request object
        req = urllib.request.Request(dispatch_endpoint, data=data, method='POST')
        
        try:
            with urllib.request.urlopen(req, timeout=2) as response:
                pass
        except socket.timeout:
            pass # Ignore timeout exceptions
        except Exception as e:
            pass # Ignore any other exceptions
        
        # Return response with 200 status code and empty body
        return {
            'statusCode': 200,
            'body': json.dumps({})
        }