#include <stdio.h>
#include <pigpio.h>

static void callback(int gpio, int level, uint32_t tick, void *data)
{
  
}

int main(int argc, char *argv[])
{
  return gpioInitialise();
}
