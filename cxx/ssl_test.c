#include <openssl/ssl.h>

int init_ssl_context(const char* cert_file,
                     const char* key_file,
                     const SSL_METHOD*& ssl_method,
                     SSL_CTX*& ssl_context)
{
  SSL_load_error_strings();      
  SSLeay_add_ssl_algorithms();
  ssl_method = SSLv23_server_method();  
  ssl_context = SSL_CTX_new(ssl_method);
  SSL_CTX_use_certificate_chain_file(ssl_context, cert_file);
  SSL_CTX_use_PrivateKey_file(ssl_context, key_file, SSL_FILETYPE_PEM);
  if (!SSL_CTX_check_private_key(ssl_context)) {
    return -1;
  }
  return 0;
}

int main(int argc, char** argv)
{
  const char* cert_file = argv[1];
  const char* key_file = argv[2];
  const SSL_METHOD* ssl_method;
  SSL_CTX* ssl_context;
  int r = init_ssl_context(cert_file, key_file, ssl_method, ssl_context);
  return 0;
}
