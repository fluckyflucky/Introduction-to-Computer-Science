import requests
import time
from datetime import datetime
import pytz

class CodeforcesAPI:
    def __init__(self):
        self.base_url = "https://codeforces.com/api/"
    
    def get_upcoming_contests(self):
        try:
            response = requests.get(f"{self.base_url}contest.list")
            if response.status_code == 200:
                contests = response.json()['result']
                upcoming = [c for c in contests if c['phase'] == "BEFORE"]
                return [self.format_contest_info(c) for c in upcoming]
            return []
        except Exception as e:
            print(f"获取比赛信息出错: {str(e)}")
            return []
    
    def format_contest_info(self, contest):
        # 转换为北京时间
        beijing_tz = pytz.timezone('Asia/Shanghai')
        start_time = datetime.fromtimestamp(contest['startTimeSeconds'], beijing_tz)
        
        return {
            "id": contest['id'],
            "name": contest['name'],
            "start_time": start_time.strftime('%Y-%m-%d %H:%M:%S'),
            "duration": f"{contest['durationSeconds'] // 3600}小时",
            "type": contest['type']
        } 