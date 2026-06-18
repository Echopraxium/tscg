; ModuleID = 'E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\projects\toolchain-tests/c89/test_doom_libc\src/test_doom_libc.c'
source_filename = "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\toolchain-tests/c89/test_doom_libc\\src/test_doom_libc.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-windows-msvc19.51.36246"

$sprintf = comdat any

$vsprintf = comdat any

$_snprintf = comdat any

$_vsnprintf = comdat any

$snprintf = comdat any

$_vsprintf_l = comdat any

$_vsnprintf_l = comdat any

$__local_stdio_printf_options = comdat any

$vsnprintf = comdat any

$"??_C@_02MOKMDPNA@42?$AA@" = comdat any

$"??_C@_02KACMFDGK@?97?$AA@" = comdat any

$"??_C@_04KCMBDBIM@?5?510?$AA@" = comdat any

$"??_C@_04KFPCKHMN@doom?$AA@" = comdat any

$"??_C@_04GJMIEFLF@DOOM?$AA@" = comdat any

$"??_C@_03BKBIMMBE@ABD?$AA@" = comdat any

$"??_C@_03FFFJFKND@ABC?$AA@" = comdat any

$"??_C@_06NHMNLEFC@wolf3d?$AA@" = comdat any

$"??_C@_06OLKLCMGA@WOLF3D?$AA@" = comdat any

$"??_C@_04KPDKMPHF@WOLF?$AA@" = comdat any

$"??_C@_07DCLBNMLN@generic?$AA@" = comdat any

$"??_C@_0M@EJPOMJDM@doomgeneric?$AA@" = comdat any

$"??_C@_03POMAGKDD@xyz?$AA@" = comdat any

$"??_C@_05CJBACGMB@hello?$AA@" = comdat any

$"??_C@_0L@NAOIGMFN@TriskeleVM?$AA@" = comdat any

$"??_C@_04GEDDIIMJ@Doom?$AA@" = comdat any

$"??_C@_06KJACHCDN@v?$CFd?4?$CFd?$AA@" = comdat any

@"??_C@_02MOKMDPNA@42?$AA@" = linkonce_odr dso_local unnamed_addr constant [3 x i8] c"42\00", comdat, align 1
@"??_C@_02KACMFDGK@?97?$AA@" = linkonce_odr dso_local unnamed_addr constant [3 x i8] c"-7\00", comdat, align 1
@"??_C@_04KCMBDBIM@?5?510?$AA@" = linkonce_odr dso_local unnamed_addr constant [5 x i8] c"  10\00", comdat, align 1
@"??_C@_04KFPCKHMN@doom?$AA@" = linkonce_odr dso_local unnamed_addr constant [5 x i8] c"doom\00", comdat, align 1
@"??_C@_04GJMIEFLF@DOOM?$AA@" = linkonce_odr dso_local unnamed_addr constant [5 x i8] c"DOOM\00", comdat, align 1
@"??_C@_03BKBIMMBE@ABD?$AA@" = linkonce_odr dso_local unnamed_addr constant [4 x i8] c"ABD\00", comdat, align 1
@"??_C@_03FFFJFKND@ABC?$AA@" = linkonce_odr dso_local unnamed_addr constant [4 x i8] c"ABC\00", comdat, align 1
@"??_C@_06NHMNLEFC@wolf3d?$AA@" = linkonce_odr dso_local unnamed_addr constant [7 x i8] c"wolf3d\00", comdat, align 1
@"??_C@_06OLKLCMGA@WOLF3D?$AA@" = linkonce_odr dso_local unnamed_addr constant [7 x i8] c"WOLF3D\00", comdat, align 1
@"??_C@_04KPDKMPHF@WOLF?$AA@" = linkonce_odr dso_local unnamed_addr constant [5 x i8] c"WOLF\00", comdat, align 1
@"??_C@_07DCLBNMLN@generic?$AA@" = linkonce_odr dso_local unnamed_addr constant [8 x i8] c"generic\00", comdat, align 1
@"??_C@_0M@EJPOMJDM@doomgeneric?$AA@" = linkonce_odr dso_local unnamed_addr constant [12 x i8] c"doomgeneric\00", comdat, align 1
@"??_C@_03POMAGKDD@xyz?$AA@" = linkonce_odr dso_local unnamed_addr constant [4 x i8] c"xyz\00", comdat, align 1
@"??_C@_05CJBACGMB@hello?$AA@" = linkonce_odr dso_local unnamed_addr constant [6 x i8] c"hello\00", comdat, align 1
@"??_C@_0L@NAOIGMFN@TriskeleVM?$AA@" = linkonce_odr dso_local unnamed_addr constant [11 x i8] c"TriskeleVM\00", comdat, align 1
@"??_C@_04GEDDIIMJ@Doom?$AA@" = linkonce_odr dso_local unnamed_addr constant [5 x i8] c"Doom\00", comdat, align 1
@"??_C@_06KJACHCDN@v?$CFd?4?$CFd?$AA@" = linkonce_odr dso_local unnamed_addr constant [7 x i8] c"v%d.%d\00", comdat, align 1
@__local_stdio_printf_options._OptionsStorage = internal global i64 0, align 8

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local i32 @sprintf(ptr noundef %0, ptr noundef %1, ...) #0 comdat {
  %3 = alloca ptr, align 8
  %4 = alloca ptr, align 8
  %5 = alloca i32, align 4
  %6 = alloca ptr, align 8
  store ptr %1, ptr %3, align 8
  store ptr %0, ptr %4, align 8
  call void @llvm.va_start.p0(ptr %6)
  %7 = load ptr, ptr %6, align 8
  %8 = load ptr, ptr %3, align 8
  %9 = load ptr, ptr %4, align 8
  %10 = call i32 @_vsprintf_l(ptr noundef %9, ptr noundef %8, ptr noundef null, ptr noundef %7)
  store i32 %10, ptr %5, align 4
  call void @llvm.va_end.p0(ptr %6)
  %11 = load i32, ptr %5, align 4
  ret i32 %11
}

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local i32 @vsprintf(ptr noundef %0, ptr noundef %1, ptr noundef %2) #0 comdat {
  %4 = alloca ptr, align 8
  %5 = alloca ptr, align 8
  %6 = alloca ptr, align 8
  store ptr %2, ptr %4, align 8
  store ptr %1, ptr %5, align 8
  store ptr %0, ptr %6, align 8
  %7 = load ptr, ptr %4, align 8
  %8 = load ptr, ptr %5, align 8
  %9 = load ptr, ptr %6, align 8
  %10 = call i32 @_vsnprintf_l(ptr noundef %9, i64 noundef -1, ptr noundef %8, ptr noundef null, ptr noundef %7)
  ret i32 %10
}

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local i32 @_snprintf(ptr noundef %0, i64 noundef %1, ptr noundef %2, ...) #0 comdat {
  %4 = alloca ptr, align 8
  %5 = alloca i64, align 8
  %6 = alloca ptr, align 8
  %7 = alloca i32, align 4
  %8 = alloca ptr, align 8
  store ptr %2, ptr %4, align 8
  store i64 %1, ptr %5, align 8
  store ptr %0, ptr %6, align 8
  call void @llvm.va_start.p0(ptr %8)
  %9 = load ptr, ptr %8, align 8
  %10 = load ptr, ptr %4, align 8
  %11 = load i64, ptr %5, align 8
  %12 = load ptr, ptr %6, align 8
  %13 = call i32 @_vsnprintf(ptr noundef %12, i64 noundef %11, ptr noundef %10, ptr noundef %9)
  store i32 %13, ptr %7, align 4
  call void @llvm.va_end.p0(ptr %8)
  %14 = load i32, ptr %7, align 4
  ret i32 %14
}

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local i32 @_vsnprintf(ptr noundef %0, i64 noundef %1, ptr noundef %2, ptr noundef %3) #0 comdat {
  %5 = alloca ptr, align 8
  %6 = alloca ptr, align 8
  %7 = alloca i64, align 8
  %8 = alloca ptr, align 8
  store ptr %3, ptr %5, align 8
  store ptr %2, ptr %6, align 8
  store i64 %1, ptr %7, align 8
  store ptr %0, ptr %8, align 8
  %9 = load ptr, ptr %5, align 8
  %10 = load ptr, ptr %6, align 8
  %11 = load i64, ptr %7, align 8
  %12 = load ptr, ptr %8, align 8
  %13 = call i32 @_vsnprintf_l(ptr noundef %12, i64 noundef %11, ptr noundef %10, ptr noundef null, ptr noundef %9)
  ret i32 %13
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca [64 x i8], align 16
  %4 = alloca ptr, align 8
  %5 = alloca i64, align 8
  %6 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  store i32 0, ptr %2, align 4
  %7 = call i32 @atoi(ptr noundef @"??_C@_02MOKMDPNA@42?$AA@")
  %8 = icmp eq i32 %7, 42
  br i1 %8, label %9, label %18

9:                                                ; preds = %0
  %10 = call i32 @atoi(ptr noundef @"??_C@_02KACMFDGK@?97?$AA@")
  %11 = icmp eq i32 %10, -7
  br i1 %11, label %12, label %18

12:                                               ; preds = %9
  %13 = call i32 @atoi(ptr noundef @"??_C@_04KCMBDBIM@?5?510?$AA@")
  %14 = icmp eq i32 %13, 10
  br i1 %14, label %15, label %18

15:                                               ; preds = %12
  %16 = load i32, ptr %2, align 4
  %17 = or i32 %16, 1
  store i32 %17, ptr %2, align 4
  br label %18

18:                                               ; preds = %15, %12, %9, %0
  %19 = call i32 @toupper(i32 noundef 97) #5
  %20 = icmp eq i32 %19, 65
  br i1 %20, label %21, label %30

21:                                               ; preds = %18
  %22 = call i32 @tolower(i32 noundef 90) #5
  %23 = icmp eq i32 %22, 122
  br i1 %23, label %24, label %30

24:                                               ; preds = %21
  %25 = call i32 @toupper(i32 noundef 51) #5
  %26 = icmp eq i32 %25, 51
  br i1 %26, label %27, label %30

27:                                               ; preds = %24
  %28 = load i32, ptr %2, align 4
  %29 = or i32 %28, 2
  store i32 %29, ptr %2, align 4
  br label %30

30:                                               ; preds = %27, %24, %21, %18
  %31 = call i32 @isspace(i32 noundef 32) #5
  %32 = icmp ne i32 %31, 0
  br i1 %32, label %33, label %54

33:                                               ; preds = %30
  %34 = call i32 @isspace(i32 noundef 9) #5
  %35 = icmp ne i32 %34, 0
  br i1 %35, label %36, label %54

36:                                               ; preds = %33
  %37 = call i32 @isspace(i32 noundef 120) #5
  %38 = icmp ne i32 %37, 0
  br i1 %38, label %54, label %39

39:                                               ; preds = %36
  %40 = call i32 @isdigit(i32 noundef 53) #5
  %41 = icmp ne i32 %40, 0
  br i1 %41, label %42, label %54

42:                                               ; preds = %39
  %43 = call i32 @isdigit(i32 noundef 120) #5
  %44 = icmp ne i32 %43, 0
  br i1 %44, label %54, label %45

45:                                               ; preds = %42
  %46 = call i32 @isalpha(i32 noundef 97) #5
  %47 = icmp ne i32 %46, 0
  br i1 %47, label %48, label %54

48:                                               ; preds = %45
  %49 = call i32 @isalpha(i32 noundef 51) #5
  %50 = icmp ne i32 %49, 0
  br i1 %50, label %54, label %51

51:                                               ; preds = %48
  %52 = load i32, ptr %2, align 4
  %53 = or i32 %52, 4
  store i32 %53, ptr %2, align 4
  br label %54

54:                                               ; preds = %51, %48, %45, %42, %39, %36, %33, %30
  %55 = call i32 @strcasecmp(ptr noundef @"??_C@_04GJMIEFLF@DOOM?$AA@", ptr noundef @"??_C@_04KFPCKHMN@doom?$AA@")
  %56 = icmp eq i32 %55, 0
  br i1 %56, label %57, label %66

57:                                               ; preds = %54
  %58 = call i32 @strcasecmp(ptr noundef @"??_C@_03FFFJFKND@ABC?$AA@", ptr noundef @"??_C@_03BKBIMMBE@ABD?$AA@")
  %59 = icmp slt i32 %58, 0
  br i1 %59, label %60, label %66

60:                                               ; preds = %57
  %61 = call i32 @strcasecmp(ptr noundef @"??_C@_03BKBIMMBE@ABD?$AA@", ptr noundef @"??_C@_03FFFJFKND@ABC?$AA@")
  %62 = icmp sgt i32 %61, 0
  br i1 %62, label %63, label %66

63:                                               ; preds = %60
  %64 = load i32, ptr %2, align 4
  %65 = or i32 %64, 8
  store i32 %65, ptr %2, align 4
  br label %66

66:                                               ; preds = %63, %60, %57, %54
  %67 = call i32 @strncasecmp(ptr noundef @"??_C@_06OLKLCMGA@WOLF3D?$AA@", ptr noundef @"??_C@_06NHMNLEFC@wolf3d?$AA@", i64 noundef 6)
  %68 = icmp eq i32 %67, 0
  br i1 %68, label %69, label %75

69:                                               ; preds = %66
  %70 = call i32 @strncasecmp(ptr noundef @"??_C@_04KPDKMPHF@WOLF?$AA@", ptr noundef @"??_C@_06NHMNLEFC@wolf3d?$AA@", i64 noundef 4)
  %71 = icmp eq i32 %70, 0
  br i1 %71, label %72, label %75

72:                                               ; preds = %69
  %73 = load i32, ptr %2, align 4
  %74 = or i32 %73, 16
  store i32 %74, ptr %2, align 4
  br label %75

75:                                               ; preds = %72, %69, %66
  %76 = call ptr @strstr(ptr noundef @"??_C@_0M@EJPOMJDM@doomgeneric?$AA@", ptr noundef @"??_C@_07DCLBNMLN@generic?$AA@") #6
  %77 = icmp ne ptr %76, null
  br i1 %77, label %78, label %84

78:                                               ; preds = %75
  %79 = call ptr @strstr(ptr noundef @"??_C@_05CJBACGMB@hello?$AA@", ptr noundef @"??_C@_03POMAGKDD@xyz?$AA@") #6
  %80 = icmp eq ptr %79, null
  br i1 %80, label %81, label %84

81:                                               ; preds = %78
  %82 = load i32, ptr %2, align 4
  %83 = or i32 %82, 32
  store i32 %83, ptr %2, align 4
  br label %84

84:                                               ; preds = %81, %78, %75
  %85 = call ptr @strdup(ptr noundef @"??_C@_0L@NAOIGMFN@TriskeleVM?$AA@") #6
  store ptr %85, ptr %4, align 8
  %86 = load ptr, ptr %4, align 8
  %87 = icmp ne ptr %86, null
  br i1 %87, label %88, label %95

88:                                               ; preds = %84
  %89 = load ptr, ptr %4, align 8
  %90 = call i32 @strcmp(ptr noundef %89, ptr noundef @"??_C@_0L@NAOIGMFN@TriskeleVM?$AA@") #6
  %91 = icmp eq i32 %90, 0
  br i1 %91, label %92, label %95

92:                                               ; preds = %88
  %93 = load i32, ptr %2, align 4
  %94 = or i32 %93, 64
  store i32 %94, ptr %2, align 4
  br label %95

95:                                               ; preds = %92, %88, %84
  %96 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 0
  store i8 0, ptr %96, align 16
  %97 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 0
  %98 = call i64 @strlcpy(ptr noundef %97, ptr noundef @"??_C@_04GEDDIIMJ@Doom?$AA@", i64 noundef 64)
  store i64 %98, ptr %5, align 8
  %99 = load i64, ptr %5, align 8
  %100 = icmp eq i64 %99, 4
  br i1 %100, label %101, label %108

101:                                              ; preds = %95
  %102 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 0
  %103 = call i32 @strcmp(ptr noundef %102, ptr noundef @"??_C@_04GEDDIIMJ@Doom?$AA@") #6
  %104 = icmp eq i32 %103, 0
  br i1 %104, label %105, label %108

105:                                              ; preds = %101
  %106 = load i32, ptr %2, align 4
  %107 = or i32 %106, 128
  store i32 %107, ptr %2, align 4
  br label %108

108:                                              ; preds = %105, %101, %95
  %109 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 0
  store i8 0, ptr %109, align 16
  %110 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 0
  %111 = call i32 (ptr, i64, ptr, ...) @snprintf(ptr noundef %110, i64 noundef 64, ptr noundef @"??_C@_06KJACHCDN@v?$CFd?4?$CFd?$AA@", i64 noundef 0, i32 noundef 3) #6
  store i32 %111, ptr %6, align 4
  %112 = load i32, ptr %6, align 4
  %113 = icmp eq i32 %112, 4
  br i1 %113, label %114, label %137

114:                                              ; preds = %108
  %115 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 0
  %116 = load i8, ptr %115, align 16
  %117 = sext i8 %116 to i32
  %118 = icmp eq i32 %117, 118
  br i1 %118, label %119, label %137

119:                                              ; preds = %114
  %120 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 1
  %121 = load i8, ptr %120, align 1
  %122 = sext i8 %121 to i32
  %123 = icmp eq i32 %122, 48
  br i1 %123, label %124, label %137

124:                                              ; preds = %119
  %125 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 2
  %126 = load i8, ptr %125, align 2
  %127 = sext i8 %126 to i32
  %128 = icmp eq i32 %127, 46
  br i1 %128, label %129, label %137

129:                                              ; preds = %124
  %130 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 3
  %131 = load i8, ptr %130, align 1
  %132 = sext i8 %131 to i32
  %133 = icmp eq i32 %132, 51
  br i1 %133, label %134, label %137

134:                                              ; preds = %129
  %135 = load i32, ptr %2, align 4
  %136 = or i32 %135, 256
  store i32 %136, ptr %2, align 4
  br label %137

137:                                              ; preds = %134, %129, %124, %119, %114, %108
  %138 = load i32, ptr %2, align 4
  ret i32 %138
}

declare dso_local i32 @atoi(ptr noundef) #1

; Function Attrs: nounwind willreturn memory(read)
declare dso_local i32 @toupper(i32 noundef) #2

; Function Attrs: nounwind willreturn memory(read)
declare dso_local i32 @tolower(i32 noundef) #2

; Function Attrs: nounwind willreturn memory(read)
declare dso_local i32 @isspace(i32 noundef) #2

; Function Attrs: nounwind willreturn memory(read)
declare dso_local i32 @isdigit(i32 noundef) #2

; Function Attrs: nounwind willreturn memory(read)
declare dso_local i32 @isalpha(i32 noundef) #2

declare dso_local i32 @strcasecmp(ptr noundef, ptr noundef) #1

declare dso_local i32 @strncasecmp(ptr noundef, ptr noundef, i64 noundef) #1

; Function Attrs: nounwind
declare dso_local ptr @strstr(ptr noundef, ptr noundef) #3

; Function Attrs: nounwind
declare dso_local ptr @strdup(ptr noundef) #3

; Function Attrs: nounwind
declare dso_local i32 @strcmp(ptr noundef, ptr noundef) #3

declare dso_local i64 @strlcpy(ptr noundef, ptr noundef, i64 noundef) #1

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local i32 @snprintf(ptr noundef %0, i64 noundef %1, ptr noundef %2, ...) #0 comdat {
  %4 = alloca ptr, align 8
  %5 = alloca i64, align 8
  %6 = alloca ptr, align 8
  %7 = alloca i32, align 4
  %8 = alloca ptr, align 8
  store ptr %2, ptr %4, align 8
  store i64 %1, ptr %5, align 8
  store ptr %0, ptr %6, align 8
  call void @llvm.va_start.p0(ptr %8)
  %9 = load ptr, ptr %8, align 8
  %10 = load ptr, ptr %4, align 8
  %11 = load i64, ptr %5, align 8
  %12 = load ptr, ptr %6, align 8
  %13 = call i32 @vsnprintf(ptr noundef %12, i64 noundef %11, ptr noundef %10, ptr noundef %9) #6
  store i32 %13, ptr %7, align 4
  call void @llvm.va_end.p0(ptr %8)
  %14 = load i32, ptr %7, align 4
  ret i32 %14
}

; Function Attrs: nocallback nofree nosync nounwind willreturn
declare void @llvm.va_start.p0(ptr) #4

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local i32 @_vsprintf_l(ptr noundef %0, ptr noundef %1, ptr noundef %2, ptr noundef %3) #0 comdat {
  %5 = alloca ptr, align 8
  %6 = alloca ptr, align 8
  %7 = alloca ptr, align 8
  %8 = alloca ptr, align 8
  store ptr %3, ptr %5, align 8
  store ptr %2, ptr %6, align 8
  store ptr %1, ptr %7, align 8
  store ptr %0, ptr %8, align 8
  %9 = load ptr, ptr %5, align 8
  %10 = load ptr, ptr %6, align 8
  %11 = load ptr, ptr %7, align 8
  %12 = load ptr, ptr %8, align 8
  %13 = call i32 @_vsnprintf_l(ptr noundef %12, i64 noundef -1, ptr noundef %11, ptr noundef %10, ptr noundef %9)
  ret i32 %13
}

; Function Attrs: nocallback nofree nosync nounwind willreturn
declare void @llvm.va_end.p0(ptr) #4

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local i32 @_vsnprintf_l(ptr noundef %0, i64 noundef %1, ptr noundef %2, ptr noundef %3, ptr noundef %4) #0 comdat {
  %6 = alloca ptr, align 8
  %7 = alloca ptr, align 8
  %8 = alloca ptr, align 8
  %9 = alloca i64, align 8
  %10 = alloca ptr, align 8
  %11 = alloca i32, align 4
  store ptr %4, ptr %6, align 8
  store ptr %3, ptr %7, align 8
  store ptr %2, ptr %8, align 8
  store i64 %1, ptr %9, align 8
  store ptr %0, ptr %10, align 8
  %12 = load ptr, ptr %6, align 8
  %13 = load ptr, ptr %7, align 8
  %14 = load ptr, ptr %8, align 8
  %15 = load i64, ptr %9, align 8
  %16 = load ptr, ptr %10, align 8
  %17 = call ptr @__local_stdio_printf_options()
  %18 = load i64, ptr %17, align 8
  %19 = or i64 %18, 1
  %20 = call i32 @__stdio_common_vsprintf(i64 noundef %19, ptr noundef %16, i64 noundef %15, ptr noundef %14, ptr noundef %13, ptr noundef %12)
  store i32 %20, ptr %11, align 4
  %21 = load i32, ptr %11, align 4
  %22 = icmp slt i32 %21, 0
  br i1 %22, label %23, label %24

23:                                               ; preds = %5
  br label %26

24:                                               ; preds = %5
  %25 = load i32, ptr %11, align 4
  br label %26

26:                                               ; preds = %24, %23
  %27 = phi i32 [ -1, %23 ], [ %25, %24 ]
  ret i32 %27
}

declare dso_local i32 @__stdio_common_vsprintf(i64 noundef, ptr noundef, i64 noundef, ptr noundef, ptr noundef, ptr noundef) #1

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local ptr @__local_stdio_printf_options() #0 comdat {
  ret ptr @__local_stdio_printf_options._OptionsStorage
}

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local i32 @vsnprintf(ptr noundef %0, i64 noundef %1, ptr noundef %2, ptr noundef %3) #0 comdat {
  %5 = alloca ptr, align 8
  %6 = alloca ptr, align 8
  %7 = alloca i64, align 8
  %8 = alloca ptr, align 8
  %9 = alloca i32, align 4
  store ptr %3, ptr %5, align 8
  store ptr %2, ptr %6, align 8
  store i64 %1, ptr %7, align 8
  store ptr %0, ptr %8, align 8
  %10 = load ptr, ptr %5, align 8
  %11 = load ptr, ptr %6, align 8
  %12 = load i64, ptr %7, align 8
  %13 = load ptr, ptr %8, align 8
  %14 = call ptr @__local_stdio_printf_options()
  %15 = load i64, ptr %14, align 8
  %16 = or i64 %15, 2
  %17 = call i32 @__stdio_common_vsprintf(i64 noundef %16, ptr noundef %13, i64 noundef %12, ptr noundef %11, ptr noundef null, ptr noundef %10)
  store i32 %17, ptr %9, align 4
  %18 = load i32, ptr %9, align 4
  %19 = icmp slt i32 %18, 0
  br i1 %19, label %20, label %21

20:                                               ; preds = %4
  br label %23

21:                                               ; preds = %4
  %22 = load i32, ptr %9, align 4
  br label %23

23:                                               ; preds = %21, %20
  %24 = phi i32 [ -1, %20 ], [ %22, %21 ]
  ret i32 %24
}

attributes #0 = { noinline nounwind optnone uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { nounwind willreturn memory(read) "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #3 = { nounwind "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #4 = { nocallback nofree nosync nounwind willreturn }
attributes #5 = { nounwind willreturn memory(read) }
attributes #6 = { nounwind }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\toolchain-tests/c89/test_doom_libc\\src\\test_doom_libc.c", directory: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 1, !"wchar_size", i32 2}
!4 = !{i32 8, !"PIC Level", i32 2}
!5 = !{i32 7, !"uwtable", i32 2}
!6 = !{i32 1, !"MaxTLSAlign", i32 65536}
!7 = !{!"clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)"}
