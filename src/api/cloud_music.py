import requests
import json
from typing import List, Dict, Optional
from ..utils.crypto import aes_encrypt
from ..config import API_CONFIG, CRYPTO_CONFIG, HEADERS, USER_CONFIG

class CloudMusic:
    """网易云音乐API封装类"""
    
    def __init__(self):
        self.headers = HEADERS
        self.base_url = API_CONFIG['base_url']
        self.playlist_id = API_CONFIG['playlist_id']
        self.cookie = None
        self.csrf_token = None
        
    def send_captcha(self, phone: str = None) -> bool:
        """发送验证码
        Args:
            phone: 手机号，如未提供则使用配置文件中的账号
        Returns:
            是否发送成功
        """
        if not phone:
            phone = USER_CONFIG['phone']
        
        data = {
            'cellphone': phone,
            'ctcode': '86'  # 国家代码，中国为86
        }
        
        params = self._encrypt_params(json.dumps(data))
        request_data = {
            "params": params,
            "encSecKey": CRYPTO_CONFIG['enc_sec_key']
        }
        
        try:
            response = requests.post(
                API_CONFIG['send_captcha_url'],
                headers=self.headers,
                data=request_data
            )
            
            result = response.json()
            if result.get('code') == 200:
                return True
            print(f"发送验证码失败: {result.get('message', '未知错误')}")
            return False
        except Exception as e:
            print(f"发送验证码时发生错误: {str(e)}")
            return False

    def verify_captcha(self, phone: str, captcha: str) -> bool:
        """验证验证码
        Args:
            phone: 手机号
            captcha: 验证码
        Returns:
            是否验证成功
        """
        data = {
            'cellphone': phone,
            'captcha': captcha,
            'ctcode': '86'
        }
        
        params = self._encrypt_params(json.dumps(data))
        request_data = {
            "params": params,
            "encSecKey": CRYPTO_CONFIG['enc_sec_key']
        }
        
        try:
            response = requests.post(
                API_CONFIG['verify_captcha_url'],
                headers=self.headers,
                data=request_data
            )
            
            result = response.json()
            if result.get('code') == 200:
                return True
            print(f"验证码验证失败: {result.get('message', '未知错误')}")
            return False
        except Exception as e:
            print(f"验证验证码时发生错误: {str(e)}")
            return False

    def login(self, phone: str = None, captcha: str = None) -> bool:
        """使用验证码登录网易云音乐
        Args:
            phone: 手机号，如未提供则使用配置文件中的账号
            captcha: 验证码
        Returns:
            是否登录成功
        """
        if not phone:
            phone = USER_CONFIG['phone']
        if not captcha:
            print("验证码不能为空！")
            return False
        
        login_data = {
            'phone': phone,
            'captcha': captcha,
            'countrycode': '86',
            'rememberLogin': 'true'
        }
        
        params = self._encrypt_params(json.dumps(login_data))
        data = {
            "params": params,
            "encSecKey": CRYPTO_CONFIG['enc_sec_key']
        }
        
        try:
            response = requests.post(
                API_CONFIG['login_url'],
                headers=self.headers,
                data=data
            )
            
            result = response.json()
            if result.get('code') == 200:
                self.cookie = response.cookies
                self.csrf_token = response.cookies.get('__csrf')
                return True
            print(f"登录失败: {result.get('message', '未知错误')}")
            return False
        except Exception as e:
            print(f"登录时发生错误: {str(e)}")
            return False

    def _encrypt_params(self, text: str) -> str:
        """加密参数
        Args:
            text: 要加密的文本
        Returns:
            加密后的参数
        """
        # 两次AES加密
        h_encText = aes_encrypt(text, CRYPTO_CONFIG['first_key'], CRYPTO_CONFIG['iv'])
        h_encText = aes_encrypt(h_encText, CRYPTO_CONFIG['second_key'], CRYPTO_CONFIG['iv'])
        return h_encText

    def get_hot_songs(self, limit: int = 50) -> List[Dict]:
        """获取热歌榜歌曲列表
        Args:
            limit: 获取的歌曲数量，默认50首
        Returns:
            歌曲信息列表，每个歌曲包含name, id, artists, album信息
        """
        # 构造请求参数
        param_data = {
            "id": self.playlist_id,
            "offset": 0,
            "total": True,
            "limit": 1000,
            "n": 1000,
            "csrf_token": self.csrf_token or ""
        }
        
        params = self._encrypt_params(json.dumps(param_data))
        data = {
            "params": params,
            "encSecKey": CRYPTO_CONFIG['enc_sec_key']
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                cookies=self.cookie,
                data=data
            )
            
            result = response.json()
            if result.get('code') != 200:
                print(f"获取歌单失败: {result.get('message', '未知错误')}")
                return []
            
            # 提取歌曲信息，限制数量
            songs = []
            for track in result['playlist']['tracks'][:limit]:
                song = {
                    'name': track['name'],
                    'id': track['id'],
                    'artists': [artist['name'] for artist in track['ar']],
                    'album': track['al']['name']
                }
                songs.append(song)
            return songs
            
        except Exception as e:
            print(f"获取歌单时发生错误: {str(e)}")
            return []
            
    def create_playlist(self, name: str, songs: List[Dict]) -> Optional[str]:
        """创建歌单并导入歌曲
        Args:
            name: 歌单名称
            songs: 要导入的歌曲列表
        Returns:
            创建的歌单ID，如果失败则返回None
        """
        if not self.cookie or not self.csrf_token:
            print("请先登录！")
            return None
            
        # 第一步：创建歌单
        create_data = {
            'name': name,
            'privacy': 0,  # 0表示公开歌单，1表示私密歌单
            'csrf_token': self.csrf_token
        }
        
        params = self._encrypt_params(json.dumps(create_data))
        data = {
            "params": params,
            "encSecKey": CRYPTO_CONFIG['enc_sec_key']
        }
        
        try:
            response = requests.post(
                API_CONFIG['create_playlist_url'],
                headers=self.headers,
                cookies=self.cookie,
                data=data
            )
            
            result = response.json()
            if result.get('code') != 200:
                print(f"创建歌单失败: {result.get('message', '未知错误')}")
                return None
                
            playlist_id = str(result['id'])
            print(f"歌单'{name}'创建成功！")
            
            # 第二步：添加歌曲到歌单
            song_ids = [str(song['id']) for song in songs]
            add_data = {
                'op': 'add',
                'pid': playlist_id,
                'trackIds': json.dumps(song_ids),
                'csrf_token': self.csrf_token
            }
            
            params = self._encrypt_params(json.dumps(add_data))
            data = {
                "params": params,
                "encSecKey": CRYPTO_CONFIG['enc_sec_key']
            }
            
            response = requests.post(
                API_CONFIG['add_songs_url'],
                headers=self.headers,
                cookies=self.cookie,
                data=data
            )
            
            result = response.json()
            if result.get('code') == 200:
                print(f"已成功添加 {len(songs)} 首歌曲到歌单！")
                return playlist_id
            else:
                print(f"添加歌曲失败: {result.get('message', '未知错误')}")
                return playlist_id  # 返回歌单ID，即使添加歌曲失败
                
        except Exception as e:
            print(f"创建歌单或添加歌曲时发生错误: {str(e)}")
            return None
