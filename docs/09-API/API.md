---
title: API
---

## HMI Subsystem

My role is the HMI subsystem. I allow the user to control the project via two
joysticks and two click-in buttons. I display sensor data and system status updates
on screen. My subsystem communicates with Adrian (ID 2) directly over LAN, with
wired UART as a fallback. I am not physically in the daisy chain — all my
communication goes to and from Adrian only.

The second joystick is used internally for screen navigation and does not generate
any UART messages.

## Team Member IDs

| Individual | Subsystem Number |
|------------|-----------------|
| Sam B (me) | 1 (0x01)        |
| Adrian P   | 2 (0x02)        |
| Andrew I   | 3 (0x03)        |
| Jacob D    | 4 (0x04)        |
| Sam M      | 5 (0x05)        |
| Mo A       | 6 (0x06)        |

---

## Messages Sent

All messages I send go directly to Adrian (0x02).

---

### Message Type 1 — Set Motor Speed (Joystick 1 Input)

Sent to Adrian when the user moves Joystick 1.

| Field         | Byte 1       | Byte 2        | Byte 3          | Byte 4       | Byte 5      | Byte 6          |
|---------------|--------------|---------------|-----------------|--------------|-------------|-----------------|
| Variable Name | message_type | sender_subsys | receiver_subsys | motor_number | motor_speed | motor_direction |
| Variable Type | uint8_t      | uint8_t       | uint8_t         | uint8_t      | int8_t      | int8_t          |
| Min Value     | 1            | 1             | 2               | 1            | 0           | 0               |
| Max Value     | 1            | 1             | 2               | 2            | 15          | 1               |
| Example       | 1            | 1             | 2               | 1            | 4           | 1               |

**Notes:**
- Joystick 1 X-axis (0–15) → `motor_speed`
- `motor_direction`: 0 = forward, 1 = reverse

**Example packet:**
```
0x41 0x5A 0x01 0x02 | 0x01 0x01 0x02 0x01 0x04 0x01 0x00 ... | 0x59 0x42
```

---

### Message Type 14 — Error Acknowledgement

Sent to Adrian in response to a Type 14 error alert. Confirms the HMI received
and displayed the error. Error codes are still being defined by the team.

| Field         | Byte 1       | Byte 2        | Byte 3          | Byte 4     |
|---------------|--------------|---------------|-----------------|------------|
| Variable Name | message_type | sender_subsys | receiver_subsys | error_code |
| Variable Type | uint8_t      | uint8_t       | uint8_t         | int8_t     |
| Min Value     | 10           | 1             | 2               | 0          |
| Max Value     | 10           | 1             | 2               | 64         |
| Example       | 10           | 1             | 2               | 0          |

**Notes:**
- Sent immediately after displaying a received Type 14 error
- `error_code` echoes back the code received — full error decode table TBD with team

**Example packet:**
```
0x41 0x5A 0x01 0x02 | 0x0A 0x01 0x02 0x00 0x00 ... | 0x59 0x42
```

---

### Message Type 67 — Button Pressed (Joystick Click-In)

Sent to Adrian when the user clicks in either joystick.

| Field         | Byte 1       | Byte 2        | Byte 3          | Byte 4        | Byte 5       |
|---------------|--------------|---------------|-----------------|---------------|--------------|
| Variable Name | message_type | sender_subsys | receiver_subsys | button_number | button_state |
| Variable Type | uint8_t      | uint8_t       | uint8_t         | uint8_t       | uint8_t      |
| Min Value     | 0x43         | 1             | 2               | 1             | 0            |
| Max Value     | 0x43         | 1             | 2               | 2             | 1            |
| Example       | 0x43         | 1             | 2               | 1             | 1            |

**Notes:**
- `button_number`: 1 = Joystick 1 click-in, 2 = Joystick 2 click-in
- `button_state`: 0 = off, 1 = on — HMI tracks and sends current state on each press

**Example packet:**
```
// Button 1 ON:
0x41 0x5A 0x01 0x02 | 0x43 0x01 0x02 0x01 0x01 0x00 ... | 0x59 0x42

// Button 1 OFF:
0x41 0x5A 0x01 0x02 | 0x43 0x01 0x02 0x01 0x00 0x00 ... | 0x59 0x42
```

---

## Messages Received

All messages I receive come directly from Adrian (0x02).

---

### Message Type 2 — Motor Info Display

Forwarded to me by Adrian from Jacob. I display current motor state on screen.

| Field         | Byte 1       | Byte 2        | Byte 3          | Byte 4   | Byte 5      | Byte 6          |
|---------------|--------------|---------------|-----------------|----------|-------------|-----------------|
| Variable Name | message_type | sender_subsys | receiver_subsys | motor_id | motor_speed | motor_direction |
| Variable Type | uint8_t      | uint8_t       | uint8_t         | uint8_t  | int8_t      | int8_t          |
| Min Value     | 2            | 2             | 1               | 2        | 0           | 0               |
| Max Value     | 2            | 2             | 1               | 2        | 15          | 1               |
| Example       | 2            | 2             | 1               | 4        | 0           | 0               |

**Example packet:**
```
0x41 0x5A 0x02 0x01 | 0x02 0x02 0x01 0x04 0x00 0x00 ... | 0x59 0x42
```

---

### Message Type 3 — Sensor Value Display

Forwarded to me by Adrian. I display this sensor reading on screen.

| Field         | Byte 1       | Byte 2        | Byte 3          | Byte 4        | Byte 5             | Byte 6             |
|---------------|--------------|---------------|-----------------|---------------|--------------------|--------------------|
| Variable Name | message_type | sender_subsys | receiver_subsys | sensor_number | sensor_value_upper | sensor_value_lower |
| Variable Type | uint8_t      | uint8_t       | uint8_t         | uint8_t       | uint8_t            | uint8_t            |
| Min Value     | 3            | 2             | 1               | 1             | 0                  | 0                  |
| Max Value     | 3            | 2             | 1               | 255           | 255                | 255                |
| Example       | 3            | 2             | 1               | 1             | 0x01               | 0x2C               |

**Notes:**
- Reconstruct: `sensor_value = (sensor_value_upper << 8) | sensor_value_lower`
- Example: `(0x01 << 8) | 0x2C = 300`

**Example packet:**
```
0x41 0x5A 0x02 0x01 | 0x03 0x02 0x01 0x01 0x01 0x2C 0x00 ... | 0x59 0x42
```

---

### Message Type 12 — Subsystem Status Request

Sent to me by Adrian containing a status request code to display.

| Field         | Byte 1       | Byte 2        | Byte 3 |
|---------------|--------------|---------------|--------|
| Variable Name | message_type | sender_subsys | code   |
| Variable Type | uint8_t      | uint8_t       | uint8_t|
| Min Value     | 12           | 2             | 0      |
| Max Value     | 12           | 2             | 15     |
| Example       | 12           | 2             | 3      |

**Example packet:**
```
0x41 0x5A 0x02 0x01 | 0x0C 0x02 0x01 0x03 0x00 ... | 0x59 0x42
```

---

### Message Type 14 — Subsystem Error Alert

Forwarded to me by Adrian. I display the error on screen and send an
acknowledgement back to Adrian.

| Field         | Byte 1       | Byte 2        | Byte 3     | Byte 4     |
|---------------|--------------|---------------|------------|------------|
| Variable Name | message_type | sender_subsys | error_code | sender_num |
| Variable Type | uint8_t      | uint8_t       | int8_t     | uint8_t    |
| Min Value     | 10           | 2             | 0          | 4          |
| Max Value     | 10           | 2             | 64         | 4          |
| Example       | 10           | 2             | 10         | 4          |

**Notes:**
- `sender_num` identifies which subsystem originated the error (e.g. 4 = Jacob)
- Upon receipt, display error then immediately send a Type 14 ack back to Adrian

**Example packet:**
```
0x41 0x5A 0x02 0x01 | 0x0A 0x02 0x01 0x0A 0x04 0x00 ... | 0x59 0x42
```

---

### Message Type 15 — Subsystem Status Response

Forwarded to me by Adrian. I display subsystem status on screen.

| Field         | Byte 1       | Byte 2        | Byte 3     | Byte 4      |
|---------------|--------------|---------------|------------|-------------|
| Variable Name | message_type | sender_subsys | sender_num | status_code |
| Variable Type | uint8_t      | uint8_t       | uint8_t    | int8_t      |
| Min Value     | 13           | 2             | 4          | 0           |
| Max Value     | 13           | 2             | 4          | 10          |
| Example       | 13           | 2             | 4          | 5           |

**Notes:**
- `sender_num` identifies which subsystem sent the status (e.g. 4 = Jacob)
- `status_code` meaning to be confirmed with team

**Example packet:**
```
0x41 0x5A 0x02 0x01 | 0x0D 0x02 0x01 0x04 0x05 0x00 ... | 0x59 0x42
```

---

## Valid Full Packet Reference

| Byte  | 1    | 2    | 3         | 4       | 5–62         | 63   | 64   |
|-------|------|------|-----------|---------|--------------|------|------|
| Field | 0x41 | 0x5A | Source ID | Dest ID | Message Data | 0x59 | 0x42 |

- Prefix: `0x41 0x5A`
- Suffix: `0x59 0x42`
- All unused bytes padded with `0x00`