from datetime import datetime
from src.api.cloud_music import CloudMusic
from src.utils.file_handler import FileHandler
from src.config import USER_CONFIG

def main():
    print("正在获取网易云音乐热歌榜...")
    try:
        # 创建CloudMusic实例
        cm = CloudMusic()
        
        # 登录流程
        phone = USER_CONFIG.get('phone')
        if not phone:
            phone = input("请输入网易云音乐手机号：")
            
        print("正在发送验证码...")
        if not cm.send_captcha(phone):
            print("发送验证码失败！请检查手机号是否正确。")
            return
            
        print(f"验证码已发送到手机号：{phone}")
        captcha = input("请输入收到的验证码：")
        
        print("正在登录...")
        login_success = cm.login(phone, captcha)
            
        if not login_success:
            print("登录失败！请检查验证码是否正确。")
            return
            
        print("登录成功！")
        
        # 获取热歌榜数据
        songs = cm.get_hot_songs(50)  # 限制50首
        
        # 保存数据到文件
        file_handler = FileHandler()
        filename = file_handler.save_songs(songs)
        
        print(f"成功获取到 {len(songs)} 首歌曲!")
        print(f"歌单数据已保存到文件: {filename}")
        
        # 创建歌单并导入歌曲
        playlist_name = f"热歌榜Top50_{datetime.now().strftime('%Y%m%d')}"
        playlist_id = cm.create_playlist(playlist_name, songs)
        
        if playlist_id:
            print(f"\n已成功创建歌单'{playlist_name}'并导入{len(songs)}首歌曲！")
            print(f"歌单链接：https://music.163.com/#/playlist?id={playlist_id}")
        
        # 打印前10首歌曲
        print("\n热歌榜Top 10:")
        for i, song in enumerate(songs[:10], 1):
            artists = ', '.join(song['artists'])
            print(f"{i}. {song['name']} - {artists}")
            
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()
