#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
   int fd;
   fd = open(argv[1], O_RDWR | O_NOCTTY);
   int RTS_flag;
   RTS_flag = TIOCM_RTS;
   ioctl(fd, TIOCMBIS, &RTS_flag); // set
   system("./ptt.sh");
   ioctl(fd, TIOCMBIC, &RTS_flag); // clear
   close(fd);
   return 0;
}
