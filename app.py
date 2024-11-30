import asyncio, httpx, json, pandas as pd, numpy as np

from tabulate import tabulate
from token_manager import TokenManager

# Game modes dictionary
GAME_MODES = {
    '0': {
        'name': 'bounty',
        'display_name': 'Bounty',
        'maps': {
            '1': 'Canal Grande',
            '2': 'Dry Season',
            '3': 'Excel',
            '4': 'Hideout',
            '5': 'Layer Cake',
            '6': 'Shooting Star',
            '7': 'Snake Prairie'
        }
    },
    '1': {
        'name': 'brawlBall',
        'display_name': 'Brawl Ball',
        'maps': {
            '1': 'Back Pocket',
            '2': 'Backyard Bowl',
            '3': 'Beach Ball',
            '4': 'Center Stage',
            '5': 'Penalty Kick',
            '6': 'Pinball Dreams',
            '7': 'Razzle Dazzle',
            '8': 'Sneaky Fields',
            '9': 'Sunny Soccer',
            '10': 'Super Beach',
            '11': 'Triple Dribble',
            '12': 'Weak Foot'
        }
    },
    '2': {
        'name': 'gemGrab',
        'display_name': 'Gem Grab',
        'maps': {
            '1': 'Acute Angle',
            '2': 'Corkscrew',
            '3': 'Double Swoosh',
            '4': 'Gem Fort',
            '5': 'Hard Rock Mine',
            '6': 'Last Stop',
            '7': 'Minecart Madness',
            '8': 'Open Space',
            '9': 'Pineapple Plaza',
            '10': 'Rustic Arcade',
            '11': 'Sneaky Sneak',
            '12': 'Undermine'
        }
    },
    '3': {
        'name': 'duoShowdown',
        'display_name': 'Duo Showdown',
        'maps': {
            '1': 'Acid Lakes',
            '2': 'Cavern Churn',
            '3': 'Dark Passage',
            '4': 'Double Trouble',
            '5': 'Feast or Famine',
            '6': 'Flying Fantasies',
            '7': 'Island Invasion',
            '8': 'Rockwall Brawl',
            '9': 'Safety Center',
            '10': 'Skull Creek',
            '11': 'Stormy Plains',
            '12': 'Sunset Vista'
        }
    },
    '4': {
        'name': 'soloShowdown',
        'display_name': 'Solo Showdown',
        'maps': {
            '1': 'Acid Lakes',
            '2': 'Cavern Churn',
            '3': 'Dark Passage',
            '4': 'Double Trouble',
            '5': 'Feast or Famine',
            '6': 'Flying Fantasies',
            '7': 'Island Invasion',
            '8': 'Rockwall Brawl',
            '9': 'Safety Center',
            '10': 'Skull Creek',
            '11': 'Stormy Plains',
            '12': 'Sunset Vista'
        }
    },
    '5': {
        'name': 'hotZone',
        'display_name': 'Hot Zone',
        'maps': {
            '1': 'Dueling Beetles',
            '2': 'From Dusk till Dawn',
            '3': 'Open Business',
            '4': 'Parallel Plays',
            '5': 'Ring of Fire',
            '6': 'Rush'
        }
    },
    '6': {
        'name': 'knockout',
        'display_name': 'Knockout',
        'maps': {
            '1': "Belle's Rock",
            '2': 'Between the Rivers',
            '3': 'Flaring Phoenix',
            '4': 'Four Levels',
            '5': 'Goldarm Gulch',
            '6': 'Gratitude',
            '7': 'Hard Lane',
            '8': 'Island Hopping',
            '9': 'New Horizons',
            '10': 'Out in the Open',
            '11': 'Sunset Spar',
            '12': 'Twilight Passage'
        }
    },
    '7': {
        'name': 'heist',
        'display_name': 'Heist',
        'maps': {
            '1': 'Bridge Too Far',
            '2': 'Electric Storm',
            '3': 'Hot Potato',
            '4': 'Kaboom Canyon',
            '5': 'Safe Zone',
            '6': 'Secret or Mystery'
        }
    },
    '8': {
        'name': 'trioShowdown',
        'display_name': 'Trio Showdown',
        'maps': {
            '1': 'Dark Passage',
            '2': 'Feast or Famine',
            '3': "Ring-'o-Brawlin",
            '4': 'Starr Fish',
            '5': 'Thousand Jellies',
        }
    }
}


async def fetch_brawl_stats(mode, map_name, token, date_str):
    """Fetch brawler statistics asynchronously with improved HTTP client handling"""
    base_url = "https://cube.brawltime.ninja/cubejs-api/v1/load"
    headers = {
        'authorization': token,
        'accept': '*/*',
        'origin': 'https://brawltime.ninja',
        'referer': 'https://brawltime.ninja/'
    }

    async with httpx.AsyncClient(
            timeout=30,
            follow_redirects=True,
            limits=httpx.Limits(max_keepalive_connections=8, max_connections=8)
    ) as client:
        tasks = []
        trophy_ranges = ['6', '8', '10', '11', '12', '13', '14', '15']

        for trophy_range in trophy_ranges:
            query = {
                "measures": ["map.winRate_measure", "map.picks_measure"],
                "dimensions": ["map.brawler_dimension"],
                "filters": [
                    {"member": "map.season_dimension", "operator": "gte", "values": [date_str]},
                    {"member": "map.mode_dimension", "operator": "equals", "values": [mode]},
                    {"member": "map.map_dimension", "operator": "equals", "values": [map_name]},
                    {"member": "map.trophyRange_dimension", "operator": "equals", "values": [trophy_range]}
                ]
            }

            params = {
                'query': json.dumps(query),
                'queryType': 'multi'
            }

            tasks.append(client.get(base_url, params=params, headers=headers))

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        all_data = []
        for response in responses:
            if isinstance(response, Exception):
                print(f"Error in request: {str(response)}")
                continue
            try:
                if isinstance(response, httpx.Response):
                    if response.status_code == 200:
                        data = response.json()
                        if 'results' in data and data['results']:
                            all_data.extend(data['results'][0]['data'])
                    else:
                        print(f"Request failed with status code: {response.status_code}")
            except Exception as e:
                print(f"Error processing response: {str(e)}")

        if not all_data:
            print("Warning: No data retrieved for any trophy range")

        return all_data


def process_and_display_data(all_data, map_name, mode, brawlers_to_remove):
    """Process and display brawler statistics with optimized DataFrame operations"""
    if not all_data:
        print("No data available to process.")
        return

    # Create DataFrame with only needed columns
    df = pd.DataFrame(all_data, columns=['map.brawler_dimension', 'map.picks_measure', 'map.winRate_measure'])

    # Convert columns to float64 for precision and compatibility
    df['map.picks_measure'] = pd.to_numeric(df['map.picks_measure'], downcast='float').astype('float64')
    df['map.winRate_measure'] = pd.to_numeric(df['map.winRate_measure'], downcast='float').astype('float64')

    # Calculate total wins
    df['total_wins'] = df['map.picks_measure'] * df['map.winRate_measure']

    # Group and aggregate data
    grouped = df.groupby('map.brawler_dimension').agg({
        'map.picks_measure': 'sum',
        'total_wins': 'sum'
    }).reset_index()

    # Calculate total picks and metrics
    total_picks = grouped['map.picks_measure'].sum()
    grouped['Win Rate'] = grouped['total_wins'] / grouped['map.picks_measure']
    grouped['pick_rate'] = grouped['map.picks_measure'] / total_picks * 100
    grouped['Win Rate %'] = grouped['Win Rate'] * 100

    # Remove the least picked brawlers
    grouped = grouped.nlargest(len(grouped) - brawlers_to_remove, 'pick_rate')

    # Calculate score
    avg_win_rate = grouped['Win Rate %'].mean()
    grouped['Win Rate Difference'] = grouped['Win Rate %'] - avg_win_rate
    grouped['Score'] = np.where(
        grouped['Win Rate Difference'] > 0,
        2 * grouped['Win Rate Difference'],
        grouped['Win Rate Difference']
    ) * np.log1p(grouped['pick_rate'])

    # Prepare final results
    result = grouped[['map.brawler_dimension', 'Win Rate %', 'pick_rate', 'Score']].copy()
    result.columns = ['Brawler', 'Win Rate %', 'Pick Rate %', 'Score']

    # Convert to float64
    result['Win Rate %'] = result['Win Rate %'].astype('float64')
    result['Pick Rate %'] = result['Pick Rate %'].astype('float64')
    result['Score'] = result['Score'].astype('float64')

    # Round numerical columns to two decimal places
    result['Win Rate %'] = result['Win Rate %'].round(2)
    result['Pick Rate %'] = result['Pick Rate %'].round(2)
    result['Score'] = result['Score'].round(2)

    # Sort by 'Score' descending
    result = result.sort_values('Score', ascending=False)

    # **Add this line to filter rows where 'Score' >= 1**
    result = result[result['Score'] >= 5]

    # Format numerical columns as strings with two decimal places
    result['Win Rate %'] = result['Win Rate %'].map('{:.2f}'.format)
    result['Pick Rate %'] = result['Pick Rate %'].map('{:.2f}'.format)
    result['Score'] = result['Score'].map('{:.2f}'.format)

    # Display results
    print(f"\nBrawler Statistics for {mode} - {map_name}")
    print(f"Average Win Rate: {avg_win_rate:.2f}%")
    print("\nBrawler Rankings:")
    print(tabulate(result, headers='keys', tablefmt='pretty', showindex=False))


def get_user_input():
    """Get user input for game mode and map selection"""
    print("\nAvailable Game Modes:")
    for key, mode in GAME_MODES.items():
        print(f"{key}. {mode['display_name']}")

    while True:
        mode_choice = input("\nSelect game mode (enter number): ")
        if mode_choice in GAME_MODES:
            break
        print("Invalid selection. Please try again.")

    print(f"\nAvailable Maps for {GAME_MODES[mode_choice]['display_name']}:")
    for key, map_name in GAME_MODES[mode_choice]['maps'].items():
        print(f"{key}. {map_name}")

    while True:
        map_choice = input("\nSelect map (enter number): ")
        if map_choice in GAME_MODES[mode_choice]['maps']:
            break
        print("Invalid selection. Please try again.")

    while True:
        brawlers_to_remove = input("\nEnter number of least picked brawlers to remove (default is 45): ").strip()
        if brawlers_to_remove == "":
            brawlers_to_remove = 45
            break
        if brawlers_to_remove.isdigit():
            brawlers_to_remove = int(brawlers_to_remove)
            break
        print("Invalid number. Please enter a positive integer.")

    return {
        'mode': GAME_MODES[mode_choice]['name'],
        'map_name': GAME_MODES[mode_choice]['maps'][map_choice],
        'brawlers_to_remove': brawlers_to_remove
    }


async def main():
    """Main program entry point"""
    try:

        token_manager = TokenManager()
        token = token_manager.get_token()
        if not token:
            print("Cannot proceed without authentication token")
            return

        user_input = get_user_input()

        data = await fetch_brawl_stats(
            user_input['mode'],
            user_input['map_name'],
            token,
            date_str="2024-11-25"
        )

        if data:
            process_and_display_data(
                data,
                user_input['map_name'],
                user_input['mode'],
                user_input['brawlers_to_remove']
            )
        else:
            print("Failed to retrieve data. Please verify your authentication token and try again.")

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    while True:
        asyncio.run(main())
