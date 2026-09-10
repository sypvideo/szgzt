# -*- coding: utf-8 -*-
"""
识字小天地 · 音频批量生成脚本
--------------------------------------------------
自动读取 index.html 里的 200 字数据，批量生成单字 / 组词发音。

用法（在本目录下打开命令行）：
    python gen_audio.py                # 生成全部（200 单字 + 533 组词）
    python gen_audio.py --only char    # 只生成单字
    python gen_audio.py --only word    # 只生成组词
    python gen_audio.py --slow         # 额外生成慢速版单字（audio/slow/）

特性：
    · 已存在且大于 1KB 的文件自动跳过（可反复运行，断点续传）
    · 失败自动重试 3 次
    · 并发 5 路，全部约 5~10 分钟

依赖：pip install edge-tts
"""
import argparse
import asyncio
import os
import re

import edge_tts

ROOT = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(ROOT, "index.html")

# 音色可选：zh-CN-XiaoxiaoNeural（女声，推荐）、zh-CN-XiaoyiNeural（女声）、
#          zh-CN-YunxiNeural（男声）、zh-CN-YunjianNeural（男声）
VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-10%"        # 正常版语速：放慢 10%，适合儿童
SLOW_RATE = "-35%"   # 慢速版语速
CONCURRENCY = 5
RETRY = 3


def parse_data():
    """从 index.html 提取全部单字与组词"""
    html = open(HTML, encoding="utf-8").read()
    body = re.search(r"const CHARS = \[(.*?)\n\];", html, re.S).group(1)
    chars, words = [], set()
    for c, w in re.findall(r"\{c:'(.)',p:'[^']*',s:\d+,w:\[([^\]]*)\]", body):
        chars.append(c)
        for x in re.findall(r"'([^']*)'", w):
            if x:
                words.add(x)
    return chars, sorted(words)


async def tts_one(text, path, rate, sem, stats):
    if os.path.exists(path) and os.path.getsize(path) > 1024:
        stats["skip"] += 1
        return
    for attempt in range(RETRY):
        try:
            async with sem:
                await edge_tts.Communicate(text, VOICE, rate=rate).save(path)
            stats["ok"] += 1
            if stats["ok"] % 25 == 0:
                print(f"  已生成 {stats['ok']} 个 …", flush=True)
            return
        except Exception as e:
            if attempt == RETRY - 1:
                stats["fail"].append(text)
                print(f"  x 失败: {text} ({e})")
            else:
                await asyncio.sleep(1.5 * (attempt + 1))


async def run():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["char", "word", "both"], default="both")
    ap.add_argument("--slow", action="store_true", help="额外生成慢速版单字到 audio/slow/")
    args = ap.parse_args()

    chars, words = parse_data()
    print(f"字库：单字 {len(chars)} 个，组词 {len(words)} 个")

    sem = asyncio.Semaphore(CONCURRENCY)
    stats = {"ok": 0, "skip": 0, "fail": []}
    tasks = []

    if args.only in ("char", "both"):
        d = os.path.join(ROOT, "audio", "chars")
        os.makedirs(d, exist_ok=True)
        tasks += [tts_one(c, os.path.join(d, c + ".mp3"), RATE, sem, stats) for c in chars]
        if args.slow:
            ds = os.path.join(ROOT, "audio", "slow")
            os.makedirs(ds, exist_ok=True)
            tasks += [tts_one(c, os.path.join(ds, c + ".mp3"), SLOW_RATE, sem, stats) for c in chars]

    if args.only in ("word", "both"):
        d = os.path.join(ROOT, "audio", "words")
        os.makedirs(d, exist_ok=True)
        tasks += [tts_one(w, os.path.join(d, w + ".mp3"), RATE, sem, stats) for w in words]

    await asyncio.gather(*tasks)
    print(f"\n完成：新生成 {stats['ok']}，跳过已存在 {stats['skip']}，失败 {len(stats['fail'])}")
    if stats["fail"]:
        print("失败列表：", " ".join(stats["fail"]))


if __name__ == "__main__":
    asyncio.run(run())
