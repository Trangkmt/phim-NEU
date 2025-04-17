from models import sample_movies, search_movies as model_search_movies

def get_api_movies(endpoint=None, params=None):
    """
    Function to fetch movies from an external API
    In the future, replace with actual API call
    """
    # This is where you would implement actual API calls
    # For now, return sample data
    return sample_movies  # For now, return sample movies

def search_movies(query):
    """
    Search for movies using the API
    Currently uses local search function
    """
    return model_search_movies(query)
