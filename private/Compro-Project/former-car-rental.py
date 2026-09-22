import struct
import os
import datetime
import traceback
import unicodedata as _ud
from typing import Dict, Any, Tuple, Optional, List, Union

# ==============================================================================
# 1. Constants สำหรับ 3 Entities
# ==============================================================================

# Car: IsActive(1)+ID(4)+Model(30)+Plate(10)+Rate(4)+IsRented(1)+Category(15) = 65 bytes
CAR_FORMAT      = '<?i30s10sf?15s'
CAR_FORMAT_KEYS = ['IsActive', 'ID', 'Model', 'LicensePlate', 'DailyRate', 'IsRented', 'Category']
CAR_FILE_NAME   = 'cars.bin'
CAR_ENCODING    = 'utf-8'
CAR_CATEGORIES  = ['Sedan', 'SUV', 'Pickup', 'Van', 'Hatchback', 'Sport', 'Other']

# Customer: IsActive(1)+ID(4)+Name(50)+Phone(15)+Email(30) = 100 bytes
CUSTOMER_FORMAT      = '<?i50s15s30sI'
CUSTOMER_FORMAT_KEYS = ['IsActive', 'ID', 'Name', 'Phone', 'Email', 'Points']
CUSTOMER_FILE_NAME   = 'customers.bin'
CUSTOMER_ENCODING    = 'utf-8'

# Rental: IsActive(1)+ID(4)+CustID(4)+CarID(4)+Start(4)+End(4)+Price(8) = 29 bytes  (unchanged)
RENTAL_FORMAT      = '<?iiiiid'
RENTAL_FORMAT_KEYS = ['IsActive', 'ID', 'CustomerID', 'CarID', 'StartDate', 'EndDate', 'TotalPrice']
RENTAL_FILE_NAME   = 'rentals.bin'
RENTAL_ENCODING    = 'utf-8'

# Report layout constants
W   = 160   # รายงาน: ความกว้างหลัก (ruler / section header)
BIW = 76    # รายงาน: ความกว้างภายใน Box (box inner width)
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
# 3. Concrete Managers
# ==============================================================================

class CarManager(FileManager):
    def __init__(self):
        super().__init__(CAR_FORMAT, CAR_FORMAT_KEYS, CAR_FILE_NAME, CAR_ENCODING)

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
        super().__init__(CUSTOMER_FORMAT, CUSTOMER_FORMAT_KEYS,
                         CUSTOMER_FILE_NAME, CUSTOMER_ENCODING)

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
        super().__init__(RENTAL_FORMAT, RENTAL_FORMAT_KEYS, RENTAL_FILE_NAME, RENTAL_ENCODING)

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
# 4. Utility Functions
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

def get_car_rental_history(
    rental_mgr: RentalManager,
    car_id: int
) -> List[Dict[str, Any]]:
    return [
        rental
        for rental in rental_mgr.get_all_records()
        if rental['CarID'] == car_id
    ]

def show_car_rental_history(
    rental_mgr: RentalManager,
    car_id: int
) -> None:
    history = get_car_rental_history(rental_mgr, car_id)
    if not history:
        print(f"  // รถ ID {car_id} ไม่มีประวัติการเช่า \\")
        return
    print(f"\n  -- ประวัติการเช่าของรถ ID {car_id} --")
    for rental in history:
        status = "ACTIVE" if rental['IsActive'] else "CLOSED"
        print(
            f"  Rental #{rental['ID']:<5} "
            f"Customer ID:{rental['CustomerID']:<4} "
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
        "      CAR RENTAL MANAGEMENT SYSTEM",
        "              OFFICIAL RECEIPT",
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

def run_car_menu(car_mgr: CarManager):
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
        elif ch == 'D': _car_delete(car_mgr)
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

def _car_delete(mgr: CarManager):
    print("\n  -- ลบรถยนต์ (Soft Delete) --")
    car_id = get_int_input("ID รถที่ต้องการลบ: ")
    result = mgr.get_record_by_id(car_id)
    if not result:
        print(f"  // ไม่พบรถ ID {car_id} \\"); return

    car, _ = result
    # ตรวจสอบว่ารถถูกเช่าอยู่หรือไม่ก่อนลบ
    if car.get('IsRented'):
        print(f"  // ไม่สามารถลบได้ รถ ID {car_id} ({car['Model']}) กำลังถูกเช่าอยู่ \\"); return

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

def validate_date_range(start_date: int, end_date: int) -> bool:
    try:
        start_obj = datetime.datetime.strptime(
            str(start_date).zfill(8), '%d%m%Y'
        )
        end_obj = datetime.datetime.strptime(
            str(end_date).zfill(8), '%d%m%Y'
        )
        return start_obj <= end_obj
    except ValueError:
        return False

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

    # [ใหม่] แสดงรายการรถว่างก่อนเสมอ
    avail = car_mgr.get_available_cars()
    if not avail:
        print("  // ไม่มีรถว่างในขณะนี้ \\"); return

    print(f"\n  รถว่างในระบบ ({len(avail)} คัน):")
    print(f"  {'ID':<5} {'รุ่น':<30} {'ทะเบียน':<12} {'ประเภท':<12} {'THB/วัน':>10}")
    print("  " + "-"*73)
    for car in avail:
        print(f"  {car['ID']:<5} {car['Model'][:28]:<30} {car['LicensePlate']:<12} "
              f"{car.get('Category',''):<12} {car['DailyRate']:>10,.2f}")

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
    if car_data.get('IsRented'):
        print(f"  // รถ ID {car_id} ถูกเช่าอยู่แล้ว \\"); return

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
        car_mgr.update_record(car_id, {'IsRented': True})
        print(f"  || สร้างสัญญา #{rental_id} และอัปเดตสถานะรถ ID {car_id} → 'ถูกเช่า' เรียบร้อย ||")

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
            car_mgr.update_record(rent['CarID'], {'IsRented': False})
            print(f"  || ปิดสัญญา #{rid} และอัปเดตสถานะรถ ID {rent['CarID']} → 'ว่าง' เรียบร้อย ||")
            cust_mgr.add_points(rent['CustomerID'], rent['TotalPrice'])
    else:
        print("  !! ยกเลิกการคืนรถ !!")

# ==============================================================================
# 8. Report Helper Functions
# ==============================================================================

def _ruler(char: str = '=') -> str:
    return char * W

def _section(title: str) -> str:
    """Section header กึ่งกลาง ความกว้าง W"""
    inner = f'[ {title} ]'
    pad   = (W - len(inner)) // 2
    return '=' * pad + inner + '=' * (W - pad - len(inner))

def _box_top(title: str = '') -> str:
    """เส้นบนสุดของ Box — ความกว้างรวม 82 chars"""
    if title:
        dashes = BIW - len(title) - 1   # 75 - len(title)
        return f"  ┌─ {title} {'─' * dashes}┐"
    return f"  ┌{'─' * (BIW + 2)}┐"

def _box_row(text: str) -> str:
    """แถวเนื้อหา Box — pad content ตาม display width"""
    return f"  │ {_pad(text, BIW)} │"

def _box_bot() -> str:
    """เส้นล่างสุดของ Box"""
    return f"  └{'─' * (BIW + 2)}┘"

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

def generate_detailed_summary_report(
    car_mgr:    CarManager,
    cust_mgr:   CustomerManager,
    rental_mgr: RentalManager,
    report_filename: str = 'detailed_summary_report.txt'
):
    # ── รวบรวมข้อมูลทั้งหมด ──────────────────────────────────────────────────
    all_cars    = car_mgr.get_all_records()
    all_custs   = cust_mgr.get_all_records()
    all_rentals = rental_mgr.get_all_records()

    active_cars    = [c for c in all_cars    if c['IsActive']]
    active_custs   = [c for c in all_custs   if c['IsActive']]
    active_rentals = [r for r in all_rentals if r['IsActive']]
    closed_rentals = [r for r in all_rentals if not r['IsActive']]

    avail_cars  = [c for c in active_cars if not c.get('IsRented')]
    rented_cars = [c for c in active_cars if     c.get('IsRented')]

    rental_by_car: Dict[int, Dict] = {r['CarID']: r for r in active_rentals}

    # ── สถิติการเงิน ──────────────────────────────────────────────────────────
    all_rev  = sum(r['TotalPrice'] for r in all_rentals)
    act_rev  = sum(r['TotalPrice'] for r in active_rentals)
    cls_rev  = sum(r['TotalPrice'] for r in closed_rentals)
    avg_rev  = all_rev / len(all_rentals) if all_rentals else 0.0
    max_rent = max(all_rentals, key=lambda r: r['TotalPrice'], default=None)

    # ── สถิติต่อลูกค้า / ต่อรถ ───────────────────────────────────────────────
    cust_spend: Dict[int, float] = {}
    cust_cnt:   Dict[int, int]   = {}
    for r in all_rentals:
        cid = r['CustomerID']
        cust_spend[cid] = cust_spend.get(cid, 0.0) + r['TotalPrice']
        cust_cnt[cid]   = cust_cnt.get(cid,   0)   + 1

    car_rent_cnt: Dict[int, int] = {}
    for r in all_rentals:
        car_rent_cnt[r['CarID']] = car_rent_cnt.get(r['CarID'], 0) + 1

    # ── สถิติค่าเช่า ──────────────────────────────────────────────────────────
    rates    = [c['DailyRate'] for c in active_cars]
    min_rate = min(rates) if rates else 0.0
    max_rate = max(rates) if rates else 0.0
    avg_rate = sum(rates) / len(rates) if rates else 0.0

    # ── Category breakdown ────────────────────────────────────────────────────
    cat_data: Dict[str, Dict[str, int]] = {}
    for c in active_cars:
        cat = c.get('Category') or 'Other'
        if cat not in cat_data:
            cat_data[cat] = {'total': 0, 'avail': 0, 'rented': 0}
        cat_data[cat]['total'] += 1
        if c.get('IsRented'): cat_data[cat]['rented'] += 1
        else:                 cat_data[cat]['avail']  += 1

    # ── Overdue rentals ───────────────────────────────────────────────────────
    today    = datetime.datetime.now()
    overdue: List[Dict] = []
    for r in active_rentals:
        try:
            end_obj = datetime.datetime.strptime(str(r['EndDate']).zfill(8), '%d%m%Y')
            if end_obj < today:
                overdue.append(r)
        except ValueError:
            pass

    # ── Helper: ค้นหาชื่อในไฟล์ทั้งหมด (รวม Deleted) ────────────────────────
    def find_cust_name(cid: int) -> str:
        for c in all_custs:
            if c['ID'] == cid:
                return c['Name'] + ('' if c['IsActive'] else ' [DEL]')
        return f'ID {cid} (Unknown)'

    def find_car_model(cid: int) -> str:
        for c in all_cars:
            if c['ID'] == cid:
                return c['Model'] + ('' if c['IsActive'] else ' [DEL]')
        return f'ID {cid} (Unknown)'

    lines: List[str] = []
    a = lines.append

    # ══════════════════════════════════════════════════════════════════════════
    # HEADER
    # ══════════════════════════════════════════════════════════════════════════
    a(_ruler('='))
    banner_lines = [
        r"",
        r"              CAR RENTAL MANAGEMENT SYSTEM",
        r"                 Detailed Summary Report",
        r"",
    ]
    for bl in banner_lines:
        a(bl)
    a(_ruler('='))
    a(f"  Generated At : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}   "
      f"Time Zone   : +07:00 (Indochina Time)")
    a(f"  Encoding     : UTF-8 (Fixed-Length Binary)    "
      f"Endianness  : Little-Endian")
    a(f"  Record Sizes : Car={car_mgr.record_size}B "
      f"| Customer={cust_mgr.record_size}B "
      f"| Rental={rental_mgr.record_size}B")
    a(_ruler('='))
    a('')

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 1 : FLEET STATUS
    # ══════════════════════════════════════════════════════════════════════════
    a(_section('SECTION 1 : FLEET STATUS'))
    a('')

    car_cols = [
        ('Status',       11), ('ID',    5), ('Category', 10), ('Model',         30),
        ('License Plate', 14), ('Rate THB/d', 11), ('Rented?', 8),
        ('Renter ID',    10), ('Rental Start', 12), ('Rental End', 12),
    ]
    car_hdr = ' | '.join(f"{n:<{w}}" for n, w in car_cols)
    car_sep = '-' * (sum(w for _, w in car_cols) + (len(car_cols) - 1) * 3)
    a(_ruler('-'))
    a('  ALL CAR RECORDS')
    a(_ruler('-'))
    a('  ' + car_hdr)
    a('  ' + car_sep)

    for car in all_cars:
        cid = car['ID']
        if not car['IsActive']:
            status = '[DELETED]'
            rflag = renter = s_d = e_d = '-'
        elif car.get('IsRented'):
            status = '[RENTED]   '
            rflag  = 'Yes'
            rent   = rental_by_car.get(cid)
            if rent:
                renter = str(rent['CustomerID'])
                s_d    = format_date_display(rent['StartDate'])
                e_d    = format_date_display(rent['EndDate'])
            else:
                renter = s_d = e_d = 'ERR'
        else:
            status = '[AVAILABLE]'
            rflag = renter = s_d = e_d = '-'

        row = ' | '.join([
            _pad(status, 10),  _pad(cid, 5),  _pad(car.get('Category',''), 10),
            _pad(_trunc(car['Model'], 28), 30),  _pad(car['LicensePlate'], 14),
            _pad(f"{car['DailyRate']:,.2f}", 11, '>'),  _pad(rflag, 8),
            _pad(renter, 10),  _pad(s_d, 12),  _pad(e_d, 12),
        ])
        a('  ' + row)

    a('  ' + car_sep)
    a('')

    # Box สถิติรถ
    max_cat = max((v['total'] for v in cat_data.values()), default=1)
    a(_box_top('CAR STATISTICS'))
    a(_box_row(f"Total Records : {len(all_cars):<5}  Active : {len(active_cars):<5}  Deleted : {len(all_cars)-len(active_cars):<5}"))
    a(_box_row(f"Available     : {len(avail_cars):<5}  Rented : {len(rented_cars):<5}"))
    a(_box_bot())
    a('')

    a(_box_top('RATE STATISTICS  (THB/day, Active Cars Only)'))
    a(_box_row(f"Minimum : {min_rate:>10,.2f}  |  Maximum : {max_rate:>10,.2f}  |  Average : {avg_rate:>10,.2f}"))
    a(_box_bot())
    a('')
    a(_box_top('FLEET BY CATEGORY  (Bar = rental utilization %)'))
    if cat_data:
        for cat, v in sorted(cat_data.items()):
            util_bar = ascii_bar(v['rented'], v['total'], 15) 
            util_pct = v['rented'] / v['total'] * 100 if v['total'] else 0
            a(_box_row(
                f"{cat:<12} {util_bar} {util_pct:>5.0f}%  "
                f"Total:{v['total']:<3}  Avail:{v['avail']:<3}  Rented:{v['rented']}"
            ))
    else:
        a(_box_row('No active cars.'))
    a(_box_bot())
    a('')

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 2 : CUSTOMER DIRECTORY
    # ══════════════════════════════════════════════════════════════════════════
    a(_section('SECTION 2 : CUSTOMER DIRECTORY'))
    a('')

    cust_cols = [
        ('Status',  9), ('ID',  5), ('Name',  31), ('Phone', 16),
        ('Email',  31), ('Rentals', 8), ('Total Spent (THB)', 18),
    ]
    cust_hdr = ' | '.join(f"{n:<{w}}" for n, w in cust_cols)
    cust_sep = '-' * (sum(w for _, w in cust_cols) + (len(cust_cols) - 1) * 3)
    a(_ruler('-'))
    a('  ALL CUSTOMER RECORDS')
    a(_ruler('-'))
    a('  ' + cust_hdr)
    a('  ' + cust_sep)

    for c in all_custs:
        status = '[ACTIVE] ' if c['IsActive'] else '[DELETED]'
        spent  = cust_spend.get(c['ID'], 0.0)
        cnt    = cust_cnt.get(c['ID'], 0)
        row = ' | '.join([
            _pad(status, 9),  _pad(c['ID'], 5),
            _pad(_trunc(c['Name'], 30), 31),
            _pad(c['Phone'], 16),
            _pad(_trunc(c.get('Email',''), 30), 31),
            _pad(cnt, 8),  _pad(f"{spent:,.2f}", 18, '>'),
        ])
        a('  ' + row)

    a('  ' + cust_sep)
    a('')
    a(_box_top('CUSTOMER STATISTICS'))
    a(_box_row(f"Total : {len(all_custs):<5}  Active : {len(active_custs):<5}  Deleted : {len(all_custs)-len(active_custs):<5}"))
    a(_box_bot())
    a('')

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 3 : RENTAL HISTORY
    # ══════════════════════════════════════════════════════════════════════════
    a(_section('SECTION 3 : RENTAL HISTORY  (Active + Closed)'))
    a('')

    rent_cols = [
        ('Status',  9), ('Rental ID', 9), ('Cust ID', 8), ('Car ID', 7),
        ('Start Date', 11), ('End Date', 11), ('Customer Name', 30), ('Total Price (THB)', 18),
    ]
    rent_hdr = ' | '.join(f"{n:<{w}}" for n, w in rent_cols)
    rent_sep = '-' * (sum(w for _, w in rent_cols) + (len(rent_cols) - 1) * 3)
    a(_ruler('-'))
    a('  ALL RENTAL RECORDS')
    a(_ruler('-'))
    a('  ' + rent_hdr)
    a('  ' + rent_sep)

    for r in all_rentals:
        status    = '[ACTIVE] ' if r['IsActive'] else '[CLOSED] '
        cust_name = find_cust_name(r['CustomerID'])
        row = ' | '.join([
            _pad(status, 9),  _pad(f"#{r['ID']}", 9),  _pad(r['CustomerID'], 8),
            _pad(r['CarID'], 7),  _pad(format_date_display(r['StartDate']), 11),
            _pad(format_date_display(r['EndDate']), 11),
            _pad(_trunc(cust_name, 28), 30),
            _pad(f"{r['TotalPrice']:,.2f}", 18, '>'),
        ])
        a('  ' + row)

    a('  ' + rent_sep)
    a('')
    a(_box_top('RENTAL STATISTICS'))
    a(_box_row(f"Total : {len(all_rentals):<5}  Active (Open) : {len(active_rentals):<5}  Closed (Returned) : {len(closed_rentals):<5}"))
    a(_box_bot())
    a('')

    if overdue:
        a(_box_top(f'!!  OVERDUE RENTALS  — {len(overdue)} contract(s) past End Date'))

        for r in overdue:
            end_str = format_date_display(r['EndDate'])
            cname = find_cust_name(r['CustomerID'])
            prefix = (
                f"Rental #{r['ID']:<5}  "
                f"Car ID:{r['CarID']:<4}  "
                f"Customer: "
            )
            suffix = f"   Due: {end_str}"
            available = BIW - _dw(prefix) - _dw(suffix)
            if _dw(cname) > available:
                cname_display = _trunc(cname, max(0, available - 3)) + "..."
            else:
                cname_display = _pad(cname, available)
            a(_box_row(prefix + cname_display + suffix))
    a(_box_bot())
    a('')

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 4 : FINANCIAL SUMMARY
    # ══════════════════════════════════════════════════════════════════════════
    a(_section('SECTION 4 : FINANCIAL SUMMARY'))
    a('')

    a(_box_top('REVENUE OVERVIEW'))
    a(_box_row(f"Total Revenue  (All Time)          : {all_rev:>14,.2f} THB"))
    a(_box_row(f"Revenue from Active  (Open) Rentals: {act_rev:>14,.2f} THB"))
    a(_box_row(f"Revenue from Closed (Returned)     : {cls_rev:>14,.2f} THB"))
    a(_box_row(f"Average Revenue per Rental         : {avg_rev:>14,.2f} THB"))
    if max_rent:
        a(_box_row(f"Highest Single Rental              : {max_rent['TotalPrice']:>14,.2f} THB  (Rental #{max_rent['ID']})"))
    a(_box_bot())
    a('')

    # Top 3 customers
    a(_box_top('TOP 3 CUSTOMERS BY TOTAL SPENDING'))
    top3_custs = sorted(cust_spend.items(), key=lambda x: x[1], reverse=True)[:3]
    if top3_custs:
        for rank, (cid, total) in enumerate(top3_custs, 1):
            name = find_cust_name(cid)
            cnt  = cust_cnt.get(cid, 0)
            a(_box_row(f"#{rank}  ID:{_pad(cid,4)}  {_pad(_trunc(name,30),30)}  "
            f"{_pad(f'{total:,.2f} THB',16,'>')}  ({cnt} rental{'s' if cnt!=1 else ''})"))
    else:
        a(_box_row('No rental data available.'))
    a(_box_bot())
    a('')

    # Top 3 most rented cars
    a(_box_top('TOP 3 MOST RENTED CARS'))
    top3_cars = sorted(car_rent_cnt.items(), key=lambda x: x[1], reverse=True)[:3]
    if top3_cars:
        for rank, (cid, cnt) in enumerate(top3_cars, 1):
            model  = find_car_model(cid)
            cr     = car_mgr.get_record_by_id(cid)
            c_stat = ('Rented' if cr[0].get('IsRented') else 'Available') if cr else 'Deleted'
            a(_box_row(f"#{rank}  ID:{_pad(cid,4)}  {_pad(_trunc(model,30),30)}  "
            f"{_pad(cnt,3,'>')} rental{'s' if cnt!=1 else ''}  ({c_stat})"))
    else:
        a(_box_row('No rental data available.'))
    a(_box_bot())
    a('')

    # ══════════════════════════════════════════════════════════════════════════
    # FOOTER
    # ══════════════════════════════════════════════════════════════════════════
    a(_ruler('='))
    a(f"  END OF REPORT  |  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    a(f"  Binary Files  :  Cars={len(all_cars)} rec × {car_mgr.record_size}B"
      f"   |  Customers={len(all_custs)} rec × {cust_mgr.record_size}B"
      f"   |  Rentals={len(all_rentals)} rec × {rental_mgr.record_size}B")
    a(_ruler('='))

    try:
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n')
        print(f"\n  !! รายงานสรุปถูกสร้างสำเร็จที่ '{report_filename}' !!")
    except IOError as e:
        print(f"  // Error writing report: {e} \\")

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

    try:
        while True:
            print("\n" + "="*52)
            print("       ระบบจัดการเช่ารถยนต์  (MAIN MENU)")
            print("="*52)
            print("  [1] จัดการข้อมูลรถยนต์")
            print("  [2] จัดการข้อมูลลูกค้า")
            print("  [3] จัดการสัญญาเช่า")
            print("  [R] สร้างรายงานสรุป (.txt)")
            print("  [X] ออกจากระบบ")

            ch = get_user_choice(">> กรุณาเลือกเมนู: ", ['1', '2', '3', 'R', 'X'])

            if   ch == '1': run_car_menu(car_mgr)
            elif ch == '2': run_customer_menu(cust_mgr, rental_mgr)
            elif ch == '3': run_rental_menu(rental_mgr, car_mgr, cust_mgr)
            elif ch == 'R':
                generate_detailed_summary_report(car_mgr, cust_mgr, rental_mgr)
            elif ch == 'X':
                print("\n" + "="*52)
                print("  กำลังปิดระบบอย่างปลอดภัย...")
                print("="*52)
                generate_detailed_summary_report(
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
