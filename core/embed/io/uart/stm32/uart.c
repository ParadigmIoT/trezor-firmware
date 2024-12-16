#include <io/uart.h>

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
static void Error_Handler(void)
{
    for(;;);
}

static UART_HandleTypeDef g_huart3 = {0};

/**
* @brief UART MSP Initialization
* This function configures the hardware resources used in this example
* @param huart: UART handle pointer
* @retval None
*/
void HAL_UART_MspInit(UART_HandleTypeDef* huart)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};
  if(huart->Instance==USART3)
  {
  /** Initializes the peripherals clock
  */
    PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_USART3;
    PeriphClkInit.Usart3ClockSelection = RCC_USART3CLKSOURCE_PCLK1;
    if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
    {
      Error_Handler();
    }

    /* Peripheral clock enable */
    __HAL_RCC_USART3_CLK_ENABLE();

    __HAL_RCC_GPIOB_CLK_ENABLE();

    GPIO_InitStruct.Pin = GPIO_PIN_10|GPIO_PIN_11;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF7_USART3;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

  }
}

/**
* @brief UART MSP De-Initialization
* This function freeze the hardware resources used in this example
* @param huart: UART handle pointer
* @retval None
*/
void HAL_UART_MspDeInit(UART_HandleTypeDef* huart)
{
  if(huart->Instance==USART3)
  {
    /* Peripheral clock disable */
    __HAL_RCC_USART3_CLK_DISABLE();

    HAL_GPIO_DeInit(GPIOB, GPIO_PIN_10|GPIO_PIN_11);
  }

}

/**
  * @brief USART3 Initialization Function
  * @param None
  * @retval None
  */
void MX_USART3_UART_Init(void)
{
  g_huart3.Instance = USART3;
  g_huart3.Init.BaudRate = 115200;
  g_huart3.Init.WordLength = UART_WORDLENGTH_8B;
  g_huart3.Init.StopBits = UART_STOPBITS_1;
  g_huart3.Init.Parity = UART_PARITY_NONE;
  g_huart3.Init.Mode = UART_MODE_TX_RX;
  g_huart3.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  g_huart3.Init.OverSampling = UART_OVERSAMPLING_16;
  g_huart3.Init.OneBitSampling = UART_ONE_BIT_SAMPLE_DISABLE;
  g_huart3.Init.ClockPrescaler = UART_PRESCALER_DIV1;
  g_huart3.AdvancedInit.AdvFeatureInit = UART_ADVFEATURE_NO_INIT;
  if (HAL_UART_Init(&g_huart3) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_UARTEx_SetTxFifoThreshold(&g_huart3, UART_TXFIFO_THRESHOLD_1_8) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_UARTEx_SetRxFifoThreshold(&g_huart3, UART_RXFIFO_THRESHOLD_1_8) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_UARTEx_DisableFifoMode(&g_huart3) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief  Send data over UART
  * @param  data: Pointer to data buffer to send
  * @param  size: Size of data buffer in bytes
  * @retval HAL status
  */
HAL_StatusTypeDef uart_send_message(uint8_t *data, uint16_t size)
{
  HAL_StatusTypeDef status;
  
  /* Send data over UART with timeout */
  status = HAL_UART_Transmit(&g_huart3, data, size, HAL_MAX_DELAY);
  
  return status;
}

/**
  * @brief  Read data from UART
  * @param  buffer: Pointer to buffer where received data will be stored
  * @param  size: Size of data to receive in bytes
  * @retval HAL status
  */
HAL_StatusTypeDef uart_read_message(uint8_t *buffer, uint16_t size)
{
  HAL_StatusTypeDef status;
  
  /* Receive data over UART with timeout */
  status = HAL_UART_Receive(&g_huart3, buffer, size, 10000);
  
  return status;
}

