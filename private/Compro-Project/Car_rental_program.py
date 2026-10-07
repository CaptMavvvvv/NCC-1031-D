import struct
import os
import datetime
import traceback
import unicodedata as _ud
from typing import Dict, Any, Tuple, Optional, List, Union

# ==============================================================================
# 1. Constants
# ==============================================================================

# Car: IsActive(1)+ID(4)+Model(30)+Plate(10)+Rate(4)+IsRented(1)+Category(15) = 65 bytes
CAR_FORMAT      = '<?i30s10sf?15s'
CAR_FORMAT_KEYS = ['IsActive', 'ID', 'Model', 'LicensePlate', 'DailyRate', 'IsRented', 'Category']
CAR_FILE_NAME   = 'cars.bin'
CAR_CATEGORIES  = ['Sedan', 'SUV', 'Pickup', 'Van', 'Hatchback', 'Sport', 'Other']

# Customer: IsActive(1)+ID(4)+Name(50)+Phone(15)+Email(30) = 100 bytes
CUSTOMER_FORMAT      = '<?i50s15s30sI'
CUSTOMER_FORMAT_KEYS = ['IsActive', 'ID', 'Name', 'Phone', 'Email', 'Points']
CUSTOMER_FILE_NAME   = 'customers.bin'

# Rental: IsActive(1)+ID(4)+CustID(4)+CarID(4)+Start(4)+End(4)+Price(8) = 29 bytes
RENTAL_FORMAT      = '<?iiiiid'
RENTAL_FORMAT_KEYS = ['IsActive', 'ID', 'CustomerID', 'CarID', 'StartDate', 'EndDate', 'TotalPrice']
RENTAL_FILE_NAME   = 'rentals.bin'

# Report layout
BIW = 76   # รายงาน: ความกว้างภายใน Box (ตอนจัดตาราง)
#             Box total width = BIW + 6 = 82 chars

# ==============================================================================
# 2. Base FileManager
# ==============================================================================

class FileManager:
    """จัดการการเข้าถึงไฟล์ Binary — CRUD + Auto-ID + Substring Search"""

    def __init__(self, format_string: str, format_keys: List[str],
                 filename: str, encoding: str = 'utf-8'):
        self.format      = format_string
        self.format_keys = format_keys
        self.filename    = filename
        self.encoding    = encoding
        self.record_size = struct.calcsize(format_string)

        try:
            self.file = open(self.filename, 'r+b')
            print(f"  File '{self.filename}' opened for R/W.  (record_size={self.record_size}B)")
        except FileNotFoundError:
            self.file = open(self.filename, 'w+b')
            print(f"  File '{self.filename}' created and opened for R/W.  (record_size={self.record_size}B)")
        self.file.seek(0, os.SEEK_SET)

    def close(self):
        if self.file and not self.file.closed:
            self.file.flush()
            os.fsync(self.file.fileno())
            self.file.close()

    def _pack_record(self, data: Dict[str, Any]) -> bytes:
        raise NotImplementedError

    def _unpack_record(self, record_bytes: bytes) -> Dict[str, Any]:
        raise NotImplementedError

    # ── CRUD ──────────────────────────────────────────────────────────────────

    def add_record(self, data: Dict[str, Any]) -> int:
        """C — เพิ่มระเบียน (เติมใน Free Slot ก่อน, ถ้าไม่มีค่อย Append)"""
        data['IsActive'] = True
        packed = self._pack_record(data)
        self.file.seek(0, os.SEEK_SET)

        while True:
            offset = self.file.tell()
            chunk  = self.file.read(self.record_size)
            if len(chunk) < self.record_size:
                break
            try:
                if not struct.unpack('<?', chunk[0:1])[0]:
                    self.file.seek(offset, os.SEEK_SET)
                    self.file.write(packed)
                    self.file.flush()
                    print(f"  [Reuse] offset {offset}B in '{self.filename}'")
                    return offset
            except struct.error:
                pass

        self.file.seek(0, os.SEEK_END)
        offset = self.file.tell()
        self.file.write(packed)
        self.file.flush()
        print(f"  [Append] offset {offset}B in '{self.filename}'")
        return offset

    def get_record_by_id(self, record_id: int) -> Optional[Tuple[Dict[str, Any], int]]:
        """R — คืน (data, offset) หรือ None ถ้าไม่พบ"""
        self.file.seek(0, os.SEEK_SET)
        offset = 0
        while True:
            chunk = self.file.read(self.record_size)
            if len(chunk) < self.record_size:
                break
            try:
                rec = self._unpack_record(chunk)
                if rec.get('IsActive') and rec.get('ID') == record_id:
                    return rec, offset
            except struct.error:
                pass
            offset += self.record_size
        return None

    def update_record(self, record_id: int, new_data: Dict[str, Any]) -> bool:
        """U — อัปเดตฟิลด์ที่ระบุ"""
        result = self.get_record_by_id(record_id)
        if result is None:
            return False
        old_data, offset = result
        merged = {**old_data, **new_data, 'IsActive': old_data.get('IsActive', True)}
        try:
            packed = self._pack_record(merged)
        except Exception as e:
            print(f"  [Error] packing record: {e}")
            return False
        self.file.seek(offset, os.SEEK_SET)
        self.file.write(packed)
        self.file.flush()
        return True

    def delete_record(self, record_id: int) -> bool:
        """D — Soft Delete (ตั้ง IsActive = False)"""
        result = self.get_record_by_id(record_id)
        if result is None:
            print(f"  // Error: ID {record_id} not found in '{self.filename}' \\")
            return False
        _, offset = result
        self.file.seek(offset, os.SEEK_SET)
        self.file.write(struct.pack('<?', False))
        self.file.flush()
        print(f"  [Soft-Delete] ID {record_id} at offset {offset}B in '{self.filename}'")
        return True

    def get_all_records(self) -> List[Dict[str, Any]]:
        """คืนทุกระเบียน ทั้ง Active และ Deleted"""
        records = []
        self.file.seek(0, os.SEEK_SET)
        while True:
            chunk = self.file.read(self.record_size)
            if len(chunk) < self.record_size:
                break
            try:
                records.append(self._unpack_record(chunk))
            except struct.error:
                pass
        return records

    def get_active_records(self) -> List[Dict[str, Any]]:
        return [r for r in self.get_all_records() if r.get('IsActive')]

    # ── เพิ่มใหม่: Auto-ID และ Search ─────────────────────────────────────────

    def get_next_id(self) -> int:
        """Auto-ID: หา max ID จากทุก record (Active+Deleted) + 1"""
        all_rec = self.get_all_records()
        return max((r['ID'] for r in all_rec), default=0) + 1

    def search_by_field(self, field_name: str, keyword: str) -> List[Dict[str, Any]]:
        """Substring search ใน Active records (case-insensitive)"""
        kw = keyword.lower()
        return [r for r in self.get_active_records()
                if kw in str(r.get(field_name, '')).lower()]

# ==============================================================================
# 3. Managers
# ==============================================================================

class CarManager(FileManager):
    def __init__(self):
        super().__init__(CAR_FORMAT, CAR_FORMAT_KEYS, CAR_FILE_NAME)

    def _pack_record(self, data: Dict[str, Any]) -> bytes:
        return struct.pack(
            self.format,
            data.get('IsActive', True),
            int(data['ID']),
            data['Model'].encode(self.encoding).ljust(30, b'\x00'),
            data['LicensePlate'].encode(self.encoding).ljust(10, b'\x00'),
            float(data['DailyRate']),
            bool(data.get('IsRented', False)),
            data.get('Category', 'Other').encode(self.encoding).ljust(15, b'\x00'),
        )

    def _unpack_record(self, chunk: bytes) -> Dict[str, Any]:
        u = struct.unpack(self.format, chunk)
        return {
            'IsActive':     u[0],
            'ID':           u[1],
            'Model':        u[2].split(b'\x00', 1)[0].decode(self.encoding, errors='ignore').strip(),
            'LicensePlate': u[3].split(b'\x00', 1)[0].decode(self.encoding, errors='ignore').strip(),
            'DailyRate':    u[4],
            'IsRented':     u[5],
            'Category':     u[6].split(b'\x00', 1)[0].decode(self.encoding, errors='ignore').strip(),
        }

    def get_available_cars(self) -> List[Dict[str, Any]]:
        return [c for c in self.get_active_records() if not c.get('IsRented')]

    def get_rented_cars(self) -> List[Dict[str, Any]]:
        return [c for c in self.get_active_records() if c.get('IsRented')]

class CustomerManager(FileManager):
    def __init__(self):
        super().__init__(CUSTOMER_FORMAT, CUSTOMER_FORMAT_KEYS, CUSTOMER_FILE_NAME)

    def _pack_record(self, data: Dict[str, Any]) -> bytes:
        return struct.pack(
            self.format,
            data.get('IsActive', True),
            int(data['ID']),
            data['Name'].encode(self.encoding).ljust(50, b'\x00'),
            data['Phone'].encode(self.encoding).ljust(15, b'\x00'),
            data.get('Email', '').encode(self.encoding).ljust(30, b'\x00'),
            int(data.get('Points', 0)),          # ← ใหม่
        )

    def _unpack_record(self, chunk: bytes) -> Dict[str, Any]:
        u = struct.unpack(self.format, chunk)
        return {
            'IsActive': u[0],
            'ID':       u[1],
            'Name':     u[2].split(b'\x00', 1)[0].decode(self.encoding, errors='ignore').strip(),
            'Phone':    u[3].split(b'\x00', 1)[0].decode(self.encoding, errors='ignore').strip(),
            'Email':    u[4].split(b'\x00', 1)[0].decode(self.encoding, errors='ignore').strip(),
            'Points':   u[5],                    # ← ใหม่
            'Tier':     get_tier(u[5]),           # ← derived, ไม่ได้เก็บในไฟล์
        }

    def add_points(self, cust_id: int, amount_thb: float) -> None:
        """บวก 1 point ต่อ 100 THB — อัปเดต binary record ทันที"""
        earned = int(amount_thb // 100)
        if earned <= 0:
            return
        result = self.get_record_by_id(cust_id)
        if result:
            rec, _ = result
            self.update_record(cust_id, {'Points': rec['Points'] + earned})
            print(f"  [Tier] +{earned} pts → รวม {rec['Points']+earned} pts"
                  f" ({get_tier(rec['Points']+earned)})")

class RentalManager(FileManager):
    def __init__(self):
        super().__init__(RENTAL_FORMAT, RENTAL_FORMAT_KEYS, RENTAL_FILE_NAME)

    def _pack_record(self, data: Dict[str, Any]) -> bytes:
        return struct.pack(
            self.format,
            data.get('IsActive', True),
            int(data['ID']),
            int(data['CustomerID']),
            int(data['CarID']),
            int(data['StartDate']),
            int(data.get('EndDate', 0)),
            float(data['TotalPrice']),
        )

    def _unpack_record(self, chunk: bytes) -> Dict[str, Any]:
        u = struct.unpack(self.format, chunk)
        return {
            'IsActive':   u[0],
            'ID':         u[1],
            'CustomerID': u[2],
            'CarID':      u[3],
            'StartDate':  u[4],
            'EndDate':    u[5],
            'TotalPrice': u[6],
        }

# ==============================================================================
# 4. Utility
# ==============================================================================

def get_user_choice(prompt: str, valid_choices: List[str]) -> str:
    while True:
        ch = input(prompt).strip().upper()
        if ch in valid_choices:
            return ch
        print("  !! ตัวเลือกไม่ถูกต้อง กรุณาเลือกใหม่ !!")

def get_user_confirmation(prompt: str) -> bool:
    """ถามยืนยัน Y/N — ป้องกัน Human Error"""
    while True:
        ans = input(f"  {prompt} (Y/N): ").strip().upper()
        if ans == 'Y':
            return True
        if ans == 'N':
            return False
        print("  !! กรุณาพิมพ์ Y หรือ N เท่านั้น !!")

def get_int_input(prompt: str) -> int:
    while True:
        try:
            return int(input(f"  {prompt}").strip())
        except ValueError:
            print("  !! กรุณาป้อนเฉพาะตัวเลขจำนวนเต็มเท่านั้น !!")

def get_float_input(prompt: str) -> float:
    while True:
        try:
            return float(input(f"  {prompt}").strip())
        except ValueError:
            print("  !! กรุณาป้อนเฉพาะตัวเลขเท่านั้น !!")

def get_date_input(prompt: str) -> int:
    while True:
        ds = input(f"  {prompt}").strip()
        if len(ds) == 8 and ds.isdigit():
            try:
                datetime.datetime.strptime(ds, '%d%m%Y')
                return int(ds)
            except ValueError:
                print("  !! รูปแบบวันที่ไม่ถูกต้อง (วัน/เดือน/ปี ไม่ถูกต้อง) !!")
        else:
            print("  !! กรุณาป้อนเป็น DDMMYYYY เช่น 25102025 !!")

def format_date_display(date_int: Union[int, float]) -> str:
    date_int = int(date_int)
    ds = str(date_int).zfill(8)
    if date_int == 0 or ds == '00000000':
        return 'N/A'
    try:
        return datetime.datetime.strptime(ds, '%d%m%Y').strftime('%d-%m-%Y')
    except ValueError:
        return 'Invalid'

def ascii_bar(value: int, max_value: int, width: int = 15) -> str:
    filled = round((value / max_value) * width) if max_value > 0 else 0
    return '[' + '|' * filled + ' ' * (width - filled) + ']'
    
def _pick_category() -> str:
    """เลือกประเภทรถจากรายการ"""
    print("  -- เลือกประเภทรถ --")
    for i, c in enumerate(CAR_CATEGORIES, 1):
        print(f"  [{i}] {c}")
    ch = get_user_choice("  >> ประเภท: ", [str(i) for i in range(1, len(CAR_CATEGORIES) + 1)])
    return CAR_CATEGORIES[int(ch) - 1]

def _auto_or_manual_id(manager: FileManager, label: str) -> Optional[int]:
    """Helper สำหรับ Auto-ID — คืน ID ที่เลือก หรือ None ถ้า ID ซ้ำ"""
    auto = manager.get_next_id()
    print(f"  (Auto-ID ถัดไปสำหรับ{label}: {auto})")
    if get_user_confirmation(f"ใช้ Auto-ID [{auto}]?"):
        return auto
    manual = get_int_input(f"ป้อน ID {label} เอง: ")
    if manager.get_record_by_id(manual) is not None:
        print(f"  !! Error: ID {manual} มีอยู่ในระบบแล้ว !!")
        return None
    return manual

def get_tier(points: int) -> str:
    for threshold, tier in TIER_TABLE:
        if points >= threshold:
            return tier

def is_car_available_for_period(
    rental_mgr: RentalManager,
    car_id: int,
    start_date: int,
    end_date: int
) -> bool:
    try:
        requested_start = datetime.datetime.strptime(
            str(start_date).zfill(8), '%d%m%Y'
        )
        requested_end = datetime.datetime.strptime(
            str(end_date).zfill(8), '%d%m%Y'
        )
    except ValueError:
        return False

    if requested_start > requested_end:
        return False

    for rental in rental_mgr.get_active_records():
        if rental['CarID'] != car_id:
            continue

        existing_start = datetime.datetime.strptime(
            str(rental['StartDate']).zfill(8), '%d%m%Y'
        )
        existing_end = datetime.datetime.strptime(
            str(rental['EndDate']).zfill(8), '%d%m%Y'
        )
        if requested_start <= existing_end and requested_end >= existing_start:
            return False
    return True

def get_car_bookings(rental_mgr: RentalManager, car_id: int) -> List[Dict[str, Any]]:
    """สัญญาที่ยังเปิดอยู่ (Active) ของรถคันนี้ เรียงตามวันเริ่ม"""
    bookings = [r for r in rental_mgr.get_active_records() if r['CarID'] == car_id]
    return sorted(bookings, key=lambda r: datetime.datetime.strptime(
        str(r['StartDate']).zfill(8), '%d%m%Y'))

def car_has_current_rental(rental_mgr: RentalManager, car_id: int) -> bool:
    """รถถูกเช่าอยู่ตอนนี้ไหม — มีสัญญา Active ที่เริ่มแล้ว (วันเริ่ม <= วันนี้)"""
    today = datetime.datetime.now()
    for r in get_car_bookings(rental_mgr, car_id):
        start = datetime.datetime.strptime(str(r['StartDate']).zfill(8), '%d%m%Y')
        if start <= today:
            return True
    return False

def sync_car_status(car_mgr: CarManager, rental_mgr: RentalManager) -> None:
    """ปรับ IsRented ของรถทุกคันให้ตรงกับสัญญา — การจองล่วงหน้าที่ถึงวันเริ่มแล้วจะกลายเป็น 'ถูกเช่า'"""
    for car in car_mgr.get_active_records():
        should_be = car_has_current_rental(rental_mgr, car['ID'])
        if bool(car.get('IsRented')) != should_be:
            car_mgr.update_record(car['ID'], {'IsRented': should_be})
            new_status = 'ถูกเช่า' if should_be else 'ว่าง'
            print(f"  [Sync] รถ ID {car['ID']} → '{new_status}'")

def get_customer_rental_history(
    rental_mgr: RentalManager,
    customer_id: int
) -> List[Dict[str, Any]]:
    return [
        rental
        for rental in rental_mgr.get_all_records()
        if rental['CustomerID'] == customer_id
    ]

def show_customer_rental_history(
    rental_mgr: RentalManager,
    customer_id: int
) -> None:
    history = get_customer_rental_history(rental_mgr, customer_id)

    if not history:
        print(f"  // ลูกค้า ID {customer_id} ไม่มีประวัติการเช่า \\")
        return

    print(f"\n  -- ประวัติการเช่าของลูกค้า ID {customer_id} --")

    for rental in history:
        status = "ACTIVE" if rental['IsActive'] else "CLOSED"

        print(
            f"  Rental #{rental['ID']:<5} "
            f"Car ID:{rental['CarID']:<4} "
            f"{format_date_display(rental['StartDate'])} -> "
            f"{format_date_display(rental['EndDate'])}  "
            f"{rental['TotalPrice']:>10,.2f} THB  "
            f"[{status}]"
        )

# ==============================================================================
# 4b. Member Tier System  (Feature 1 — no binary format change)
# ==============================================================================

TIER_TABLE = [
    (5000, 'Gold'),
    (1000, 'Silver'),
    (0,    'Bronze'),
]

TIER_CONFIG = {
    'GOLD':   (6, 0.10, '★★★ GOLD    — 10% discount'),
    'SILVER': (3, 0.05, '★★☆ SILVER  —  5% discount'),
    'BRONZE': (0, 0.00, '★☆☆ BRONZE  —  0% discount'),
}

def get_customer_tier(cust_id: int, rental_mgr: RentalManager) -> str:
    """
    Derive tier from LIFETIME rental count (Active + soft-deleted = history).
    Pure computation over existing records — zero binary format change.
    """
    lifetime = sum(
        1 for r in rental_mgr.get_all_records()
        if r.get('CustomerID') == cust_id
    )
    for tier, (threshold, _, _) in TIER_CONFIG.items():
        if lifetime >= threshold:
            return tier
    return 'BRONZE'

# ==============================================================================
# 4c. Receipt Generator  (Feature 2)
# ==============================================================================

RECEIPT_DIR = 'receipts'

def generate_rental_receipt(
    rental_data:  Dict[str, Any],
    cust_data:    Dict[str, Any],
    car_data:     Dict[str, Any],
    days:         int,
    tier:         str,
    discount_pct: float,
    gross_total:  float,
    final_total:  float,
) -> str:
    
    os.makedirs(RECEIPT_DIR, exist_ok=True)
    filepath = os.path.join(RECEIPT_DIR, f"receipt_R{rental_data['ID']:04d}.txt")

    _, _, tier_label = TIER_CONFIG[tier]
    discount_amt = round(gross_total - final_total, 2)
    border       = '═' * 52
    thin         = '─' * 52

    lines = [
        border,
        "           CAR RENTAL MANAGEMENT SYSTEM",
        "                 OFFICIAL RECEIPT",
        border,
        f"  Receipt No.  : R{rental_data['ID']:04d}",
        f"  Issued At    : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"  Storage      : Binary (.bin) | struct | Little-Endian",
        thin,
        "  CUSTOMER",
        f"    ID     : {cust_data['ID']}",
        f"    Name   : {cust_data['Name']}",
        f"    Phone  : {cust_data['Phone']}",
        f"    Email  : {cust_data.get('Email') or '-'}",
        f"    Tier   : {tier_label}",
        thin,
        "  VEHICLE",
        f"    ID       : {car_data['ID']}",
        f"    Model    : {car_data['Model']}",
        f"    Plate    : {car_data['LicensePlate']}",
        f"    Category : {car_data.get('Category', 'N/A')}",
        f"    Rate     : {car_data['DailyRate']:>10,.2f} THB/day",
        thin,
        "  RENTAL PERIOD",
        f"    From  : {format_date_display(rental_data['StartDate'])}",
        f"    To    : {format_date_display(rental_data['EndDate'])}",
        f"    Days  : {days}",
        thin,
        "  CHARGES",
        f"    Gross Total  : {gross_total:>10,.2f} THB",
        f"    Discount     : {discount_pct*100:>4.0f}%   -{discount_amt:>9,.2f} THB",
        f"    {'─'*40}",
        f"    AMOUNT DUE   : {final_total:>10,.2f} THB",
        border,
        "    Thank you for your rental najaaa :)    ",
        border,
        "",
    ]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return filepath

# ==============================================================================
# 5. Car Menu
# ==============================================================================

def run_car_menu(car_mgr: CarManager, rental_mgr: RentalManager):
    while True:
        print("\n" + "="*52)
        print("          [1] จัดการข้อมูลรถยนต์")
        print("="*52)
        print("  A: เพิ่มรถ (Auto-ID)    U: แก้ไข    D: ลบ (Soft)")
        print("  V: ดูทั้งหมด            S: ค้นหาด้วย ID")
        print("  F: ค้นหาด้วยรุ่น        T: กรองตามสถานะ")
        print("  X: กลับเมนูหลัก")
        ch = get_user_choice(">> กรุณาเลือก: ", ['A','U','D','V','S','F','T','X'])

        if   ch == 'A': _car_add(car_mgr)
        elif ch == 'U': _car_update(car_mgr)
        elif ch == 'D': _car_delete(car_mgr, rental_mgr)
        elif ch == 'V': _car_view_all(car_mgr)
        elif ch == 'S': _car_search_id(car_mgr)
        elif ch == 'F': _car_search_model(car_mgr)
        elif ch == 'T': _car_filter(car_mgr)
        elif ch == 'X': break

def _car_table_header():
    h = f"  {'ID':<5} {'รุ่นรถ':<32} {'ทะเบียน':<13} {'ประเภท':<11} {'THB/วัน':>10} {'สถานะ':<10}"
    sep = "  " + "-" * 78
    print(sep); print(h); print(sep)

def _car_table_row(car: Dict[str, Any]):
    status = "ถูกเช่า" if car.get('IsRented') else "ว่าง"
    print(f"  {car['ID']:<5} {car['Model'][:28]:<30} {car['LicensePlate']:<12} "
          f"{car.get('Category',''):<12} {car['DailyRate']:>10,.2f} {status:<10}")

def _car_add(mgr: CarManager):
    print("\n  -- เพิ่มรถยนต์ใหม่ --")
    car_id = _auto_or_manual_id(mgr, "รถยนต์")
    if car_id is None:
        return

    model    = input("  รุ่นรถยนต์ (สูงสุด 30 ตัวอักษร): ").strip()[:30]
    plate    = input("  ป้ายทะเบียน (สูงสุด 10 ตัวอักษร): ").strip()[:10]
    rate     = get_float_input("อัตราค่าเช่า/วัน (THB): ")
    category = _pick_category()

    # ── Preview ก่อน Confirm ───────────────────────────────────────────────
    print("\n  " + "="*46)
    print("     *** ยืนยันการเพิ่มรถยนต์ ***")
    print("  " + "="*46)
    print(f"  ID       : {car_id:<6}  ประเภท   : {category}")
    print(f"  รุ่น     : {model}")
    print(f"  ทะเบียน  : {plate:<10}  ค่าเช่า  : {rate:,.2f} THB/วัน")
    print("  " + "="*46)

    if get_user_confirmation("ยืนยันเพิ่มรถคันนี้?"):
        mgr.add_record({'ID': car_id, 'Model': model, 'LicensePlate': plate,
                        'DailyRate': rate, 'IsRented': False, 'Category': category})
        print(f"  || เพิ่มรถ ID {car_id} เรียบร้อย (สถานะ: ว่างให้เช่า) ||")
    else:
        print("  !! ยกเลิกการเพิ่มรถ !!")

def _car_update(mgr: CarManager):
    print("\n  -- แก้ไขรถยนต์ --")
    car_id = get_int_input("ID รถที่ต้องการแก้ไข: ")
    result = mgr.get_record_by_id(car_id)
    if not result:
        print(f"  // ไม่พบรถ ID {car_id} \\"); return

    car, _ = result
    new_data: Dict[str, Any] = {}

    nm = input(f"  รุ่นใหม่ (เดิม: {car['Model']}, Enter ถ้าไม่แก้): ").strip()[:30]
    if nm: new_data['Model'] = nm

    np_ = input(f"  ทะเบียนใหม่ (เดิม: {car['LicensePlate']}, Enter ถ้าไม่แก้): ").strip()[:10]
    if np_: new_data['LicensePlate'] = np_

    nr = input(f"  ค่าเช่า/วันใหม่ (เดิม: {car['DailyRate']:,.2f}, Enter ถ้าไม่แก้): ").strip()
    if nr:
        try:
            new_data['DailyRate'] = float(nr)
        except ValueError:
            print("  !! ค่าเช่าไม่ถูกต้อง !!"); return

    if get_user_confirmation(f"เปลี่ยนประเภท (เดิม: {car.get('Category','-')})?"):
        new_data['Category'] = _pick_category()

    if new_data:
        if get_user_confirmation(f"ยืนยันแก้ไขรถ ID {car_id}?"):
            mgr.update_record(car_id, new_data)
            print(f"  || แก้ไขรถ ID {car_id} เรียบร้อย ||")
    else:
        print("  !! ไม่มีการเปลี่ยนแปลง !!")

def _car_delete(mgr: CarManager, rental_mgr: RentalManager):
    print("\n  -- ลบรถยนต์ (Soft Delete) --")
    car_id = get_int_input("ID รถที่ต้องการลบ: ")
    result = mgr.get_record_by_id(car_id)
    if not result:
        print(f"  // ไม่พบรถ ID {car_id} \\"); return

    car, _ = result
    # ตรวจสอบว่ารถถูกเช่าอยู่หรือไม่ก่อนลบ
    if car.get('IsRented'):
        print(f"  // ไม่สามารถลบได้ รถ ID {car_id} ({car['Model']}) กำลังถูกเช่าอยู่ \\"); return

    # ตรวจสอบการจองล่วงหน้า — รถที่ยังมีสัญญาเปิดอยู่ ลบไม่ได้
    bookings = get_car_bookings(rental_mgr, car_id)
    if bookings:
        ids = ', '.join(f"#{r['ID']}" for r in bookings)
        print(f"  // ไม่สามารถลบได้ รถ ID {car_id} มีการจองที่ยังเปิดอยู่: {ids} \\")
        print(f"  // กรุณาปิดสัญญาเหล่านั้นก่อน (เมนู [3] → D) \\")
        return

    print(f"\n  รถที่จะลบ → ID {car_id} | {car['Model']} | {car['LicensePlate']} | {car.get('Category','')}")
    if get_user_confirmation("ยืนยันลบรถคันนี้?"):
        mgr.delete_record(car_id)
        print(f"  || ลบรถ ID {car_id} เรียบร้อย (Soft Deleted) ||")
    else:
        print("  !! ยกเลิกการลบ !!")

def _car_view_all(mgr: CarManager):
    print("\n  -- รายการรถยนต์ทั้งหมด (Active) --")
    cars = mgr.get_active_records()
    if not cars:
        print("  ไม่มีข้อมูลรถยนต์ที่ใช้งานอยู่"); return
    _car_table_header()
    for c in cars: _car_table_row(c)
    print("  " + "-"*78)
    av = sum(1 for c in cars if not c.get('IsRented'))
    print(f"  รวม {len(cars)} คัน  |  ว่าง: {av}  |  ถูกเช่า: {len(cars)-av}")

def _car_search_id(mgr: CarManager):
    print("\n  -- ค้นหารถด้วย ID --")
    car_id = get_int_input("ID รถ: ")
    result = mgr.get_record_by_id(car_id)
    if result:
        car, offset = result
        _car_table_header(); _car_table_row(car)
        print(f"  Offset : {offset} bytes")
    else:
        print("  // ไม่พบรถ ID นี้ หรือถูกลบไปแล้ว \\")

def _car_search_model(mgr: CarManager):
    """[ใหม่] ค้นหาด้วย substring ของรุ่นรถ"""
    print("\n  -- ค้นหารถด้วยรุ่น/ชื่อ --")
    kw = input("  คำค้นหา: ").strip()
    results = mgr.search_by_field('Model', kw)
    if not results:
        print("  // ไม่พบรถที่ตรงกับคำค้นหา \\"); return
    print(f"  พบ {len(results)} คัน:")
    _car_table_header()
    for c in results: _car_table_row(c)

def _car_filter(mgr: CarManager):
    """[ใหม่] กรองรถตามสถานะ"""
    print("\n  -- กรองรถตามสถานะ --")
    print("  [1] เฉพาะรถว่าง  [2] เฉพาะรถถูกเช่า  [3] ทั้งหมด (Active)")
    ch = get_user_choice("  >> เลือก: ", ['1', '2', '3'])
    if   ch == '1': cars, label = mgr.get_available_cars(), "รถว่าง"
    elif ch == '2': cars, label = mgr.get_rented_cars(),    "รถถูกเช่า"
    else:           cars, label = mgr.get_active_records(), "ทั้งหมด (Active)"

    print(f"\n  [{label}] — {len(cars)} คัน")
    if not cars:
        print("  ไม่มีรถในหมวดนี้"); return
    _car_table_header()
    for c in cars: _car_table_row(c)

# ==============================================================================
# 6. Customer Menu
# ==============================================================================

def run_customer_menu(cust_mgr: CustomerManager, rental_mgr: RentalManager):
    while True:
        print("\n" + "="*52)
        print("          [2] จัดการข้อมูลลูกค้า")
        print("="*52)
        print("  A: เพิ่มลูกค้า (Auto-ID)   U: แก้ไข    D: ลบ (Soft)")
        print("  V: ดูทั้งหมด               S: ค้นหาด้วย ID")
        print("  F: ค้นหาด้วยชื่อ")
        print("  X: กลับเมนูหลัก")
        ch = get_user_choice(">> กรุณาเลือก: ", ['A','U','D','V','S','F','X'])

        if   ch == 'A': _cust_add(cust_mgr)
        elif ch == 'U': _cust_update(cust_mgr)
        elif ch == 'D': _cust_delete(cust_mgr, rental_mgr)
        elif ch == 'V': _cust_view_all(cust_mgr)
        elif ch == 'S': _cust_search_id(cust_mgr)
        elif ch == 'F': _cust_search_name(cust_mgr)
        elif ch == 'X': break

def _cust_table_header():
    h = f"  {'ID':<5} {'ชื่อ-นามสกุล':<35} {'โทรศัพท์':<18} {'Email':<30}"
    sep = "  " + "-"*86
    print(sep); print(h); print(sep)

def _cust_table_row(c: Dict[str, Any]):
    print(f"  {c['ID']:<5} {c['Name'][:30]:<32} {c['Phone']:<16} {c.get('Email','')[:28]:<30}")

def _cust_add(mgr: CustomerManager):
    print("\n  -- เพิ่มลูกค้าใหม่ --")
    cust_id = _auto_or_manual_id(mgr, "ลูกค้า")
    if cust_id is None:
        return

    name  = input("  ชื่อ-นามสกุล (สูงสุด 50 ตัวอักษร): ").strip()[:50]
    phone = input("  เบอร์โทรศัพท์ (สูงสุด 15 หลัก): ").strip()[:15] # Phone Number
    if not validate_phone(phone):
        print("  !! เบอร์โทรศัพท์ไม่ถูกต้อง !!")
        return
    email = input("  อีเมล (สูงสุด 30 ตัวอักษร, Enter ถ้าไม่มี): ").strip()[:30] # Email
    if not validate_email(email):
        print("  !! รูปแบบอีเมลไม่ถูกต้อง !!")
        return
    
    # ── Preview ก่อน Confirm ───────────────────────────────────────────────
    print("\n  " + "="*46)
    print("     *** ยืนยันการเพิ่มลูกค้า ***")
    print("  " + "="*46)
    print(f"  ID    : {cust_id}")
    print(f"  ชื่อ  : {name}")
    print(f"  โทร   : {phone}    Email : {email or '-'}")
    print("  " + "="*46)

    if get_user_confirmation("ยืนยันเพิ่มลูกค้า?"):
        mgr.add_record({'ID': cust_id, 'Name': name, 'Phone': phone, 'Email': email})
        print(f"  || เพิ่มลูกค้า ID {cust_id} เรียบร้อย ||")
    else:
        print("  !! ยกเลิกการเพิ่มลูกค้า !!")

def _cust_update(mgr: CustomerManager):
    print("\n  -- แก้ไขลูกค้า --")
    cust_id = get_int_input("ID ลูกค้าที่ต้องการแก้ไข: ")
    result = mgr.get_record_by_id(cust_id)
    if not result:
        print(f"  // ไม่พบลูกค้า ID {cust_id} \\"); return

    cust, _ = result
    new_data: Dict[str, Any] = {}

    nn = input(f"  ชื่อใหม่ (เดิม: {cust['Name']}, Enter ถ้าไม่แก้): ").strip()[:50]
    if nn: new_data['Name'] = nn
    np_ = input(f"  โทรใหม่ (เดิม: {cust['Phone']}, Enter ถ้าไม่แก้): ").strip()[:15]
    if np_: new_data['Phone'] = np_
    ne = input(f"  Email ใหม่ (เดิม: {cust.get('Email','-')}, Enter ถ้าไม่แก้): ").strip()[:30]
    if ne: new_data['Email'] = ne

    if new_data:
        if get_user_confirmation(f"ยืนยันแก้ไขลูกค้า ID {cust_id}?"):
            mgr.update_record(cust_id, new_data)
            print(f"  || แก้ไขลูกค้า ID {cust_id} เรียบร้อย ||")
    else:
        print("  !! ไม่มีการเปลี่ยนแปลง !!")

def _cust_delete(mgr: CustomerManager, rental_mgr: RentalManager):
    """Soft-delete a customer — blocked if they have any open (Active) rental."""
    print("\n  -- ลบลูกค้า (Soft Delete) --")
    cust_id = get_int_input("ID ลูกค้าที่ต้องการลบ: ")
    result = mgr.get_record_by_id(cust_id)
    if not result:
        print(f"  // ไม่พบลูกค้า ID {cust_id} \\"); return
    cust, _ = result

    # ── Guard: block delete if customer has open rentals ──────────────────────
    open_rentals = [
        r for r in rental_mgr.get_active_records()
        if r['CustomerID'] == cust_id
    ]
    if open_rentals:
        ids = ', '.join(f"#{r['ID']}" for r in open_rentals)
        print(f"  // ไม่สามารถลบได้ ลูกค้า ID {cust_id} มีสัญญาเช่าที่ยังเปิดอยู่: {ids} \\")
        print(f"  // กรุณาปิดสัญญาเหล่านั้นก่อน (เมนู [3] → D) \\")
        return

    print(f"\n  ลูกค้าที่จะลบ → ID {cust_id} | {cust['Name']} | {cust['Phone']}")
    if get_user_confirmation("ยืนยันลบลูกค้า?"):
        mgr.delete_record(cust_id)
        print(f"  || ลบลูกค้า ID {cust_id} เรียบร้อย (Soft Deleted) ||")
    else:
        print("  !! ยกเลิกการลบ !!")

def _cust_view_all(mgr: CustomerManager):
    print("\n  -- รายชื่อลูกค้าทั้งหมด (Active) --")
    custs = mgr.get_active_records()
    if not custs:
        print("  ไม่มีข้อมูลลูกค้า"); return
    _cust_table_header()
    for c in custs: _cust_table_row(c)
    print("  " + "-"*86)
    print(f"  รวม {len(custs)} คน")

def _cust_search_id(mgr: CustomerManager):
    print("\n  -- ค้นหาลูกค้าด้วย ID --")
    cust_id = get_int_input("ID ลูกค้า: ")
    result = mgr.get_record_by_id(cust_id)
    if result:
        cust, offset = result
        _cust_table_header(); _cust_table_row(cust)
        print(f"  Offset : {offset} bytes")
    else:
        print("  // ไม่พบลูกค้า ID นี้ หรือถูกลบไปแล้ว \\")

def _cust_search_name(mgr: CustomerManager):
    """[ใหม่] ค้นหาด้วย substring ของชื่อ"""
    print("\n  -- ค้นหาลูกค้าด้วยชื่อ --")
    kw = input("  คำค้นหา: ").strip()
    results = mgr.search_by_field('Name', kw)
    if not results:
        print("  // ไม่พบลูกค้าที่ตรงกับคำค้นหา \\"); return
    print(f"  พบ {len(results)} คน:")
    _cust_table_header()
    for c in results: _cust_table_row(c)

def validate_phone(phone: str) -> bool:
    phone = phone.strip()
    return (
        phone.isdigit()
        and 9 <= len(phone) <= 15
    )

def validate_email(email: str) -> bool:
    email = email.strip()
    if email == '':
        return True
    if ' ' in email:
        return False
    if '@' not in email:
        return False
    local, domain = email.split('@', 1)
    if not local or not domain:
        return False
    if '.' not in domain:
        return False
    return True

# ==============================================================================
# 7. Rental Menu
# ==============================================================================

def run_rental_menu(rental_mgr: RentalManager, car_mgr: CarManager, cust_mgr: CustomerManager):
    while True:
        print("\n" + "="*52)
        print("          [3] จัดการสัญญาเช่า")
        print("="*52)
        print("  A: สร้างสัญญาเช่าใหม่")
        print("  V: ดูสัญญา Active ทั้งหมด")
        print("  S: ค้นหาสัญญาด้วย ID")
        print("  D: คืนรถ (ปิดสัญญา / Soft Delete)")
        print("  H: ดูประวัติการเช่าของลูกค้า")
        print("  X: กลับเมนูหลัก")
        ch = get_user_choice(">> กรุณาเลือก: ", ['A','V','S','D','H','X'])

        if   ch == 'A': _rental_create(rental_mgr, car_mgr, cust_mgr)
        elif ch == 'V': _rental_view_all(rental_mgr)
        elif ch == 'S': _rental_search(rental_mgr)
        elif ch == 'D': _rental_close(rental_mgr, car_mgr, cust_mgr)
        elif ch == 'H':
                    customer_id = get_int_input("ID ลูกค้า: ")
                    show_customer_rental_history(rental_mgr, customer_id)
        elif ch == 'X': break

def _rental_view_all(mgr: RentalManager):
    print("\n  -- สัญญาเช่า Active ทั้งหมด --")
    rentals = mgr.get_active_records()
    if not rentals:
        print("  ไม่มีสัญญาเช่าที่ใช้งานอยู่"); return
    h = f"  {'ID':<7} {'ลูกค้า ID':<12} {'รถ ID':<7} {'วันเริ่ม':<15} {'วันสิ้นสุด':<16} {'ราคารวม (THB)':>15}"
    sep = "  " + "-"*67
    print(sep); print(h); print(sep)
    for r in rentals:
        print(f"  #{r['ID']:<6} {r['CustomerID']:<10} {r['CarID']:<7} "
              f"{format_date_display(r['StartDate']):<12} "
              f"{format_date_display(r['EndDate']):<12} "
              f"{r['TotalPrice']:>15,.2f}")
    print(sep)
    total_rev = sum(r['TotalPrice'] for r in rentals)
    print(f"  รวม {len(rentals)} สัญญา  |  รายได้ Active รวม: {total_rev:,.2f} THB")

def _rental_search(mgr: RentalManager):
    print("\n  -- ค้นหาสัญญาด้วย ID --")
    rid = get_int_input("ID สัญญา: ")
    result = mgr.get_record_by_id(rid)
    if result:
        r, _ = result
        print(f"  สัญญา #{r['ID']}  ลูกค้า ID: {r['CustomerID']}  รถ ID: {r['CarID']}")
        print(f"  วันเริ่ม : {format_date_display(r['StartDate'])}    วันสิ้นสุด : {format_date_display(r['EndDate'])}")
        print(f"  ราคารวม  : {r['TotalPrice']:,.2f} THB")
    else:
        print("  // ไม่พบสัญญา ID นี้ หรือถูกปิดไปแล้ว \\")

def _rental_create(rental_mgr: RentalManager, car_mgr: CarManager, cust_mgr: CustomerManager):
    print("\n  -- สร้างสัญญาเช่าใหม่ --")

    # แสดงรถทั้งหมด (Active) พร้อมสถานะ — รถที่ถูกเช่าอยู่ยังจองล่วงหน้าได้
    cars = car_mgr.get_active_records()
    if not cars:
        print("  // ไม่มีรถในระบบ \\"); return

    print(f"\n  รถในระบบ ({len(cars)} คัน):")
    print(f"  {'ID':<5} {'รุ่น':<30} {'ทะเบียน':<12} {'ประเภท':<12} {'THB/วัน':>10}  {'สถานะ':<10}")
    print("  " + "-"*85)
    for car in cars:
        status = "ถูกเช่า" if car.get('IsRented') else "ว่าง"
        print(f"  {car['ID']:<5} {car['Model'][:28]:<30} {car['LicensePlate']:<12} "
              f"{car.get('Category',''):<12} {car['DailyRate']:>10,.2f}  {status:<10}")

    # Auto-ID สัญญา
    rental_id = _auto_or_manual_id(rental_mgr, "สัญญา")
    if rental_id is None:
        return

    # ลูกค้า
    cust_id = get_int_input("ID ลูกค้า: ")
    cust_result = cust_mgr.get_record_by_id(cust_id)
    if not cust_result:
        print("  // ID ลูกค้าไม่ถูกต้อง หรือถูกลบไปแล้ว \\"); return
    cust_data, _ = cust_result

    # รถ
    car_id = get_int_input("ID รถยนต์ที่ต้องการเช่า: ")
    car_result = car_mgr.get_record_by_id(car_id)
    if not car_result:
        print("  // ID รถยนต์ไม่ถูกต้อง หรือถูกลบไปแล้ว \\"); return
    car_data, _ = car_result

    # แสดงช่วงวันที่ถูกจองไว้แล้ว เพื่อให้เลือกวันที่ไม่ทับซ้อน
    bookings = get_car_bookings(rental_mgr, car_id)
    if car_data.get('IsRented'):
        print(f"  !! คำเตือน: ตอนนี้รถ ID {car_id} กำลังถูกเช่าอยู่ !!")
        print("  !! แต่ยังจองล่วงหน้าได้ ถ้าช่วงวันที่ไม่ทับซ้อนกับการจองเดิม !!")
    if bookings:
        print(f"  ช่วงวันที่ที่รถ ID {car_id} ถูกจองแล้ว:")
        for r in bookings:
            print(f"    สัญญา #{r['ID']:<5} {format_date_display(r['StartDate'])} -> "
                  f"{format_date_display(r['EndDate'])}")

    # วันที่
    start_int = get_date_input("วันที่เริ่มเช่า (DDMMYYYY): ")
    end_int   = get_date_input("วันที่สิ้นสุด  (DDMMYYYY): ")

    try:
        start_obj = datetime.datetime.strptime(
            str(start_int).zfill(8), '%d%m%Y'
        )
        end_obj = datetime.datetime.strptime(
            str(end_int).zfill(8), '%d%m%Y'
        )
        if start_obj > end_obj:
            print("  // วันเริ่มต้องไม่เกินวันสิ้นสุด \\")
            return
        if not is_car_available_for_period(
            rental_mgr, car_id, start_int, end_int
        ):
            print(
                f"  // รถ ID {car_id} มีการจอง/เช่าซ้อนในช่วงวันที่เลือก \\"
            )
            return
        days = (end_obj - start_obj).days + 1
        gross_total = car_data['DailyRate'] * days
    except ValueError:
        print("  // ข้อผิดพลาดในการคำนวณวันที่ \\")
        return

    # ── Tier discount ─────────────────────────────────────────────────────────
    tier          = get_customer_tier(cust_id, rental_mgr)
    _, disc_pct, tier_label = TIER_CONFIG[tier]
    discount_amt  = round(gross_total * disc_pct, 2)
    final_total   = round(gross_total - discount_amt, 2)

    # ── Summary before confirm ────────────────────────────────────────────────
    print("\n  " + "="*52)
    print("         ***  สรุปสัญญาเช่า  ***")
    print("  " + "="*52)
    print(f"  เลขสัญญา    : #{rental_id}")
    print(f"  ลูกค้า       : ID {cust_id} — {cust_data['Name']}")
    print(f"  เบอร์โทร     : {cust_data['Phone']}    Email: {cust_data.get('Email') or '-'}")
    print(f"  ระดับสมาชิก  : {tier_label}")
    print(f"  รถยนต์       : ID {car_id} — {car_data['Model']}")
    print(f"  ทะเบียน      : {car_data['LicensePlate']}    ประเภท: {car_data.get('Category','')}")
    print(f"  ค่าเช่า/วัน  : {car_data['DailyRate']:>10,.2f} THB")
    print(f"  วันเริ่ม     : {format_date_display(start_int)}")
    print(f"  วันสิ้นสุด   : {format_date_display(end_int)}")
    print(f"  จำนวนวัน    : {days} วัน")
    print("  " + "-"*52)
    print(f"  ราคาเต็ม     : {gross_total:>12,.2f} THB")
    print(f"  ส่วนลด {disc_pct*100:.0f}%    : -{discount_amt:>11,.2f} THB")
    print(f"  >>> ราคารวม  :  {final_total:>12,.2f} THB <<<")
    print("  " + "="*52)

    if get_user_confirmation("ยืนยันสร้างสัญญา?"):
        rental_record = {
            'ID': rental_id, 'CustomerID': cust_id, 'CarID': car_id,
            'StartDate': start_int, 'EndDate': end_int, 'TotalPrice': final_total,
        }
        rental_mgr.add_record(rental_record)
        # ตั้งสถานะ 'ถูกเช่า' เฉพาะเมื่อสัญญาเริ่มแล้ว — ถ้าเป็นการจองล่วงหน้า สถานะรถไม่เปลี่ยน
        if start_obj <= datetime.datetime.now():
            car_mgr.update_record(car_id, {'IsRented': True})
            print(f"  || สร้างสัญญา #{rental_id} และอัปเดตสถานะรถ ID {car_id} → 'ถูกเช่า' เรียบร้อย ||")
        else:
            print(f"  || จองล่วงหน้า #{rental_id} เรียบร้อย "
                  f"(เริ่ม {format_date_display(start_int)}) ||")

        # ── Auto receipt ──────────────────────────────────────────────────────
        receipt_path = generate_rental_receipt(
            rental_data  = rental_record,
            cust_data    = cust_data,
            car_data     = car_data,
            days         = days,
            tier         = tier,
            discount_pct = disc_pct,
            gross_total  = gross_total,
            final_total  = final_total,
        )
        print(f"  !! ใบเสร็จถูกสร้างที่: {receipt_path} !!")
    else:
        print("  !! ยกเลิกการสร้างสัญญา !!")

def _rental_close(rental_mgr: RentalManager, car_mgr: CarManager, cust_mgr: CustomerManager):
    print("\n  -- คืนรถ / ปิดสัญญา --")
    rid = get_int_input("ID สัญญาที่ต้องการปิด: ")
    result = rental_mgr.get_record_by_id(rid)
    if not result:
        print(f"  // ไม่พบสัญญา #{rid} หรือถูกปิดไปแล้ว \\"); return

    rent, _ = result
    print(f"\n  สัญญา #{rid}  ลูกค้า ID {rent['CustomerID']}  รถ ID {rent['CarID']}")
    print(f"  ราคา: {rent['TotalPrice']:,.2f} THB")

    if get_user_confirmation("ยืนยันคืนรถและปิดสัญญา?"):
        if rental_mgr.delete_record(rid):
            # รถอาจมีสัญญาอื่นที่เริ่มแล้วค้างอยู่ — คำนวณสถานะใหม่แทนการตั้ง False ตรง ๆ
            still_rented = car_has_current_rental(rental_mgr, rent['CarID'])
            car_mgr.update_record(rent['CarID'], {'IsRented': still_rented})
            new_status = 'ถูกเช่า' if still_rented else 'ว่าง'
            print(f"  || ปิดสัญญา #{rid} และอัปเดตสถานะรถ ID {rent['CarID']} → '{new_status}' เรียบร้อย ||")
            cust_mgr.add_points(rent['CustomerID'], rent['TotalPrice'])
    else:
        print("  !! ยกเลิกการคืนรถ !!")

# ==============================================================================
# 8. Report Helper Functions
# ==============================================================================

def _heading(a, title: str):
    """หัวข้อของแต่ละ Section — บรรทัดว่าง + ชื่อ + เส้นใต้"""
    a('')
    a(f'  {title}')
    a('  ' + '═' * _dw(title))

def _box_top(title: str = '') -> str:
    """เส้นบนสุดของ Box — ความกว้างรวม 82 chars"""
    if title:
        dashes = BIW - _dw(title) - 1
        return f"  ┌─ {title} {'─' * dashes}┐"
    return f"  ┌{'─' * (BIW + 2)}┐"

def _box_row(text: str) -> str:
    """แถวเนื้อหา Box — pad content ตาม display width"""
    return f"  │ {_pad(text, BIW)} │"

def _box_bot() -> str:
    """เส้นล่างสุดของ Box"""
    return f"  └{'─' * (BIW + 2)}┘"

def _table(a, cols: List[Tuple], rows: List[List[Any]]):
    """ตาราง: cols = [(ชื่อ, กว้าง) หรือ (ชื่อ, กว้าง, '>')] — ตัดข้อความที่ยาวเกินให้อัตโนมัติ"""
    def fmt(cells):
        return '  '.join(_pad(_trunc(str(v), c[1]), c[1], c[2] if len(c) > 2 else '<')
                         for v, c in zip(cells, cols))
    sep = '─' * (sum(c[1] for c in cols) + 2 * (len(cols) - 1))
    a('')
    a('  ' + fmt([c[0] for c in cols]))
    a('  ' + sep)
    for row in rows:
        a('  ' + fmt(row))
    if not rows:
        a('  (ไม่มีข้อมูล)')
    a('  ' + sep)

# ==============================================================================
# 9. Report Generator (Enhanced)
# ==============================================================================

def _char_width(ch: str) -> int:
    """Display cells for one character (0 for Thai combining marks)."""
    if _ud.category(ch) in ('Mn', 'Me', 'Cf'):   # non-spacing / combining
        return 0
    return 2 if _ud.east_asian_width(ch) in ('W', 'F') else 1

def _dw(s: str) -> int:
    """Total display width of string."""
    return sum(_char_width(c) for c in str(s))

def _pad(s: str, width: int, align: str = '<') -> str:
    """Cell-aware pad — replaces f'{s:<N}' / f'{s:>N}'."""
    s   = str(s)
    gap = max(0, width - _dw(s))
    return (s + ' ' * gap) if align == '<' else (' ' * gap + s)

def _trunc(s: str, max_cells: int) -> str:
    """Truncate to max_cells display cells — replaces s[:N] on Thai text."""
    out, w = '', 0
    for ch in s:
        cw = _char_width(ch)
        if w + cw > max_cells: break
        out += ch; w += cw
    return out

REPORT_FILES = {
    '1': ('detailed_summary_report.txt', 'Fleet Status & Overview'),
    '2': ('customer_report.txt',         'Customer Directory'),
    '3': ('rental_report.txt',           'Rental History'),
    '4': ('financial_report.txt',        'Financial Summary'),
}
FULL_REPORT_FILE = 'full_summary_report.txt'

# ไฟล์ binary ที่แต่ละรายงานดึงข้อมูลมาแสดง (แสดงที่หัวไฟล์ .txt)
REPORT_SOURCES = {
    '1': [CAR_FILE_NAME, CUSTOMER_FILE_NAME, RENTAL_FILE_NAME],  # ตารางรถ + ผู้เช่าปัจจุบัน + Overview
    '2': [CUSTOMER_FILE_NAME, RENTAL_FILE_NAME],                 # ลูกค้า + จำนวนครั้ง/ยอดเช่า
    '3': [RENTAL_FILE_NAME, CUSTOMER_FILE_NAME],                 # สัญญา + ชื่อลูกค้า
    '4': [RENTAL_FILE_NAME, CAR_FILE_NAME, CUSTOMER_FILE_NAME],  # รายได้ + ประเภท/รุ่นรถ + ชื่อลูกค้า
}

def _parse_date(date_int: int) -> Optional[datetime.datetime]:
    try:
        return datetime.datetime.strptime(str(date_int).zfill(8), '%d%m%Y')
    except ValueError:
        return None

def _rental_status(r: Dict[str, Any], now: datetime.datetime) -> str:
    """CLOSED / BOOKED (จองล่วงหน้า) / OVERDUE (เลยกำหนดคืน) / RENTING (กำลังเช่า)"""
    if not r['IsActive']:
        return 'CLOSED'
    start, end = _parse_date(r['StartDate']), _parse_date(r['EndDate'])
    if start and start > now:
        return 'BOOKED'
    if end and end.date() < now.date():   # วันสุดท้ายของสัญญายังไม่นับว่าเลยกำหนด
        return 'OVERDUE'
    return 'RENTING'

def _collect_report_data(
    car_mgr:    CarManager,
    cust_mgr:   CustomerManager,
    rental_mgr: RentalManager,
) -> Dict[str, Any]:
    """อ่านไฟล์ .bin ทั้ง 3 ครั้งเดียว แล้วคำนวณสถิติทั้งหมดที่ทุก Section ใช้"""
    all_cars    = car_mgr.get_all_records()    # cars.bin
    all_custs   = cust_mgr.get_all_records()   # customers.bin
    all_rentals = rental_mgr.get_all_records() # rentals.bin

    active_cars    = [c for c in all_cars    if c['IsActive']]
    active_custs   = [c for c in all_custs   if c['IsActive']]
    active_rentals = [r for r in all_rentals if r['IsActive']]
    closed_rentals = [r for r in all_rentals if not r['IsActive']]

    now = datetime.datetime.now()
    status_cnt = {'RENTING': 0, 'BOOKED': 0, 'OVERDUE': 0, 'CLOSED': 0}
    for r in all_rentals:
        status_cnt[_rental_status(r, now)] += 1

    # สัญญาปัจจุบันของรถแต่ละคัน (เริ่มแล้ว) — ไม่เอาการจองล่วงหน้ามาแสดงเป็นผู้เช่า
    rental_by_car: Dict[int, Dict] = {}
    for r in active_rentals:
        start = _parse_date(r['StartDate'])
        if start and start <= now:
            rental_by_car[r['CarID']] = r

    # ── สถิติต่อลูกค้า / ต่อรถ ───────────────────────────────────────────────
    cust_spend: Dict[int, float] = {}
    cust_cnt:   Dict[int, int]   = {}
    car_rent_cnt: Dict[int, int] = {}
    for r in all_rentals:
        cid = r['CustomerID']
        cust_spend[cid] = cust_spend.get(cid, 0.0) + r['TotalPrice']
        cust_cnt[cid]   = cust_cnt.get(cid,   0)   + 1
        car_rent_cnt[r['CarID']] = car_rent_cnt.get(r['CarID'], 0) + 1

    # ── Category breakdown ────────────────────────────────────────────────────
    cat_data: Dict[str, Dict[str, int]] = {}
    for c in active_cars:
        cat = c.get('Category') or 'Other'
        if cat not in cat_data:
            cat_data[cat] = {'total': 0, 'avail': 0, 'rented': 0}
        cat_data[cat]['total'] += 1
        if c.get('IsRented'): cat_data[cat]['rented'] += 1
        else:                 cat_data[cat]['avail']  += 1

    all_rev = sum(r['TotalPrice'] for r in all_rentals)
    rates   = [c['DailyRate'] for c in active_cars]

    return {
        'now': now,
        'all_cars': all_cars, 'all_custs': all_custs, 'all_rentals': all_rentals,
        'active_cars': active_cars, 'active_custs': active_custs,
        'active_rentals': active_rentals, 'closed_rentals': closed_rentals,
        'avail_cars':  [c for c in active_cars if not c.get('IsRented')],
        'rented_cars': [c for c in active_cars if     c.get('IsRented')],
        'active_car_by_id': {c['ID']: c for c in active_cars},
        'rental_by_car': rental_by_car,
        'status_cnt': status_cnt,
        'cust_spend': cust_spend, 'cust_cnt': cust_cnt, 'car_rent_cnt': car_rent_cnt,
        'cat_data': cat_data,
        # สถิติการเงิน
        'all_rev':  all_rev,
        'act_rev':  sum(r['TotalPrice'] for r in active_rentals),
        'cls_rev':  sum(r['TotalPrice'] for r in closed_rentals),
        'avg_rev':  all_rev / len(all_rentals) if all_rentals else 0.0,
        'max_rent': max(all_rentals, key=lambda r: r['TotalPrice'], default=None),
        # สถิติค่าเช่า
        'min_rate': min(rates) if rates else 0.0,
        'max_rate': max(rates) if rates else 0.0,
        'avg_rate': sum(rates) / len(rates) if rates else 0.0,
        # ขนาด record (ข้อมูลทางเทคนิค — แสดงเฉพาะในรายงานรวม)
        'car_size': car_mgr.record_size, 'cust_size': cust_mgr.record_size,
        'rent_size': rental_mgr.record_size,
    }

# ── Helper: ค้นหาชื่อในไฟล์ทั้งหมด (รวม Deleted) ─────────────────────────────

def _find_cust_name(d: Dict[str, Any], cid: int) -> str:
    for c in d['all_custs']:
        if c['ID'] == cid:
            return c['Name'] + ('' if c['IsActive'] else ' [DEL]')
    return f'ID {cid} (Unknown)'

def _find_car_model(d: Dict[str, Any], cid: int) -> str:
    for c in d['all_cars']:
        if c['ID'] == cid:
            return c['Model'] + ('' if c['IsActive'] else ' [DEL]')
    return f'ID {cid} (Unknown)'

# ── Overview (ข้อมูลสำคัญจากทุก Section — ใช้ในไฟล์ Section 1) ─────────────────

def _build_overview(a, d: Dict[str, Any]):
    sc = d['status_cnt']
    _heading(a, 'OVERVIEW')
    a(_box_top())
    a(_box_row(f"Cars      : {len(d['active_cars'])} active  "
               f"(Available {len(d['avail_cars'])} / Rented {len(d['rented_cars'])})"))
    a(_box_row(f"Customers : {len(d['active_custs'])} active"))
    a(_box_row(f"Rentals   : Renting {sc['RENTING']} / Booked {sc['BOOKED']} / "
               f"Overdue {sc['OVERDUE']} / Closed {sc['CLOSED']}"))
    a(_box_row(f"Revenue   : {d['all_rev']:,.2f} THB (All Time)"))
    a(_box_bot())
    a('  รายละเอียดเพิ่มเติม: ' + ', '.join(REPORT_FILES[k][0] for k in ('2', '3', '4')))

def _summary(a, rows: List[str], title: str = 'SUMMARY'):
    """กล่องสรุปท้ายแต่ละ Section"""
    a('')
    a(_box_top(title))
    for r in rows:
        a(_box_row(r))
    a(_box_bot())

def _tier_from_count(n: int) -> str:
    """ระดับสมาชิกจากจำนวนสัญญา — เกณฑ์เดียวกับ get_customer_tier"""
    for tier, (threshold, _, _) in TIER_CONFIG.items():
        if n >= threshold:
            return tier
    return 'BRONZE'

# ── SECTION 1 : FLEET STATUS ──────────────────────────────────────────────────

def _build_fleet_section(a, d: Dict[str, Any]):
    _heading(a, 'FLEET STATUS')

    rows = []
    for car in sorted(d['all_cars'], key=lambda c: not c['IsActive']):
        renter = s_d = e_d = '-'
        if not car['IsActive']:
            status = 'DELETED'
        elif car.get('IsRented'):
            status = 'RENTED'
            rent   = d['rental_by_car'].get(car['ID'])
            if rent:
                renter = rent['CustomerID']
                s_d    = format_date_display(rent['StartDate'])
                e_d    = format_date_display(rent['EndDate'])
        else:
            status = 'AVAILABLE'
        rows.append([status, car['ID'], car.get('Category', ''), car['Model'],
                     car['LicensePlate'], f"{car['DailyRate']:,.2f}", renter, s_d, e_d])
    _table(a, [('Status', 9), ('ID', 4), ('Category', 9), ('Model', 28),
               ('Plate', 10), ('THB/day', 10, '>'), ('Renter', 6),
               ('From', 10), ('To', 10)], rows)

    # ── สรุปท้ายไฟล์ ──
    n_active, n_rented = len(d['active_cars']), len(d['rented_cars'])
    util = n_rented / n_active * 100 if n_active else 0
    rented_income = sum(c['DailyRate'] for c in d['rented_cars'])
    _summary(a, [
        f"Total cars      : {len(d['all_cars'])}  (Active {n_active} / Deleted {len(d['all_cars']) - n_active})",
        f"Available       : {len(d['avail_cars'])}    Rented : {n_rented}    Utilization : {util:.0f}%",
        f"Daily rate      : Min {d['min_rate']:,.2f} / Max {d['max_rate']:,.2f} / Avg {d['avg_rate']:,.2f} THB",
        f"Rented income   : {rented_income:,.2f} THB/day (from cars currently rented)",
    ])
    a('  Fleet by Category  (bar = % rented)')
    if d['cat_data']:
        for cat, v in sorted(d['cat_data'].items()):
            pct = v['rented'] / v['total'] * 100 if v['total'] else 0
            a(f"    {cat:<10} {ascii_bar(v['rented'], v['total'], 10)} {pct:>4.0f}%  "
              f"({v['rented']}/{v['total']} rented)")
    else:
        a('    No active cars.')

# ── SECTION 2 : CUSTOMER DIRECTORY ────────────────────────────────────────────

def _build_customer_section(a, d: Dict[str, Any]):
    _heading(a, 'CUSTOMER DIRECTORY')

    rows = []
    for c in sorted(d['all_custs'], key=lambda c: not c['IsActive']):
        rows.append(['ACTIVE' if c['IsActive'] else 'DELETED', c['ID'], c['Name'],
                     c['Phone'], c.get('Email') or '-', d['cust_cnt'].get(c['ID'], 0),
                     f"{d['cust_spend'].get(c['ID'], 0.0):,.2f}"])
    _table(a, [('Status', 7), ('ID', 4), ('Name', 28), ('Phone', 15),
               ('Email', 28), ('Rentals', 7, '>'), ('Spent THB', 12, '>')], rows)

    # ── สรุปท้ายไฟล์ ──
    active = d['active_custs']
    renters = [c for c in active if d['cust_cnt'].get(c['ID'], 0) > 0]
    total_spent = sum(d['cust_spend'].get(c['ID'], 0.0) for c in active)
    avg_spent = total_spent / len(renters) if renters else 0.0
    tiers = {t: 0 for t in TIER_CONFIG}
    for c in active:
        tiers[_tier_from_count(d['cust_cnt'].get(c['ID'], 0))] += 1
    top = max(active, key=lambda c: d['cust_spend'].get(c['ID'], 0.0), default=None)
    summary = [
        f"Total customers : {len(d['all_custs'])}  (Active {len(active)} / Deleted {len(d['all_custs']) - len(active)})",
        f"Have rented     : {len(renters)}    Never rented : {len(active) - len(renters)}",
        f"Total spent     : {total_spent:,.2f} THB    Avg per renter : {avg_spent:,.2f} THB",
        f"Member tiers    : Gold {tiers['GOLD']} / Silver {tiers['SILVER']} / Bronze {tiers['BRONZE']}",
    ]
    if top and d['cust_spend'].get(top['ID'], 0.0) > 0:
        summary.append(f"Top spender     : {_trunc(top['Name'], 30)} ({d['cust_spend'][top['ID']]:,.2f} THB)")
    _summary(a, summary)

# ── SECTION 3 : RENTAL HISTORY ────────────────────────────────────────────────

def _build_rental_section(a, d: Dict[str, Any]):
    sc = d['status_cnt']
    _heading(a, 'RENTAL HISTORY')
    a('  RENTING = กำลังเช่า   BOOKED = จองล่วงหน้า   OVERDUE = เลยกำหนดคืน   CLOSED = คืนแล้ว')

    rows = []
    for r in sorted(d['all_rentals'], key=lambda r: not r['IsActive']):
        rows.append([_rental_status(r, d['now']), f"#{r['ID']}", r['CarID'],
                     _find_cust_name(d, r['CustomerID']),
                     format_date_display(r['StartDate']), format_date_display(r['EndDate']),
                     f"{r['TotalPrice']:,.2f}"])
    _table(a, [('Status', 7), ('Rental', 6), ('Car', 4), ('Customer', 26),
               ('From', 10), ('To', 10), ('Total THB', 12, '>')], rows)

    # ── สรุปท้ายไฟล์ ──
    days = []
    for r in d['all_rentals']:
        s, e = _parse_date(r['StartDate']), _parse_date(r['EndDate'])
        if s and e:
            days.append((e - s).days + 1)
    avg_days = sum(days) / len(days) if days else 0
    _summary(a, [
        f"Total rentals   : {len(d['all_rentals'])}  (Open {len(d['active_rentals'])} / Closed {len(d['closed_rentals'])})",
        f"By status       : Renting {sc['RENTING']} / Booked {sc['BOOKED']} / Overdue {sc['OVERDUE']} / Closed {sc['CLOSED']}",
        f"Total value     : {d['all_rev']:,.2f} THB  (Open {d['act_rev']:,.2f} / Closed {d['cls_rev']:,.2f})",
        f"Average length  : {avg_days:.1f} days per rental",
    ])
    overdue = [r for r in d['active_rentals'] if _rental_status(r, d['now']) == 'OVERDUE']
    if overdue:
        a('  !! Overdue !!')
        for r in overdue:
            a(f"    Rental #{r['ID']:<4} Car {r['CarID']:<4} {_trunc(_find_cust_name(d, r['CustomerID']), 26)}"
              f"  (due {format_date_display(r['EndDate'])})")

# ── SECTION 4 : FINANCIAL SUMMARY ─────────────────────────────────────────────

def _build_financial_section(a, d: Dict[str, Any]):
    _heading(a, 'FINANCIAL SUMMARY')

    # ── ตาราง: รายได้แยกตามประเภทรถ ──
    cat_of: Dict[int, str] = {}
    for c in d['all_cars']:   # รถที่ใช้งานอยู่มีสิทธิ์ก่อน ถ้า ID ซ้ำกับรถที่ถูกลบ
        if c['IsActive'] or c['ID'] not in cat_of:
            cat_of[c['ID']] = c.get('Category') or 'Other'
    by_cat: Dict[str, List[float]] = {}
    for r in d['all_rentals']:
        cat = cat_of.get(r['CarID'], 'Unknown')
        by_cat.setdefault(cat, []).append(r['TotalPrice'])
    rows = []
    for cat, prices in sorted(by_cat.items(), key=lambda x: sum(x[1]), reverse=True):
        share = sum(prices) / d['all_rev'] * 100 if d['all_rev'] else 0
        rows.append([cat, len(prices), f"{sum(prices):,.2f}", f"{share:.1f}%"])
    if rows:
        rows.append(['TOTAL', len(d['all_rentals']), f"{d['all_rev']:,.2f}", '100.0%'])
    a('  Revenue by Car Category')
    _table(a, [('Category', 12), ('Rentals', 7, '>'), ('Revenue THB', 14, '>'), ('Share', 7, '>')], rows)

    # ── สรุปท้ายไฟล์ ──
    a('')
    a(_box_top('REVENUE (THB)'))
    a(_box_row(f"All Time            : {d['all_rev']:>14,.2f}"))
    a(_box_row(f"  - Open rentals    : {d['act_rev']:>14,.2f}"))
    a(_box_row(f"  - Closed rentals  : {d['cls_rev']:>14,.2f}"))
    a(_box_row(f"Average per Rental  : {d['avg_rev']:>14,.2f}"))
    max_rent = d['max_rent']
    if max_rent:
        a(_box_row(f"Highest Rental      : {max_rent['TotalPrice']:>14,.2f}  (Rental #{max_rent['ID']})"))
    a(_box_bot())

    a(_box_top('TOP 3 CUSTOMERS'))
    top3_custs = sorted(d['cust_spend'].items(), key=lambda x: x[1], reverse=True)[:3]
    if top3_custs:
        for rank, (cid, total) in enumerate(top3_custs, 1):
            cnt = d['cust_cnt'].get(cid, 0)
            a(_box_row(f"{rank}. {_pad(_trunc(_find_cust_name(d, cid), 30), 30)}  "
                       f"{_pad(f'{total:,.2f} THB', 16, '>')}  ({cnt} rental{'s' if cnt != 1 else ''})"))
    else:
        a(_box_row('No rental data available.'))
    a(_box_bot())

    a(_box_top('TOP 3 MOST RENTED CARS'))
    top3_cars = sorted(d['car_rent_cnt'].items(), key=lambda x: x[1], reverse=True)[:3]
    if top3_cars:
        for rank, (cid, cnt) in enumerate(top3_cars, 1):
            car    = d['active_car_by_id'].get(cid)
            c_stat = ('Rented' if car.get('IsRented') else 'Available') if car else 'Deleted'
            a(_box_row(f"{rank}. {_pad(_trunc(_find_car_model(d, cid), 30), 30)}  "
                       f"{_pad(cnt, 3, '>')} rental{'s' if cnt != 1 else ''}  ({c_stat})"))
    else:
        a(_box_row('No rental data available.'))
    a(_box_bot())

SECTION_BUILDERS = {
    '1': _build_fleet_section,
    '2': _build_customer_section,
    '3': _build_rental_section,
    '4': _build_financial_section,
}

# ── เขียนไฟล์รายงาน ───────────────────────────────────────────────────────────

def _write_report(d: Dict[str, Any], filename: str, title: str, sections: List[str],
                  with_overview: bool = False, with_tech: bool = False,
                  sources: Optional[List[str]] = None) -> bool:
    body: List[str] = []
    a = body.append
    if with_overview:
        _build_overview(a, d)
    for key in sections:
        SECTION_BUILDERS[key](a, d)

    # เส้นหัว/ท้ายกว้างเท่าบรรทัดที่ยาวที่สุดในรายงาน
    width = max(max((_dw(l) for l in body), default=0), 60)
    lines = [
        '=' * width,
        f"  CAR RENTAL MANAGEMENT SYSTEM  —  {title}",
        f"  Generated : {d['now'].strftime('%Y-%m-%d %H:%M:%S')}",
        f"  Data from : {', '.join(sources or [CAR_FILE_NAME, CUSTOMER_FILE_NAME, RENTAL_FILE_NAME])}",
        '=' * width,
    ] + body + ['', '=' * width]
    if with_tech:
        lines.append(f"  Binary Files : Cars={len(d['all_cars'])} rec × {d['car_size']}B"
                     f"  |  Customers={len(d['all_custs'])} rec × {d['cust_size']}B"
                     f"  |  Rentals={len(d['all_rentals'])} rec × {d['rent_size']}B"
                     f"  (UTF-8, Little-Endian)")
    lines += ['  END OF REPORT', '=' * width]

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n')
        print(f"  !! สร้างรายงานสำเร็จที่ '{filename}' !!")
        return True
    except IOError as e:
        print(f"  // Error writing report '{filename}': {e} \\")
        return False

def generate_section_report(car_mgr: CarManager, cust_mgr: CustomerManager,
                            rental_mgr: RentalManager, key: str,
                            d: Optional[Dict[str, Any]] = None) -> bool:
    """สร้างรายงานแยกของ Section เดียว (key = '1'..'4')"""
    if d is None:
        d = _collect_report_data(car_mgr, cust_mgr, rental_mgr)
    filename, title = REPORT_FILES[key]
    # ไฟล์ Section 1 เป็นไฟล์สรุปหลัก — ใส่ภาพรวมจาก Section อื่นไว้ด้วย
    return _write_report(d, filename, title, [key], with_overview=(key == '1'),
                         sources=REPORT_SOURCES[key])

def generate_full_report(car_mgr: CarManager, cust_mgr: CustomerManager,
                         rental_mgr: RentalManager,
                         report_filename: str = FULL_REPORT_FILE) -> bool:
    """รายงานรวมทุก Section ในไฟล์เดียว (มีข้อมูลทางเทคนิคของไฟล์ Binary ด้วย)"""
    d = _collect_report_data(car_mgr, cust_mgr, rental_mgr)
    return _write_report(d, report_filename, 'Full Summary Report',
                         ['1', '2', '3', '4'], with_overview=True, with_tech=True)

def run_report_menu(car_mgr: CarManager, cust_mgr: CustomerManager, rental_mgr: RentalManager):
    while True:
        print("\n" + "="*52)
        print("          [R] สร้างรายงาน (.txt)")
        print("="*52)
        for key, (fname, title) in REPORT_FILES.items():
            print(f"  {key}: {title:<24} → {fname}")
        print(f"  A: สร้างทั้ง 4 ไฟล์ข้างบน")
        print(f"  F: รายงานรวมทุก Section ไฟล์เดียว → {FULL_REPORT_FILE}")
        print("  X: กลับเมนูหลัก")
        ch = get_user_choice(">> กรุณาเลือก: ", ['1', '2', '3', '4', 'A', 'F', 'X'])

        if ch in REPORT_FILES:
            generate_section_report(car_mgr, cust_mgr, rental_mgr, ch)
        elif ch == 'A':
            d = _collect_report_data(car_mgr, cust_mgr, rental_mgr)
            for key in REPORT_FILES:
                generate_section_report(car_mgr, cust_mgr, rental_mgr, key, d)
        elif ch == 'F':
            generate_full_report(car_mgr, cust_mgr, rental_mgr)
        elif ch == 'X':
            break

# ==============================================================================
# 10. Main
# ==============================================================================

def main():
    print("="*52)
    print("   ยินดีต้อนรับสู่ระบบจัดการเช่ารถยนต์")
    print("="*52)
    car_mgr    = CarManager()
    cust_mgr   = CustomerManager()
    rental_mgr = RentalManager()
    sync_car_status(car_mgr, rental_mgr)

    try:
        while True:
            print("\n" + "="*52)
            print("       ระบบจัดการเช่ารถยนต์  (MAIN MENU)")
            print("="*52)
            print("  [1] จัดการข้อมูลรถยนต์")
            print("  [2] จัดการข้อมูลลูกค้า")
            print("  [3] จัดการสัญญาเช่า")
            print("  [R] สร้างรายงาน (.txt) — เลือกได้ทีละ Section")
            print("  [X] ออกจากระบบ")

            ch = get_user_choice(">> กรุณาเลือกเมนู: ", ['1', '2', '3', 'R', 'X'])

            if   ch == '1': run_car_menu(car_mgr, rental_mgr)
            elif ch == '2': run_customer_menu(cust_mgr, rental_mgr)
            elif ch == '3': run_rental_menu(rental_mgr, car_mgr, cust_mgr)
            elif ch == 'R': run_report_menu(car_mgr, cust_mgr, rental_mgr)
            elif ch == 'X':
                print("\n" + "="*52)
                print("  กำลังปิดระบบอย่างปลอดภัย...")
                print("="*52)
                generate_full_report(
                    car_mgr, cust_mgr, rental_mgr,
                    report_filename='final_exit_summary.txt'
                )
                print("  || ปิดโปรแกรมเรียบร้อยแล้ว ||")
                break

    except Exception as e:
        print(f"\n  // เกิดข้อผิดพลาดร้ายแรง: {e} \\")
        traceback.print_exc()

    finally:
        print("  !! บันทึกและซิงค์ข้อมูลทั้งหมด !!")
        car_mgr.close()
        cust_mgr.close()
        rental_mgr.close()

if __name__ == '__main__':
    main()
