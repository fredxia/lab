#include <sys/vfs.h>
#include <stdio.h>

inline int fs_print(const char* abcd)
{
  static_assert(sizeof(abcd) > 8, "Failed");
  return 0;
}

// collect stat on a file system
int main(int argc, char** argv)
{
  const char* fs = argv[1];
  
  fs_print("csdcsdcsdcsc");
  
  struct statfs stat_fs;
  int r = statfs(fs, &stat_fs);
  printf("fs %s\n", fs);
  printf("f_type %x, f_bsize %d\n", stat_fs.f_type, stat_fs.f_bsize);
  printf("f_blocks %d, f_bfree %d, f_bavail %d\n",
         stat_fs.f_blocks, stat_fs.f_bfree, stat_fs.f_bavail);
  printf("f_files %d, f_ffree %d, f_fsid %d, f_namelen %d, "
         "f_frsize %d, f_flags %x\n",
         stat_fs.f_files, stat_fs.f_ffree, stat_fs.f_fsid,
         stat_fs.f_namelen, stat_fs.f_frsize, stat_fs.f_flags);
}
