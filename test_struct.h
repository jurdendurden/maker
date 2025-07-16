// Sample C structures for database schema generation testing
#ifndef TEST_STRUCT_H
#define TEST_STRUCT_H

// User table structure
typedef struct {
    int user_id;
    char* username;
    char* email;
    int age;
    bool is_active;
} User;

// Product table structure
typedef struct {
    int product_id;
    char* name;
    double price;
    int quantity;
    char* description;
} Product;

// Order table structure
typedef struct {
    int order_id;
    int user_id;
    int product_id;
    int quantity;
    double total_amount;
} Order;

#endif // TEST_STRUCT_H 