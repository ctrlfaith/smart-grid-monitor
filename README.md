# ⚡ Smart Grid Monitor

**Python · Automation · Anomaly Detection · Predictive Alerting · Discord Webhook · Unit Testing**

> ระบบ Monitoring จำลองสำหรับ Smart Grid ที่ออกแบบมาเพื่อเฝ้าระวังสถานะอุปกรณ์ ตรวจจับความผิดปกติ และแจ้งเตือนเชิงรุกก่อนเกิดปัญหาจริง

A lightweight monitoring and alerting system that simulates Smart Grid devices, detects anomalies, identifies rising-risk conditions through trend analysis, and delivers real-time alerts via Discord.

---

## Smart Grid Monitor คืออะไร

Smart Grid Monitor เป็น Automation Script ที่จำลองการทำงานของระบบเฝ้าระวังอุปกรณ์ในโครงข่าย Smart Grid โดยใช้ข้อมูลจากหม้อแปลงไฟฟ้า (Transformer) สวิตช์ตัดต่อ (Switch Gear) และเซอร์กิตเบรกเกอร์ (Circuit Breaker) เพื่อจำลองสถานการณ์การตรวจสอบสถานะอุปกรณ์แบบ Real-time

โปรเจกต์นี้มุ่งเน้นการพัฒนาระบบ Monitoring และ Alerting ในรูปแบบ Modular Architecture สำหรับงานด้าน Digital Engineering โดยรองรับการตรวจจับความผิดปกติหลายประเภทพร้อมกัน (Multi-reason Detection) การคาดการณ์แนวโน้มก่อนเกิดปัญหาจริง (Predictive Alerting) และการแจ้งเตือนแบบ Real-time ผ่าน Discord Webhook

นอกจากการตรวจจับเหตุการณ์ที่เกิดขึ้นแล้ว ระบบยังสามารถวิเคราะห์แนวโน้มอุณหภูมิที่เพิ่มขึ้นต่อเนื่อง เพื่อแจ้งเตือนล่วงหน้าก่อนที่ค่าจะเกิน Threshold ที่กำหนด ช่วยให้สามารถเฝ้าระวังและตอบสนองต่อความเสี่ยงได้ตั้งแต่ระยะเริ่มต้น

เป้าหมายของโปรเจกต์คือการจำลองแนวคิดของระบบ Monitoring ในระดับ Production โดยใช้ Severity Levels เพื่อจัดลำดับความสำคัญของเหตุการณ์ แทนการตรวจสอบแบบ Reactive ที่รอให้เกิดปัญหาขึ้นก่อนแล้วจึงแจ้งเตือน

---

## Features

- **Multi-device Monitoring** — ตรวจสอบอุปกรณ์ 7 ตัวพร้อมกันในแต่ละรอบ ครอบคลุม Transformer, Switch Gear และ Circuit Breaker
- **Per-device Threshold** — Circuit Breaker ใช้ Threshold อุณหภูมิแยกต่างหาก (65°C) เนื่องจากทนความร้อนได้น้อยกว่า Transformer (75°C)
- **Multi-reason Anomaly Detection** — ตรวจจับและรายงานความผิดปกติได้หลายประเภทพร้อมกันในอุปกรณ์เดียว เช่น อุณหภูมิสูงและแรงดันไฟตก โดยแสดงทุกสาเหตุที่ตรวจพบภายในรอบการตรวจสอบเดียวกัน
- **Adaptive Anomaly Detection** — ตรวจจับพฤติกรรมผิดปกติด้วย Z-Score Analysis โดยเปรียบเทียบค่าปัจจุบันกับ Historical Baseline ของแต่ละอุปกรณ์ สามารถตรวจพบความผิดปกติได้แม้ค่ายังอยู่ในช่วง Threshold ที่กำหนด
- **Predictive Alerting** — แจ้งเตือนล่วงหน้าด้วยสถานะ PRE-WARNING เมื่อตรวจพบแนวโน้มอุณหภูมิที่เพิ่มขึ้นอย่างต่อเนื่อง แม้ค่ายังไม่เกิน Threshold ที่กำหนด
- **Severity Levels** — แบ่งระดับความรุนแรงเป็น CRITICAL, WARNING, PRE-WARNING และ INFO เพื่อช่วยจัดลำดับความสำคัญของการตอบสนองต่อเหตุการณ์
- **Discord Webhook Integration** — ส่งการแจ้งเตือนแบบ Real-time ไปยัง Discord พร้อมแสดงข้อมูลสำคัญ เช่น Temperature และ Voltage ในแต่ละ Alert
- **Streamlit Dashboard** — แสดงผลข้อมูลแบบ Real-time ผ่าน Web UI พร้อม Auto-refresh ครอบคลุมสถานะอุปกรณ์, แนวโน้มอุณหภูมิ, ประวัติการแจ้งเตือน และ Pattern Analysis
- **Runtime Logging** — บันทึกผลการตรวจสอบและเหตุการณ์ที่เกิดขึ้นในแต่ละรอบลงไฟล์ `smart_grid.log` พร้อม Timestamp สำหรับการตรวจสอบย้อนหลัง
- **CSV Reporting** — สร้างรายงานสรุปผลการตรวจสอบในรูปแบบ CSV และบันทึกลง `smart_grid_report.csv` อัตโนมัติ
- **Graceful Shutdown & Run Summary** — รองรับการหยุดระบบด้วย Ctrl+C อย่างปลอดภัย พร้อมสรุปจำนวนรอบการทำงานและเหตุการณ์ที่ตรวจพบก่อนปิดโปรแกรม

---

## Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.10+ |
| Standard Library | `csv`, `logging`, `datetime`, `random`, `time`, `math`, `collections`, `pathlib`, `unittest` |
| External Dependencies | `requests` (Discord Webhook), `streamlit` (Dashboard), `pandas` (Data processing), `altair` (Charts) |
| Testing Framework | `pytest` (16 test cases) |

---

## Project Structure & Architecture

โปรเจกต์นี้ถูกออกแบบในรูปแบบ Modular Architecture โดยแยกแต่ละส่วนของระบบออกตามหน้าที่รับผิดชอบ (Separation of Concerns) ทำให้โค้ดอ่านง่าย ดูแลรักษาได้สะดวก และสามารถขยายความสามารถของระบบในอนาคตได้โดยไม่กระทบส่วนอื่น

```
smart-grid-monitor/
├── config.py            # Thresholds, CB_THRESHOLDS, device list, Discord Webhook URL (ไม่ push ขึ้น GitHub)
├── config.example.py    # Template config สำหรับ reference (ไม่มี URL จริง)
├── .gitignore           # Excludes config.py, *.log, *.csv
├── simulator.py         # Mock sensor data generator
├── monitor.py           # Core detection logic — anomaly detection + predictive alerting
├── detector.py          # Adaptive anomaly detection (Z-Score based)
├── alert.py             # Alert dispatcher — severity levels + Discord Webhook
├── reporter.py          # Summary printer + CSV exporter
├── scheduler.py         # Auto-loop runner พร้อม graceful shutdown
├── dashboard.py         # Streamlit dashboard — real-time visualization
├── test_monitor.py      # Unit tests (16 test cases)
├── requirements.txt
└── README.md
```

### Data Flow

```
config.py ──────────────────────────────────────┐
                                                ▼
simulator.py ── generates sensor data ────▶ monitor.py ──▶ alert.py (Discord + print)
                                                │ ▲
                                                │ └── detector.py (Z-Score adaptive detection)
                                                │
                                                └──▶ smart_grid.log

scheduler.py ── calls monitor.py in a loop ──▶ reporter.py (summary + CSV)

dashboard.py ── reads smart_grid_report.csv ──▶ Streamlit UI
```

### Component Responsibilities

- **config.py** — จัดเก็บ Threshold, CB_THRESHOLDS, รายชื่ออุปกรณ์ และค่าการตั้งค่าต่าง ๆ ของระบบ เพื่อหลีกเลี่ยงการ Hard-code ภายในโค้ด
- **simulator.py** — จำลองข้อมูลจาก Sensor เพื่อสร้างสถานการณ์สำหรับการทดสอบและสาธิตการทำงานของระบบ
- **monitor.py** — ศูนย์กลางของระบบ ทำหน้าที่วิเคราะห์ข้อมูล ตรวจจับความผิดปกติ และประเมินแนวโน้มความเสี่ยงล่วงหน้า
- **detector.py** — วิเคราะห์ความผิดปกติเชิงสถิติด้วย Z-Score โดยเรียนรู้ Baseline จากข้อมูลย้อนหลังของแต่ละอุปกรณ์แบบ Rolling Window
- **alert.py** — จัดการการแจ้งเตือนตามระดับความรุนแรง พร้อมส่งข้อความผ่าน Discord Webhook
- **reporter.py** — สรุปผลการตรวจสอบและสร้างรายงานในรูปแบบ CSV หลังจบแต่ละรอบการทำงาน
- **scheduler.py** — ควบคุมการทำงานแบบต่อเนื่อง โดยเรียกใช้งาน Monitoring Engine ตามช่วงเวลาที่กำหนด
- **dashboard.py** — แสดงผลข้อมูลจาก CSV ผ่าน Streamlit Web UI พร้อม Auto-refresh ครอบคลุม 5 sections ได้แก่ Summary Stats, Live Device Status, Temperature Trend, Alert History และ Pattern Analysis

---

## Anomaly Conditions

ระบบจะวิเคราะห์ข้อมูลของอุปกรณ์แต่ละตัวตามชุดกฎ (Rule-based Detection) ที่กำหนดไว้ล่วงหน้า โดยแต่ละเงื่อนไขจะถูกจัดระดับความรุนแรง (Severity Level) ตามผลกระทบของเหตุการณ์

เมื่อพบความผิดปกติ ระบบจะสร้าง Alert ที่เหมาะสมโดยอัตโนมัติ และในกรณีที่พบหลายความผิดปกติพร้อมกัน ระบบจะรวบรวมทุกสาเหตุที่ตรวจพบก่อนนำไปประมวลผลตาม Priority Logic

| Condition | Severity | Trigger |
|---|---|---|
| Device Offline | CRITICAL | `status == "offline"` |
| Overheating (Transformer / Switch Gear) | WARNING | `temp > 75°C` |
| Overheating (Circuit Breaker) | WARNING | `temp > 65°C` |
| Voltage Drop (Brownout) | WARNING | `voltage < 210V` |
| Multiple Anomalies Detected | WARNING (Multi-reason) | `reasons = ['OVERHEAT', 'BROWNOUT']` |
| Rising Temperature Trend | PRE-WARNING | อุณหภูมิขึ้น ≥ 2°C ติดต่อกัน 3 รอบ |
| Adaptive Anomaly (Z-Score) | PRE-WARNING | ค่าเบี่ยงเบนจาก Baseline เกิน Z-Score threshold ที่ `2.5` |
| Normal Operation | INFO | ไม่มี Condition ใดถูก Trigger |

กลยุทธ์การตรวจจับของระบบผสมผสานทั้ง Static Threshold-based Rules และ Adaptive Anomaly Detection เข้าด้วยกัน นอกจาก Fixed Threshold แล้ว ระบบยังสามารถตรวจจับพฤติกรรมผิดปกติผ่าน Trend Analysis และ Statistical Deviation จาก Historical Baseline ของแต่ละอุปกรณ์ ทำให้สามารถตรวจพบความเสี่ยงได้ก่อนที่ค่าจะเกิน Threshold จริง

---

## Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure the Application

```bash
cp config.example.py config.py
```

เปิด `config.py` แล้วกำหนดค่า Discord Webhook URL (ไม่บังคับ)

> หากไม่ได้กำหนด Webhook URL ระบบจะยังคงทำงานตามปกติ แต่จะข้ามการส่งแจ้งเตือนไปยัง Discord

### 3. Run Once

```bash
python monitor.py
```

### 4. Run Continuously

```bash
python scheduler.py
```

ระบบจะทำการตรวจสอบอุปกรณ์ทุก 10 วินาทีตามค่าเริ่มต้น

กด `Ctrl+C` เพื่อหยุดการทำงานอย่างปลอดภัย

### 5. Run Dashboard (Optional)

เปิด Terminal ใหม่แยกต่างหาก แล้วรัน:

```bash
streamlit run dashboard.py
```

> Dashboard อ่านข้อมูลจาก `smart_grid_report.csv` ที่ `scheduler.py` สร้างขึ้น — ต้องรัน `scheduler.py` ก่อนเพื่อให้มีข้อมูลแสดงผล

---

## Run Tests

```bash
python -m pytest test_monitor.py -v
```

Example output:

```
collected 16 items

test_monitor.py::TestAnomalyDetection::test_brownout PASSED
test_monitor.py::TestAnomalyDetection::test_cb_normal PASSED
test_monitor.py::TestAnomalyDetection::test_cb_overheat PASSED
...
16 passed in 0.28s
```

ชุดทดสอบจำนวน 16 Test Cases ครอบคลุมการทำงานหลักของระบบ ได้แก่

- Normal values
- Boundary conditions
- Anomaly detection ทุกประเภท
- Predictive trend detection
- Multi-reason detection
- Edge cases และ Invalid inputs
- Priority logic (Trend detection skipped when WARNING exists)
- Circuit Breaker threshold (per-device threshold verification)

---

## Sample Output

ตัวอย่าง Output จากหนึ่งรอบการตรวจสอบ แสดงการทำงานครบทุกประเภท ได้แก่ สถานะปกติ การตรวจจับ Anomaly การแจ้งเตือนเชิงรุก และการสรุปผลหลังจบรอบ

```
--- ⚡ Smart Grid Monitor | 2026-06-21 14:32:01 ---
[TF-001] Transformer | Temp: 62.3°C | Voltage: 223.0V | Status: online → INFO (NORMAL)
[TF-002] Transformer | Temp: 76.1°C | Voltage: 218.0V | Status: online → WARNING (OVERHEAT)
  → ALERT: ⚠️ [WARNING] TF-002 | Transformer | Substation B | OVERHEAT | Temp: 76.1°C | Voltage: 218.0V
[TF-003] Transformer | Temp: 71.0°C | Voltage: 207.0V | Status: online → WARNING (BROWNOUT)
  → ALERT: ⚠️ [WARNING] TF-003 | Transformer | Substation C | BROWNOUT | Temp: 71.0°C | Voltage: 207.0V
[SW-001] Switch Gear | Temp: N/A | Voltage: N/A | Status: offline → CRITICAL (OFFLINE)
  → ALERT: 🚨 [CRITICAL] SW-001 | Switch Gear | Main Line | OFFLINE | Temp: N/A | Voltage: N/A
[SW-002] Switch Gear | Temp: 68.0°C | Voltage: 221.0V | Status: online → PRE-WARNING (TEMP RISING TREND)
  → ALERT: 🔔 [PRE-WARNING] SW-002 | Switch Gear | Secondary Line | TEMP RISING TREND | Temp: 68.0°C | Voltage: 221.0V
[CB-001] Circuit Breaker | Temp: 58.0°C | Voltage: 222.0V | Status: online → INFO (NORMAL)
[CB-002] Circuit Breaker | Temp: 67.5°C | Voltage: 219.0V | Status: online → WARNING (OVERHEAT)
  → ALERT: ⚠️ [WARNING] CB-002 | Circuit Breaker | Secondary Panel | OVERHEAT | Temp: 67.5°C | Voltage: 219.0V

📋 Summary: 7 devices checked | ✅ 2 normal | 🔔 1 pre-warning | ⚠️ 3 warning | 🚨 1 critical | ❌ 0 error
📊 Report exported → smart_grid_report.csv
```

---

## Screenshot

ตัวอย่างการแจ้งเตือนผ่าน Discord ควบคู่กับ Terminal Output แสดง Alert ระดับ WARNING, CRITICAL และ PRE-WARNING พร้อม Run Summary หลังกด Ctrl+C

![Smart Grid Monitor — Discord + Terminal](assets/screenshot.png)

ตัวอย่าง Streamlit Dashboard แสดงสถานะอุปกรณ์แบบ Real-time, แนวโน้มอุณหภูมิ, ประวัติการแจ้งเตือน และ Pattern Analysis

![Smart Grid Monitor — Dashboard](assets/dashboard.png)

---

## Notable Implementation Examples

ตัวอย่างด้านล่างแสดงแนวคิดการออกแบบหลักของระบบในแต่ละ Layer โดยแยกความรับผิดชอบของแต่ละโมดูลออกจากกันอย่างชัดเจน ตั้งแต่การตรวจจับความผิดปกติ การวิเคราะห์เชิงคาดการณ์ การแจ้งเตือน ไปจนถึงการทดสอบ เพื่อให้ระบบสามารถดูแลรักษาและขยายต่อได้ง่าย

### Detection & Predictive Layer

[`monitor.py`](https://github.com/ctrlfaith/smart-grid-monitor/blob/main/monitor.py)

เป็นศูนย์กลางของระบบ ทำหน้าที่วิเคราะห์ข้อมูลจากอุปกรณ์และตรวจจับความผิดปกติตามเงื่อนไขที่กำหนด โดยรองรับการตรวจจับหลายเหตุการณ์พร้อมกันในอุปกรณ์เดียว (Multi-reason Detection) แทนการหยุดประมวลผลเมื่อพบความผิดปกติรายการแรก

นอกจากนี้ยังมีการวิเคราะห์แนวโน้มอุณหภูมิผ่าน `_detect_trend()` ซึ่งใช้ข้อมูลย้อนหลัง 3 รอบการทำงานเพื่อตรวจจับการเพิ่มขึ้นของอุณหภูมิอย่างต่อเนื่อง และแจ้งเตือนในระดับ PRE-WARNING ก่อนที่ค่าจะเกิน Threshold จริง

ระบบยังรองรับ Threshold ที่แตกต่างกันตามประเภทอุปกรณ์ เพื่อให้การตรวจจับความผิดปกติมีความเหมาะสมกับลักษณะการทำงานของอุปกรณ์แต่ละชนิด

---

### Adaptive Detection Layer

[`detector.py`](https://github.com/ctrlfaith/smart-grid-monitor/blob/main/detector.py)

ทำหน้าที่ตรวจจับความผิดปกติเชิงสถิติ (Adaptive Anomaly Detection) ด้วย Z-Score เพื่อค้นหาพฤติกรรมที่ผิดปกติ แม้ว่าค่าปัจจุบันจะยังไม่เกิน Threshold ที่กำหนดไว้

โมดูลนี้เรียนรู้ Baseline ของอุณหภูมิและแรงดันไฟจากข้อมูลย้อนหลังของแต่ละอุปกรณ์ผ่าน Rolling Window จำนวน 50 จุดข้อมูล และเริ่ม Flag เหตุการณ์เมื่อค่าเบี่ยงเบนเกิน Z-Score Threshold ที่กำหนด

การแยก Adaptive Detection ออกจาก `monitor.py` ช่วยให้ Rule-based Detection และ Statistical Detection ทำงานร่วมกันได้อย่างอิสระ โดยไม่เพิ่มความซับซ้อนให้กับ Core Detection Logic

---

### Alert Dispatch Layer

[`alert.py`](https://github.com/ctrlfaith/smart-grid-monitor/blob/main/alert.py)

รับผลลัพธ์จาก Monitoring Engine และจัดการการแจ้งเตือนตามระดับความรุนแรงของเหตุการณ์ โดยแต่ละ Alert จะประกอบด้วยข้อมูลสำคัญ เช่น Device ID, Temperature และ Voltage เพื่อช่วยให้ผู้รับแจ้งเตือนสามารถประเมินสถานการณ์ได้ทันที

การแยกส่วน Alert Dispatch ออกจาก Detection Logic ช่วยลดการพึ่งพากันระหว่างโมดูล และเปิดโอกาสให้สามารถเพิ่มช่องทางการแจ้งเตือนอื่น ๆ เช่น Email หรือ LINE ได้ในอนาคตโดยไม่ต้องแก้ไข Detection Layer

---

### Test Coverage Layer

[`test_monitor.py`](https://github.com/ctrlfaith/smart-grid-monitor/blob/main/test_monitor.py)

ประกอบด้วย 16 Test Cases ที่ครอบคลุมทั้งการทำงานปกติ (Normal Values), Boundary Conditions, การตรวจจับความผิดปกติทุกประเภท, Predictive Trend Detection, Multi-reason Detection, Edge Cases, Priority Logic และการเลือก Threshold ตามประเภทอุปกรณ์

ชุดทดสอบถูกออกแบบให้ตรวจสอบทั้งผลลัพธ์ที่คาดหวังและพฤติกรรมของระบบในสถานการณ์ที่อาจเกิดขึ้นจริง เพื่อช่วยลดความเสี่ยงจากการเปลี่ยนแปลงโค้ดในอนาคตและเพิ่มความมั่นใจในการทำงานของ Detection Logic

การใช้ `assertIn()` แทน `assertEqual()` สำหรับ Multi-reason Detection ช่วยให้การทดสอบไม่ขึ้นอยู่กับลำดับของเหตุการณ์ที่ตรวจพบ และสะท้อนพฤติกรรมจริงของระบบที่สามารถรายงานหลายความผิดปกติพร้อมกันได้

---

## Development Approach

โปรเจกต์นี้ถูกพัฒนาแบบเป็นลำดับขั้นโดยแบ่งงานออกเป็น 7 Sprint เพื่อกำหนดเป้าหมายและขอบเขตงานของแต่ละช่วงอย่างชัดเจน ตั้งแต่การวางโครงสร้างระบบ การพัฒนา Detection Logic ไปจนถึงการทดสอบ Dashboard และ Adaptive Detection

- Sprint 1 — Foundation (config + simulator)
- Sprint 2 — Core Detection Logic (monitor + logging)
- Sprint 3 — Alerting & Reporting (alert + reporter)
- Sprint 4 — Automation & Testing (scheduler + unit tests)
- Sprint 5 — Documentation & Polish (README + code review)
- Sprint 6 — Dashboard (Streamlit real-time visualization)
- Sprint 7 — Adaptive Detection (Z-Score based anomaly detection)

---

## Author

Designed, Developed and Maintained by **Phuriphat Rattanatham**

- Portfolio · [ctrlfaith-portfolio.vercel.app](https://ctrlfaith-portfolio.vercel.app)
- GitHub · [github.com/ctrlfaith](https://github.com/ctrlfaith)
