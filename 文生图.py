import requests
import time

API_KEY = "sk-4c4d1ff35ad94626bb758fc8f1cf12cb"
import requests
import time


# 要生成的图像描述
prompt = "生成一个卡通公司logo的格式：一只白色的仓鼠，手里包着瓜子，龇着大牙"

# 创建任务（异步请求）
create_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "X-DashScope-Async": "enable"
}

payload = {
    "model": "wanx2.1-t2i-turbo",
    "input": {
        "prompt": prompt
    },
    "parameters": {
        "size": "1024*1024",
        "n": 1
    }
}

response = requests.post(create_url, headers=headers, json=payload)
response_data = response.json()

if "output" not in response_data:
    print("创建任务失败：", response_data)
    exit()

task_id = response_data["output"]["task_id"]
print(f"[✓] 创建任务成功，task_id: {task_id}")

# 轮询任务状态
status_url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"

while True:
    time.sleep(3)  # 每次轮询间隔3秒
    try:
        result_resp = requests.get(status_url, headers={"Authorization": f"Bearer {API_KEY}"}, timeout=10)
        result = result_resp.json()
        status = result["output"]["task_status"]

        if status == "SUCCEEDED":
            image_url = result["output"]["results"][0]["url"]
            print(f"[✓] 图像生成成功！下载链接：{image_url}")

            # 下载图片保存
            img_data = requests.get(image_url).content
            with open("output.jpg", "wb") as f:
                f.write(img_data)
            print("[✓] 图片已保存为 output.jpg")
            break

        elif status == "FAILED":
            print("[✗] 任务失败")
            break
        else:
            print(f"[…] 当前状态：{status}，等待中...")

    except requests.exceptions.Timeout:
        print("[!] 请求超时，重试中...")
    except Exception as e:
        print(f"[!] 出现错误：{e}")
        break
