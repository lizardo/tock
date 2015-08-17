#include "nrf_delay.h"
#include "nrf_gpio.h"

void nrf_lib_gpio_range_cfg_output(uint32_t pin_range_start, uint32_t pin_range_end)
{
	nrf_gpio_range_cfg_output(pin_range_start, pin_range_end);
}

void nrf_lib_gpio_port_write(uint8_t port, uint8_t value)
{
	nrf_gpio_port_write(port, value);
}

void nrf_lib_delay_ms(uint32_t number_of_ms)
{
	nrf_delay_ms(number_of_ms);
}
