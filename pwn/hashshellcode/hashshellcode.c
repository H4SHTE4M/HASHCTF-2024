#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <seccomp.h>
#include <linux/seccomp.h>
#include <sys/mman.h>

char random_choice(char *array, int size)
{
	int random_index = rand() % size;
	return array[random_index];
}

void sandbox()
{
	scmp_filter_ctx ctx;
	ctx = seccomp_init(SCMP_ACT_ALLOW);
	seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execve), 0);
	seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execveat), 0);
	// seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execvp), 0);
	seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(exit), 0);
	seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(exit_group), 0);
	seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(sigreturn), 0);
	seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(mmap), 0);
	seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(brk), 0);
	seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(mprotect), 0);
	seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(fstat), 0);
	seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(read), 0);
	seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(ptrace), 0);
	seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(close), 0);
	// seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(open)), 0);
	seccomp_load(ctx);
}

void shell() {}

int main()
{
	setvbuf(stdin, 0, 2, 0);
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stderr, 0, 2, 0);

	printf("hash had lost 100 hashcoins\n");
	printf("He found them in the police station then, but the police said that he must prove that he is the owner of the hashcoins\n");
	printf("hash thought hard and hard and got some hints: \n");
	char hashteam[] = {'H', 'A', 'S', 'H', 'T', 'E', 'A', 'M'};
	int size = sizeof(hashteam) / sizeof(hashteam[0]);

	// 使用当前时间作为随机数种子
	srand(time(NULL));

	// 随机选择一个元素
	char choice1 = random_choice(hashteam, size);
	char choice2 = random_choice(hashteam, size);
	char choice3 = random_choice(hashteam, size);
	int choice = (int)(choice1) * 10000 + (int)(choice2) * 100 + (int)(choice3);
	int seed = choice; // 0x555552d0;//time(NULL) % 100;
					   // printf("seed: %d\n", seed);
	srand(seed);
	for (int i = 0; i < 19; i++)
		printf("%d,", rand() % 1000);
	printf("%d\n", rand() % 1000);
	int rdnum21 = rand() % 1000;
	printf("Now please help hash to prove it's his\n");
	int answer;
	scanf("%d", &answer);

	if (answer != rdnum21)
	{
		printf("You are not the owner of hashcoins!\n");
		printf("Cai jiu duo lian\n");
		exit(1);
	}

	// char addr[100];
	printf("Nice!!!!, you have proved you are the owner\n");
	// printf("It's time for me: %p\n", addr);
	// printf("Dot' you want to make friends with me?\n");
	printf("Then you can use the hashcoins to buy the flag\n");
	void *addr = mmap(NULL,								  // 内存地址，NULL表示由系统选择
					  4096,								  // 内存大小，这里选择一页大小
					  PROT_READ | PROT_WRITE | PROT_EXEC, // 内存权限：可读、可写、可执行
					  MAP_PRIVATE | MAP_ANONYMOUS,		  // 内存映射标志：私有、匿名
					  -1,								  // 文件描述符，在匿名映射中忽略
					  0);								  // 文件偏移量，在匿名映射中忽略

	if (addr == MAP_FAILED)
	{
		perror("mmap");
		exit(EXIT_FAILURE);
	}

	read(0, addr, 0x1000);
	if()
	// shell = addr;
	// shell();
	sandbox();
	((void (*)())addr)();

	// 释放内存
	if (munmap(addr, 4096) == -1)
	{
		perror("munmap");
		exit(EXIT_FAILURE);
	}
}
