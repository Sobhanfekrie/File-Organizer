#include <stdio.h>

// نمونه تابع C برای DLL
__declspec(dllexport) void dummy() {
    printf("File helper DLL loaded\n");
}
