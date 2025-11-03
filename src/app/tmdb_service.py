import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

class TMDBService:
    """Service to interact with The Movie Database (TMDB) API"""
    
    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.base_url = settings.TMDB_BASE_URL
        self.image_base_url = settings.TMDB_IMAGE_BASE_URL
    
    def _make_request(self, endpoint, params=None):
        """Make a request to TMDB API"""
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        
        try:
            response = requests.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error("Error fetching from TMDB: %s", e)
            return None
    
    def get_poster_url(self, poster_path, size='w500'):
        """Get full URL for poster image
        Sizes: w92, w154, w185, w342, w500, w780, original
        """
        if not poster_path:
            return None
        return f"{self.image_base_url}/{size}{poster_path}"
    
    def get_backdrop_url(self, backdrop_path, size='w1280'):
        """Get full URL for backdrop image
        Sizes: w300, w780, w1280, original
        """
        if not backdrop_path:
            return None
        return f"{self.image_base_url}/{size}{backdrop_path}"
    
    def get_trending(self, media_type='all', time_window='week', page=1):
        """Get trending movies/TV shows
        media_type: 'all', 'movie', 'tv'
        time_window: 'day', 'week'
        """
        endpoint = f"/trending/{media_type}/{time_window}"
        return self._make_request(endpoint, {'page': page})
    
    def get_popular_movies(self, page=1):
        """Get popular movies"""
        return self._make_request('/movie/popular', {'page': page})
    
    def get_popular_tv(self, page=1):
        """Get popular TV shows"""
        return self._make_request('/tv/popular', {'page': page})
    
    def get_movie_details(self, movie_id):
        """Get detailed information about a movie"""
        return self._make_request(f'/movie/{movie_id}')
    
    def get_tv_details(self, tv_id):
        """Get detailed information about a TV show"""
        return self._make_request(f'/tv/{tv_id}')
    
    def get_movie_recommendations(self, movie_id, page=1):
        """Get recommended movies for a given movie"""
        return self._make_request(f'/movie/{movie_id}/recommendations', {'page': page})

    def get_tv_recommendations(self, tv_id, page=1):
        """Get recommended TV shows for a given show"""
        return self._make_request(f'/tv/{tv_id}/recommendations', {'page': page})

    def get_movie_similar(self, movie_id, page=1):
        """Get similar movies for a given movie"""
        return self._make_request(f'/movie/{movie_id}/similar', {'page': page})

    def get_tv_similar(self, tv_id, page=1):
        """Get similar TV shows for a given show"""
        return self._make_request(f'/tv/{tv_id}/similar', {'page': page})
    
    def search_multi(self, query, page=1):
        """Search for movies, TV shows, and people"""
        return self._make_request('/search/multi', {'query': query, 'page': page})
    
    def search_movies(self, query, page=1):
        """Search for movies only"""
        return self._make_request('/search/movie', {'query': query, 'page': page})
    
    def search_tv(self, query, page=1):
        """Search for TV shows only"""
        return self._make_request('/search/tv', {'query': query, 'page': page})
    
    def get_movie_genres(self):
        """Get list of movie genres"""
        return self._make_request('/genre/movie/list')
    
    def get_tv_genres(self):
        """Get list of TV show genres"""
        return self._make_request('/genre/tv/list')
    
    def discover_movies(self, year=None, min_rating=None, genre_id=None, sort_by='popularity.desc', page=1):
        """Discover movies with filters
        sort_by options: 'popularity.desc', 'vote_average.desc', 'release_date.desc', etc.
        """
        params = {
            'page': page,
            'sort_by': sort_by
        }
        
        if year:
            params['primary_release_year'] = year
        if min_rating:
            params['vote_average.gte'] = min_rating
        if genre_id:
            params['with_genres'] = genre_id
        
        return self._make_request('/discover/movie', params)
    
    def discover_tv(self, year=None, min_rating=None, genre_id=None, sort_by='popularity.desc', page=1, keywords=None, without_genres=None):
        """Discover TV shows with filters"""
        params = {
            'page': page,
            'sort_by': sort_by
        }
        
        if year:
            params['first_air_date_year'] = year
        if min_rating:
            params['vote_average.gte'] = min_rating
        if genre_id:
            params['with_genres'] = genre_id
        if keywords:
            params['with_keywords'] = keywords
        if without_genres:
            params['without_genres'] = without_genres
        
        return self._make_request('/discover/tv', params)
    
