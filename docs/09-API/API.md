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

Sent to Adrian when the user moves Joystick 1. The X-axis maps to motor speed
(0–255) and the Y-axis maps to motor direction (0=forward, 1=reverse).

| Field         | Byte 1-2     | Byte 3         | Byte 4          | Byte 5         | Byte 6              | Byte 7              | Byte 8           |
|---------------|--------------|----------------|-----------------|----------------|---------------------|---------------------|------------------|
| Variable Name | message_type | sender_subsys  | receiver_subsys | motor_number   | motor_speed_upper   | motor_speed_lower   | motor_direction  |
| Variable Type | uint16_t     | uint8_t        | uint8_t         | uint8_t        | uint8_t             | uint8_t             | uint8_t          |
| Min Value     | 0x01         | 1              | 2               | 1              | 0                   | 0                   | 0                |
| Max Value     | 0x01         | 1              | 2               | 255            | 0                   | 255                 | 1                |
| Example       | 0x01         | 1              | 2               | 1              | 0x00                | 0x80                | 0                |

**Notes:**
- `sender_subsys` always 1 (me), `receiver_subsys` always 2 (Adrian)
- Joystick X-axis (0–255) maps directly to `motor_speed_lower`
- `motor_speed_upper` is always 0x00 since our range is 0–255 (fits in one byte)
- Joystick Y-axis: center-to-top = forward (0), center-to-bottom = reverse (1)
- Example: speed 128, forward → `(0x00 << 8) | 0x80 = 128`

---

### Message Type 67 — Button Pressed (Joystick Click-In)

Sent to Adrian when the user clicks in either joystick. Carries the current toggle
state so Adrian can act on it directly without tracking state himself.

| Field         | Byte 1-2     | Byte 3         | Byte 4          | Byte 5        | Byte 6       | Bytes 7-8 |
|---------------|--------------|----------------|-----------------|---------------|--------------|-----------|
| Variable Name | message_type | sender_subsys  | receiver_subsys | button_number | button_state | unused    |
| Variable Type | uint16_t     | uint8_t        | uint8_t         | uint8_t       | uint8_t      | uint8_t   |
| Min Value     | 0x43         | 1              | 2               | 1             | 0            | 0         |
| Max Value     | 0x43         | 1              | 2               | 2             | 1            | 0         |
| Example       | 0x43         | 1              | 2               | 1             | 1            | 0x00      |

**Notes:**
- `button_number`: 1 = Joystick 1 click-in, 2 = Joystick 2 click-in
- `button_state`: 0 = off, 1 = on — you track state on the HMI side and send
  the current value on each press
- Bytes 7–8 padded with 0x00
```

**Updated packet example:**
```
// Button 1, turned ON:
0x41 0x5A 0x01 0x02 | 0x43 0x01 0x02 0x01 0x01 0x00 0x00 0x00 | ... 0x59 0x42

// Button 1, turned OFF:
0x41 0x5A 0x01 0x02 | 0x43 0x01 0x02 0x01 0x00 0x00 0x00 0x00 | ... 0x59 0x42

---

## Messages Received

All messages I receive come directly from Adrian (0x02).

---

### Message Type 3 — Sensor Value Display

Forwarded to me by Adrian. I display this sensor reading on screen.

| Field         | Byte 1-2     | Byte 3         | Byte 4          | Byte 5        | Byte 6               | Byte 7               | Byte 8  |
|---------------|--------------|----------------|-----------------|---------------|----------------------|----------------------|---------|
| Variable Name | message_type | sender_subsys  | receiver_subsys | sensor_number | sensor_value_upper   | sensor_value_lower   | unused  |
| Variable Type | uint16_t     | uint8_t        | uint8_t         | uint8_t       | uint8_t              | uint8_t              | uint8_t |
| Min Value     | 0x03         | 2              | 1               | 1             | 0                    | 0                    | 0       |
| Max Value     | 0x03         | 2              | 1               | 255           | 255                  | 255                  | 0       |
| Example       | 0x03         | 2              | 1               | 1             | 0x01                 | 0x2C                 | 0x00    |

**Notes:**
- `sender_subsys` always 2 (Adrian), `receiver_subsys` always 1 (me)
- Reconstruct full value: `sensor_value = (sensor_value_upper << 8) | sensor_value_lower`
- Example: `(0x01 << 8) | 0x2C = 300`
- Byte 8 padded with 0x00

---

### Message Type 12 — Subsystem Status Code

Sent to me by Adrian, summarizing the status of a subsystem as a numeric code.

| Field         | Byte 1-2     | Byte 3         | Byte 4          | Byte 5       | Byte 6       | Bytes 7-8 |
|---------------|--------------|----------------|-----------------|--------------|--------------|-----------|
| Variable Name | message_type | sender_subsys  | receiver_subsys | status_upper | status_lower | unused    |
| Variable Type | uint16_t     | uint8_t        | uint8_t         | uint8_t      | uint8_t      | uint8_t   |
| Min Value     | 0x0C         | 2              | 1               | 0            | 0            | 0         |
| Max Value     | 0x0C         | 2              | 1               | 255          | 255          | 0         |
| Example       | 0x0C         | 2              | 1               | 0x00         | 0x01         | 0x00      |

**Notes:**
- `sender_subsys` always 2 (Adrian), `receiver_subsys` always 1 (me)
- Reconstruct: `full_status = (status_upper << 8) | status_lower`
- Example: status code 1 = system OK (confirm codes with team)
- Bytes 7–8 padded with 0x00

---

### Message Type 13 — Subsystem Status Message

A human-readable status string from Adrian to display on my screen.

| Field         | Byte 1-2     | Byte 3         | Byte 4          | Bytes 5-8     |
|---------------|--------------|----------------|-----------------|---------------|
| Variable Name | message_type | sender_subsys  | receiver_subsys | status_string |
| Variable Type | uint16_t     | uint8_t        | uint8_t         | char[]        |
| Min Value     | 0x0D         | 2              | 1               | N/A           |
| Max Value     | 0x0D         | 2              | 1               | N/A           |
| Example       | 0x0D         | 2              | 1               | "OK\0"        |

**Notes:**
- `sender_subsys` always 2 (Adrian), `receiver_subsys` always 1 (me)
- Null-terminated ASCII string, max 4 characters in bytes 5–8
- Unused bytes padded with 0x00

---

## Valid Full Packet Examples

Message data fits inside the class protocol frame:

| Byte  | 1    | 2    | 3         | 4       | 5–62         | 63   | 64   |
|-------|------|------|-----------|---------|--------------|------|------|
| Field | 0x41 | 0x5A | Source ID | Dest ID | Message Data | 0x59 | 0x42 |

**Sending — Joystick 1, speed 128, forward (Type 1, me → Adrian):**
```
0x41 0x5A 0x01 0x02 | 0x01 0x01 0x02 0x01 0x00 0x80 0x00 0x00 | ... 0x59 0x42
```

**Sending — Joystick 1 click-in pressed (Type 67, button 1, me → Adrian):**
```
0x41 0x5A 0x01 0x02 | 0x43 0x01 0x02 0x01 0x00 0x00 0x00 0x00 | ... 0x59 0x42
```

**Receiving — Sensor value 300, sensor 1 (Type 3, Adrian → me):**
```
0x41 0x5A 0x02 0x01 | 0x03 0x02 0x01 0x01 0x01 0x2C 0x00 0x00 | ... 0x59 0x42
```

**Receiving — Status code 1 (Type 12, Adrian → me):**
```
0x41 0x5A 0x02 0x01 | 0x0C 0x02 0x01 0x00 0x01 0x00 0x00 0x00 | ... 0x59 0x42
```

**Receiving — Status message "OK" (Type 13, Adrian → me):**
```
0x41 0x5A 0x02 0x01 | 0x0D 0x02 0x01 0x4F 0x4B 0x00 0x00 0x00 | ... 0x59 0x42
```