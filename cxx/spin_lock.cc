#include <pthread.h>
#include <stdio.h>

int main()
{
    pthread_spinlock_t test_lock;
    pthread_spin_init(&test_lock, PTHREAD_PROCESS_PRIVATE);
    int r = pthread_spin_lock(&test_lock);
    printf("locked %d\n", r);
    pthread_spin_unlock(&test_lock);
    return 0;
}
