#include <stdio.h>
#include <stdlib.h>
#include <sqlite3.h>

bool does_table_exist(sqlite3* db, const char* table_name)
{
  char* buffer;
  asprintf(&buffer, "PRAGMA table_info(%s)", table_name);

  sqlite3_stmt *stmt;
  int rc = sqlite3_prepare_v2(db, buffer, -1, &stmt, 0);
//  free(buffer);
  if (rc != SQLITE_OK) {
    fprintf(stderr, "Failed to prepare %s\n", sqlite3_errmsg(db));
    return false;
  }
  rc = sqlite3_step(stmt);
  printf("rc %d\n", rc == SQLITE_ROW);
  if (rc == SQLITE_ROW) {
    int col_count = sqlite3_column_count(stmt);
    printf("Number of columns %d\n", col_count);
  }
  sqlite3_finalize(stmt);
  return true;
}

int create_reseller_table(sqlite3* db)
{
  if (does_table_exist(db, "PFPT_Reseller")) {
    return 0;
  }
  static const char* create_table_sql =
    "CREATE TABLE PFPT_Reseller("
    " Id INT, Prefix TEXT, Description TEXT"
    ")";
  char* err_msg = 0;
  int rc = sqlite3_exec(db, create_table_sql, 0, 0, &err_msg);
  if (rc != SQLITE_OK) {
    fprintf(stderr, "Failed to prepare: %s\n", err_msg);
    sqlite3_free(err_msg);
    return -1;
  }
  return 0;
}

int main(int argc, char** argv)
{
  if (argc != 2) {
    fprintf(stderr, "Invalid arguments\n");
    exit(1);
  }

  const char* db_name = argv[1];
  sqlite3 *db;
  
  printf("%s, %s\n", db_name, sqlite3_libversion());
  int rc = sqlite3_open(db_name, &db);
  if (rc != SQLITE_OK) {
    fprintf(stderr, "Cannot open database %s\n", sqlite3_errmsg(db));
    sqlite3_close(db);
    exit(1);
  }
  sqlite3_stmt *stmt;
  rc = sqlite3_prepare_v2(db, "SELECT SQLITE_VERSION()", -1, &stmt, 0);
  if (rc != SQLITE_OK) {
    fprintf(stderr, "Failed to prepare: %s\n", sqlite3_errmsg(db));
    sqlite3_close(db);
    exit(1);
  }
  rc = sqlite3_step(stmt);
  if (rc == SQLITE_ROW) {
    printf("type str is %s\n", sqlite3_column_decltype(stmt, 0));
    printf("type is %d\n", sqlite3_column_type(stmt, 0));
    printf("%s\n", sqlite3_column_text(stmt, 0));
  }

  rc = create_reseller_table(db);
  if (rc == 0) {
    printf("table exist %d\n", does_table_exist(db, "PFPT_Reseller"));
  }
  sqlite3_finalize(stmt);
  sqlite3_close(db);
  return 0;
}
