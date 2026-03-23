import requests
import pandas as pd
import time

def get_steam_reviews(app_id, max_reviews=10000):
    """
    获取指定 Steam 游戏的高热度评论
    """
    reviews = []
    cursor = '*'  # Steam API 分页指针
    target_reviews = max_reviews  # 实际目标条数，可能会根据总评测数下调
    
    print(f"开始抓取 AppID: {app_id} 的 Steam 评论...")
    
    while len(reviews) < target_reviews:
        # Steam 评测 API 接口
        url = f"https://store.steampowered.com/appreviews/{app_id}"
        
        # 请求参数
        params = {
            'json': 1,
            'filter': 'all',       # 按所有高价值评价排序 (可以换成 'recent' 看最新)
            'language': 'schinese', # 只抓取简体中文，方便做词云和分析
            'day_range': 365,
            'cursor': cursor,
            'review_type': 'all',  # 包含好评和差评
            'purchase_type': 'all',
            'num_per_page': 100    # 每次请求 100 条
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if data['success'] != 1 or not data['reviews']:
                print("抓取完毕或遇到错误。")
                break

            # 第一次请求时，可以根据 Steam 返回的总评测数，自动下调目标条数，避免死等
            if len(reviews) == 0:
                try:
                    total = int(data.get('query_summary', {}).get('total_reviews', 0))
                    if 0 < total < target_reviews:
                        print(f"当前游戏总共有 {total} 条评论，小于你请求的 {max_reviews} 条，将自动只抓取 {total} 条。")
                        target_reviews = total
                except Exception:
                    # 如果字段缺失或解析失败，就保持原来的 target_reviews 不变
                    pass
                
            for review in data['reviews']:
                reviews.append({
                    '玩家评价': review['review'],
                    '是否推荐': '推荐' if review['voted_up'] else '不推荐',
                    '游玩时长(小时)': round(review['author']['playtime_forever'] / 60, 1),
                    '觉得有价值的人数': review['votes_up'],
                    '觉得好笑的人数': review['votes_funny']
                })
                
            cursor = data['cursor'] # 更新指针到下一页
            print(f"已抓取 {len(reviews)} 条评论...")
            time.sleep(1) # 礼貌性延迟，防止被 Steam 封 IP
            
        except Exception as e:
            print(f"请求出错: {e}")
            break
            
    return reviews[:target_reviews]

if __name__ == "__main__":
    # 替换为《杀戮尖塔2》的真实 Steam App ID
    # 举例：杀戮尖塔1代的ID是 646570，你需要在Steam商店页面URL中找到2代的数字
    APP_ID = "2868840" 
    
    # 抓取前 500 条高热度评论
    reviews_data = get_steam_reviews(APP_ID, max_reviews=10000)
    
    if reviews_data:
        # 使用 pandas 将数据导出为 CSV 文件
        df = pd.DataFrame(reviews_data)
        # utf-8-sig 可以防止 Excel 打开中文乱码
        df.to_csv("slay_the_spire_2_reviews.csv", index=False, encoding='utf-8-sig') 
        print("抓取成功！数据已保存为 slay_the_spire_2_reviews.csv")
        print("你可以用 Excel 打开它，看看玩家们的平均游玩时长和痛点评价。")
