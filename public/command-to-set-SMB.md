### **# Command to configure SMB (Lab 3 Resource)**





##### **อัปเดตแพ็กเกจระบบและติดตั้ง Samba**

sudo apt update \&\& sudo apt upgrade -y

sudo apt install samba -y



##### **เปิดใช้งานบริการ smbd และ nmbd**

sudo systemctl enable smbd nmbd

sudo systemctl start smbd nmbd



##### **ตั้งค่า Firewall (UFW) อนุญาตพอร์ต Samba**

sudo ufw enable

sudo ufw allow 137:138/udp

sudo ufw allow 139,445/tcp



##### **สำรองไฟล์คอนฟิกเดิมไว้ก่อน**

sudo cp /etc/samba/smb.conf{,.backup}



##### **เปิดไฟล์คอนฟิกขึ้นมาแก้ไข**

sudo nano /etc/samba/smb.conf



##### **ส่วนในการตั้งค่าใน smb.conf**

; interfaces = 127.0.0.0/8 eth0 (ลบ ; ข้างหน้าออก และ eth0 เปลี่ยนเป็น Network Interface ของเครื่องเราเอง ส่วนใหญ่จะเป็น ens33, ens160 เช็คได้ด้วยคำสั่ง ip a)

; bind interfaces only = yes (ลบ ; ข้างหน้าออก)



##### **ส่วนการตั้งค่า Share เอาไปต่อล่างสุด**

\[ShareA]

&#x20;  comment = Everyone in the groupA

&#x20;  path = /Share/ShareA

&#x20;  browseable = yes

&#x20;  read only = no

&#x20;  force create mode = 0660

&#x20;  force directory mode = 2770

&#x20;  valid users = @groupA



\[ShareB]

&#x20;  comment = Everyone in the groupB and userA1

&#x20;  path = /Share/ShareB

&#x20;  browseable = yes

&#x20;  read only = no

&#x20;  force create mode = 0660

&#x20;  force directory mode = 2770

&#x20;  valid users = @groupB userA1



##### **การสร้าง Groups, Users และกำหนดสิทธิ์ Directory**

**# 3.1 สร้าง Group บน Linux** 

sudo groupadd groupA

sudo groupadd groupB



**# 3.2 สร้าง User บน Linux แบบไม่ให้มี Shell Login** 

sudo useradd -s /usr/sbin/nologin userA1

sudo useradd -s /usr/sbin/nologin userB1



**# 3.3 ดึง User เข้า Group**

sudo usermod -aG groupA,groupB userA1

sudo usermod -aG groupB userB1



**# 3.4 ตั้งรหัสผ่าน Samba ให้กับ User** 

sudo smbpasswd -a userA1

sudo smbpasswd -a userB1



**# 3.5 สร้างโฟลเดอร์แชร์หลักและโฟลเดอร์ย่อย**

sudo mkdir -p /Share/ShareA

sudo mkdir -p /Share/ShareB



**# 3.6 กำหนด Owner และ Permission ให้ถูกต้อง**

sudo chown -R userA1:groupA /Share/ShareA

sudo chown -R userB1:groupB /Share/ShareB



sudo chmod -R 2770 /Share/ShareA

sudo chmod -R 2770 /Share/ShareB



**# 3.7 รีสตาร์ทบริการ Samba เพื่อนำค่าใหม่ไปใช้** 

sudo systemctl restart smbd nmbd



##### **คำสั่งเคลียร์ Session เมื่อต้องการสลับ User (รันคำสั่งใน CMD แบบ Run as Administrator)**

net use \* /delete /y

klist purge



net stop workstation /y

net start workstation 

