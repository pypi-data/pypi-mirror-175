# -*- coding: utf-8 -*-
# @Time        : 2022/11/4 18:50
# @File        : __init__.py
# @Description : None
# ----------------------------------------------
# ☆ ☆ ☆ ☆ ☆ ☆ ☆ 
# >>> Author    : Alex
# >>> Mail      : liu_zhao_feng_alex@163.com
# >>> Github    : https://github.com/koking0
# >>> Blog      : https://alex007.blog.csdn.net/
# ☆ ☆ ☆ ☆ ☆ ☆ ☆
import httpx
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.matcher import Matcher
from nonebot.params import CommandArg

from .config import config
from .limiter import limiter

writer = on_command("写作文", priority=5, block=True)


async def get_token():
	url = "https://wenxin.baidu.com/moduleApi/portal/api/oauth/token"
	async with httpx.AsyncClient(verify=False, timeout=None) as client:
		resp = await client.post(
			url,
			data={
				"grant_type": "client_credentials",
				"client_id": config.wen_xin_ak,
				"client_secret": config.wen_xin_sk
			},
			headers={
				"Content-Type": "application/x-www-form-urlencoded"
			}
		)
		access_token = resp.json()["data"]
		return access_token


async def get_write(access_token, text):
	url = "https://wenxin.baidu.com/moduleApi/portal/api/rest/1.0/ernie/3.0.21/zeus"
	payload = {
		"access_token": access_token,
		"text": text,
		"seq_len": 512,
		"topp": 0.9,
		"penalty_score": 1.2,
		"min_dec_len": 128
	}  # 请求参数
	async with httpx.AsyncClient(verify=False, timeout=None) as client:
		resp = await client.post(url, data=payload)
		data = resp.json()
		print(data)
		if data["code"] == 0:  # 请求成功
			return [True, data["data"]["result"]]

		return [False, data["msg"]]


@writer.handle()
async def _(matcher: Matcher, event: MessageEvent, args=CommandArg()):
	# 判断用户是否触发频率限制
	user_id = event.user_id
	managers = config.manager_list  # 管理员列表(不触发冷却时间限制)
	if not limiter.check(user_id):
		left_time = limiter.left_time(user_id)
		await matcher.finish(f"不可以哦，你刚画了一次哎，需要等待{int(left_time)}秒再找俺画画！")

	# 启动画画任务
	text = args  # 绘画的任务描述文字
	await matcher.send(f"小麦正在奋笔疾书，给您写{text}，预计需要1-2分钟~...")

	try:
		access_token = await get_token()

		if not str(user_id) in managers:
			limiter.start_cd(user_id)  # 启动冷却时间限制

		success, result = await get_write(access_token, text)
		if success:
			result = f"{result}\n\n本文章由百度飞桨文心大模型原创生成，不会雷同的哦~"
			result = f"{result}\n不过生成效果还有些逊色，如有不周之处，还需手动润色。"
			await matcher.finish(result)
		else:
			await matcher.finish(f"对不起，呜呜呜，创作失败了：{result}\n可以联系管理员QQ：2426671397!")

	except Exception as e:
		print(e)
