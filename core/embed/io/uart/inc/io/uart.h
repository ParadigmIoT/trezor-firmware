/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __UART_H
#define __UART_H

/* Includes ------------------------------------------------------------------*/
#include <trezor_types.h>
#include <trezor_bsp.h>

/* Exported constants --------------------------------------------------------*/
/* Size of Transmission buffer */
#define TXBUFFERSIZE                (COUNTOF(aTxBuffer) - 1)
/* Size of Reception buffer */
#define RXBUFFERSIZE                TXBUFFERSIZE

/* Exported macro ------------------------------------------------------------*/
#define COUNTOF(__BUFFER__)   (sizeof(__BUFFER__) / sizeof(*(__BUFFER__)))

/* Exported functions prototypes ---------------------------------------------*/
void HAL_UART_MspInit(UART_HandleTypeDef* huart);
void HAL_UART_MspDeInit(UART_HandleTypeDef* huart);
void MX_USART3_UART_Init(void);
void MX_USART3_UART_DeInit(void);
HAL_StatusTypeDef uart_send_message(uint8_t *data, uint16_t size);
HAL_StatusTypeDef uart_read_message(uint8_t *buffer, uint16_t size);

#endif /* __UART_H */
