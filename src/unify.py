# src/unify.py

def unify_app_data(google_data_row, apple_data_dict):
    """
    Unifies data from Google Play and Apple App Store into a standard schema.
    """
    # Start with the clean Google Play data
    unified_data = {
        'app_name': google_data_row['App'],
        'google_play_rating': google_data_row.get('Rating'),
        'google_play_reviews': google_data_row.get('Reviews'),
        'google_play_installs': google_data_row.get('Installs'),
        'platform': 'Google Play'
    }

    # If we found matching data from the Apple App Store, add it
    if apple_data_dict:
        unified_data['apple_app_store_rating'] = apple_data_dict.get('score')
        # Note: The 'reviews' field might not be in the search result,
        # so we'll leave it out for now unless you fetch detailed app info.
        unified_data['platform'] = 'Both' # Update platform if it exists on both

    return unified_data