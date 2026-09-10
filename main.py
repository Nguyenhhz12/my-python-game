import json
import os
import random
import sys
import time

# --- MÃ MÀU ANSI ---
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"

SAVE_FILE = "tutien.json"


class TuTienGame:
  BRANCH_DATA = {
      "Pháp Tu": {
          "realms": [
              "Luyện Khí",
              "Trúc Cơ",
              "Kim Đan",
              "Nguyên Anh",
              "Hóa Thần",
              "Luyện Hư",
              "Hợp Thể",
              "Đại Thừa",
              "Độ Kiếp",
          ],
          "energy": "Linh Lực",
          "desc": "Chuyên tâm ngộ đạo, hấp thụ linh khí thiên địa.",
          "life_bonus": 0,
      },
      "Thể Tu": {
          "realms": [
              "Tôi Thể",
              "Hoán Cốt",
              "Kim Thân",
              "Thần Lực",
              "Bất Hoại",
              "Dục Huyết",
              "Thần Thể",
              "Chân Thánh",
              "Đạo Cực",
          ],
          "energy": "Huyết Khí",
          "desc": "Rèn luyện thể xác, thọ nguyên dồi dào, kháng lôi kiếp tốt.",
          "life_bonus": 50,
      },
      "Đan Tu": {
          "realms": [
              "Dược Đồ",
              "Đan Sư",
              "Đại Đan Sư",
              "Đan Thánh",
              "Đan Mộc",
              "Đan Tôn",
              "Đan Đế",
              "Đan Thần",
              "Đan Đạo",
          ],
          "energy": "Đan Khí",
          "desc": "Lấy đan nhập đạo, luyện đan tuyệt đối thành công, đan hiệu gấp đôi.",
          "life_bonus": 10,
      },
  }

  SUB_REALMS = ["Sơ Kỳ", "Trung Kỳ", "Hậu Kỳ", "Viên Mãn"]

  ROOTS = {
      "Phàm Căn": 0.5,
      "Tạp Linh Căn": 1.0,
      "Song Linh Căn": 1.5,
      "Thiên Linh Căn": 3.0,
      "Hỗn Độn Thể": 5.0,
  }

  LOCATIONS = [
      {
          "name": "Núi Luyện Khí",
          "req_realm": 0,
          "risk": 20,
          "desc": "Nơi an toàn cho tân thủ, nhiều Linh Thảo.",
      },
      {
          "name": "U Mê Cốc (Trúc Cơ)",
          "req_realm": 1,
          "risk": 40,
          "desc": "Sương mù bao phủ, chứa nhiều Huyền Thiết.",
      },
      {
          "name": "Xích Đầm (Kim Đan)",
          "req_realm": 2,
          "risk": 65,
          "desc": "Đầm lầy núi lửa, chứa Tinh Kim và Yêu Thú hung dữ.",
      },
      {
          "name": "Vạn Yêu Lĩnh (Nguyên Anh)",
          "req_realm": 3,
          "risk": 85,
          "desc": "Yêu Vương hoành hành, nhiều bảo vật quý hiếm.",
      },
      {
          "name": "Núi Hóa Thần",
          "req_realm": 4,
          "risk": 110,
          "desc": "Cấm địa thiên lôi, nơi thử thách lực chiến thực tế.",
      },
  ]

  def __init__(self):
    self.name = "Đạo Hữu"
    self.branch = "Pháp Tu"
    self.realm_idx = 0
    self.sub_idx = 0

    self.qi = 0
    self.max_qi = 100
    self.age = 15
    self.max_age = 80
    self.linh_thach = 50
    self.breakthrough_buff = 0

    self.weapon_name = "Mộc Kiếm Phàm Nhân"
    self.weapon_mult = 1.0

    self.herbs = {"Linh Thảo": 2, "Kim Ngân Hoa": 1, "Tuyết Liên": 0}
    self.ores = {"Huyền Thiết": 2, "Tinh Kim": 0}
    self.pills = {"Tụ Khí Đan": 1, "Thọ Nguyên Đan": 0, "Phá Cảnh Đan": 0}

    root_choice = random.choices(
        list(self.ROOTS.keys()), weights=[10, 40, 30, 15, 5], k=1
    )[0]
    self.root_name = root_choice
    self.root_mult = self.ROOTS[root_choice]

  def clear_screen(self):
    os.system("cls" if os.name == "nt" else "clear")

  def get_current_realm(self):
    realms = self.BRANCH_DATA[self.branch]["realms"]
    return f"{realms[self.realm_idx]} - {self.SUB_REALMS[self.sub_idx]}"

  def render_bar(self, current, maximum, length=15, color=GREEN):
    filled = int(length * current / maximum) if maximum > 0 else length
    if filled > length:
      filled = length
    bar = "=" * filled + "-" * (length - filled)
    return f"{color}[{bar}]{RESET}"

  def print_typing(self, text, delay=0.015):
    for char in text:
      sys.stdout.write(char)
      sys.stdout.flush()
      time.sleep(delay)
    print()

  def save_game(self):
    data = {
        "name": self.name,
        "branch": self.branch,
        "realm_idx": self.realm_idx,
        "sub_idx": self.sub_idx,
        "qi": self.qi,
        "max_qi": self.max_qi,
        "age": self.age,
        "max_age": self.max_age,
        "linh_thach": self.linh_thach,
        "breakthrough_buff": self.breakthrough_buff,
        "weapon_name": self.weapon_name,
        "weapon_mult": self.weapon_mult,
        "root_name": self.root_name,
        "root_mult": self.root_mult,
        "herbs": self.herbs,
        "ores": self.ores,
        "pills": self.pills,
    }
    try:
      with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
      print(f"\n{GREEN}[+] Đã lưu tiến trình thành công!{RESET}")
    except Exception as e:
      print(f"\n{RED}[!] Lỗi lưu game: {e}{RESET}")
    time.sleep(1.2)

  def load_game(self):
    try:
      with open(SAVE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
      self.name = data["name"]
      self.branch = data["branch"]
      self.realm_idx = data["realm_idx"]
      self.sub_idx = data["sub_idx"]
      self.qi = data["qi"]
      self.max_qi = data["max_qi"]
      self.age = data["age"]
      self.max_age = data["max_age"]
      self.linh_thach = data["linh_thach"]
      self.breakthrough_buff = data.get("breakthrough_buff", 0)
      self.weapon_name = data.get("weapon_name", "Mộc Kiếm Phàm Nhân")
      self.weapon_mult = data.get("weapon_mult", 1.0)
      self.root_name = data["root_name"]
      self.root_mult = data["root_mult"]
      self.herbs = data.get(
          "herbs", {"Linh Thảo": 0, "Kim Ngân Hoa": 0, "Tuyết Liên": 0}
      )
      self.ores = data.get("ores", {"Huyền Thiết": 0, "Tinh Kim": 0})
      self.pills = data.get(
          "pills", {"Tụ Khí Đan": 0, "Thọ Nguyên Đan": 0, "Phá Cảnh Đan": 0}
      )
      return True
    except Exception:
      return False

  def setup_new_game(self):
    self.clear_screen()
    print(f"{YELLOW}--- BẮT ĐẦU TU LUYỆN ---{RESET}\n")
    name_in = input(f"{WHITE}Tên đạo hiệu của bạn: {RESET}").strip()
    if name_in:
      self.name = name_in

    print(f"\n{CYAN}Chọn con đường tu luyện:{RESET}")
    print(f"1. Pháp Tu : {self.BRANCH_DATA['Pháp Tu']['desc']}")
    print(f"2. Thể Tu  : {self.BRANCH_DATA['Thể Tu']['desc']}")
    print(f"3. Đan Tu  : {self.BRANCH_DATA['Đan Tu']['desc']}")

    while True:
      c = input(f"\n{WHITE}Chọn nhánh (1-3): {RESET}").strip()
      if c == "1":
        self.branch = "Pháp Tu"
        break
      elif c == "2":
        self.branch = "Thể Tu"
        self.max_age += self.BRANCH_DATA["Thể Tu"]["life_bonus"]
        break
      elif c == "3":
        self.branch = "Đan Tu"
        self.max_age += self.BRANCH_DATA["Đan Tu"]["life_bonus"]
        break

  def show_status(self):
    self.clear_screen()
    age_color = RED if (self.max_age - self.age) < 15 else GREEN
    energy_name = self.BRANCH_DATA[self.branch]["energy"]

    print(f"{CYAN}===================================================={RESET}")
    print(
        f"{BOLD}{MAGENTA}         THÔNG TIN NHÂN VẬT ({self.branch.upper()})         {RESET}"
    )
    print(f"{CYAN}===================================================={RESET}")
    print(
        f"  Đạo Hiệu  : {BOLD}{self.name}{RESET} | Nhánh: {YELLOW}{self.branch}{RESET}"
    )
    print(
        f"  Thể Chất  : {YELLOW}{self.root_name}{RESET} (Hệ số"
        f" x{self.root_mult})"
    )
    print(
        f"  Vũ Khí    : {GREEN}{self.weapon_name}{RESET} (Sức mạnh:"
        f" x{self.weapon_mult:.1f})"
    )
    print(
        f"  Cảnh Giới : {BOLD}{MAGENTA}{self.get_current_realm()}{RESET}"
    )
    print(
        f"  {energy_name.ljust(10)}: {self.render_bar(self.qi, self.max_qi, 15, CYAN)}"
        f" {CYAN}{self.qi}/{self.max_qi}{RESET}"
    )
    print(
        f"  Thọ Nguyên: {self.render_bar(self.age, self.max_age, 15, age_color)}"
        f" {age_color}{int(self.age)}/{self.max_age} năm{RESET}"
    )
    print(f"  Tài Sản   : {YELLOW}{self.linh_thach} Linh Thạch{RESET}")

    if self.breakthrough_buff > 0:
      print(
          f"  Hiệu Ứng  : {GREEN}+{self.breakthrough_buff}% Tỉ lệ đột"
          f" phá{RESET}"
      )

    print(f"{CYAN}===================================================={RESET}\n")

  def check_death(self):
    if self.age >= self.max_age:
      self.show_status()
      print(
          f"\n{RED}[!] Thọ nguyên cạn kiệt! {self.name} đã tạ thế. Kết thúc"
          f" luân hồi.{RESET}"
      )
      if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
      sys.exit()

  def meditate(self):
    energy_name = self.BRANCH_DATA[self.branch]["energy"]
    self.print_typing(f"{CYAN}Đang tĩnh tọa ngưng tụ {energy_name}...{RESET}")
    time.sleep(0.4)

    base_gained = random.randint(20, 45)
    gained = int(
        base_gained
        * self.root_mult
        * (1 + self.realm_idx * 0.3)
        * self.weapon_mult
    )

    self.qi += gained
    self.age += 0.5
    print(f"{GREEN}[+] Tăng {gained} {energy_name}.{RESET}")
    self.check_death()
    time.sleep(1)

  def breakthrough(self):
    if self.qi < self.max_qi:
      print(f"{RED}[!] Tu vi chưa viên mãn, không thể đột phá!{RESET}")
      time.sleep(1.2)
      return

    energy_name = self.BRANCH_DATA[self.branch]["energy"]
    self.print_typing(
        f"{MAGENTA}Đang xung kích bình cảnh {energy_name}...{RESET}"
    )
    time.sleep(0.8)

    cost = self.max_qi

    if self.sub_idx < 3:
      self.sub_idx += 1
      self.qi -= cost
      self.max_qi = int(self.max_qi * 1.5)
      print(f"{GREEN}[+] Đột phá thành công {self.get_current_realm()}!{RESET}")
    else:
      realms = self.BRANCH_DATA[self.branch]["realms"]
      if self.realm_idx >= len(realms) - 1:
        print(f"{YELLOW}[+] Đã đạt cảnh giới tối cao!{RESET}")
        if os.path.exists(SAVE_FILE):
          os.remove(SAVE_FILE)
        sys.exit()

      success_rate = (
          max(15, 75 - (self.realm_idx * 10)) + self.breakthrough_buff
      )
      roll = random.randint(1, 100)

      print(
          f"Tỉ lệ thành công: {CYAN}{success_rate}%{RESET} | Thử thách:"
          f" {YELLOW}{roll}{RESET}"
      )
      time.sleep(0.8)

      if roll <= success_rate:
        self.realm_idx += 1
        self.sub_idx = 0
        self.qi -= cost
        self.max_qi = int(self.max_qi * 2.5)
        self.max_age += 40 + (self.realm_idx * 50)
        print(
            f"{YELLOW}[+] Đột phá Đại Cảnh Giới thành công:"
            f" {realms[self.realm_idx]}!{RESET}"
        )
      else:
        pen_age = 1 if self.branch == "Thể Tu" else 3
        damage = int(self.max_qi * 0.3)
        self.qi = max(0, self.qi - damage)
        self.age += pen_age
        print(
            f"{RED}[!] Đột phá thất bại! Mất {damage} {energy_name}, giảm"
            f" {pen_age} năm thọ.{RESET}"
        )

      self.breakthrough_buff = 0
    time.sleep(1.8)

  def forge(self):
    self.clear_screen()
    print(f"{CYAN}=== RÈN VŨ KHÍ TỰ CHỌN ==={RESET}")
    print(
        f"Vũ khí hiện tại: {YELLOW}{self.weapon_name}{RESET} (Sức mạnh:"
        f" x{self.weapon_mult:.1f})"
    )
    print(
        f"Khoáng thạch: Huyền Thiết: {self.ores['Huyền Thiết']} | Tinh Kim:"
        f" {self.ores['Tinh Kim']}\n"
    )

    w_name = input(
        f"{WHITE}Nhập tên vũ khí mới (Bỏ trống để hủy): {RESET}"
    ).strip()
    if not w_name:
      return

    try:
      w_mult = float(
          input(f"{WHITE}Nhập hệ số sức mạnh (Từ 1.2 đến 10.0): {RESET}")
      )
    except ValueError:
      print(f"{RED}[!] Chỉ số không hợp lệ!{RESET}")
      time.sleep(1.2)
      return

    if w_mult < 1.2 or w_mult > 10.0:
      print(f"{RED}[!] Hệ số chỉ được nằm trong khoảng 1.2 đến 10.0!{RESET}")
      time.sleep(1.2)
      return

    success_rate = max(5, int(115 - (w_mult * 18)))
    req_ht = int(w_mult * 1.5)
    req_tk = int(w_mult * 0.8)

    print("\nThông tin rèn:")
    print(f"- Tên vũ khí: {GREEN}{w_name}{RESET}")
    print(f"- Sức mạnh: {YELLOW}x{w_mult:.1f}{RESET}")
    print(f"- Yêu cầu: {req_ht} Huyền Thiết, {req_tk} Tinh Kim")
    print(f"- Tỉ lệ thành công: {CYAN}{success_rate}%{RESET}")

    ans = (
        input(f"\n{WHITE}Xác nhận tiến hành rèn? (y/n): {RESET}")
        .strip()
        .lower()
    )
    if ans == "y":
      if self.ores["Huyền Thiết"] >= req_ht and self.ores["Tinh Kim"] >= req_tk:
        self.ores["Huyền Thiết"] -= req_ht
        self.ores["Tinh Kim"] -= req_tk

        self.print_typing(f"{MAGENTA}Đang tiến hành tôi luyện...{RESET}")
        time.sleep(1.2)

        roll = random.randint(1, 100)
        if roll <= success_rate:
          self.weapon_name = w_name
          self.weapon_mult = w_mult
          print(f"{GREEN}[+] Rèn thành công vũ khí: {w_name}!{RESET}")
        else:
          print(f"{RED}[!] Rèn thất bại, mất toàn bộ nguyên liệu!{RESET}")
      else:
        print(f"{RED}[!] Không đủ khoáng thạch!{RESET}")
    time.sleep(1.8)

  def explore(self):
    while True:
      self.clear_screen()
      print(f"{BLUE}=== BẢN ĐỒ LỊCH LUYỆN ==={RESET}")
      for idx, loc in enumerate(self.LOCATIONS, 1):
        req_name = self.BRANCH_DATA[self.branch]["realms"][loc["req_realm"]]
        print(f"{idx}. {loc['name']} (Yêu cầu: {req_name})")
        print(f"   Mô tả: {loc['desc']}")
      print("0. Trở về")
      print(f"{BLUE}========================={RESET}")

      c = input(f"\n{WHITE}Chọn điểm đến: {RESET}").strip()
      if c == "0":
        break

      if c in ["1", "2", "3", "4", "5"]:
        loc = self.LOCATIONS[int(c) - 1]

        if self.realm_idx < loc["req_realm"]:
          print(
              f"\n{RED}[!] Cảnh báo: Cảnh giới quá thấp so với địa hình"
              f" này!{RESET}"
          )
          confirm = (
              input(f"{WHITE}Vẫn tiếp tục vào? (y/n): {RESET}").strip().lower()
          )
          if confirm != "y":
            continue

        self.print_typing(f"{BLUE}Đang tiến vào {loc['name']}...{RESET}")
        time.sleep(0.8)
        self.age += 0.5

        combat_power = (self.realm_idx + 1) * 20 + (self.weapon_mult * 15)
        risk = loc["risk"]
        event = random.randint(1, 100)

        if event <= 40:
          lt = random.randint(20, 80) * (int(c))
          herb = random.choice(["Linh Thảo", "Kim Ngân Hoa", "Tuyết Liên"])
          self.linh_thach += lt
          self.herbs[herb] += 1
          print(f"{GREEN}[+] Thu hoạch: {lt} Linh Thạch và 1 {herb}.{RESET}")

        elif event <= 75:
          print(
              f"{RED}[!] Gặp Yêu Thú! (Yêu cầu lực chiến: {risk} | Hiện tại:"
              f" {int(combat_power)}){RESET}"
          )
          print(
              f"1. Dùng Tụ Khí Đan (Còn {self.pills['Tụ Khí Đan']}) - Tăng lực"
              " chiến"
          )
          print(
              f"2. Dùng Thọ Nguyên Đan (Còn {self.pills['Thọ Nguyên Đan']}) -"
              " Phục hồi thọ nguyên"
          )
          print("0. Trực tiếp chiến đấu")

          pill_choice = input("Lựa chọn: ").strip()
          bonus_power = 0
          if pill_choice == "1" and self.pills["Tụ Khí Đan"] > 0:
            self.pills["Tụ Khí Đan"] -= 1
            bonus_power = 35
            print(f"{GREEN}[+] Đã dùng Tụ Khí Đan, lực chiến tăng tạm thời!{RESET}")
          elif pill_choice == "2" and self.pills["Thọ Nguyên Đan"] > 0:
            self.pills["Thọ Nguyên Đan"] -= 1
            self.max_age += 10
            print(f"{GREEN}[+] Đã dùng Thọ Nguyên Đan, tăng thọ nguyên!{RESET}")

          if (combat_power + bonus_power) >= risk:
            gain_qi = int(random.randint(50, 150) * self.weapon_mult)
            self.qi += gain_qi
            print(
                f"{YELLOW}[+] Đánh bại Yêu Thú nhờ vũ khí"
                f" {self.weapon_name}! Nhận +{gain_qi} Tu vi.{RESET}"
            )
          else:
            dmg = random.randint(30, 90)
            self.qi = max(0, self.qi - dmg)
            print(f"{RED}[!] Thất bại trong chiến đấu, mất {dmg} tu vi!{RESET}")

        else:
          ore = random.choice(["Huyền Thiết", "Tinh Kim"])
          self.ores[ore] += 2
          print(f"{MAGENTA}[+] Nhặt được 2 khối {ore}.{RESET}")

        self.check_death()
        time.sleep(2)

  def alchemy(self):
    while True:
      self.clear_screen()
      print(f"{GREEN}=== LUYỆN ĐAN ==={RESET}")
      print(
          f"Kho dược: Linh Thảo: {self.herbs['Linh Thảo']} | Kim Ngân Hoa:"
          f" {self.herbs['Kim Ngân Hoa']} | Tuyết Liên:"
          f" {self.herbs['Tuyết Liên']}"
      )
      print("1. Tụ Khí Đan    (2 Linh Thảo + 1 Kim Ngân Hoa) -> Tăng Tu Vi")
      print("2. Thọ Nguyên Đan(2 Linh Thảo + 1 Tuyết Liên)  -> Tăng Thọ Nguyên")
      print("3. Phá Cảnh Đan (2 Tuyết Liên + 2 Kim Ngân Hoa) -> Tăng Tỉ Lệ Đột Phá")
      print("0. Rời đi")
      print(f"{GREEN}================={RESET}")

      c = input(f"\n{WHITE}Chọn đan dược cần luyện: {RESET}").strip()
      if c == "0":
        break

      rate = 100 if self.branch == "Đan Tu" else 75

      if c == "1":
        if self.herbs["Linh Thảo"] >= 2 and self.herbs["Kim Ngân Hoa"] >= 1:
          self.herbs["Linh Thảo"] -= 2
          self.herbs["Kim Ngân Hoa"] -= 1
          if random.randint(1, 100) <= rate:
            qty = 2 if self.branch == "Đan Tu" else 1
            self.pills["Tụ Khí Đan"] += qty
            print(f"{GREEN}[+] Thu được {qty} Tụ Khí Đan.{RESET}")
          else:
            print(f"{RED}[!] Luyện đan thất bại!{RESET}")
        else:
          print(f"{RED}[!] Không đủ dược liệu!{RESET}")

      elif c == "2":
        if self.herbs["Linh Thảo"] >= 2 and self.herbs["Tuyết Liên"] >= 1:
          self.herbs["Linh Thảo"] -= 2
          self.herbs["Tuyết Liên"] -= 1
          if random.randint(1, 100) <= rate:
            qty = 2 if self.branch == "Đan Tu" else 1
            self.pills["Thọ Nguyên Đan"] += qty
            print(f"{GREEN}[+] Thu được {qty} Thọ Nguyên Đan.{RESET}")
          else:
            print(f"{RED}[!] Luyện đan thất bại!{RESET}")
        else:
          print(f"{RED}[!] Không đủ dược liệu!{RESET}")

      elif c == "3":
        if self.herbs["Tuyết Liên"] >= 2 and self.herbs["Kim Ngân Hoa"] >= 2:
          self.herbs["Tuyết Liên"] -= 2
          self.herbs["Kim Ngân Hoa"] -= 2
          if random.randint(1, 100) <= rate:
            qty = 2 if self.branch == "Đan Tu" else 1
            self.pills["Phá Cảnh Đan"] += qty
            print(f"{GREEN}[+] Thu được {qty} Phá Cảnh Đan.{RESET}")
          else:
            print(f"{RED}[!] Luyện đan thất bại!{RESET}")
        else:
          print(f"{RED}[!] Không đủ dược liệu!{RESET}")

      time.sleep(1.2)

  def inventory(self):
    while True:
      self.clear_screen()
      print(f"{MAGENTA}=== TÚI TRỮ VẬT ==={RESET}")
      print(f"1. Tụ Khí Đan    : {self.pills['Tụ Khí Đan']} viên")
      print(f"2. Thọ Nguyên Đan: {self.pills['Thọ Nguyên Đan']} viên")
      print(f"3. Phá Cảnh Đan  : {self.pills['Phá Cảnh Đan']} viên")
      print(
          f"\nDược liệu: Linh Thảo ({self.herbs['Linh Thảo']}), Kim Ngân Hoa"
          f" ({self.herbs['Kim Ngân Hoa']}), Tuyết Liên"
          f" ({self.herbs['Tuyết Liên']})"
      )
      print(
          f"Khoáng thạch: Huyền Thiết ({self.ores['Huyền Thiết']}), Tinh Kim"
          f" ({self.ores['Tinh Kim']})"
      )
      print("0. Trở về")
      print(f"{MAGENTA}===================={RESET}")

      c = input(f"\n{WHITE}Chọn đan dược cần dùng: {RESET}").strip()
      if c == "0":
        break

      mult = 2 if self.branch == "Đan Tu" else 1

      if c == "1" and self.pills["Tụ Khí Đan"] > 0:
        self.pills["Tụ Khí Đan"] -= 1
        gain = 300 * mult
        self.qi += gain
        print(f"{GREEN}[+] Sử dụng Tụ Khí Đan: +{gain} Tu Vi.{RESET}")
      elif c == "2" and self.pills["Thọ Nguyên Đan"] > 0:
        self.pills["Thọ Nguyên Đan"] -= 1
        gain = 15 * mult
        self.max_age += gain
        print(f"{GREEN}[+] Sử dụng Thọ Nguyên Đan: +{gain} năm thọ.{RESET}")
      elif c == "3" and self.pills["Phá Cảnh Đan"] > 0:
        self.pills["Phá Cảnh Đan"] -= 1
        gain = 25 * mult
        self.breakthrough_buff += gain
        print(
            f"{GREEN}[+] Sử dụng Phá Cảnh Đan: +{gain}% Tỉ lệ đột phá.{RESET}"
        )
      else:
        print(f"{RED}[!] Số lượng không đủ hoặc chọn sai!{RESET}")
      time.sleep(1.2)

  def shop(self):
    while True:
      self.clear_screen()
      print(f"{YELLOW}=== TỤ BẢO CÁC ==={RESET}")
      print(f"Số dư: {YELLOW}{self.linh_thach} Linh Thạch{RESET}")
      print(f"1. Linh Thảo     - {YELLOW}20 LT{RESET}")
      print(f"2. Kim Ngân Hoa  - {YELLOW}35 LT{RESET}")
      print(f"3. Tuyết Liên    - {YELLOW}50 LT{RESET}")
      print(f"4. Huyền Thiết   - {YELLOW}50 LT{RESET}")
      print(f"5. Tinh Kim      - {YELLOW}100 LT{RESET}")
      print("0. Rời đi")
      print(f"{YELLOW}=================={RESET}")

      c = input(f"\n{WHITE}Chọn vật phẩm mua: {RESET}").strip()
      if c == "0":
        break

      if c == "1" and self.linh_thach >= 20:
        self.linh_thach -= 20
        self.herbs["Linh Thảo"] += 1
      elif c == "2" and self.linh_thach >= 35:
        self.linh_thach -= 35
        self.herbs["Kim Ngân Hoa"] += 1
      elif c == "3" and self.linh_thach >= 50:
        self.linh_thach -= 50
        self.herbs["Tuyết Liên"] += 1
      elif c == "4" and self.linh_thach >= 50:
        self.linh_thach -= 50
        self.ores["Huyền Thiết"] += 1
      elif c == "5" and self.linh_thach >= 100:
        self.linh_thach -= 100
        self.ores["Tinh Kim"] += 1
      else:
        print(f"{RED}[!] Không đủ Linh Thạch!{RESET}")
      time.sleep(1)

  def start(self):
    self.clear_screen()
    print(f"{CYAN}========================================{RESET}")
    print(f"{BOLD}{YELLOW}        ĐẠI THẾ GIỚI TU TIÊN V3.0        {RESET}")
    print(f"{CYAN}========================================{RESET}\n")

    if os.path.exists(SAVE_FILE):
      print(f"{MAGENTA}[+] Phát hiện dữ liệu đã lưu.{RESET}")
      ans = (
          input("Tải lại tiến trình cũ? (y/n): ").strip().lower()
      )
      if ans == "y" and self.load_game():
        print(f"{GREEN}[+] Tải dữ liệu thành công!{RESET}")
        time.sleep(1)
      else:
        self.setup_new_game()
    else:
      self.setup_new_game()

    while True:
      self.show_status()
      print(f"{WHITE}1.{RESET} Bế Quan Tu Luyện")
      print(f"{WHITE}2.{RESET} Đột Phá Cảnh Giới")
      print(f"{WHITE}3.{RESET} Lịch Luyện Cấm Địa")
      print(f"{WHITE}4.{RESET} Luyện Đan")
      print(f"{WHITE}5.{RESET} Tự Rèn Vũ Khí")
      print(f"{WHITE}6.{RESET} Túi Trữ Vật & Dùng Đan")
      print(f"{WHITE}7.{RESET} Cửa Hàng (Shop)")
      print(f"{WHITE}8.{RESET} Lưu Tiến Trình")
      print(f"{WHITE}9.{RESET} Thoát Game")

      c = input(f"\n{WHITE}Lựa chọn của bạn: {RESET}").strip()

      if c == "1":
        self.meditate()
      elif c == "2":
        self.breakthrough()
      elif c == "3":
        self.explore()
      elif c == "4":
        self.alchemy()
      elif c == "5":
        self.forge()
      elif c == "6":
        self.inventory()
      elif c == "7":
        self.shop()
      elif c == "8":
        self.save_game()
      elif c == "9":
        print(f"\n{YELLOW}Tạm biệt đạo hữu!{RESET}")
        break


if __name__ == "__main__":
  try:
    game = TuTienGame()
    game.start()
  except KeyboardInterrupt:
    print(f"\n\n{RED}[!] Đã thoát trò chơi.{RESET}")