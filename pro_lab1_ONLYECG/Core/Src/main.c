/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2023 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
#define MAX86150_Addr 0xBC //updated per I2Cscanner, 8 bit version of 7 bit code 0x5E
#define InterruptStatusReg1 0x00 //Interrupt status byte 0 (read both bytes 0x00 and 0x01 when checking int status)
#define InterruptStatusReg2 0x01
#define InterruptEnableReg1 0x02 //Interrupt enable byte 0
#define InterruptEnableReg2 0x03
#define FIFOWritePointerReg 0x04
#define OverflowCounterReg 0x05
#define FIFOReadPointerReg 0x06
#define FIFODataReg 0x07
#define FIFOConfigReg 0x08
#define FIFODataControlReg1 0x09
#define FIFODataControlReg2 0x0A
#define SystemControlReg 0x0D
#define ppgConfigReg0 0x0E
#define ppgConfigReg1 0x0F
#define ProxIntThreshReg 0x10
#define LED1PulseAmpReg 0x11
#define LED2PulseAmpReg 0x12
#define LEDRangeReg 0x14
#define LEDPilotPAReg 0x15
#define EcgConfigReg1 0x3C
#define EcgConfigReg2 0x3D
#define EcgConfigReg3 0x3E
#define EcgConfigReg4 0x3F
#define PartIDReg 0xFF
#define maxi2cFreq 1000000
#define recommendedi2cFreq 400000
#define interrupt_pin D12 //INTB pin --see InterruptIn declaration
#define maxECGrate 0
#define normECGrate 1
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
I2C_HandleTypeDef hi2c1;

UART_HandleTypeDef huart2;
UART_HandleTypeDef huart3;

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_I2C1_Init(void);
static void MX_USART2_UART_Init(void);
static void MX_USART3_UART_Init(void);
/* USER CODE BEGIN PFP */


	uint8_t Data[] = "123";
	float aaa = 0;
uint8_t tran[4];
int j;

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */
	uint8_t p[2];

	uint8_t start[3]={'o','k','\n'};
	uint8_t dd[3] = {'d','i','\n'};
	uint8_t buf[12]={0}; //receive data buffer 
	uint32_t Elem[3]; 
	uint8_t pp=0 ; 
	float ppg;
	float ecg;
  float iir;
	union Float_c {
		float m_float;
		uint8_t m_bytes[sizeof(float)];
	};
	union Float_c myFloat;
	int i;
	uint8_t dda=0x01;
  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_I2C1_Init();
  MX_USART2_UART_Init();
  MX_USART3_UART_Init();
  /* USER CODE BEGIN 2 */
//	HAL_I2C_Master_Transmit(&hi2c1,0xBC,p,2,100);
//  HAL_UARTEx_ReceiveToIdle_IT(&huart3, Data, 64);
	
	p[0]=0x0;
	p[1]=0;
//	if(HAL_I2C_Master_Transmit(&hi2c1,0x5e,p,2,100)==HAL_OK)
//	{
//		//if transmit is success, the function will 
//		HAL_UART_Transmit(&huart3,start,3,100);
//		aaa = 5;
//		HAL_Delay(1000);
//	}

/*
	HAL_I2C_Mem_Write(&hi2c1,0xbc,0x0d,1,&dda,1,100);
	HAL_Delay(30);
	dda = 0x04;
	HAL_I2C_Mem_Write(&hi2c1,0xbc,0x0d,1,&dda,1,100);	
	dda = 0x21;
	HAL_I2C_Mem_Write(&hi2c1,0xbc,0x09,1,&dda,1,100);
	dda = 0x09;
	HAL_I2C_Mem_Write(&hi2c1,0xbc,0x0A,1,&dda,1,100);
	dda = 0X00;
	HAL_I2C_Mem_Write(&hi2c1,0xbc,0x3E,1,&dda,1,100);
	dda = 0x01;
	HAL_I2C_Mem_Write(&hi2c1,0xbc,0x11,1,&dda,1,100);
	HAL_I2C_Mem_Write(&hi2c1,0xbc,0x12,1,&dda,1,100);
	HAL_I2C_Mem_Write(&hi2c1,0xbc,0x15,1,&dda,1,100);
	dda = 0x80;
	HAL_I2C_Mem_Write(&hi2c1,0xbc,0x02,1,&dda,1,100);

*/

dda = 0x80;
HAL_I2C_Mem_Write(&hi2c1,0xbc,0x02,1,&dda,1,100);	
dda = 0x01;
HAL_I2C_Mem_Write(&hi2c1,0xbc,0x0d,1,&dda,1,100);	
dda = 0x04;
HAL_I2C_Mem_Write(&hi2c1,0xbc,0x0d,1,&dda,1,100);	
dda = 0x1f;
HAL_I2C_Mem_Write(&hi2c1,0xbc,0x08,1,&dda,1,100);	
dda = 0x12;
HAL_I2C_Mem_Write(&hi2c1,0xbc,0x09,1,&dda,1,100);	
dda = 0x09;
HAL_I2C_Mem_Write(&hi2c1,0xbc,0x0a,1,&dda,1,100);	
dda = 0x05;
HAL_I2C_Mem_Write(&hi2c1,0xbc,0x14,1,&dda,1,100);
dda = 0x19;
HAL_I2C_Mem_Write(&hi2c1,0xbc,0x11,1,&dda,1,100);	
dda = 0x19;
HAL_I2C_Mem_Write(&hi2c1,0xbc,0x12,1,&dda,1,100);	

dda = 0x14;
HAL_I2C_Mem_Write(&hi2c1,0xbc,0x0e,1,&dda,1,100);	
dda = 0x00;
HAL_I2C_Mem_Write(&hi2c1,0xbc,0x0f,1,&dda,1,100);	
dda = 0x03;
HAL_I2C_Mem_Write(&hi2c1,0xbc,0x3c,1,&dda,1,100);	
dda = 0x00;
HAL_I2C_Mem_Write(&hi2c1,0xbc,0x3e,1,&dda,1,100);	
dda = 0xc0;
HAL_I2C_Mem_Write(&hi2c1,0xbc,0x02,1,&dda,1,100);	

/*dda = 0x54;
HAL_I2C_Mem_Write(&hi2c1,0xbc,0xff,1,&dda,1,100);	
dda = 0x4d;
HAL_I2C_Mem_Write(&hi2c1,0xbc,0xff,1,&dda,1,100);	
dda = 0x0a;
HAL_I2C_Mem_Write(&hi2c1,0xbc,0xce,1,&dda,1,100);	
dda = 0x18;
HAL_I2C_Mem_Write(&hi2c1,0xbc,0xcf,1,&dda,1,100);	
dda = 0x00;
HAL_I2C_Mem_Write(&hi2c1,0xbc,0xff,1,&dda,1,100);*/
HAL_UART_Transmit(&huart3,(uint8_t*)("3"),1,100);
HAL_UART_Transmit(&huart2,(uint8_t*)("2"),1,100);
// // HAL_UARTEx_ReceiveToIdle_IT(&huart4, Data, 64);
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  uint8_t ecgbt[4];
	
	HAL_UART_Transmit(&huart3,tran,4,100);
	HAL_Delay(3000);
 
  while (1)
  {


		pp = 0x00;

	//	HAL_I2C_Mem_Read(&hi2c1,0xbd,0x00,1,&dda,1,100);
	//	HAL_Delay(1);	
		if(HAL_I2C_Master_Transmit(&hi2c1,0xbc,&pp,1,100)==HAL_OK){//access 0x00 register
			//aaa = 50;
			//j=HAL_I2C_Master_Receive(&hi2c1,0xBD,buf,1,100);
			if(HAL_I2C_Master_Receive(&hi2c1,0xbD,&buf[0],1,100)==HAL_OK){//receive answer
				if((buf[0]&0x80)>0){//FIFO status check
					pp=7;
					if(HAL_I2C_Master_Transmit(&hi2c1,0xBc,&pp,1,100)==HAL_OK){
						if(HAL_I2C_Master_Receive(&hi2c1,0xBD,buf, 9,100)==HAL_OK){
							Elem[0] = ((buf[0]<<16) | (buf[1]<<8) | buf[2]) & 0x03ffff;//IIR
							Elem[1] = ((buf[3]<<16) | (buf[4]<<8) | buf[5]) & 0x07ffff;//PPG
							Elem[2] = ((buf[6]<<16) | (buf[7]<<8) | buf[8]) & 0x03ffff;//ECG 
							ppg = (float) Elem[1];
							ecg = (float) Elem[2];
              iir = (float) Elem[0];
							HAL_UART_Transmit(&huart2,(uint8_t*)("1"),1,100);

              myFloat.m_float=(float) ppg;
              tran[0]=myFloat.m_bytes[0];
              tran[1]=myFloat.m_bytes[1];
              tran[2]=myFloat.m_bytes[2];
              tran[3]=myFloat.m_bytes[3];
              HAL_UART_Transmit(&huart2,tran,4,100);
             /* ecgbt[0] = 0;
              ecgbt[1] = buf[6];
              ecgbt[2] = buf[7];
              ecgbt[3] = buf[8];*/

              myFloat.m_float=(float) ecg; 
              tran[0]=myFloat.m_bytes[0];
              tran[1]=myFloat.m_bytes[1];
              tran[2]=myFloat.m_bytes[2];
              tran[3]=myFloat.m_bytes[3];
              HAL_UART_Transmit(&huart2,tran,4,100);
							/*myFloat.m_float=(float) ppg;
							tran[0]=myFloat.m_bytes[0];
							tran[1]=myFloat.m_bytes[1];
							tran[2]=myFloat.m_bytes[2];
							tran[3]=myFloat.m_bytes[3];*/
							//HAL_UART_Transmit(&huart3,Elem[1],4,100);
							/*myFloat.m_float=(float) ecg;
							tran[0]=myFloat.m_bytes[0];
							tran[1]=myFloat.m_bytes[1];
							tran[2]=myFloat.m_bytes[2];
							tran[3]=myFloat.m_bytes[3];*/
							//HAL_UART_Transmit(&huart3,Elen[2],4,100);
						}
					}
				}
			}

		}
	//	aaa = ppg;
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
	//	HAL_UART_Transmit(&huart3,start,2,100);
//		HAL_Delay(1);
			
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI|RCC_OSCILLATORTYPE_HSI48;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSI48State = RCC_HSI48_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSI48;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_1) != HAL_OK)
  {
    Error_Handler();
  }
  PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_USART2|RCC_PERIPHCLK_I2C1;
  PeriphClkInit.Usart2ClockSelection = RCC_USART2CLKSOURCE_PCLK1;
  PeriphClkInit.I2c1ClockSelection = RCC_I2C1CLKSOURCE_HSI;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief I2C1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_I2C1_Init(void)
{

  /* USER CODE BEGIN I2C1_Init 0 */

  /* USER CODE END I2C1_Init 0 */

  /* USER CODE BEGIN I2C1_Init 1 */

  /* USER CODE END I2C1_Init 1 */
  hi2c1.Instance = I2C1;
  hi2c1.Init.Timing = 0x0000020B;
  hi2c1.Init.OwnAddress1 = 0;
  hi2c1.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
  hi2c1.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
  hi2c1.Init.OwnAddress2 = 0;
  hi2c1.Init.OwnAddress2Masks = I2C_OA2_NOMASK;
  hi2c1.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
  hi2c1.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;
  if (HAL_I2C_Init(&hi2c1) != HAL_OK)
  {
    Error_Handler();
  }

  /** Configure Analogue filter
  */
  if (HAL_I2CEx_ConfigAnalogFilter(&hi2c1, I2C_ANALOGFILTER_ENABLE) != HAL_OK)
  {
    Error_Handler();
  }

  /** Configure Digital filter
  */
  if (HAL_I2CEx_ConfigDigitalFilter(&hi2c1, 0) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN I2C1_Init 2 */

  /* USER CODE END I2C1_Init 2 */

}

/**
  * @brief USART2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART2_UART_Init(void)
{

  /* USER CODE BEGIN USART2_Init 0 */

  /* USER CODE END USART2_Init 0 */

  /* USER CODE BEGIN USART2_Init 1 */

  /* USER CODE END USART2_Init 1 */
  huart2.Instance = USART2;
  huart2.Init.BaudRate = 115200;
  huart2.Init.WordLength = UART_WORDLENGTH_8B;
  huart2.Init.StopBits = UART_STOPBITS_1;
  huart2.Init.Parity = UART_PARITY_NONE;
  huart2.Init.Mode = UART_MODE_TX_RX;
  huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart2.Init.OverSampling = UART_OVERSAMPLING_16;
  huart2.Init.OneBitSampling = UART_ONE_BIT_SAMPLE_DISABLE;
  huart2.AdvancedInit.AdvFeatureInit = UART_ADVFEATURE_NO_INIT;
  if (HAL_UART_Init(&huart2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART2_Init 2 */

  /* USER CODE END USART2_Init 2 */

}

/**
  * @brief USART3 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART3_UART_Init(void)
{

  /* USER CODE BEGIN USART3_Init 0 */

  /* USER CODE END USART3_Init 0 */

  /* USER CODE BEGIN USART3_Init 1 */

  /* USER CODE END USART3_Init 1 */
  huart3.Instance = USART3;
  huart3.Init.BaudRate = 38400;
  huart3.Init.WordLength = UART_WORDLENGTH_8B;
  huart3.Init.StopBits = UART_STOPBITS_1;
  huart3.Init.Parity = UART_PARITY_NONE;
  huart3.Init.Mode = UART_MODE_TX_RX;
  huart3.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart3.Init.OverSampling = UART_OVERSAMPLING_16;
  huart3.Init.OneBitSampling = UART_ONE_BIT_SAMPLE_DISABLE;
  huart3.AdvancedInit.AdvFeatureInit = UART_ADVFEATURE_NO_INIT;
  if (HAL_UART_Init(&huart3) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART3_Init 2 */

  /* USER CODE END USART3_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};
/* USER CODE BEGIN MX_GPIO_Init_1 */
/* USER CODE END MX_GPIO_Init_1 */

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOF_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(LD2_GPIO_Port, LD2_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin : B1_Pin */
  GPIO_InitStruct.Pin = B1_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_FALLING;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(B1_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pin : LD2_Pin */
  GPIO_InitStruct.Pin = LD2_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(LD2_GPIO_Port, &GPIO_InitStruct);

/* USER CODE BEGIN MX_GPIO_Init_2 */
/* USER CODE END MX_GPIO_Init_2 */
}

/* USER CODE BEGIN 4 */
void HAL_UARTEx_RxEventCallback(UART_HandleTypeDef *huart, uint16_t Size)
{
	if (huart->Instance==USART3)
	{
		HAL_UART_Transmit(&huart3, Data, Size, 1000);
	}
	HAL_UARTEx_ReceiveToIdle_IT(huart, Data, 64);
}
/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
