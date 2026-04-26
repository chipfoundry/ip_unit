---
title: CF_TMR32.c

---

# CF_TMR32.c



## Functions

|                | Name           |
| -------------- | -------------- |
| void | **[CF_TMR32_enable](Files/CF__TMR32_8c.md#function-ef-tmr32-enable)**(uint32_t tmr32_base)<br>enables timer by setting "TE" bit in the CTRL register to 1  |
| void | **[CF_TMR32_restart](Files/CF__TMR32_8c.md#function-ef-tmr32-restart)**(uint32_t tmr32_base)<br>enables timer re-start; used in the one-shot mode to restart the timer.  |
| void | **[CF_TMR32_PWM0Enable](Files/CF__TMR32_8c.md#function-ef-tmr32-pwm0enable)**(uint32_t tmr32_base)<br>enables PWM0 by setting "P0E" bit in the CTRL register to 1  |
| void | **[CF_TMR32_PWM1Enable](Files/CF__TMR32_8c.md#function-ef-tmr32-pwm1enable)**(uint32_t tmr32_base)<br>enables PWM1 by setting "P1E" bit in the CTRL register to 1  |
| void | **[CF_TMR32_deadtimeEnable](Files/CF__TMR32_8c.md#function-ef-tmr32-deadtimeenable)**(uint32_t tmr32_base)<br>enables deadtime by setting "DTE" bit in the CTRL register to 1  |
| void | **[CF_TMR32_PWM0Invert](Files/CF__TMR32_8c.md#function-ef-tmr32-pwm0invert)**(uint32_t tmr32_base)<br>invert PWM0 by setting "P0I" bit in the CTRL register to 1  |
| void | **[CF_TMR32_PWM1Invert](Files/CF__TMR32_8c.md#function-ef-tmr32-pwm1invert)**(uint32_t tmr32_base)<br>invert PWM1 by setting "P1I" bit in the CTRL register to 1  |
| void | **[CF_TMR32_setUpCount](Files/CF__TMR32_8c.md#function-ef-tmr32-setupcount)**(uint32_t tmr32_base)<br>set the timer direction to be up counting  |
| void | **[CF_TMR32_setDownCount](Files/CF__TMR32_8c.md#function-ef-tmr32-setdowncount)**(uint32_t tmr32_base)<br>set the timer direction to be down counting  |
| void | **[CF_TMR32_setUpDownCount](Files/CF__TMR32_8c.md#function-ef-tmr32-setupdowncount)**(uint32_t tmr32_base)<br>set the timer direction to be up/down counting  |
| void | **[CF_TMR32_setPeriodic](Files/CF__TMR32_8c.md#function-ef-tmr32-setperiodic)**(uint32_t tmr32_base)<br>set the timer to be periodic  |
| void | **[CF_TMR32_setOneShot](Files/CF__TMR32_8c.md#function-ef-tmr32-setoneshot)**(uint32_t tmr32_base)<br>set the timer to be one shot  |
| void | **[CF_TMR32_setPWM0MatchingZeroAction](Files/CF__TMR32_8c.md#function-ef-tmr32-setpwm0matchingzeroaction)**(uint32_t tmr32_base, enum [actions](Files/CF__TMR32_8h.md#enum-actions) action)<br>set the action of PWM0 when the timer matches Zero value  |
| void | **[CF_TMR32_setPWM0MatchingCMPXAction](Files/CF__TMR32_8c.md#function-ef-tmr32-setpwm0matchingcmpxaction)**(uint32_t tmr32_base, enum [actions](Files/CF__TMR32_8h.md#enum-actions) action)<br>set the action of PWM0 when the timer matches CMPX value while up counting  |
| void | **[CF_TMR32_setPWM0MatchingCMPYAction](Files/CF__TMR32_8c.md#function-ef-tmr32-setpwm0matchingcmpyaction)**(uint32_t tmr32_base, enum [actions](Files/CF__TMR32_8h.md#enum-actions) action)<br>set the action of PWM0 when the timer matches CMPY value while up counting  |
| void | **[CF_TMR32_setPWM0MatchingRELOADAction](Files/CF__TMR32_8c.md#function-ef-tmr32-setpwm0matchingreloadaction)**(uint32_t tmr32_base, enum [actions](Files/CF__TMR32_8h.md#enum-actions) action)<br>set the action of PWM0 when the timer matches Reload value  |
| void | **[CF_TMR32_setPWM0MatchingCMPYDownCountAction](Files/CF__TMR32_8c.md#function-ef-tmr32-setpwm0matchingcmpydowncountaction)**(uint32_t tmr32_base, enum [actions](Files/CF__TMR32_8h.md#enum-actions) action)<br>set the action of PWM0 when the timer matches CMPX value while down counting  |
| void | **[CF_TMR32_setPWM0MatchingCMPXDownCountAction](Files/CF__TMR32_8c.md#function-ef-tmr32-setpwm0matchingcmpxdowncountaction)**(uint32_t tmr32_base, enum [actions](Files/CF__TMR32_8h.md#enum-actions) action)<br>set the action of PWM0 when the timer matches CMPY value while down counting  |
| void | **[CF_TMR32_setPWM1MatchingZeroAction](Files/CF__TMR32_8c.md#function-ef-tmr32-setpwm1matchingzeroaction)**(uint32_t tmr32_base, enum [actions](Files/CF__TMR32_8h.md#enum-actions) action)<br>set the action of PWM1 when the timer matches Zero value  |
| void | **[CF_TMR32_setPWM1MatchingCMPXAction](Files/CF__TMR32_8c.md#function-ef-tmr32-setpwm1matchingcmpxaction)**(uint32_t tmr32_base, enum [actions](Files/CF__TMR32_8h.md#enum-actions) action)<br>set the action of PWM1 when the timer matches CMPY value while up counting  |
| void | **[CF_TMR32_setPWM1MatchingCMPYAction](Files/CF__TMR32_8c.md#function-ef-tmr32-setpwm1matchingcmpyaction)**(uint32_t tmr32_base, enum [actions](Files/CF__TMR32_8h.md#enum-actions) action) |
| void | **[CF_TMR32_setPWM1MatchingRELOADAction](Files/CF__TMR32_8c.md#function-ef-tmr32-setpwm1matchingreloadaction)**(uint32_t tmr32_base, enum [actions](Files/CF__TMR32_8h.md#enum-actions) action)<br>set the action of PWM1 when the timer matches Reload value  |
| void | **[CF_TMR32_setPWM1MatchingCMPYDownCountAction](Files/CF__TMR32_8c.md#function-ef-tmr32-setpwm1matchingcmpydowncountaction)**(uint32_t tmr32_base, enum [actions](Files/CF__TMR32_8h.md#enum-actions) action)<br>set the action of PWM1 when the timer matches CMPX value while down counting  |
| void | **[CF_TMR32_setPWM1MatchingCMPXDownCountAction](Files/CF__TMR32_8c.md#function-ef-tmr32-setpwm1matchingcmpxdowncountaction)**(uint32_t tmr32_base, enum [actions](Files/CF__TMR32_8h.md#enum-actions) action)<br>set the action of PWM1 when the timer matches CMPY value while down counting  |
| void | **[CF_TMR32_setRELOAD](Files/CF__TMR32_8c.md#function-ef-tmr32-setreload)**(uint32_t tmr32_base, int value)<br>set the timer reload value  |
| int | **[CF_TMR32_getRELOAD](Files/CF__TMR32_8c.md#function-ef-tmr32-getreload)**(uint32_t tmr32_base)<br>get the timer reload value  |
| void | **[CF_TMR32_setCMPX](Files/CF__TMR32_8c.md#function-ef-tmr32-setcmpx)**(uint32_t tmr32_base, int value)<br>set the CMPX register value  |
| int | **[CF_TMR32_getCMPX](Files/CF__TMR32_8c.md#function-ef-tmr32-getcmpx)**(uint32_t tmr32_base)<br>get the CMPX register value  |
| void | **[CF_TMR32_setCMPY](Files/CF__TMR32_8c.md#function-ef-tmr32-setcmpy)**(uint32_t tmr32_base, int value)<br>set the CMPY register value  |
| int | **[CF_TMR32_getCMPY](Files/CF__TMR32_8c.md#function-ef-tmr32-getcmpy)**(uint32_t tmr32_base)<br>get the CMPY register value  |
| int | **[CF_TMR32_getTMR](Files/CF__TMR32_8c.md#function-ef-tmr32-gettmr)**(uint32_t tmr32_base)<br>get the current value of the timer  |
| void | **[CF_TMR32_setDeadtime](Files/CF__TMR32_8c.md#function-ef-tmr32-setdeadtime)**(uint32_t tmr32_base, int value)<br>set the timer deadtime register value  |
| int | **[CF_TMR32_getDeadtime](Files/CF__TMR32_8c.md#function-ef-tmr32-getdeadtime)**(uint32_t tmr32_base) |

## Defines

|                | Name           |
| -------------- | -------------- |
|  | **[CF_TMR32_C](Files/CF__TMR32_8c.md#define-ef-tmr32-c)**  |


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

set the action of PWM1 when the timer matches CMPY value while up counting 

**Parameters**: 

  * **tmr32_base** The base memory address of TMR32 registers. 
  * **action** enum actions could be NONE, LOW, HIGH, or INVERT 


set the action of PWM1 when the timer matches CMPX value while up counting


### function CF_TMR32_setPWM1MatchingCMPYAction

```cpp
void CF_TMR32_setPWM1MatchingCMPYAction(
    uint32_t tmr32_base,
    enum actions action
)
```


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


### function CF_TMR32_getDeadtime

```cpp
int CF_TMR32_getDeadtime(
    uint32_t tmr32_base
)
```




## Macros Documentation

### define CF_TMR32_C

```cpp
#define CF_TMR32_C 
```


## Source code

```cpp

#ifndef CF_TMR32_C
#define CF_TMR32_C
#include <CF_TMR32.h>


void CF_TMR32_enable(uint32_t tmr32_base){

     CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

    // set the enable bit to 1 at the specified offset
    tmr32->CTRL |= (1 << CF_TMR32_CTRL_REG_TE_BIT);
}

void CF_TMR32_restart(uint32_t tmr32_base){

     CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

    // set the enable bit to 1 at the specified offset
    tmr32->CTRL |= (1 << CF_TMR32_CTRL_REG_TS_BIT);
}

void CF_TMR32_PWM0Enable(uint32_t tmr32_base){

     CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

    // set the enable bit to 1 at the specified offset
    tmr32->CTRL |= (1 << CF_TMR32_CTRL_REG_P0E_BIT);
}

void CF_TMR32_PWM1Enable(uint32_t tmr32_base){

     CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

    // set the enable bit to 1 at the specified offset
    tmr32->CTRL |= (1 << CF_TMR32_CTRL_REG_P1E_BIT);
}

void CF_TMR32_deadtimeEnable(uint32_t tmr32_base){

     CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

    // set the enable bit to 1 at the specified offset
    tmr32->CTRL |= (1 << CF_TMR32_CTRL_REG_DTE_BIT);
}

void CF_TMR32_PWM0Invert(uint32_t tmr32_base){

     CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

    // set the enable bit to 1 at the specified offset
    tmr32->CTRL |= (1 << CF_TMR32_CTRL_REG_PI0_BIT);
}

void CF_TMR32_PWM1Invert(uint32_t tmr32_base){

     CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

    // set the enable bit to 1 at the specified offset
    tmr32->CTRL |= (1 << CF_TMR32_CTRL_REG_PI1_BIT);
}

void CF_TMR32_setUpCount(uint32_t tmr32_base){

     CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

    // Clear the field bits in the register using the defined mask
    tmr32->CFG &= ~CF_TMR32_CFG_REG_DIR_MASK;

    // Set the bits with the given value at the defined offset
    tmr32->CFG |= ((0b10 << CF_TMR32_CFG_REG_DIR_BIT) & CF_TMR32_CFG_REG_DIR_MASK);
}

void CF_TMR32_setDownCount(uint32_t tmr32_base){

     CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

    // Clear the field bits in the register using the defined mask
    tmr32->CFG &= ~CF_TMR32_CFG_REG_DIR_MASK;

    // Set the bits with the given value at the defined offset
    tmr32->CFG |= ((0b01 << CF_TMR32_CFG_REG_DIR_BIT) & CF_TMR32_CFG_REG_DIR_MASK);
}

void CF_TMR32_setUpDownCount(uint32_t tmr32_base){

     CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

    // Clear the field bits in the register using the defined mask
    tmr32->CFG &= ~CF_TMR32_CFG_REG_DIR_MASK;

    // Set the bits with the given value at the defined offset
    tmr32->CFG |= ((0b11 << CF_TMR32_CFG_REG_DIR_BIT) & CF_TMR32_CFG_REG_DIR_MASK);
}

void CF_TMR32_setPeriodic(uint32_t tmr32_base){

     CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

    // set the enable bit to 1 at the specified offset
    tmr32->CTRL |= (1 << CF_TMR32_CFG_REG_P_BIT);
}

void CF_TMR32_setOneShot(uint32_t tmr32_base){

     CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

    // Clear the enable bit using the specified  mask
    tmr32->CTRL &= ~CF_TMR32_CFG_REG_P_BIT;
}

void CF_TMR32_setPWM0MatchingZeroAction(uint32_t tmr32_base, enum actions action){

    CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

    // Clear the field bits in the register using the defined mask
    tmr32->PWM0CFG &= ~CF_TMR32_PWM0CFG_REG_E0_MASK;

    // Set the bits with the given value at the defined offset
    tmr32->PWM0CFG |= ((action << CF_TMR32_PWM0CFG_REG_E0_BIT) & CF_TMR32_PWM0CFG_REG_E0_MASK);

}

void CF_TMR32_setPWM0MatchingCMPXAction(uint32_t tmr32_base, enum actions action){

    CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

    // Clear the field bits in the register using the defined mask
    tmr32->PWM0CFG &= ~CF_TMR32_PWM0CFG_REG_E1_MASK;

    // Set the bits with the given value at the defined offset
    tmr32->PWM0CFG |= ((action << CF_TMR32_PWM0CFG_REG_E1_BIT) & CF_TMR32_PWM0CFG_REG_E1_MASK);

}

void CF_TMR32_setPWM0MatchingCMPYAction(uint32_t tmr32_base, enum actions action){

    CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

    // Clear the field bits in the register using the defined mask
    tmr32->PWM0CFG &= ~CF_TMR32_PWM0CFG_REG_E2_MASK;

    // Set the bits with the given value at the defined offset
    tmr32->PWM0CFG |= ((action << CF_TMR32_PWM0CFG_REG_E2_BIT) & CF_TMR32_PWM0CFG_REG_E2_MASK);

}

void CF_TMR32_setPWM0MatchingRELOADAction(uint32_t tmr32_base, enum actions action){

    CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

    // Clear the field bits in the register using the defined mask
    tmr32->PWM0CFG &= ~CF_TMR32_PWM0CFG_REG_E3_MASK;

    // Set the bits with the given value at the defined offset
    tmr32->PWM0CFG |= ((action << CF_TMR32_PWM0CFG_REG_E3_BIT) & CF_TMR32_PWM0CFG_REG_E3_MASK);

}

void CF_TMR32_setPWM0MatchingCMPYDownCountAction(uint32_t tmr32_base, enum actions action){

    CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

    // Clear the field bits in the register using the defined mask
    tmr32->PWM0CFG &= ~CF_TMR32_PWM0CFG_REG_E4_MASK;

    // Set the bits with the given value at the defined offset
    tmr32->PWM0CFG |= ((action << CF_TMR32_PWM0CFG_REG_E4_BIT) & CF_TMR32_PWM0CFG_REG_E4_MASK);

}

void CF_TMR32_setPWM0MatchingCMPXDownCountAction(uint32_t tmr32_base, enum actions action){

    CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

    // Clear the field bits in the register using the defined mask
    tmr32->PWM0CFG &= ~CF_TMR32_PWM0CFG_REG_E5_MASK;

    // Set the bits with the given value at the defined offset
    tmr32->PWM0CFG |= ((action << CF_TMR32_PWM0CFG_REG_E5_BIT) & CF_TMR32_PWM0CFG_REG_E5_MASK);

}

void CF_TMR32_setPWM1MatchingZeroAction(uint32_t tmr32_base, enum actions action){

    CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

    // Clear the field bits in the register using the defined mask
    tmr32->PWM1CFG &= ~CF_TMR32_PWM1CFG_REG_E0_MASK;

    // Set the bits with the given value at the defined offset
    tmr32->PWM1CFG |= ((action << CF_TMR32_PWM1CFG_REG_E0_BIT) & CF_TMR32_PWM1CFG_REG_E0_MASK);

}

void CF_TMR32_setPWM1MatchingCMPXAction(uint32_t tmr32_base, enum actions action){

    CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

    // Clear the field bits in the register using the defined mask
    tmr32->PWM1CFG &= ~CF_TMR32_PWM1CFG_REG_E1_MASK;

    // Set the bits with the given value at the defined offset
    tmr32->PWM1CFG |= ((action << CF_TMR32_PWM1CFG_REG_E1_BIT) & CF_TMR32_PWM1CFG_REG_E1_MASK);

}

void CF_TMR32_setPWM1MatchingCMPYAction(uint32_t tmr32_base, enum actions action){

    CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

    // Clear the field bits in the register using the defined mask
    tmr32->PWM1CFG &= ~CF_TMR32_PWM1CFG_REG_E2_MASK;

    // Set the bits with the given value at the defined offset
    tmr32->PWM1CFG |= ((action << CF_TMR32_PWM1CFG_REG_E2_BIT) & CF_TMR32_PWM1CFG_REG_E2_MASK);

}

void CF_TMR32_setPWM1MatchingRELOADAction(uint32_t tmr32_base, enum actions action){

    CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

    // Clear the field bits in the register using the defined mask
    tmr32->PWM1CFG &= ~CF_TMR32_PWM1CFG_REG_E3_MASK;

    // Set the bits with the given value at the defined offset
    tmr32->PWM1CFG |= ((action << CF_TMR32_PWM1CFG_REG_E3_BIT) & CF_TMR32_PWM1CFG_REG_E3_MASK);

}

void CF_TMR32_setPWM1MatchingCMPYDownCountAction(uint32_t tmr32_base, enum actions action){

    CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

    // Clear the field bits in the register using the defined mask
    tmr32->PWM1CFG &= ~CF_TMR32_PWM1CFG_REG_E4_MASK;

    // Set the bits with the given value at the defined offset
    tmr32->PWM1CFG |= ((action << CF_TMR32_PWM1CFG_REG_E4_BIT) & CF_TMR32_PWM1CFG_REG_E4_MASK);

}

void CF_TMR32_setPWM1MatchingCMPXDownCountAction(uint32_t tmr32_base, enum actions action){

    CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

    // Clear the field bits in the register using the defined mask
    tmr32->PWM1CFG &= ~CF_TMR32_PWM1CFG_REG_E5_MASK;

    // Set the bits with the given value at the defined offset
    tmr32->PWM1CFG |= ((action << CF_TMR32_PWM1CFG_REG_E5_BIT) & CF_TMR32_PWM1CFG_REG_E5_MASK);

}

void CF_TMR32_setRELOAD (uint32_t tmr32_base, int value){

     CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

     tmr32->RELOAD = value;

}

int CF_TMR32_getRELOAD (uint32_t tmr32_base){

     CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

     return (tmr32->RELOAD);

}

void CF_TMR32_setCMPX (uint32_t tmr32_base, int value){

     CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

     tmr32->CMPX = value;

}

int CF_TMR32_getCMPX (uint32_t tmr32_base){

     CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

     return (tmr32->CMPX);

}

void CF_TMR32_setCMPY (uint32_t tmr32_base, int value){

     CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

     tmr32->CMPY = value;

}

int CF_TMR32_getCMPY (uint32_t tmr32_base){

     CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

     return (tmr32->CMPY);

}

int CF_TMR32_getTMR (uint32_t tmr32_base){

     CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

     return (tmr32->TMR);

}

void CF_TMR32_setDeadtime (uint32_t tmr32_base, int value){

     CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

     tmr32->PWMDT = value;

}

int CF_TMR32_getDeadtime (uint32_t tmr32_base){

     CF_TMR32_TYPE* tmr32 = (CF_TMR32_TYPE*)tmr32_base;

     return (tmr32->PWMDT);

}

#endif
```


-------------------------------

Updated on 2024-04-07 at 13:02:30 +0200
