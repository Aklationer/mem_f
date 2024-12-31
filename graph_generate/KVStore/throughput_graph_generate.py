import matplotlib.pyplot as plt
import json
import os

# 手動輸入檔案名稱
files = {
    "$10^2$": {
        "MPT": "readwriteeven-mpt-1k-fan4-ratio4-mem64-ts.json",
        "CMI": "readwriteeven-non_learn_cmi-1k-fan4-ratio4-mem64-ts.json",
        "COLE": "readwriteeven-cole-1k-fan4-ratio4-mem450000-ts.json",
        "COLE*": "readwriteeven-cole_star-1k-fan4-ratio4-mem450000-ts.json",
    },
    "$10^3$": {
        "MPT": "readwriteeven-mpt-10k-fan4-ratio4-mem64-ts.json",
        "CMI": "readwriteeven-non_learn_cmi-10k-fan4-ratio4-mem64-ts.json",
        "COLE": "readwriteeven-cole-10k-fan4-ratio4-mem450000-ts.json",
        "COLE*": "readwriteeven-cole_star-10k-fan4-ratio4-mem450000-ts.json",
    },
    "$10^4$": {
        "MPT": "readwriteeven-mpt-100k-fan4-ratio4-mem64-ts.json",
        "CMI": "readwriteeven-non_learn_cmi-100k-fan4-ratio4-mem64-ts.json",
        "COLE": "readwriteeven-cole-100k-fan4-ratio4-mem450000-ts.json",
        "COLE*": "readwriteeven-cole_star-100k-fan4-ratio4-mem450000-ts.json",
    },
    "$10^5$": {
        "MPT": "readwriteeven-mpt-10000k-fan4-ratio4-mem64-ts.json",
        "CMI": "readwriteeven-non_learn_cmi-1000k-fan4-ratio4-mem64-ts.json",
        "COLE": "readwriteeven-cole-1000k-fan4-ratio4-mem450000-ts.json",
        "COLE*": "readwriteeven-cole_star-1000k-fan4-ratio4-mem450000-ts.json",
    },
}

# 資料目錄
directory = "./"

# 計算 Throughput 的函數
def calculate_throughput(file_path):
    with open(file_path, "r") as f:
        data = [json.loads(line) for line in f]  # 每行解析 JSON
    
    # 計算總時間和 Throughput
    start_time = data[0]["start_ts"] / 1_000_000_000  # 起始時間 (秒)
    end_time = data[-1]["end_ts"] / 1_000_000_000    # 結束時間 (秒)
    total_time = end_time - start_time
    block_count = len(data)
    throughput_tps = (block_count / total_time)   # Throughput (TPS) 乘以 1000
    return throughput_tps

# 計算所有檔案的 Throughput
throughput_data = {}
for block_height, methods in files.items():
    throughput_data[block_height] = {}
    for method, file_name in methods.items():
        file_path = os.path.join(directory, file_name)
        throughput_data[block_height][method] = calculate_throughput(file_path)

# 繪製圖表
def plot_throughput(throughput_data):
    block_heights = sorted(throughput_data.keys())  # 按區塊高度排序
    methods = list(next(iter(throughput_data.values())).keys())  # 提取方法名稱
    x = range(len(block_heights))  # x 軸位置
    bar_width = 0.2  # 每個條形寬度

    plt.figure(figsize=(12, 8))

    # 繪製條形圖
    for i, method in enumerate(methods):
        throughput_values = [throughput_data[block_height][method] for block_height in block_heights]
        plt.bar(
            [pos + i * bar_width for pos in x],
            throughput_values,
            bar_width,
            label=method,
            hatch=["/", "\\", "x", "-", "+"].pop(i % 5),  # 設置不同圖案
            edgecolor="black"
        )

    # 設置圖表屬性
    plt.xticks([pos + (len(methods) - 1) * bar_width / 2 for pos in x], block_heights)
    plt.yscale("log")  # y 軸對數刻度
    plt.xlabel("Block Height (SmallBank)")
    plt.ylabel("Throughput (TPS")
    plt.title("Throughput Comparison by Block Height")
    plt.legend(title="Indexes", loc="upper left")
    plt.grid(axis="y", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.show()

# 繪製圖表
plot_throughput(throughput_data)
