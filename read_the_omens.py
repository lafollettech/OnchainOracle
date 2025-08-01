import os
from argparse import ArgumentParser

from dotenv import load_dotenv
from tqdm import tqdm
from web3 import Web3

# --- Цветовые константы для мистического интерфейса ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def consult_the_aether():
    """Устанавливает связь с эфиром (сетью Ethereum) для получения знамений."""
    load_dotenv()
    infura_project_id = os.getenv("INFURA_PROJECT_ID")
    if not infura_project_id or infura_project_id == "YOUR_INFURA_PROJECT_ID_HERE":
        print(f"{Colors.FAIL}Разрыв связи: Ключ доступа к эфиру (INFURA_PROJECT_ID) не найден.{Colors.ENDC}")
        print(f"Требуется ритуал настройки. Создайте файл {Colors.BOLD}.env{Colors.ENDC} с вашим ключом.")
        print("Формула: INFURA_PROJECT_ID=\"abcdef1234567890\"")
        return None
    
    w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{infura_project_id}'))
    
    if not w3.is_connected():
        print(f"{Colors.FAIL}Эфир молчит... Не удалось установить соединение.{Colors.ENDC}")
        return None
        
    print(f"{Colors.GREEN}Связь с эфиром установлена. Оракул готов слушать.{Colors.ENDC}")
    return w3

def read_the_omens(w3, focus_address, divination_window):
    """
    Читает и толкует знамения (транзакции) вокруг указанного фокуса (контракта).
    """
    try:
        target_focus = w3.to_checksum_address(focus_address)
    except ValueError:
        print(f"{Colors.FAIL}Неверный фокус: формат адреса искажен.{Colors.ENDC}")
        return

    latest_block_number = w3.eth.block_number
    start_block = latest_block_number - divination_window + 1

    print(f"\n{Colors.HEADER}{Colors.BOLD}🔮 Onchain Oracle... Чтение знамений из эфира...{Colors.ENDC}")
    print(f"ФОКУС ГАДАНИЯ:{Colors.CYAN} {target_focus}{Colors.ENDC}")
    print(f"ОКНО ГАДАНИЯ:{Colors.CYAN} {divination_window} блоков (от {start_block} до {latest_block_number}){Colors.ENDC}")
    
    observed_omens = set()
    total_interactions = 0

    pbar = tqdm(range(start_block, latest_block_number + 1), 
                desc=f"{Colors.BLUE}Толкование знаков{Colors.ENDC}",
                ncols=100)

    for block_num in pbar:
        try:
            block = w3.eth.get_block(block_num, full_transactions=True)
            for tx in block.transactions:
                if tx['to'] and w3.to_checksum_address(tx['to']) == target_focus:
                    total_interactions += 1
                    # Каждое "знамение" - это новый уникальный пользователь
                    omen_source = w3.to_checksum_address(tx['from'])
                    observed_omens.add(omen_source)
        except Exception as e:
            tqdm.write(f"{Colors.WARNING}Помехи в эфире в блоке {block_num}: {e}{Colors.ENDC}")
            continue

    # --- РАСШИФРОВКА ПРЕДСКАЗАНИЯ ---
    total_unique_omens = len(observed_omens)
    
    # Считаем, что все знамения, увиденные в этом окне, - новые.
    # Продвинутый оракул мог бы сверяться с древними свитками (базой данных).
    known_omens_from_past = set() 
    new_omens = observed_omens - known_omens_from_past
    
    # Наша ключевая метрика: Индекс Предвидения!
    foresight_score = (len(new_omens) / total_unique_omens) * 100 if total_unique_omens > 0 else 0

    # --- ВЫВОД ВЕРДИКТА ---
    print(f"\n{Colors.HEADER}{Colors.BOLD}📜 Вердикт Оракула:{Colors.ENDC}")
    print("~" * 50)
    print(f"Всего взаимодействий с фокусом: {Colors.BOLD}{Colors.GREEN}{total_interactions}{Colors.ENDC}")
    print(f"Уникальных знамений (пользователей): {Colors.BOLD}{Colors.GREEN}{total_unique_omens}{Colors.ENDC}")
    
    print(f"\n{Colors.HEADER}{Colors.UNDERLINE}Ключевой показатель предсказания:{Colors.ENDC}")
    print(f"✨ {Colors.WARNING}Индекс Предвидения (Foresight Score):{Colors.ENDC} "
          f"{Colors.BOLD}{foresight_score:.2f}%{Colors.ENDC}")
    print(f"   {Colors.WARNING}(Доля новых знамений среди всех увиденных){Colors.ENDC}")
    print("~" * 50)
    
    if foresight_score > 85:
         print(f"{Colors.GREEN}ПРЕДСКАЗАНИЕ: Благоприятное знамение! Грядет эпоха великого роста и процветания.{Colors.ENDC}")
    elif foresight_score > 50:
        print(f"{Colors.CYAN}ПРЕДСКАЗАНИЕ: Зарождающийся тренд. Звезды указывают на стабильный приток новых последователей.{Colors.ENDC}")
    else:
        print(f"{Colors.BLUE}ПРЕДСКАЗАНИЕ: Устоявшийся порядок. Будущее будет определяться текущими силами.{Colors.ENDC}")


if __name__ == "__main__":
    parser = ArgumentParser(description="OnchainOracle - читает знамения в блокчейне для предсказания роста.")
    parser.add_argument("focus", help="Адрес фокуса (смарт-контракта) для гадания.")
    parser.add_argument("-w", "--window", type=int, default=1000, help="Окно гадания в блоках (по умолчанию: 1000).")
    
    args = parser.parse_args()
    
    aether_link = consult_the_aether()
    if aether_link:
        read_the_omens(aether_link, args.focus, args.window)
