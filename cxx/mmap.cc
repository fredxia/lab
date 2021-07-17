#include <sys/stat.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/resource.h>
#include <sys/time.h>
#include <fcntl.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <errno.h>

static char* ptrs[1000000];

static void make_dirty(char* start, size_t sz)
{
    int pgSize = getpagesize();

    char* pg = start;

    // Write one byte each page to make the page dirty
    int count = 0;
    while ((size_t)(pg - start) < sz) {
        char* caddr = pg + (rand() % pgSize);
        *caddr = '1';
        count++;
        pg += pgSize;
        ptrs[count] = caddr;
    }
    if (msync(start, sz, MS_SYNC) < 0) {
        fprintf(stderr, "msync failed %s", strerror(errno));
    }
    printf("Write %d pages\n", count);
}

static void print_usage()
{
    struct rusage usg;
    getrusage(RUSAGE_SELF, &usg);
    printf("rss %ld, minflt %ld\n", usg.ru_maxrss, usg.ru_minflt);
}

int main(int argc, const char** argv)
{
    if (argc != 2) {
        fprintf(stderr, "Invalid parameters\n");
        return -1;
    }
    
    const char* filePath = argv[1];

    int fd = open(filePath, O_RDWR);
    if (fd == 0) {
        fprintf(stderr, "Cannot open %s: %s", filePath, strerror(errno));
        return -1;
    }
    struct stat statBuf;
    if (stat(filePath, &statBuf) < 0) {
        fprintf(stderr, "Cannot stat %s: %s", filePath, strerror(errno));
        return -1;
    }
    
    char* addr = (char*)mmap(NULL, statBuf.st_size, PROT_READ | PROT_WRITE,
                             MAP_SHARED, fd, 0);
    if (addr == 0) {
        fprintf(stderr, "mmap failed: %s", strerror(errno));
        return -1;
    }

    printf("Mapped %s total size %ld\n", filePath, statBuf.st_size);

    make_dirty(addr, statBuf.st_size);
    while (1) {
        sleep(10);
        printf("Sleeping\n");
        make_dirty(addr, statBuf.st_size);
        print_usage();
        fflush(stdout);
    }
}

