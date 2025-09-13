# API配置
API_CONFIG = {
    "base_url": "https://music.163.com/weapi/v3/playlist/detail",
    "playlist_id": "3778678",  # 热歌榜ID
    "send_captcha_url": "https://music.163.com/weapi/sms/captcha/sent",  # 发送验证码
    "verify_captcha_url": "https://music.163.com/weapi/sms/captcha/verify",  # 验证验证码
    "login_url": "https://music.163.com/weapi/login/cellphone",  # 手机号登录
    "create_playlist_url": "https://music.163.com/weapi/playlist/create",  # 创建歌单
    "add_songs_url": "https://music.163.com/weapi/playlist/manipulate/tracks",  # 添加歌曲到歌单
}

# 用户配置（需要替换为自己的账号信息）
USER_CONFIG = {
    "phone": "",  # 手机号
    "password": ""  # 密码的MD5值
}

# 加密配置
CRYPTO_CONFIG = {
    "iv": "0102030405060708",
    "first_key": "0CoJUm6Qyw8W8jud",
    "second_key": "FFFFFFFFFFFFFFFF",
    "enc_sec_key": "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
}

# 请求头配置
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}
