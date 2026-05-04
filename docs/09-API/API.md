---
title: API
---

## HMI Subsystem

My role is the HMI subsystem. I allow the user to control the project via two
joysticks and two click-in buttons. I display sensor data and system status updates
on screen. My subsystem communicates with Adrian (Subsystem 2) directly over
ESP-NOW (primary), with wired UART as a fallback. I am not physically
in the daisy chain — all my communication goes to and from Adrian only. We had initally utalized MQTT, however I decided to go with ESP-NOW because it utalized lower power and had lower draw on the system as a whole. I also did not want to fight with all the networks that were likely in the inovation showcase. Our code can switch over to MQTT by adjusting a few quick lines in the config folder, however as with the mentioned issues we weren't able to get it fully working.

Joystick 2 is used internally for on-screen menu navigation and does not generate
any messages unless the click-in button is pressed.

---

## Packet Format

All packets are ASCII strings in the following format:
AZ + sender + receiver + type_char + data + YB

| Field    | Value   | Notes                                                        |
|----------|---------|--------------------------------------------------------------|
| Prefix   | `AZ`    | Always 2 chars                                               |
| Sender   | `1`–`6` | ASCII subsystem number                                       |
| Receiver | `1`–`6` | ASCII subsystem number                                       |
| Type     | See table below | Single ASCII char (or `43` for buttons)              |
| Data     | Variable | Type-specific payload                                       |
| Suffix   | `YB`    | Always 2 chars                                               |

### Message Type Character Encoding

| Type Number | Type Char | Description             |
|-------------|-----------|-------------------------|
| 1           | `1`       | Motor speed set         |
| 2           | `2`       | Motor info display      |
| 3           | `3`       | Sensor value            |
| 10          | `A`       | Error alert             |
| 12          | `C`       | Status request/response |
| 13          | `D`       | Status forwarded        |
| 14          | `E`       | Error ACK               |
| 15          | `F`       | Status response         |
| 67          | `43`      | Button press (two chars to avoid collision with Type 12 `C`) |

---

## Team Member IDs

| Individual | Subsystem Number |
|------------|-----------------|
| Sam B (me) | 1               |
| Adrian P   | 2               |
| Andrew I   | 3               |
| Jacob D    | 4               |
| Sam M      | 5               |
| Mo A       | 6               |

---

## Messages Sent

All messages I send go directly to Adrian (Subsystem 2) over ESP-NOW (private wifi network).

---

### Message Type 1 — Set Motor Speed (Joystick 1 Input)

Joystick 1 X and Y axes are sent as **two separate packets** — one per motor.
X-axis = Motor 1 (forward/reverse), Y-axis = Motor 2 (left/right). Speed is
derived from joystick deflection magnitude with a dead zone of ±8 units.

| Field         | sender | receiver | type | motor_id | speed | direction |
|---------------|--------|----------|------|----------|-------|-----------|
| Variable Name | sender_subsys | receiver_subsys | T_MOTOR_SET | motor_id | speed | direction |
| Variable Type | char   | char     | char | char     | char  | char      |
| Min Value     | `1`    | `2`      | `1`  | `1`      | `0`   | `0`       |
| Max Value     | `1`    | `2`      | `1`  | `2`      | `15`  | `1`       |
| Example       | `1`    | `2`      | `1`  | `1`      | `8`   | `0`       |

**Notes:**
- Joystick signed value (-127 to +127) converted to speed (0–15) and direction
- Dead zone: abs(val) ≤ 8 → speed = 0, no packet sent
- `motor_id`: 1 = X axis (forward/reverse), 2 = Y axis (left/right)
- `direction`: 0 = forward/left, 1 = reverse/right
- Send rate limited to every 880ms (`JOY_POLL_MS`)

**Example packets (X=speed 8 forward, Y=speed 4 right):**
AZ12 1 1 8 0 YB   ← Motor 1: speed=8 forward
AZ12 1 2 4 1 YB   ← Motor 2: speed=4 right

---

### Message Type 12 — Subsystem Status Request

Sent to Adrian to request a system status update.

| Field         | sender | receiver | type |
|---------------|--------|----------|------|
| Variable Name | sender_subsys | receiver_subsys | T_STATUS |
| Variable Type | char   | char     | char |
| Value         | `1`    | `2`      | `C`  |

**Notes:**
- No additional data needed — Adrian handles routing the status check
- Sent when user requests a system status check via HMI

**Example packet:**
AZ12CYB

---

### Message Type 14 — Error Acknowledgement

Sent to Adrian immediately after displaying a received error alert.

| Field         | sender | receiver | type | error_code  |
|---------------|--------|----------|------|-------------|
| Variable Name | sender_subsys | receiver_subsys | T_ERROR_ACK | error_code |
| Variable Type | char   | char     | char | char (0–64) |
| Min Value     | `1`    | `2`      | `E`  | `0`         |
| Max Value     | `1`    | `2`      | `E`  | `64`        |
| Example       | `1`    | `2`      | `E`  | `5`         |

**Notes:**
- `error_code` echoes back the code received — full error decode table TBD with team
- Sent immediately after displaying the error on screen

**Example packet:**
AZ12E5YB

---

### Message Type 67 — Button Press (Joystick Click-In)

Sent to Adrian when either joystick click-in button is pressed. HMI tracks
toggle state and sends current value on each press.

| Field         | sender | receiver | type  | button_num | button_state |
|---------------|--------|----------|-------|------------|--------------|
| Variable Name | sender_subsys | receiver_subsys | T_BUTTON | button_number | button_state |
| Variable Type | char   | char     | char  | char       | char         |
| Min Value     | `1`    | `2`      | `43`  | `1`        | `0`          |
| Max Value     | `1`    | `2`      | `43`  | `2`        | `1`          |
| Example       | `1`    | `2`      | `43`  | `1`        | `1`          |

**Notes:**
- `button_number`: 1 = Joystick 1 click-in, 2 = Joystick 2 click-in
- `button_state`: 0 = off, 1 = on — HMI owns toggle state, sends current value
- Type uses two-char `43` to avoid collision with Type 12 `C`
- Joystick 1 also supports double-click (menu toggle) and long press

**Example packets:**
AZ124311YB   ← Button 1 ON
AZ124310YB   ← Button 1 OFF

---

## Messages Received

All messages I receive come from Adrian (Subsystem 2) over ESP-NOW.

---

### Message Type 2 — Motor Info Display

Forwarded to me by Adrian from Jacob. I display current motor state on screen.

| Field         | sender | receiver | type | motor_id | motor_speed | motor_direction |
|---------------|--------|----------|------|----------|-------------|-----------------|
| Variable Name | sender_subsys | receiver_subsys | T_MOTOR_INFO | motor_id | motor_speed | motor_direction |
| Variable Type | char   | char     | char | char     | char        | char            |
| Min Value     | `2`    | `1`      | `2`  | `1`      | `0`         | `0`             |
| Max Value     | `2`    | `1`      | `2`  | `3`      | `15`        | `1`             |
| Example       | `2`    | `1`      | `2`  | `2`      | `8`         | `0`             |

**Example packet:**
AZ212280YB   ← Motor 2, speed 8, forward

---

### Message Type 3 — Sensor Value Display

Forwarded to me by Adrian. Format varies by originating subsystem.

#### From Mo (Subsystem 6) — Light Sensor / From Sam M (Subsystem 5) — Temperature

| Field         | sender | receiver | type | sensor_num | value_upper | value_lower |
|---------------|--------|----------|------|------------|-------------|-------------|
| Variable Type | char   | char     | char | char       | uint8_t     | uint8_t     |
| Min Value     | `2`    | `1`      | `3`  | `1`        | 0           | 0           |
| Max Value     | `2`    | `1`      | `3`  | `6`        | 255         | 255         |
| Example       | `2`    | `1`      | `3`  | `1`        | 0x01        | 0x2C        |

**Notes:**
- Reconstruct: `value = (value_upper << 8) | value_lower`
- Example: `(0x01 << 8) | 0x2C = 300`
- Sam M temperature value is in Celsius

#### From Andrew (Subsystem 3) — IMU Yaw/Pitch/Roll

Data field is a comma-separated ASCII string:

| Field         | sender | receiver | type | data          |
|---------------|--------|----------|------|---------------|
| Variable Type | char   | char     | char | ASCII string  |
| Example       | `2`    | `1`      | `3`  | `NE,4,-30`    |

**Notes:**
- Format: `yaw,pitch,roll`
- `yaw` = compass direction string (e.g. `N`, `NE`, `SW`)
- `pitch`, `roll` = signed integer degrees, range -180 to 180

**Example packets:**
AZ21310012CYB    ← Light/Temp: sensor 1, value 300
AZ213NE,4,-30YB  ← IMU: yaw=NE, pitch=4, roll=-30

---

### Message Type 10 — Subsystem Error Alert

Forwarded to me by Adrian. I display the error and send a Type 14 ack back.

| Field         | sender | receiver | type | error_code | sender_num |
|---------------|--------|----------|------|------------|------------|
| Variable Type | char   | char     | char | char       | char       |
| Min Value     | `2`    | `1`      | `A`  | `0`        | `1`        |
| Max Value     | `2`    | `1`      | `A`  | `64`       | `6`        |
| Example       | `2`    | `1`      | `A`  | `5`        | `4`        |

**Notes:**
- `sender_num` = subsystem that originated the error (e.g. `4` = Jacob)
- Upon receipt: display error on screen, then immediately send Type 14 ack to Adrian

**Example packet:**
AZ21A54YB   ← Error code 5 from Jacob

---

### Message Type 12 — Subsystem Status Response

Sent to me by Adrian in response to my Type 12 request.

| Field         | sender | receiver | type | status_code |
|---------------|--------|----------|------|-------------|
| Variable Type | char   | char     | char | char        |
| Min Value     | `2`    | `1`      | `C`  | `0`         |
| Max Value     | `2`    | `1`      | `C`  | `15`        |
| Example       | `2`    | `1`      | `C`  | `3`         |

**Example packet:**
AZ21C3YB

---

### Message Type 13 — Status Forwarded

Forwarded to me by Adrian with status from another subsystem.

| Field         | sender | receiver | type | sender_num | status_code |
|---------------|--------|----------|------|------------|-------------|
| Variable Type | char   | char     | char | char       | char        |
| Min Value     | `2`    | `1`      | `D`  | `1`        | `0`         |
| Max Value     | `2`    | `1`      | `D`  | `6`        | `15`        |
| Example       | `2`    | `1`      | `D`  | `4`        | `5`         |

**Example packet:**
AZ21D45YB   ← Status from Jacob, code 5

---

### Message Type 15 — Subsystem Status Response

Forwarded to me by Adrian from another subsystem.

| Field         | sender | receiver | type | sender_num | status_code |
|---------------|--------|----------|------|------------|-------------|
| Variable Type | char   | char     | char | char       | char        |
| Min Value     | `2`    | `1`      | `F`  | `1`        | `0`         |
| Max Value     | `2`    | `1`      | `F`  | `6`        | `10`        |
| Example       | `2`    | `1`      | `F`  | `4`        | `5`         |

**Notes:**
- `sender_num` identifies which subsystem sent the status (e.g. `4` = Jacob)
- Type 15 encoded as `F` (0x0F) confirmed from protocol.py

**Example packet:**
AZ21F45YB   ← Status response from Jacob, code 5

---

## Valid Full Packet Reference

| Field  | Prefix | Sender | Receiver | Type Char | Data     | Suffix |
|--------|--------|--------|----------|-----------|----------|--------|
| Value  | `AZ`   | `1`–`6`| `1`–`6`  | See table | Variable | `YB`   |

- All fields are ASCII characters
- Type 67 uses two-char type `43` to avoid collision with Type 12 `C`
- Variable length — no padding required

The software zip folder for this project can be found [*here*](HMI_SUBSYSTEM.zip)

## Final Notes 

I would recomend confirming with your team all the different methods or coding and decoding you plan on doing with your measages. AI has a tendancy of adding advanced processes without telling you and can cause conflict between team members code. Make sure that you and your teammates update the whole team if anyone adjusts their expected measages.