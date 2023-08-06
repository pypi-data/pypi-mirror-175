# nonebot_plugin_wen_xin

✨ NoneBot 百度文心 ✨

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/Matrix-King-Studio/nonebot_plugin_wen_xin.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot_plugin_wen_xin">
    <img src="https://img.shields.io/pypi/v/nonebot_plugin_wen_xin.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

## 📖 介绍

接入Stable Diffusion做AI文生图。

## 💿 安装

<details>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot_plugin_wen_xin

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot_plugin_wen_xin
</details>
<details>
<summary>conda</summary>

    conda install nonebot_plugin_wen_xin
</details>

打开 nonebot2 项目的 `bot.py` 文件, 在其中写入

    nonebot.load_plugin("nonebot_plugin_wen_xin")

</details>

<details>
<summary>从 github 安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 输入以下命令克隆此储存库

    git clone https://github.com/Matrix-King-Studio/nonebot_plugin_wen_xin.git

打开 nonebot2 项目的 `bot.py` 文件, 在其中写入

    nonebot.load_plugin("src.plugins.nonebot_plugin_wen_xin")

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值  |                                  说明                                  |
|:-----:|:----:|:----:|:--------------------------------------------------------------------:|
| cd_time | 否 | 100s |      CD时间         |
| manager_list | 否 |  无   | 不受冷却时间限制的管理员 |

## 🎉 使用

### 指令表

|    指令    |  权限   | 需要@ | 范围 |
|:--------:|:-----:|:----:|:----:|
|  /画画帮助   | 所有人 | 否 | 群聊 |
|  /画画 二次元，中国女孩，唯美，烟火，棕红色长发，金色眼睛，洛丽塔风格，精致面容，毛发细致，cg感，高清，8k，浪漫主义   |  所有人   | 否 | 群聊 |

### 效果图
