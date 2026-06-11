; ModuleID = 'E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\projects\toolchain-tests/c89/test_variadic\src/test_variadic.c'
source_filename = "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\toolchain-tests/c89/test_variadic\\src/test_variadic.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-windows-msvc19.51.36246"

$sprintf = comdat any

$vsprintf = comdat any

$_snprintf = comdat any

$_vsnprintf = comdat any

$printf = comdat any

$_vsprintf_l = comdat any

$_vsnprintf_l = comdat any

$__local_stdio_printf_options = comdat any

$_vfprintf_l = comdat any

$"??_C@_03PMGGPEJJ@?$CFd?6?$AA@" = comdat any

$"??_C@_02DPKJAMEF@?$CFd?$AA@" = comdat any

$"??_C@_05CJBACGMB@hello?$AA@" = comdat any

$"??_C@_02DKCKIIND@?$CFs?$AA@" = comdat any

$"??_C@_08EOAOKAEG@?$CFd?$CL?$CFd?$DN?$CFd?$AA@" = comdat any

$"??_C@_06EPBHIJPH@val?$DN?$CFd?$AA@" = comdat any

$"??_C@_01FJMABOPO@x?$AA@" = comdat any

$"??_C@_05HKPGCKL@?$CFs?3?$CFd?$AA@" = comdat any

$"??_C@_03DJDALPN@ok?6?$AA@" = comdat any

$"??_C@_06EDLDFGHC@err?$DN?$CFd?$AA@" = comdat any

@"??_C@_03PMGGPEJJ@?$CFd?6?$AA@" = linkonce_odr dso_local unnamed_addr constant [4 x i8] c"%d\0A\00", comdat, align 1
@"??_C@_02DPKJAMEF@?$CFd?$AA@" = linkonce_odr dso_local unnamed_addr constant [3 x i8] c"%d\00", comdat, align 1
@"??_C@_05CJBACGMB@hello?$AA@" = linkonce_odr dso_local unnamed_addr constant [6 x i8] c"hello\00", comdat, align 1
@"??_C@_02DKCKIIND@?$CFs?$AA@" = linkonce_odr dso_local unnamed_addr constant [3 x i8] c"%s\00", comdat, align 1
@"??_C@_08EOAOKAEG@?$CFd?$CL?$CFd?$DN?$CFd?$AA@" = linkonce_odr dso_local unnamed_addr constant [9 x i8] c"%d+%d=%d\00", comdat, align 1
@"??_C@_06EPBHIJPH@val?$DN?$CFd?$AA@" = linkonce_odr dso_local unnamed_addr constant [7 x i8] c"val=%d\00", comdat, align 1
@"??_C@_01FJMABOPO@x?$AA@" = linkonce_odr dso_local unnamed_addr constant [2 x i8] c"x\00", comdat, align 1
@"??_C@_05HKPGCKL@?$CFs?3?$CFd?$AA@" = linkonce_odr dso_local unnamed_addr constant [6 x i8] c"%s:%d\00", comdat, align 1
@"??_C@_03DJDALPN@ok?6?$AA@" = linkonce_odr dso_local unnamed_addr constant [4 x i8] c"ok\0A\00", comdat, align 1
@"??_C@_06EDLDFGHC@err?$DN?$CFd?$AA@" = linkonce_odr dso_local unnamed_addr constant [7 x i8] c"err=%d\00", comdat, align 1
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
  %4 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  store i32 0, ptr %2, align 4
  %5 = call i32 (ptr, ...) @printf(ptr noundef @"??_C@_03PMGGPEJJ@?$CFd?6?$AA@", i32 noundef 42)
  store i32 %5, ptr %4, align 4
  %6 = load i32, ptr %4, align 4
  %7 = icmp sge i32 %6, 2
  br i1 %7, label %8, label %11

8:                                                ; preds = %0
  %9 = load i32, ptr %2, align 4
  %10 = or i32 %9, 1
  store i32 %10, ptr %2, align 4
  br label %11

11:                                               ; preds = %8, %0
  %12 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 0
  store i8 0, ptr %12, align 16
  %13 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 0
  %14 = call i32 (ptr, ptr, ...) @sprintf(ptr noundef %13, ptr noundef @"??_C@_02DPKJAMEF@?$CFd?$AA@", i32 noundef 99) #3
  %15 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 0
  %16 = load i8, ptr %15, align 16
  %17 = sext i8 %16 to i32
  %18 = icmp eq i32 %17, 57
  br i1 %18, label %19, label %32

19:                                               ; preds = %11
  %20 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 1
  %21 = load i8, ptr %20, align 1
  %22 = sext i8 %21 to i32
  %23 = icmp eq i32 %22, 57
  br i1 %23, label %24, label %32

24:                                               ; preds = %19
  %25 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 2
  %26 = load i8, ptr %25, align 2
  %27 = sext i8 %26 to i32
  %28 = icmp eq i32 %27, 0
  br i1 %28, label %29, label %32

29:                                               ; preds = %24
  %30 = load i32, ptr %2, align 4
  %31 = or i32 %30, 2
  store i32 %31, ptr %2, align 4
  br label %32

32:                                               ; preds = %29, %24, %19, %11
  %33 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 0
  store i8 0, ptr %33, align 16
  %34 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 0
  %35 = call i32 (ptr, ptr, ...) @sprintf(ptr noundef %34, ptr noundef @"??_C@_02DKCKIIND@?$CFs?$AA@", ptr noundef @"??_C@_05CJBACGMB@hello?$AA@") #3
  %36 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 0
  %37 = load i8, ptr %36, align 16
  %38 = sext i8 %37 to i32
  %39 = icmp eq i32 %38, 104
  br i1 %39, label %40, label %63

40:                                               ; preds = %32
  %41 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 1
  %42 = load i8, ptr %41, align 1
  %43 = sext i8 %42 to i32
  %44 = icmp eq i32 %43, 101
  br i1 %44, label %45, label %63

45:                                               ; preds = %40
  %46 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 2
  %47 = load i8, ptr %46, align 2
  %48 = sext i8 %47 to i32
  %49 = icmp eq i32 %48, 108
  br i1 %49, label %50, label %63

50:                                               ; preds = %45
  %51 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 3
  %52 = load i8, ptr %51, align 1
  %53 = sext i8 %52 to i32
  %54 = icmp eq i32 %53, 108
  br i1 %54, label %55, label %63

55:                                               ; preds = %50
  %56 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 4
  %57 = load i8, ptr %56, align 4
  %58 = sext i8 %57 to i32
  %59 = icmp eq i32 %58, 111
  br i1 %59, label %60, label %63

60:                                               ; preds = %55
  %61 = load i32, ptr %2, align 4
  %62 = or i32 %61, 4
  store i32 %62, ptr %2, align 4
  br label %63

63:                                               ; preds = %60, %55, %50, %45, %40, %32
  %64 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 0
  store i8 0, ptr %64, align 16
  %65 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 0
  %66 = call i32 (ptr, ptr, ...) @sprintf(ptr noundef %65, ptr noundef @"??_C@_08EOAOKAEG@?$CFd?$CL?$CFd?$DN?$CFd?$AA@", i32 noundef 1, i32 noundef 2, i32 noundef 3) #3
  %67 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 0
  %68 = load i8, ptr %67, align 16
  %69 = sext i8 %68 to i32
  %70 = icmp eq i32 %69, 49
  br i1 %70, label %71, label %84

71:                                               ; preds = %63
  %72 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 2
  %73 = load i8, ptr %72, align 2
  %74 = sext i8 %73 to i32
  %75 = icmp eq i32 %74, 50
  br i1 %75, label %76, label %84

76:                                               ; preds = %71
  %77 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 4
  %78 = load i8, ptr %77, align 4
  %79 = sext i8 %78 to i32
  %80 = icmp eq i32 %79, 51
  br i1 %80, label %81, label %84

81:                                               ; preds = %76
  %82 = load i32, ptr %2, align 4
  %83 = or i32 %82, 8
  store i32 %83, ptr %2, align 4
  br label %84

84:                                               ; preds = %81, %76, %71, %63
  %85 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 0
  store i8 0, ptr %85, align 16
  %86 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 0
  %87 = call i32 (ptr, ptr, ...) @my_format(ptr noundef %86, ptr noundef @"??_C@_06EPBHIJPH@val?$DN?$CFd?$AA@", i32 noundef 7)
  %88 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 0
  %89 = load i8, ptr %88, align 16
  %90 = sext i8 %89 to i32
  %91 = icmp eq i32 %90, 118
  br i1 %91, label %92, label %115

92:                                               ; preds = %84
  %93 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 1
  %94 = load i8, ptr %93, align 1
  %95 = sext i8 %94 to i32
  %96 = icmp eq i32 %95, 97
  br i1 %96, label %97, label %115

97:                                               ; preds = %92
  %98 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 2
  %99 = load i8, ptr %98, align 2
  %100 = sext i8 %99 to i32
  %101 = icmp eq i32 %100, 108
  br i1 %101, label %102, label %115

102:                                              ; preds = %97
  %103 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 3
  %104 = load i8, ptr %103, align 1
  %105 = sext i8 %104 to i32
  %106 = icmp eq i32 %105, 61
  br i1 %106, label %107, label %115

107:                                              ; preds = %102
  %108 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 4
  %109 = load i8, ptr %108, align 4
  %110 = sext i8 %109 to i32
  %111 = icmp eq i32 %110, 55
  br i1 %111, label %112, label %115

112:                                              ; preds = %107
  %113 = load i32, ptr %2, align 4
  %114 = or i32 %113, 16
  store i32 %114, ptr %2, align 4
  br label %115

115:                                              ; preds = %112, %107, %102, %97, %92, %84
  %116 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 0
  store i8 0, ptr %116, align 16
  %117 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 0
  %118 = call i32 (ptr, ptr, ...) @my_format(ptr noundef %117, ptr noundef @"??_C@_05HKPGCKL@?$CFs?3?$CFd?$AA@", ptr noundef @"??_C@_01FJMABOPO@x?$AA@", i32 noundef 5)
  %119 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 0
  %120 = load i8, ptr %119, align 16
  %121 = sext i8 %120 to i32
  %122 = icmp eq i32 %121, 120
  br i1 %122, label %123, label %136

123:                                              ; preds = %115
  %124 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 1
  %125 = load i8, ptr %124, align 1
  %126 = sext i8 %125 to i32
  %127 = icmp eq i32 %126, 58
  br i1 %127, label %128, label %136

128:                                              ; preds = %123
  %129 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 2
  %130 = load i8, ptr %129, align 2
  %131 = sext i8 %130 to i32
  %132 = icmp eq i32 %131, 53
  br i1 %132, label %133, label %136

133:                                              ; preds = %128
  %134 = load i32, ptr %2, align 4
  %135 = or i32 %134, 32
  store i32 %135, ptr %2, align 4
  br label %136

136:                                              ; preds = %133, %128, %123, %115
  %137 = call i32 (ptr, ...) @printf(ptr noundef @"??_C@_03DJDALPN@ok?6?$AA@")
  store i32 %137, ptr %4, align 4
  %138 = load i32, ptr %4, align 4
  %139 = icmp sge i32 %138, 2
  br i1 %139, label %140, label %143

140:                                              ; preds = %136
  %141 = load i32, ptr %2, align 4
  %142 = or i32 %141, 64
  store i32 %142, ptr %2, align 4
  br label %143

143:                                              ; preds = %140, %136
  %144 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 0
  store i8 0, ptr %144, align 16
  %145 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 0
  call void (ptr, ptr, ...) @my_error_str(ptr noundef %145, ptr noundef @"??_C@_06EDLDFGHC@err?$DN?$CFd?$AA@", i32 noundef 42)
  %146 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 0
  %147 = load i8, ptr %146, align 16
  %148 = sext i8 %147 to i32
  %149 = icmp eq i32 %148, 101
  br i1 %149, label %150, label %178

150:                                              ; preds = %143
  %151 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 1
  %152 = load i8, ptr %151, align 1
  %153 = sext i8 %152 to i32
  %154 = icmp eq i32 %153, 114
  br i1 %154, label %155, label %178

155:                                              ; preds = %150
  %156 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 2
  %157 = load i8, ptr %156, align 2
  %158 = sext i8 %157 to i32
  %159 = icmp eq i32 %158, 114
  br i1 %159, label %160, label %178

160:                                              ; preds = %155
  %161 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 3
  %162 = load i8, ptr %161, align 1
  %163 = sext i8 %162 to i32
  %164 = icmp eq i32 %163, 61
  br i1 %164, label %165, label %178

165:                                              ; preds = %160
  %166 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 4
  %167 = load i8, ptr %166, align 4
  %168 = sext i8 %167 to i32
  %169 = icmp eq i32 %168, 52
  br i1 %169, label %170, label %178

170:                                              ; preds = %165
  %171 = getelementptr inbounds [64 x i8], ptr %3, i64 0, i64 5
  %172 = load i8, ptr %171, align 1
  %173 = sext i8 %172 to i32
  %174 = icmp eq i32 %173, 50
  br i1 %174, label %175, label %178

175:                                              ; preds = %170
  %176 = load i32, ptr %2, align 4
  %177 = or i32 %176, 128
  store i32 %177, ptr %2, align 4
  br label %178

178:                                              ; preds = %175, %170, %165, %160, %155, %150, %143
  %179 = load i32, ptr %2, align 4
  ret i32 %179
}

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local i32 @printf(ptr noundef %0, ...) #0 comdat {
  %2 = alloca ptr, align 8
  %3 = alloca i32, align 4
  %4 = alloca ptr, align 8
  store ptr %0, ptr %2, align 8
  call void @llvm.va_start.p0(ptr %4)
  %5 = load ptr, ptr %4, align 8
  %6 = load ptr, ptr %2, align 8
  %7 = call ptr @__acrt_iob_func(i32 noundef 1)
  %8 = call i32 @_vfprintf_l(ptr noundef %7, ptr noundef %6, ptr noundef null, ptr noundef %5)
  store i32 %8, ptr %3, align 4
  call void @llvm.va_end.p0(ptr %4)
  %9 = load i32, ptr %3, align 4
  ret i32 %9
}

; Function Attrs: noinline nounwind optnone uwtable
define internal i32 @my_format(ptr noundef %0, ptr noundef %1, ...) #0 {
  %3 = alloca ptr, align 8
  %4 = alloca ptr, align 8
  %5 = alloca ptr, align 8
  %6 = alloca i32, align 4
  store ptr %1, ptr %3, align 8
  store ptr %0, ptr %4, align 8
  call void @llvm.va_start.p0(ptr %5)
  %7 = load ptr, ptr %5, align 8
  %8 = load ptr, ptr %3, align 8
  %9 = load ptr, ptr %4, align 8
  %10 = call i32 @vsprintf(ptr noundef %9, ptr noundef %8, ptr noundef %7) #3
  store i32 %10, ptr %6, align 4
  call void @llvm.va_end.p0(ptr %5)
  %11 = load i32, ptr %6, align 4
  ret i32 %11
}

; Function Attrs: noinline nounwind optnone uwtable
define internal void @my_error_str(ptr noundef %0, ptr noundef %1, ...) #0 {
  %3 = alloca ptr, align 8
  %4 = alloca ptr, align 8
  %5 = alloca ptr, align 8
  store ptr %1, ptr %3, align 8
  store ptr %0, ptr %4, align 8
  call void @llvm.va_start.p0(ptr %5)
  %6 = load ptr, ptr %5, align 8
  %7 = load ptr, ptr %3, align 8
  %8 = load ptr, ptr %4, align 8
  %9 = call i32 @vsprintf(ptr noundef %8, ptr noundef %7, ptr noundef %6) #3
  call void @llvm.va_end.p0(ptr %5)
  ret void
}

; Function Attrs: nocallback nofree nosync nounwind willreturn
declare void @llvm.va_start.p0(ptr) #1

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
declare void @llvm.va_end.p0(ptr) #1

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

declare dso_local i32 @__stdio_common_vsprintf(i64 noundef, ptr noundef, i64 noundef, ptr noundef, ptr noundef, ptr noundef) #2

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local ptr @__local_stdio_printf_options() #0 comdat {
  ret ptr @__local_stdio_printf_options._OptionsStorage
}

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local i32 @_vfprintf_l(ptr noundef %0, ptr noundef %1, ptr noundef %2, ptr noundef %3) #0 comdat {
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
  %13 = call ptr @__local_stdio_printf_options()
  %14 = load i64, ptr %13, align 8
  %15 = call i32 @__stdio_common_vfprintf(i64 noundef %14, ptr noundef %12, ptr noundef %11, ptr noundef %10, ptr noundef %9)
  ret i32 %15
}

declare dso_local ptr @__acrt_iob_func(i32 noundef) #2

declare dso_local i32 @__stdio_common_vfprintf(i64 noundef, ptr noundef, ptr noundef, ptr noundef, ptr noundef) #2

attributes #0 = { noinline nounwind optnone uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nocallback nofree nosync nounwind willreturn }
attributes #2 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #3 = { nounwind }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\toolchain-tests/c89/test_variadic\\src\\test_variadic.c", directory: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 1, !"wchar_size", i32 2}
!4 = !{i32 8, !"PIC Level", i32 2}
!5 = !{i32 7, !"uwtable", i32 2}
!6 = !{i32 1, !"MaxTLSAlign", i32 65536}
!7 = !{!"clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)"}
