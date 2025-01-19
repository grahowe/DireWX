# #!/usr/bin/env python3
# Uncomment the line above if on Linux

# Requests library for API access
import requests

# Change this to reflect your UGC code
# You can find this on the National Weather Service's website or Google
zone = ""

# Function to fetch weather alerts from the NWS API
def fetch_nws_alerts():
    url = "https://api.weather.gov/alerts/active/zone/" + zone

    # Try-catch/except for API access
    # If it succeeds, the request will return the information
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        alerts = response.json()
        return alerts.get("features", [])
    
    # If it fails, an error message will be generated
    except requests.RequestException as e:
        print(f"Error fetching NWS alerts: {e}")
        return []

# Function to extract alert types from the NWS data
def extract_alert_types(alerts):
    # This function extracts the "event" type from each alert and avoids duplicates
    alert_types = []
    for alert in alerts:
        properties = alert.get("properties", {})
        event = properties.get("event")
        if event and event not in alert_types:
            alert_types.append(event)
    return alert_types

# Main function
def main():
    # Fetch alerts from the NWS API
    alerts = fetch_nws_alerts()
    alert_types = extract_alert_types(alerts)

    # Process and display alerts
    if alert_types:
        for alert_type in alert_types:
            print(f"WX Alert: {alert_type}. Take precautions now!")
    else:
        print("No active weather alerts found.")

if __name__ == "__main__":
    main()
