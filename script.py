# Uncomment the line below if on Linux
# #!usr/bin/env python3

# Requests library for API access
import requests

# Time library for polling API
import time

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
    seen_alerts = set()  # Track alerts that have already been displayed
    no_alerts_printed = False  # Flag to prevent repeated "No alerts" messages
    polling_interval = 5  # Poll every 5 seconds

    while True:
        # Fetch alerts from the NWS API
        alerts = fetch_nws_alerts()
        alert_types = extract_alert_types(alerts)

        # Process new alerts
        for alert_type in alert_types:
            if alert_type not in seen_alerts:
                # Print the alert message if it's new
                print(f"WX Alert: {alert_type}. Take precautions now!")
                seen_alerts.add(alert_type)
                no_alerts_printed = False  # Reset flag since there are new alerts

        # If no alerts and "No alerts" message hasn't been printed recently
        if not alert_types and not no_alerts_printed:
            print("No active weather alerts found.")
            no_alerts_printed = True  # Prevent repeated "No alerts" messages

        # Wait for the polling interval before the next API request
        time.sleep(polling_interval)

if __name__ == "__main__":
    main()
