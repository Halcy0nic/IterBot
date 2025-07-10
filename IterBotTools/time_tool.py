import datetime
import time
import pytz

class TimeTool:
    """Tool for working with time and date information."""
    
    @staticmethod
    def get_current_time():
        """Returns current time in HH:MM:SS format"""
        return datetime.datetime.now().strftime("%H:%M:%S")
    
    @staticmethod
    def get_current_date():
        """Returns current date in YYYY-MM-DD format"""
        return datetime.datetime.now().strftime("%Y-%m-%d")
    
    @staticmethod
    def get_current_datetime(format="%Y-%m-%d %H:%M:%S"):
        """Returns formatted datetime string
        Args: 
            format (str): strftime format string
        """
        return datetime.datetime.now().strftime(format)
    
    @staticmethod
    def get_epoch_time():
        """Returns Unix epoch timestamp"""
        return int(time.time())
    
    @staticmethod
    def get_timezone_aware_time(tz_str="UTC"):
        """Returns timezone-aware datetime (requires pytz)
        Args:
            tz_str (str): Timezone identifier (e.g., 'America/New_York')
        """
        try:
            tz = pytz.timezone(tz_str)
            return datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z%z")
        except ImportError:
            return "pytz required for timezone-aware operations"
