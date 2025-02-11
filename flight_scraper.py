import json
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import psycopg2

url = 'https://www.google.com/travel/flights/search?tfs=CBwQAhoqEgoyMDI1LTA2LTExKAFqDAgCEggvbS8wM2wybnIMCAMSCC9tLzBwMmdxGioSCjIwMjUtMDYtMTcoAWoMCAMSCC9tLzBwMmdxcgwIAhIIL20vMDNsMm5AAUgBcAGCAQsI____________AZgBAQ&hl=en&gl=us&curr=USD'

flightSelectors = {
    'departingAirport' : "div.G2WY5c.sSHqwe.ogfYpf.tPgKwe",
    'duration' : "div.hF6lYb.sSHqwe.ogfYpf.tPgKwe span.qeoz6e.HKHSfd + span",
    'airline' : "div.hF6lYb.sSHqwe.ogfYpf.tPgKwe span.h1fkLb",
    'price' : "div.BVAVmf.tPgKwe",
    'stops' : "span.VG3hNb",
    'arrivalAirport' : 'div.c8rWCd.sSHqwe.ogfYpf.tPgKwe',
    'arrivalTime': 'div[aria-label^="Arrival time"]',
    'departingTime' : 'div[aria-label^="Departure time"]'
}


# Scrape URL and store flight details as list of dictionaries: 

with sync_playwright() as p:
    browser = p.chromium.launch(headless= True)
    page = browser.new_page()
    # stealth_sync(page) -- results actually worstened 

    page.goto(url)
    page.wait_for_selector("li.pIav2d")  # Wait for flight results 
    page.wait_for_timeout(10000)  # Wait for additional seconds to ensure all prices load
    print("Done waiting")

    flights = page.locator("li.pIav2d").all()
    print("Located selector")

    flight_count = 0
    flights_dict = {}
    for flight in flights:
        flight_count += 1 
        flightDetails = {}
        for key, selector in flightSelectors.items():
            flightDetails[key] = flight.locator(selector).text_content() 
        flights_dict[f"flight{flight_count}"] = flightDetails 
    print(flights_dict)
    browser.close()






