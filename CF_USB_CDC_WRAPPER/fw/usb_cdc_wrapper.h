#ifndef usb_cdc_wrapper_H
#define usb_cdc_wrapper_H

#include <stdint.h>
#include <usb_cdc_wrapper_regs.h>

void USB_CDC_setTXTH(uint32_t usb_cdc_base, int threshold);

void USB_CDC_setRXTH(uint32_t usb_cdc_base, int threshold);

void USB_CDC_init(uint32_t usb_cdc_base, int tx_threshold, int rx_threshold);

int USB_CDC_getTXLEVEL(uint32_t usb_cdc_base);

int USB_CDC_getRXLEVEL(uint32_t usb_cdc_base);

int USB_CDC_getTXTH(uint32_t usb_cdc_base);

int USB_CDC_getRXTH(uint32_t usb_cdc_base);

int USB_CDC_getRIS(uint32_t usb_cdc_base);

int USB_CDC_getMIS(uint32_t usb_cdc_base);

int USB_CDC_getIM(uint32_t usb_cdc_base);

void USB_CDC_setIM(uint32_t usb_cdc_base, int mask);

int USB_CDC_getICR(uint32_t usb_cdc_base);

void USB_CDC_setICR(uint32_t usb_cdc_base, int mask);

char USB_CDC_readByte(uint32_t usb_cdc_base);

void USB_CDC_writeByte(uint32_t usb_cdc_base, char byte);

#endif