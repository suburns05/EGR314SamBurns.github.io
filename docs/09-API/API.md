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
| Sam B (me) | 1               |
| Adrian P   | 2               |
| Andrew I   | 3               |
| Jacob D    | 4               |
| Sam M      | 5               |
| Mo A       | 6               |

---

## Messages Sent

All messages I send go directly to Adrian (Subsystem 2).

---

### Message Type 1 — Set Motor Speed (Joystick 1 Input)

Sent to Adrian when the user moves Joystick 1. One message carries both axes:
X-axis controls forward/reverse, Y-axis controls left/right. Speed increases
with deflection from center on each axis.

| Field         | Byte 1       | Byte 2        | Byte 3          | Byte 4       | Byte 5        | Byte 6         | Byte 7       | Byte 8        |
|---------------|--------------|---------------|-----------------|--------------|---------------|----------------|--------------|---------------|
| Variable Name | message_type | sender_subsys | receiver_subsys | x_speed      | x_direction   | y_speed        | y_direction  | unused        |
| Variable Type | uint8_t      | uint8_t       | uint8_t         | uint8_t      | uint8_t       | uint8_t        | uint8_t      | uint8_t       |
| Min Value     | 1            | 1             | 2               | 0            | 0             | 0              | 0            | 0             |
| Max Value     | 1            | 1             | 2               | 15           | 1             | 15             | 1            | 0             |
| Example       | 1            | 1             | 2               | 8            | 0             | 4              | 1            | 0             |

**Notes:**
- `x_speed`: Joystick X-axis deflection mapped to 0–15 (0 = center/stopped)
- `x_direction`: 0 = forward, 1 = reverse
- `y_speed`: Joystick Y-axis deflection mapped to 0–15 (0 = center/stopped)
- `y_direction`: 0 = left, 1 = right
- Speed increases with distance from joystick center on each axis
- Byte 8 padded with 0x00

**Example packet:**
```
415A0102 01010208000401 ... 5942
```
*(x_speed=8 forward, y_speed=4 right)*

---

### Message Type 12 — Subsystem Status Request

Sent to Adrian to request a status update from the system.

| Field         | Byte 1       | Byte 2        | Byte 3          |
|---------------|--------------|---------------|-----------------|
| Variable Name | message_type | sender_subsys | receiver_subsys |
| Variable Type | uint8_t      | uint8_t       | uint8_t         |
| Min Value     | 12           | 1             | 2               |
| Max Value     | 12           | 1             | 2               |
| Example       | 12           | 1             | 2               |

**Notes:**
- No additional data needed — Adrian handles routing the status check
- Sent when user requests a system status check via HMI

**Example packet:**
```
415A0102 0C0102000000 ... 5942
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
415A0102 0A010200000000 ... 5942
```

---

### Message Type 67 — Button Pressed (Joystick Click-In)

Sent to Adrian when the user clicks in either joystick. Carries the current
toggle state so Adrian can act on it directly.

| Field         | Byte 1       | Byte 2        | Byte 3          | Byte 4        | Byte 5       |
|---------------|--------------|---------------|-----------------|---------------|--------------|
| Variable Name | message_type | sender_subsys | receiver_subsys | button_number | button_state |
| Variable Type | uint8_t      | uint8_t       | uint8_t         | uint8_t       | uint8_t      |
| Min Value     | 0x43         | 1             | 2               | 1             | 0            |
| Max Value     | 0x43         | 1             | 2               | 2             | 1            |
| Example       | 0x43         | 1             | 2               | 1             | 1            |

**Notes:**
- `button_number`: 1 = Joystick 1 click-in, 2 = Joystick 2 click-in
- `button_state`: 0 = off, 1 = on — HMI tracks state and sends current value on press

**Example packet:**
```
// Button 1 ON:
415A0102 430102010100 ... 5942

// Button 1 OFF:
415A0102 430102010000 ... 5942
```

---

## Messages Received

All messages I receive come directly from Adrian (Subsystem 2).

---

### Message Type 2 — Motor Info Display

Forwarded to me by Adrian from Jacob. I display current motor state on screen.

| Field         | Byte 1       | Byte 2        | Byte 3          | Byte 4   | Byte 5      | Byte 6          |
|---------------|--------------|---------------|-----------------|----------|-------------|-----------------|
| Variable Name | message_type | sender_subsys | receiver_subsys | motor_id | motor_speed | motor_direction |
| Variable Type | uint8_t      | uint8_t       | uint8_t         | uint8_t  | int8_t      | int8_t          |
| Min Value     | 2            | 2             | 1               | 1        | 0           | 0               |
| Max Value     | 2            | 2             | 1               | 3        | 15          | 1               |
| Example       | 2            | 2             | 1               | 2        | 8           | 0               |

**Example packet:**
```
415A0201 020201020800 ... 5942
```

---

### Message Type 3 — Sensor Value Display

Forwarded to me by Adrian. I display this sensor reading on screen.

| Field         | Byte 1       | Byte 2        | Byte 3          | Byte 4        | Byte 5             | Byte 6             |
|---------------|--------------|---------------|-----------------|---------------|--------------------|--------------------|
| Variable Name | message_type | sender_subsys | receiver_subsys | sensor_number | sensor_value_upper | sensor_value_lower |
| Variable Type | uint8_t      | uint8_t       | uint8_t         | uint8_t       | uint8_t            | uint8_t            |
| Min Value     | 3            | 2             | 1               | 1             | 0                  | 0                  |
| Max Value     | 3            | 2             | 1               | 3             | 255                | 255                |
| Example       | 3            | 2             | 1               | 1             | 0x01               | 0x2C               |

**Notes:**
- Reconstruct full value: `sensor_value = (sensor_value_upper << 8) | sensor_value_lower`
- Example: `(0x01 << 8) | 0x2C = 300`

**Example packet:**
```
415A0201 03020101012C ... 5942
```

---

### Message Type 12 — Subsystem Status Response

Sent to me by Adrian containing a status code to display.

| Field         | Byte 1       | Byte 2        | Byte 3          | Byte 4 |
|---------------|--------------|---------------|-----------------|--------|
| Variable Name | message_type | sender_subsys | receiver_subsys | code   |
| Variable Type | uint8_t      | uint8_t       | uint8_t         | uint8_t|
| Min Value     | 12           | 2             | 1               | 0      |
| Max Value     | 12           | 2             | 1               | 15     |
| Example       | 12           | 2             | 1               | 3      |

**Example packet:**
```
415A0201 0C020103000000 ... 5942
```

---

### Message Type 14 — Subsystem Error Alert

Forwarded to me by Adrian. I display the error on screen and send an
acknowledgement back to Adrian.

| Field         | Byte 1       | Byte 2        | Byte 3          | Byte 4     | Byte 5     |
|---------------|--------------|---------------|-----------------|------------|------------|
| Variable Name | message_type | sender_subsys | receiver_subsys | error_code | sender_num |
| Variable Type | uint8_t      | uint8_t       | uint8_t         | int8_t     | uint8_t    |
| Min Value     | 10           | 2             | 1               | 0          | 1          |
| Max Value     | 10           | 2             | 1               | 64         | 6          |
| Example       | 10           | 2             | 1               | 10         | 4          |

**Notes:**
- `sender_num` identifies which subsystem originated the error (e.g. 4 = Jacob)
- Upon receipt, display error then immediately send a Type 14 ack back to Adrian

**Example packet:**
```
415A0201 0A02010A04000000 ... 5942
```

---

### Message Type 15 — Subsystem Status Response

Forwarded to me by Adrian. I display subsystem status on screen.

| Field         | Byte 1       | Byte 2        | Byte 3          | Byte 4     | Byte 5      |
|---------------|--------------|---------------|-----------------|------------|-------------|
| Variable Name | message_type | sender_subsys | receiver_subsys | sender_num | status_code |
| Variable Type | uint8_t      | uint8_t       | uint8_t         | uint8_t    | int8_t      |
| Min Value     | 13           | 2             | 1               | 1          | 0           |
| Max Value     | 13           | 2             | 1               | 6          | 10          |
| Example       | 13           | 2             | 1               | 4          | 5           |

**Notes:**
- `sender_num` identifies which subsystem sent the status (e.g. 4 = Jacob)
- `status_code` meaning to be confirmed with team

**Example packet:**
```
415A0201 0D020104050000 ... 5942
```

The software of this API download is available [*here*](pending.pdf), and the Zip folder of the project [*here*](ending.zip).