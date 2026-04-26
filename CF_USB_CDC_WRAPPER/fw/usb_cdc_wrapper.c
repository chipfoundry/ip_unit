#ifndef usb_cdc_wrapper_C
#define usb_cdc_wrapper_C

#include <usb_cdc_wrapper.h>

void USB_CDC_setTXTH(uint32_t usb_cdc_base, int threshold){

    USB_CDC_WRAPPER_TYPE* usb_cdc = (USB_CDC_WRAPPER_TYPE*)usb_cdc_base;
    usb_cdc->TXFIFOT = threshold;
}
void USB_CDC_setRXTH(uint32_t usb_cdc_base, int threshold){

    USB_CDC_WRAPPER_TYPE* usb_cdc = (USB_CDC_WRAPPER_TYPE*)usb_cdc_base;
    usb_cdc->RXFIFOT = threshold;
}

void USB_CDC_init(uint32_t usb_cdc_base, int tx_threshold, int rx_threshold){

    USB_CDC_setTXTH(usb_cdc_base, tx_threshold); 
    USB_CDC_setRXTH(usb_cdc_base, rx_threshold); 
}

int USB_CDC_getTXLEVEL(uint32_t usb_cdc_base){

    USB_CDC_WRAPPER_TYPE* usb_cdc = (USB_CDC_WRAPPER_TYPE*)usb_cdc_base;
    return (usb_cdc->TXFIFOLEVEL);
}

int USB_CDC_getRXLEVEL(uint32_t usb_cdc_base){

    USB_CDC_WRAPPER_TYPE* usb_cdc = (USB_CDC_WRAPPER_TYPE*)usb_cdc_base;
    return (usb_cdc->RXFIFOLEVEL);
}

int USB_CDC_getTXTH(uint32_t usb_cdc_base){

    USB_CDC_WRAPPER_TYPE* usb_cdc = (USB_CDC_WRAPPER_TYPE*)usb_cdc_base;
    return (usb_cdc->TXFIFOT);
}

int USB_CDC_getRXTH(uint32_t usb_cdc_base){

    USB_CDC_WRAPPER_TYPE* usb_cdc = (USB_CDC_WRAPPER_TYPE*)usb_cdc_base;
    return (usb_cdc->RXFIFOT);
}

int USB_CDC_getRIS(uint32_t usb_cdc_base){

    USB_CDC_WRAPPER_TYPE* usb_cdc = (USB_CDC_WRAPPER_TYPE*)usb_cdc_base;
    return (usb_cdc->ris);
}

int USB_CDC_getMIS(uint32_t usb_cdc_base){

    USB_CDC_WRAPPER_TYPE* usb_cdc = (USB_CDC_WRAPPER_TYPE*)usb_cdc_base;
    return (usb_cdc->mis);
}

int USB_CDC_getIM(uint32_t usb_cdc_base){

    USB_CDC_WRAPPER_TYPE* usb_cdc = (USB_CDC_WRAPPER_TYPE*)usb_cdc_base;
    return (usb_cdc->im);
}

void USB_CDC_setIM(uint32_t usb_cdc_base, int mask){

    USB_CDC_WRAPPER_TYPE* usb_cdc = (USB_CDC_WRAPPER_TYPE*)usb_cdc_base;
    usb_cdc->im = mask;
}

int USB_CDC_getICR(uint32_t usb_cdc_base){

    USB_CDC_WRAPPER_TYPE* usb_cdc = (USB_CDC_WRAPPER_TYPE*)usb_cdc_base;
    return (usb_cdc->icr);
}

void USB_CDC_setICR(uint32_t usb_cdc_base, int mask){
    
    USB_CDC_WRAPPER_TYPE* usb_cdc = (USB_CDC_WRAPPER_TYPE*)usb_cdc_base;
    usb_cdc->icr = mask;
}


// Interrupts 
// bit 0: TX FIFO is Empty
// bit 1: TX FIFO level is below the value in the TX FIFO Level Threshold Register
// bit 2: RX FIFO is Full
// bit 3: RX FIFO level is above the value in the RX FIFO Level Threshold Register


char USB_CDC_readByte(uint32_t usb_cdc_base){                      

    USB_CDC_WRAPPER_TYPE* usb_cdc = (USB_CDC_WRAPPER_TYPE*)usb_cdc_base;
    while((USB_CDC_getRIS(usb_cdc_base) & 0x8) == 0x0); // wait over RX fifo is empty Flag to unset  
    int data = usb_cdc->rxdata;
    USB_CDC_setICR(usb_cdc_base, 0x8);
    return data;
}

void USB_CDC_writeByte(uint32_t usb_cdc_base, char byte){

    USB_CDC_WRAPPER_TYPE* usb_cdc = (USB_CDC_WRAPPER_TYPE*)usb_cdc_base;
    while((USB_CDC_getRIS(usb_cdc_base) & 0x2) == 0x0); // wait until there is space in the fifo so level is below threshhold (10) 
    usb_cdc->txdata = byte; //write what has been recieved
    USB_CDC_setICR(usb_cdc_base, 0x2);  
}


#endif