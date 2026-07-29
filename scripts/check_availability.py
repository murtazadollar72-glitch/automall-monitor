#!/usr/bin/env python3
"""
Honda Pilot & Nissan Pathfinder Availability Checker for Alfuttaim Automall
Checks if Honda Pilot or Nissan Pathfinder is available and outputs results for GitHub Actions
"""

import requests
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime

def check_availability():
    """Check Honda Pilot and Nissan Pathfinder availability on Alfuttaim Automall"""
    
    # Get URL from environment variable or use default
    base_url = os.getenv('ALFUTTAIM_URL', 'https://www.alfuttaim.com/automall')
    
    results = {
        'honda_pilot': {'available': False, 'count': 0},
        'nissan_pathfinder': {'available': False, 'count': 0}
    }
    
    vehicles_to_check = [
        {'name': 'Honda Pilot', 'key': 'honda_pilot', 'search': 'Honda%20Pilot'},
        {'name': 'Nissan Pathfinder', 'key': 'nissan_pathfinder', 'search': 'Nissan%20Pathfinder'}
    ]
    
    try:
        for vehicle in vehicles_to_check:
            vehicle_name = vehicle['name']
            vehicle_key = vehicle['key']
            search_query = vehicle['search']
            
            search_url = f"{base_url}/vehicles?search={search_query}"
            
            print(f"\n{'='*50}")
            print(f"Checking {vehicle_name}...")
            print(f"URL: {search_url}")
            print(f"{'='*50}")
            
            # Make request with proper headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': base_url
            }
            
            response = requests.get(search_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try multiple selectors to find vehicles (adjust based on actual website structure)
            selectors = [
                '.vehicle-item',
                '[data-vehicle]',
                '.car-listing',
                '.vehicle-card',
                '.listing-item',
                '.car-card'
            ]
            
            vehicles = []
            for selector in selectors:
                vehicles = soup.select(selector)
                if vehicles:
                    print(f"Found vehicles using selector: {selector}")
                    break
            
            # Alternative: Look for specific vehicle text
            if not vehicles:
                all_text = soup.get_text().lower()
                search_terms = vehicle_name.lower().split()
                if all(term in all_text for term in search_terms):
                    print(f"Found {vehicle_name} text in page")
                    vehicles = [True]  # Mark as found
            
            available = len(vehicles) > 0
            count = len(vehicles)
            
            results[vehicle_key] = {
                'available': available,
                'count': count,
                'url': search_url
            }
            
            if available:
                print(f"✅ {vehicle_name} AVAILABLE! Found {count} vehicle(s)")
            else:
                print(f"❌ {vehicle_name} not available at this moment")
        
        timestamp = datetime.now().isoformat()
        
        print(f"\n{'='*60}")
        print(f"FINAL AVAILABILITY CHECK RESULTS")
        print(f"{'='*60}")
        print(f"Honda Pilot - Available: {results['honda_pilot']['available']} | Count: {results['honda_pilot']['count']}")
        print(f"Nissan Pathfinder - Available: {results['nissan_pathfinder']['available']} | Count: {results['nissan_pathfinder']['count']}")
        print(f"Timestamp: {timestamp}")
        print(f"{'='*60}\n")
        
        # Determine overall availability
        any_available = results['honda_pilot']['available'] or results['nissan_pathfinder']['available']
        total_count = results['honda_pilot']['count'] + results['nissan_pathfinder']['count']
        
        # Output for GitHub Actions
        print(f"::set-output name=available::{str(any_available).lower()}")
        print(f"::set-output name=count::{total_count}")
        print(f"::set-output name=timestamp::{timestamp}")
        print(f"::set-output name=honda_pilot_available::{str(results['honda_pilot']['available']).lower()}")
        print(f"::set-output name=honda_pilot_count::{results['honda_pilot']['count']}")
        print(f"::set-output name=pathfinder_available::{str(results['nissan_pathfinder']['available']).lower()}")
        print(f"::set-output name=pathfinder_count::{results['nissan_pathfinder']['count']}")
        
        # Save to log file
        log_entry = {
            "timestamp": timestamp,
            "honda_pilot": results['honda_pilot'],
            "nissan_pathfinder": results['nissan_pathfinder'],
            "any_available": any_available,
            "total_count": total_count
        }
        
        log_file = "availability_log.json"
        logs = []
        
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            except:
                logs = []
        
        logs.append(log_entry)
        
        # Keep only last 100 entries
        logs = logs[-100:]
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        print(f"Logged to {log_file}")
        
        if any_available:
            print(f"\n🎉 VEHICLES AVAILABLE!")
            if results['honda_pilot']['available']:
                print(f"   • Honda Pilot: {results['honda_pilot']['count']} vehicle(s)")
            if results['nissan_pathfinder']['available']:
                print(f"   • Nissan Pathfinder: {results['nissan_pathfinder']['count']} vehicle(s)")
            return 0
        else:
            print(f"\n⏳ No vehicles available at this moment")
            return 0
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {str(e)}")
        print(f"::set-output name=available::false")
        print(f"::set-output name=count::0")
        print(f"::set-output name=timestamp::{datetime.now().isoformat()}")
        print(f"::set-output name=honda_pilot_available::false")
        print(f"::set-output name=honda_pilot_count::0")
        print(f"::set-output name=pathfinder_available::false")
        print(f"::set-output name=pathfinder_count::0")
        return 1
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print(f"::set-output name=available::false")
        print(f"::set-output name=count::0")
        print(f"::set-output name=timestamp::{datetime.now().isoformat()}")
        print(f"::set-output name=honda_pilot_available::false")
        print(f"::set-output name=honda_pilot_count::0")
        print(f"::set-output name=pathfinder_available::false")
        print(f"::set-output name=pathfinder_count::0")
        return 1

if __name__ == "__main__":
    exit(check_availability())
