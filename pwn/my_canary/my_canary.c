#include <stdio.h>
#include <stdlib.h>

long my_canary = 0xdeadbeefdeadbe00;
// int file = fopen('/dev/urandom', 0);
// read(file, my_canary, 8);

void init()
{
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);
    FILE *urandom;
    unsigned char buffer[8];

    // 打开 /dev/urandom 文件
    urandom = fopen("/dev/urandom", "rb");
    if (urandom == NULL)
    {
        perror("Error opening /dev/urandom");
        return 1;
    }

    // 读取八个字节的随机数据
    if (fread(buffer, sizeof(unsigned char), 8, urandom) != 8)
    {
        perror("Error reading from /dev/urandom");
        fclose(urandom);
        return 1;
    }

    // 关闭文件
    fclose(urandom);

    buffer[0] = '\x00';
    // printf("buffer: ");
    // for (int i = 0; i < 8; i++)
    // {
    //     printf("%02x ", buffer[i]);
    // }
    // printf("\n");

    // 将随机数据解释为 long 类型整数
    my_canary = *((long *)buffer);

    // printf("my_canary: %p\n", my_canary);

    puts("Welcome to the verification code system!");
    puts(" _   _    _    ____  _   ___     __        _               _");
    puts("| | | |  / \\  / ___|| | | \\ \\   / /__ _ __(_) ___ ___   __| | ___");
    puts("| |_| | / _ \\ \\___ \\| |_| |\\ \\ / / _ \\ '__| |/ __/ _ \\ / _` |/ _ \\");
    puts("|  _  |/ ___ \\ ___) |  _  | \\ V /  __/ |  | | (_| (_) | (_| |  __/");
    puts("|_| |_/_/   \\_\\____/|_| |_|  \\_/ \\___|_|  |_|\\___\\___/ \\__,_|\\___|");

    alarm(0x3c);
    return;
}

// void my_read(char *vericode, unsigned int length)
void my_read(char *vericode)
{
    int i;
    for (i = 0;; i++)
    {
        scanf("%c", &vericode[i]);
        if (i == 72)
            // if (i == length)
            break;
        if (vericode[i] == '\n')
        {
            vericode[i] = '\0';
            break;
        }
    }
    return;
}

// int my_gets(){
//     char buf[0x10];
//     return gets(buf);

// }

int vuln()
{
    char buf[0x8];
    long canary = my_canary;
    system("The system function is strange....");
    // read(0, buf, 0x200);

    gets(buf);
    if (canary != my_canary)
    {
        printf("*** stack smashing detected ***: terminated");
        exit(0);
    }
    // __asm__(
    //     "pushq %rdx\n"
    //     "pushq %rdx\n");
}

int main()
{
    init();

    // int length = 6;
    // char vericode[length];
    char vericode[64];
    long canary = my_canary;
    printf("\n\nPlease input your Verification code:");
    // my_read(vericode, 6);
    my_read(vericode);
    printf("Your Verification code ");
    // for (int i = 0; i < 6; i++)
    // {
    //     if (vericode[i]=='\n')
    //         break;
    //     printf("%c", vericode[i]);
    // }
    printf("%s", vericode);
    printf(" is wrong !");
    vuln();
    return 0;
}
