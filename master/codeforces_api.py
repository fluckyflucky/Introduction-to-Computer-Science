import requests
import time
from datetime import datetime
import pytz

class CodeforcesAPI:
    def __init__(self):
        self.base_url = "https://codeforces.com/api/"
    
    def get_upcoming_contests(self):
        try:
            headers = {
                'Cache-Control': 'no-cache'
            }
            response = requests.get(f"{self.base_url}contest.list", headers=headers)
            if response.status_code == 200:
                contests = response.json()['result']
                upcoming = [c for c in contests if c['phase'] == "BEFORE"]
                return [self.format_contest_info(c) for c in upcoming]
            return []
        except Exception as e:
            print(f"获取比赛信息出错: {str(e)}")
            return []
    
    def get_ongoing_and_upcoming_contests(self):
        try:
            headers = {
                'Cache-Control': 'no-cache'
            }
            response = requests.get(f"{self.base_url}contest.list", headers=headers)
            if response.status_code == 200:
                contests = response.json()['result']
                ongoing_and_upcoming = [c for c in contests if c['phase'] in ["BEFORE", "CODING"]]
                ongoing_and_upcoming.sort(key=lambda c: c['startTimeSeconds'])
                top_six = ongoing_and_upcoming[:6]
                return [self.format_contest_info(c) for c in top_six]
            return []
        except Exception as e:
            print(f"获取比赛信息出错: {str(e)}")
            return []
    
    def get_recent_finished_contests(self):
        try:
            headers = {
                'Cache-Control': 'no-cache'
            }
            response = requests.get(f"{self.base_url}contest.list", headers=headers)
            if response.status_code == 200:
                contests = response.json()['result']
                finished = [c for c in contests if c['phase'] == "FINISHED"]
                # 按结束时间排序，选择最近三场
                finished.sort(key=lambda c: c['startTimeSeconds'], reverse=True)
                recent_finished = finished[:3]
                return [self.format_contest_info(c) for c in recent_finished]
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