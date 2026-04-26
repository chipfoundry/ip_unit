---
title: CF_TMR32.h

---

# CF_TMR32.h



## Types

|                | Name           |
| -------------- | -------------- |
| enum| **[actions](Files/CF__TMR32_8h.md#enum-actions)** { NONE = 0b00, LOW = 0b01, HIGH = 0b10, INVERT = 0b11} |

## Functions

|                | Name           |
| -------------- | -------------- |
| void | **[CF_TMR32_enable](Files/CF__TMR32_8h.md#function-ef-tmr32-enable)**(uint32_t tmr32_base)<br>enables timer by setting "TE" bit in the CTRL register to 1  |
| void | **[CF_TMR32_restart](Files/CF__TMR32_8h.md#function-ef-tmr32-restart)**(uint32_t tmr32_base)<br>enables timer re-start; used in the one-shot mode to restart the timer.  |
| void | **[CF_TMR32_PWM0Enable](Files/CF__TMR32_8h.md#function-ef-tmr32-pwm0enable)**(uint32_t tmr32_base)<br>enables PWM0 by setting "P0E" bit in the CTRL register to 1  |
| void | **[CF_TMR32_PWM1Enable](Files/CF__TMR32_8h.md#function-ef-tmr32-pwm1enable)**(uint32_t tmr32_base)<br>enables PWM1 by setting "P1E" bit in the CTRL register to 1  |
| void | **[CF_TMR32_deadtimeEnable](Files/CF__TMR32_8h.md#function-ef-tmr32-deadtimeenable)**(uint32_t tmr32_base)<br>enables deadtime by setting "DTE" bit in the CTRL register to 1  |
| void | **[CF_TMR32_PWM0Invert](Files/CF__TMR32_8h.md#function-ef-tmr32-pwm0invert)**(uint32_t tmr32_base)<br>invert PWM0 by setting "P0I" bit in the CTRL register to 1  |
| void | **[CF_TMR32_PWM1Invert](Files/CF__TMR32_8h.md#function-ef-tmr32-pwm1invert)**(uint32_t tmr32_base)<br>invert PWM1 by setting "P1I" bit in the CTRL register to 1  |
| void | **[CF_TMR32_setUpCount](Files/CF__TMR32_8h.md#function-ef-tmr32-setupcount)**(uint32_t tmr32_base)<br>set the timer direction to be up counting  |
| void | **[CF_TMR32_setDownCount](Files/CF__TMR32_8h.md#function-ef-tmr32-setdowncount)**(uint32_t tmr32_base)<br>set the timer direction to be down counting  |
| void | **[CF_TMR32_setUpDownCount](Files/CF__TMR32_8h.md#function-ef-tmr32-setupdowncount)**(uint32_t tmr32_base)<br>set the timer direction to be up/down counting  |
| void | **[CF_TMR32_setPeriodic](Files/CF__TMR32_8h.md#function-ef-tmr32-setperiodic)**(uint32_t tmr32_base)<br>set the timer to be periodic  |
| void | **[CF_TMR32_setOneShot](Files/CF__TMR32_8h.md#function-ef-tmr32-setoneshot)**(uint32_t tmr32_base)<br>set the timer to be one shot  |
| void | **[CF_TMR32_setPWM0MatchingZeroAction](Files/CF__TMR32_8h.md#function-ef-tmr32-setpwm0matchingzeroaction)**(uint32_t tmr32_base, enum [actions](Files/CF__TMR32_8h.md#enum-actions) action)<br>set the action of PWM0 when the timer matches Zero value  |
| void | **[CF_TMR32_setPWM0MatchingCMPXAction](Files/CF__TMR32_8h.md#function-ef-tmr32-setpwm0matchingcmpxaction)**(uint32_t tmr32_base, enum [actions](Files/CF__TMR32_8h.md#enum-actions) action)<br>set the action of PWM0 when the timer matches CMPX value while up counting  |
| void | **[CF_TMR32_setPWM0MatchingCMPYAction](Files/CF__TMR32_8h.md#function-ef-tmr32-setpwm0matchingcmpyaction)**(uint32_t tmr32_base, enum [actions](Files/CF__TMR32_8h.md#enum-actions) action)<br>set the action of PWM0 when the timer matches CMPY value while up counting  |
| void | **[CF_TMR32_setPWM0MatchingRELOADAction](Files/CF__TMR32_8h.md#function-ef-tmr32-setpwm0matchingreloadaction)**(uint32_t tmr32_base, enum [actions](Files/CF__TMR32_8h.md#enum-actions) action)<br>set the action of PWM0 when the timer matches Reload value  |
| void | **[CF_TMR32_setPWM0MatchingCMPYDownCountAction](Files/CF__TMR32_8h.md#function-ef-tmr32-setpwm0matchingcmpydowncountaction)**(uint32_t tmr32_base, enum [actions](Files/CF__TMR32_8h.md#enum-actions) action)<br>set the action of PWM0 when the timer matches CMPX value while down counting  |
| void | **[CF_TMR32_setPWM0MatchingCMPXDownCountAction](Files/CF__TMR32_8h.md#function-ef-tmr32-setpwm0matchingcmpxdowncountaction)**(uint32_t tmr32_base, enum [actions](Files/CF__TMR32_8h.md#enum-actions) action)<br>set the action of PWM0 when the timer matches CMPY value while down counting  |
| void | **[CF_TMR32_setPWM1MatchingZeroAction](Files/CF__TMR32_8h.md#function-ef-tmr32-setpwm1matchingzeroaction)**(uint32_t tmr32_base, enum [actions](Files/CF__TMR32_8h.md#enum-actions) action)<br>set the action of PWM1 when the timer matches Zero value  |
| void | **[CF_TMR32_setPWM1MatchingCMPXAction](Files/CF__TMR32_8h.md#function-ef-tmr32-setpwm1matchingcmpxaction)**(uint32_t tmr32_base, enum [actions](Files/CF__TMR32_8h.md#enum-actions) action)<br>set the action of PWM1 when the timer matches CMPX value while up counting  |
| void | **[CF_TMR32_setPWM1MatchingRELOADAction](Files/CF__TMR32_8h.md#function-ef-tmr32-setpwm1matchingreloadaction)**(uint32_t tmr32_base, enum [actions](Files/CF__TMR32_8h.md#enum-actions) action)<br>set the action of PWM1 when the timer matches Reload value  |
| void | **[CF_TMR32_setPWM1MatchingCMPYDownCountAction](Files/CF__TMR32_8h.md#function-ef-tmr32-setpwm1matchingcmpydowncountaction)**(uint32_t tmr32_base, enum [actions](Files/CF__TMR32_8h.md#enum-actions) action)<br>set the action of PWM1 when the timer matches CMPX value while down counting  |
| void | **[CF_TMR32_setPWM1MatchingCMPXDownCountAction](Files/CF__TMR32_8h.md#function-ef-tmr32-setpwm1matchingcmpxdowncountaction)**(uint32_t tmr32_base, enum [actions](Files/CF__TMR32_8h.md#enum-actions) action)<br>set the action of PWM1 when the timer matches CMPY value while down counting  |
| void | **[CF_TMR32_setRELOAD](Files/CF__TMR32_8h.md#function-ef-tmr32-setreload)**(uint32_t tmr32_base, int value)<br>set the timer reload value  |
| int | **[CF_TMR32_getRELOAD](Files/CF__TMR32_8h.md#function-ef-tmr32-getreload)**(uint32_t tmr32_base)<br>get the timer reload value  |
| void | **[CF_TMR32_setCMPX](Files/CF__TMR32_8h.md#function-ef-tmr32-setcmpx)**(uint32_t tmr32_base, int value)<br>set the CMPX register value  |
| int | **[CF_TMR32_getCMPX](Files/CF__TMR32_8h.md#function-ef-tmr32-getcmpx)**(uint32_t tmr32_base)<br>get the CMPX register value  |
| void | **[CF_TMR32_setCMPY](Files/CF__TMR32_8h.md#function-ef-tmr32-setcmpy)**(uint32_t tmr32_base, int value)<br>set the CMPY register value  |
| int | **[CF_TMR32_getCMPY](Files/CF__TMR32_8h.md#function-ef-tmr32-getcmpy)**(uint32_t tmr32_base)<br>get the CMPY register value  |
| int | **[CF_TMR32_getTMR](Files/CF__TMR32_8h.md#function-ef-tmr32-gettmr)**(uint32_t tmr32_base)<br>get the current value of the timer  |
| void | **[CF_TMR32_setDeadtime](Files/CF__TMR32_8h.md#function-ef-tmr32-setdeadtime)**(uint32_t tmr32_base, int value)<br>set the timer deadtime register value  |

## Types Documentation

### enum actions

| Enumerator | Value | Description |
| ---------- | ----- | ----------- |
| NONE | 0b00|   |
| LOW | 0b01|   |
| HIGH | 0b10|   |
| INVERT | 0b11|   |





## Functions Documentation

### function CF_TMR32_enable

```cpp
void CF_TMR32_enable(
    uint32_t tmr32_base
)
```

enables timer by setting "TE" bit in the CTRL register to 1 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 


### function CF_TMR32_restart

```cpp
void CF_TMR32_restart(
    uint32_t tmr32_base
)
```

enables timer re-start; used in the one-shot mode to restart the timer. 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 


### function CF_TMR32_PWM0Enable

```cpp
void CF_TMR32_PWM0Enable(
    uint32_t tmr32_base
)
```

enables PWM0 by setting "P0E" bit in the CTRL register to 1 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 


### function CF_TMR32_PWM1Enable

```cpp
void CF_TMR32_PWM1Enable(
    uint32_t tmr32_base
)
```

enables PWM1 by setting "P1E" bit in the CTRL register to 1 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 


### function CF_TMR32_deadtimeEnable

```cpp
void CF_TMR32_deadtimeEnable(
    uint32_t tmr32_base
)
```

enables deadtime by setting "DTE" bit in the CTRL register to 1 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 


### function CF_TMR32_PWM0Invert

```cpp
void CF_TMR32_PWM0Invert(
    uint32_t tmr32_base
)
```

invert PWM0 by setting "P0I" bit in the CTRL register to 1 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 


### function CF_TMR32_PWM1Invert

```cpp
void CF_TMR32_PWM1Invert(
    uint32_t tmr32_base
)
```

invert PWM1 by setting "P1I" bit in the CTRL register to 1 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 


### function CF_TMR32_setUpCount

```cpp
void CF_TMR32_setUpCount(
    uint32_t tmr32_base
)
```

set the timer direction to be up counting 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 


### function CF_TMR32_setDownCount

```cpp
void CF_TMR32_setDownCount(
    uint32_t tmr32_base
)
```

set the timer direction to be down counting 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 


### function CF_TMR32_setUpDownCount

```cpp
void CF_TMR32_setUpDownCount(
    uint32_t tmr32_base
)
```

set the timer direction to be up/down counting 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 


### function CF_TMR32_setPeriodic

```cpp
void CF_TMR32_setPeriodic(
    uint32_t tmr32_base
)
```

set the timer to be periodic 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 


### function CF_TMR32_setOneShot

```cpp
void CF_TMR32_setOneShot(
    uint32_t tmr32_base
)
```

set the timer to be one shot 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 


### function CF_TMR32_setPWM0MatchingZeroAction

```cpp
void CF_TMR32_setPWM0MatchingZeroAction(
    uint32_t tmr32_base,
    enum actions action
)
```

set the action of PWM0 when the timer matches Zero value 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 
  * **action** enum actions could be NONE, LOW, HIGH, or INVERT 


### function CF_TMR32_setPWM0MatchingCMPXAction

```cpp
void CF_TMR32_setPWM0MatchingCMPXAction(
    uint32_t tmr32_base,
    enum actions action
)
```

set the action of PWM0 when the timer matches CMPX value while up counting 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 
  * **action** enum actions could be NONE, LOW, HIGH, or INVERT 


### function CF_TMR32_setPWM0MatchingCMPYAction

```cpp
void CF_TMR32_setPWM0MatchingCMPYAction(
    uint32_t tmr32_base,
    enum actions action
)
```

set the action of PWM0 when the timer matches CMPY value while up counting 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 
  * **action** enum actions could be NONE, LOW, HIGH, or INVERT 


### function CF_TMR32_setPWM0MatchingRELOADAction

```cpp
void CF_TMR32_setPWM0MatchingRELOADAction(
    uint32_t tmr32_base,
    enum actions action
)
```

set the action of PWM0 when the timer matches Reload value 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 
  * **action** enum actions could be NONE, LOW, HIGH, or INVERT 


### function CF_TMR32_setPWM0MatchingCMPYDownCountAction

```cpp
void CF_TMR32_setPWM0MatchingCMPYDownCountAction(
    uint32_t tmr32_base,
    enum actions action
)
```

set the action of PWM0 when the timer matches CMPX value while down counting 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 
  * **action** enum actions could be NONE, LOW, HIGH, or INVERT 


### function CF_TMR32_setPWM0MatchingCMPXDownCountAction

```cpp
void CF_TMR32_setPWM0MatchingCMPXDownCountAction(
    uint32_t tmr32_base,
    enum actions action
)
```

set the action of PWM0 when the timer matches CMPY value while down counting 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 
  * **action** enum actions could be NONE, LOW, HIGH, or INVERT 


### function CF_TMR32_setPWM1MatchingZeroAction

```cpp
void CF_TMR32_setPWM1MatchingZeroAction(
    uint32_t tmr32_base,
    enum actions action
)
```

set the action of PWM1 when the timer matches Zero value 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 
  * **action** enum actions could be NONE, LOW, HIGH, or INVERT 


### function CF_TMR32_setPWM1MatchingCMPXAction

```cpp
void CF_TMR32_setPWM1MatchingCMPXAction(
    uint32_t tmr32_base,
    enum actions action
)
```

set the action of PWM1 when the timer matches CMPX value while up counting 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 
  * **action** enum actions could be NONE, LOW, HIGH, or INVERT
  * **tmr32_base** The base memory address of TMR32 registers. 
  * **action** enum actions could be NONE, LOW, HIGH, or INVERT 


set the action of PWM1 when the timer matches CMPY value while up counting


set the action of PWM1 when the timer matches CMPX value while up counting


### function CF_TMR32_setPWM1MatchingRELOADAction

```cpp
void CF_TMR32_setPWM1MatchingRELOADAction(
    uint32_t tmr32_base,
    enum actions action
)
```

set the action of PWM1 when the timer matches Reload value 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 
  * **action** enum actions could be NONE, LOW, HIGH, or INVERT 


### function CF_TMR32_setPWM1MatchingCMPYDownCountAction

```cpp
void CF_TMR32_setPWM1MatchingCMPYDownCountAction(
    uint32_t tmr32_base,
    enum actions action
)
```

set the action of PWM1 when the timer matches CMPX value while down counting 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 
  * **action** enum actions could be NONE, LOW, HIGH, or INVERT 


### function CF_TMR32_setPWM1MatchingCMPXDownCountAction

```cpp
void CF_TMR32_setPWM1MatchingCMPXDownCountAction(
    uint32_t tmr32_base,
    enum actions action
)
```

set the action of PWM1 when the timer matches CMPY value while down counting 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 
  * **action** enum actions could be NONE, LOW, HIGH, or INVERT 


### function CF_TMR32_setRELOAD

```cpp
void CF_TMR32_setRELOAD(
    uint32_t tmr32_base,
    int value
)
```

set the timer reload value 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 
  * **value** timer reload value 


### function CF_TMR32_getRELOAD

```cpp
int CF_TMR32_getRELOAD(
    uint32_t tmr32_base
)
```

get the timer reload value 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 


**Return**: reload register value 

### function CF_TMR32_setCMPX

```cpp
void CF_TMR32_setCMPX(
    uint32_t tmr32_base,
    int value
)
```

set the CMPX register value 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 
  * **value** CMPX value 


### function CF_TMR32_getCMPX

```cpp
int CF_TMR32_getCMPX(
    uint32_t tmr32_base
)
```

get the CMPX register value 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 


**Return**: CMPX register value 

### function CF_TMR32_setCMPY

```cpp
void CF_TMR32_setCMPY(
    uint32_t tmr32_base,
    int value
)
```

set the CMPY register value 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 
  * **value** CMPY value 


### function CF_TMR32_getCMPY

```cpp
int CF_TMR32_getCMPY(
    uint32_t tmr32_base
)
```

get the CMPY register value 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 


**Return**: CMPY register value 

### function CF_TMR32_getTMR

```cpp
int CF_TMR32_getTMR(
    uint32_t tmr32_base
)
```

get the current value of the timer 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 


**Return**: current timer value 

### function CF_TMR32_setDeadtime

```cpp
void CF_TMR32_setDeadtime(
    uint32_t tmr32_base,
    int value
)
```

set the timer deadtime register value 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 
  * **value** deadtime register value 




## Source code

```cpp
#ifndef CF_UART_H
#define CF_UART_H

#include <CF_TMR32_regs.h>
#include <stdint.h>
#include <stdbool.h>

enum actions {NONE = 0b00, LOW = 0b01, HIGH = 0b10, INVERT = 0b11};


void CF_TMR32_enable(uint32_t tmr32_base);


void CF_TMR32_restart(uint32_t tmr32_base);


void CF_TMR32_PWM0Enable(uint32_t tmr32_base);


void CF_TMR32_PWM1Enable(uint32_t tmr32_base);


void CF_TMR32_deadtimeEnable(uint32_t tmr32_base);


void CF_TMR32_PWM0Invert(uint32_t tmr32_base);


void CF_TMR32_PWM1Invert(uint32_t tmr32_base);


void CF_TMR32_setUpCount(uint32_t tmr32_base);


void CF_TMR32_setDownCount(uint32_t tmr32_base);


void CF_TMR32_setUpDownCount(uint32_t tmr32_base);


void CF_TMR32_setPeriodic(uint32_t tmr32_base);


void CF_TMR32_setOneShot(uint32_t tmr32_base);


void CF_TMR32_setPWM0MatchingZeroAction(uint32_t tmr32_base, enum actions action);


void CF_TMR32_setPWM0MatchingCMPXAction(uint32_t tmr32_base, enum actions action);


void CF_TMR32_setPWM0MatchingCMPYAction(uint32_t tmr32_base, enum actions action);


void CF_TMR32_setPWM0MatchingRELOADAction(uint32_t tmr32_base, enum actions action);


void CF_TMR32_setPWM0MatchingCMPYDownCountAction(uint32_t tmr32_base, enum actions action);


void CF_TMR32_setPWM0MatchingCMPXDownCountAction(uint32_t tmr32_base, enum actions action);


void CF_TMR32_setPWM1MatchingZeroAction(uint32_t tmr32_base, enum actions action);


void CF_TMR32_setPWM1MatchingCMPXAction(uint32_t tmr32_base, enum actions action);


void CF_TMR32_setPWM1MatchingCMPXAction(uint32_t tmr32_base, enum actions action);


void CF_TMR32_setPWM1MatchingRELOADAction(uint32_t tmr32_base, enum actions action);


void CF_TMR32_setPWM1MatchingCMPYDownCountAction(uint32_t tmr32_base, enum actions action);


void CF_TMR32_setPWM1MatchingCMPXDownCountAction(uint32_t tmr32_base, enum actions action);


void CF_TMR32_setRELOAD (uint32_t tmr32_base, int value);


int CF_TMR32_getRELOAD (uint32_t tmr32_base);


void CF_TMR32_setCMPX (uint32_t tmr32_base, int value);


int CF_TMR32_getCMPX (uint32_t tmr32_base);


void CF_TMR32_setCMPY (uint32_t tmr32_base, int value);


int CF_TMR32_getCMPY (uint32_t tmr32_base);


int CF_TMR32_getTMR (uint32_t tmr32_base);


void CF_TMR32_setDeadtime (uint32_t tmr32_base, int value);

#endif
```


-------------------------------

Updated on 2024-04-07 at 13:02:30 +0200
