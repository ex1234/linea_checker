import requests
import pandas as pd
from tabulate import tabulate
from tqdm import tqdm

# Функция для чтения кошельков из файла
def read_wallets_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            wallets = [line.strip() for line in file if line.strip()]
        return wallets
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return []

# Функция для получения данных по одному кошельку
def get_wallet_data(wallet):
    wallet = wallet.lower()  # Преобразуем кошелек в нижний регистр
    url = f"https://kx58j6x5me.execute-api.us-east-1.amazonaws.com/linea/getUserPointsSearch?user={wallet}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data[0] if data else None
    else:
        return None

# Функция для обработки списка кошельков
def check_wallets(wallets):
    results = []
    total_xp = 0
    for wallet in tqdm(wallets, desc="Обработка кошельков"):
        data = get_wallet_data(wallet)
        if data:
            ea_flag = "YES" if data.get("ea_flag") == 1 else "хуйня"
            results.append({
                "wallet": wallet,
                "Rank": data.get("rank_xp"),
                "Total Points (XP)": data.get("xp"),
                "Active Liquidity Points": data.get("alp"),
                "Ecosystem Points": data.get("ep"),
                "Referral Points": data.get("rp"),
                "Veteran Points": data.get("plp"),
                "Backfilled Points": data.get("bp"),
                "Early Adoptor Flag": ea_flag
            })
            total_xp += data.get("xp", 0)
        else:
            print(f"Нет данных для кошелька {wallet}")
    return results, total_xp

# Основная функция
def main():
    wallets_file_path = 'wallets.txt'  # Укажите путь к вашему файлу с кошельками
    wallets = read_wallets_from_file(wallets_file_path)
    if wallets:
        print(f"Найдено {len(wallets)} кошельков.")
        results, total_xp = check_wallets(wallets)
        if results:
            df = pd.DataFrame(results)
            print("\nТаблица результатов:")
            print(tabulate(df, headers='keys', tablefmt='psql'))
            print(f"\nОбщее количество xp: {total_xp}")
        else:
            print("Нет данных для отображения.")
    else:
        print("Список кошельков пуст или файл не найден.")

# Запуск основной функции
if __name__ == "__main__":
    main()
