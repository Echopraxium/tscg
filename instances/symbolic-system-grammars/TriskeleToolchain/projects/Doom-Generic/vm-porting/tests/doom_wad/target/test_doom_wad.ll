; ModuleID = 'E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\projects\Doom-Generic/vm-porting/tests/doom_wad\src/test_doom_wad.c'
source_filename = "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\Doom-Generic/vm-porting/tests/doom_wad\\src/test_doom_wad.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-windows-msvc19.51.36246"

$sprintf = comdat any

$vsprintf = comdat any

$_snprintf = comdat any

$_vsnprintf = comdat any

$vsnprintf = comdat any

$printf = comdat any

$_vsprintf_l = comdat any

$_vsnprintf_l = comdat any

$__local_stdio_printf_options = comdat any

$_vfprintf_l = comdat any

$"??_C@_0N@CCCCPFEN@I_Error?3?5?$CFs?6?$AA@" = comdat any

$"??_C@_0BL@INEDCBAC@I_ZoneBase?3?5malloc?5failed?6?$AA@" = comdat any

$"??_C@_04KFPCKHMN@doom?$AA@" = comdat any

$"??_C@_05IAABINL@doom2?$AA@" = comdat any

$"??_C@_03DDPMENPA@tnt?$AA@" = comdat any

$"??_C@_08LLIJOHMO@plutonia?$AA@" = comdat any

$"??_C@_04LACHCAKG@chex?$AA@" = comdat any

$"??_C@_04LOHCCCIP@hacx?$AA@" = comdat any

$"??_C@_07CIFAGBMG@unknown?$AA@" = comdat any

$"??_C@_0BB@NDKCCECJ@test_minimal?4wad?$AA@" = comdat any

$"??_C@_07FLMOFAHC@PLAYPAL?$AA@" = comdat any

$"??_C@_06BBOHFMBE@ENDOOM?$AA@" = comdat any

$"??_C@_02GMLFBBN@wb?$AA@" = comdat any

@"??_C@_0N@CCCCPFEN@I_Error?3?5?$CFs?6?$AA@" = linkonce_odr dso_local unnamed_addr constant [13 x i8] c"I_Error: %s\0A\00", comdat, align 1
@"??_C@_0BL@INEDCBAC@I_ZoneBase?3?5malloc?5failed?6?$AA@" = linkonce_odr dso_local unnamed_addr constant [27 x i8] c"I_ZoneBase: malloc failed\0A\00", comdat, align 1
@"??_C@_04KFPCKHMN@doom?$AA@" = linkonce_odr dso_local unnamed_addr constant [5 x i8] c"doom\00", comdat, align 1
@"??_C@_05IAABINL@doom2?$AA@" = linkonce_odr dso_local unnamed_addr constant [6 x i8] c"doom2\00", comdat, align 1
@"??_C@_03DDPMENPA@tnt?$AA@" = linkonce_odr dso_local unnamed_addr constant [4 x i8] c"tnt\00", comdat, align 1
@"??_C@_08LLIJOHMO@plutonia?$AA@" = linkonce_odr dso_local unnamed_addr constant [9 x i8] c"plutonia\00", comdat, align 1
@"??_C@_04LACHCAKG@chex?$AA@" = linkonce_odr dso_local unnamed_addr constant [5 x i8] c"chex\00", comdat, align 1
@"??_C@_04LOHCCCIP@hacx?$AA@" = linkonce_odr dso_local unnamed_addr constant [5 x i8] c"hacx\00", comdat, align 1
@"??_C@_07CIFAGBMG@unknown?$AA@" = linkonce_odr dso_local unnamed_addr constant [8 x i8] c"unknown\00", comdat, align 1
@"??_C@_0BB@NDKCCECJ@test_minimal?4wad?$AA@" = linkonce_odr dso_local unnamed_addr constant [17 x i8] c"test_minimal.wad\00", comdat, align 1
@numlumps = external dso_local global i32, align 4
@"??_C@_07FLMOFAHC@PLAYPAL?$AA@" = linkonce_odr dso_local unnamed_addr constant [8 x i8] c"PLAYPAL\00", comdat, align 1
@"??_C@_06BBOHFMBE@ENDOOM?$AA@" = linkonce_odr dso_local unnamed_addr constant [7 x i8] c"ENDOOM\00", comdat, align 1
@__local_stdio_printf_options._OptionsStorage = internal global i64 0, align 8
@"??_C@_02GMLFBBN@wb?$AA@" = linkonce_odr dso_local unnamed_addr constant [3 x i8] c"wb\00", comdat, align 1

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
define dso_local void @I_Error(ptr noundef %0, ...) #0 {
  %2 = alloca ptr, align 8
  %3 = alloca [256 x i8], align 16
  %4 = alloca ptr, align 8
  store ptr %0, ptr %2, align 8
  call void @llvm.va_start.p0(ptr %4)
  %5 = load ptr, ptr %4, align 8
  %6 = load ptr, ptr %2, align 8
  %7 = getelementptr inbounds [256 x i8], ptr %3, i64 0, i64 0
  %8 = call i32 @vsnprintf(ptr noundef %7, i64 noundef 256, ptr noundef %6, ptr noundef %5) #8
  call void @llvm.va_end.p0(ptr %4)
  %9 = getelementptr inbounds [256 x i8], ptr %3, i64 0, i64 0
  %10 = call i32 (ptr, ...) @printf(ptr noundef @"??_C@_0N@CCCCPFEN@I_Error?3?5?$CFs?6?$AA@", ptr noundef %9)
  call void @exit(i32 noundef 1) #9
  unreachable
}

; Function Attrs: nocallback nofree nosync nounwind willreturn
declare void @llvm.va_start.p0(ptr) #1

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

; Function Attrs: nocallback nofree nosync nounwind willreturn
declare void @llvm.va_end.p0(ptr) #1

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

; Function Attrs: noreturn
declare dso_local void @exit(i32 noundef) #2

; Function Attrs: noinline nounwind optnone uwtable
define dso_local ptr @I_ZoneBase(ptr noundef %0) #0 {
  %2 = alloca ptr, align 8
  %3 = alloca ptr, align 8
  store ptr %0, ptr %2, align 8
  %4 = call noalias ptr @malloc(i64 noundef 1048576) #10
  store ptr %4, ptr %3, align 8
  %5 = load ptr, ptr %3, align 8
  %6 = icmp ne ptr %5, null
  br i1 %6, label %9, label %7

7:                                                ; preds = %1
  %8 = call i32 (ptr, ...) @printf(ptr noundef @"??_C@_0BL@INEDCBAC@I_ZoneBase?3?5malloc?5failed?6?$AA@")
  call void @exit(i32 noundef 1) #9
  unreachable

9:                                                ; preds = %1
  %10 = load ptr, ptr %2, align 8
  store i32 1048576, ptr %10, align 4
  %11 = load ptr, ptr %3, align 8
  ret ptr %11
}

; Function Attrs: allocsize(0)
declare dso_local noalias ptr @malloc(i64 noundef) #3

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @I_BeginRead() #0 {
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @I_EndRead() #0 {
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @M_FileLength(ptr noundef %0) #0 {
  %2 = alloca ptr, align 8
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  store ptr %0, ptr %2, align 8
  %5 = load ptr, ptr %2, align 8
  %6 = call i32 @ftell(ptr noundef %5)
  store i32 %6, ptr %3, align 4
  %7 = load ptr, ptr %2, align 8
  %8 = call i32 @fseek(ptr noundef %7, i32 noundef 0, i32 noundef 2)
  %9 = load ptr, ptr %2, align 8
  %10 = call i32 @ftell(ptr noundef %9)
  store i32 %10, ptr %4, align 4
  %11 = load i32, ptr %3, align 4
  %12 = load ptr, ptr %2, align 8
  %13 = call i32 @fseek(ptr noundef %12, i32 noundef %11, i32 noundef 0)
  %14 = load i32, ptr %4, align 4
  ret i32 %14
}

declare dso_local i32 @ftell(ptr noundef) #4

declare dso_local i32 @fseek(ptr noundef, i32 noundef, i32 noundef) #4

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @M_StringCopy(ptr noundef %0, ptr noundef %1, i64 noundef %2) #0 {
  %4 = alloca i32, align 4
  %5 = alloca i64, align 8
  %6 = alloca ptr, align 8
  %7 = alloca ptr, align 8
  store i64 %2, ptr %5, align 8
  store ptr %1, ptr %6, align 8
  store ptr %0, ptr %7, align 8
  %8 = load i64, ptr %5, align 8
  %9 = icmp ult i64 %8, 1
  br i1 %9, label %10, label %11

10:                                               ; preds = %3
  store i32 0, ptr %4, align 4
  br label %21

11:                                               ; preds = %3
  %12 = load i64, ptr %5, align 8
  %13 = sub i64 %12, 1
  %14 = load ptr, ptr %6, align 8
  %15 = load ptr, ptr %7, align 8
  %16 = call ptr @strncpy(ptr noundef %15, ptr noundef %14, i64 noundef %13) #8
  %17 = load ptr, ptr %7, align 8
  %18 = load i64, ptr %5, align 8
  %19 = sub i64 %18, 1
  %20 = getelementptr inbounds nuw i8, ptr %17, i64 %19
  store i8 0, ptr %20, align 1
  store i32 1, ptr %4, align 4
  br label %21

21:                                               ; preds = %11, %10
  %22 = load i32, ptr %4, align 4
  ret i32 %22
}

; Function Attrs: nounwind
declare dso_local ptr @strncpy(ptr noundef, ptr noundef, i64 noundef) #5

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @M_ExtractFileBase(ptr noundef %0, ptr noundef %1) #0 {
  %3 = alloca ptr, align 8
  %4 = alloca ptr, align 8
  %5 = alloca ptr, align 8
  %6 = alloca ptr, align 8
  %7 = alloca i32, align 4
  store ptr %1, ptr %3, align 8
  store ptr %0, ptr %4, align 8
  %8 = load ptr, ptr %4, align 8
  store ptr %8, ptr %5, align 8
  %9 = load ptr, ptr %4, align 8
  store ptr %9, ptr %6, align 8
  br label %10

10:                                               ; preds = %28, %2
  %11 = load ptr, ptr %6, align 8
  %12 = load i8, ptr %11, align 1
  %13 = icmp ne i8 %12, 0
  br i1 %13, label %14, label %31

14:                                               ; preds = %10
  %15 = load ptr, ptr %6, align 8
  %16 = load i8, ptr %15, align 1
  %17 = sext i8 %16 to i32
  %18 = icmp eq i32 %17, 47
  br i1 %18, label %24, label %19

19:                                               ; preds = %14
  %20 = load ptr, ptr %6, align 8
  %21 = load i8, ptr %20, align 1
  %22 = sext i8 %21 to i32
  %23 = icmp eq i32 %22, 92
  br i1 %23, label %24, label %27

24:                                               ; preds = %19, %14
  %25 = load ptr, ptr %6, align 8
  %26 = getelementptr inbounds i8, ptr %25, i64 1
  store ptr %26, ptr %5, align 8
  br label %27

27:                                               ; preds = %24, %19
  br label %28

28:                                               ; preds = %27
  %29 = load ptr, ptr %6, align 8
  %30 = getelementptr inbounds nuw i8, ptr %29, i32 1
  store ptr %30, ptr %6, align 8
  br label %10, !llvm.loop !8

31:                                               ; preds = %10
  store i32 0, ptr %7, align 4
  br label %32

32:                                               ; preds = %66, %31
  %33 = load i32, ptr %7, align 4
  %34 = icmp slt i32 %33, 8
  br i1 %34, label %35, label %51

35:                                               ; preds = %32
  %36 = load ptr, ptr %5, align 8
  %37 = load i32, ptr %7, align 4
  %38 = sext i32 %37 to i64
  %39 = getelementptr inbounds i8, ptr %36, i64 %38
  %40 = load i8, ptr %39, align 1
  %41 = sext i8 %40 to i32
  %42 = icmp ne i32 %41, 0
  br i1 %42, label %43, label %51

43:                                               ; preds = %35
  %44 = load ptr, ptr %5, align 8
  %45 = load i32, ptr %7, align 4
  %46 = sext i32 %45 to i64
  %47 = getelementptr inbounds i8, ptr %44, i64 %46
  %48 = load i8, ptr %47, align 1
  %49 = sext i8 %48 to i32
  %50 = icmp ne i32 %49, 46
  br label %51

51:                                               ; preds = %43, %35, %32
  %52 = phi i1 [ false, %35 ], [ false, %32 ], [ %50, %43 ]
  br i1 %52, label %53, label %69

53:                                               ; preds = %51
  %54 = load ptr, ptr %5, align 8
  %55 = load i32, ptr %7, align 4
  %56 = sext i32 %55 to i64
  %57 = getelementptr inbounds i8, ptr %54, i64 %56
  %58 = load i8, ptr %57, align 1
  %59 = zext i8 %58 to i32
  %60 = call i32 @toupper(i32 noundef %59) #11
  %61 = trunc i32 %60 to i8
  %62 = load ptr, ptr %3, align 8
  %63 = load i32, ptr %7, align 4
  %64 = sext i32 %63 to i64
  %65 = getelementptr inbounds i8, ptr %62, i64 %64
  store i8 %61, ptr %65, align 1
  br label %66

66:                                               ; preds = %53
  %67 = load i32, ptr %7, align 4
  %68 = add nsw i32 %67, 1
  store i32 %68, ptr %7, align 4
  br label %32, !llvm.loop !10

69:                                               ; preds = %51
  br label %70

70:                                               ; preds = %78, %69
  %71 = load i32, ptr %7, align 4
  %72 = icmp slt i32 %71, 8
  br i1 %72, label %73, label %81

73:                                               ; preds = %70
  %74 = load ptr, ptr %3, align 8
  %75 = load i32, ptr %7, align 4
  %76 = sext i32 %75 to i64
  %77 = getelementptr inbounds i8, ptr %74, i64 %76
  store i8 0, ptr %77, align 1
  br label %78

78:                                               ; preds = %73
  %79 = load i32, ptr %7, align 4
  %80 = add nsw i32 %79, 1
  store i32 %80, ptr %7, align 4
  br label %70, !llvm.loop !11

81:                                               ; preds = %70
  ret void
}

; Function Attrs: nounwind willreturn memory(read)
declare dso_local i32 @toupper(i32 noundef) #6

; Function Attrs: noinline nounwind optnone uwtable
define dso_local ptr @D_GameMissionString(i32 noundef %0) #0 {
  %2 = alloca ptr, align 8
  %3 = alloca i32, align 4
  store i32 %0, ptr %3, align 4
  %4 = load i32, ptr %3, align 4
  switch i32 %4, label %11 [
    i32 0, label %5
    i32 1, label %6
    i32 2, label %7
    i32 3, label %8
    i32 4, label %9
    i32 5, label %10
  ]

5:                                                ; preds = %1
  store ptr @"??_C@_04KFPCKHMN@doom?$AA@", ptr %2, align 8
  br label %12

6:                                                ; preds = %1
  store ptr @"??_C@_05IAABINL@doom2?$AA@", ptr %2, align 8
  br label %12

7:                                                ; preds = %1
  store ptr @"??_C@_03DDPMENPA@tnt?$AA@", ptr %2, align 8
  br label %12

8:                                                ; preds = %1
  store ptr @"??_C@_08LLIJOHMO@plutonia?$AA@", ptr %2, align 8
  br label %12

9:                                                ; preds = %1
  store ptr @"??_C@_04LACHCAKG@chex?$AA@", ptr %2, align 8
  br label %12

10:                                               ; preds = %1
  store ptr @"??_C@_04LOHCCCIP@hacx?$AA@", ptr %2, align 8
  br label %12

11:                                               ; preds = %1
  store ptr @"??_C@_07CIFAGBMG@unknown?$AA@", ptr %2, align 8
  br label %12

12:                                               ; preds = %11, %10, %9, %8, %7, %6, %5
  %13 = load ptr, ptr %2, align 8
  ret ptr %13
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local ptr @D_SuggestGameName(i32 noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  store i32 %1, ptr %3, align 4
  store i32 %0, ptr %4, align 4
  %5 = load i32, ptr %3, align 4
  %6 = load i32, ptr %4, align 4
  %7 = call ptr @D_GameMissionString(i32 noundef %6)
  ret ptr %7
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @I_VideoWaitVBL(i32 noundef %0) #0 {
  %2 = alloca i32, align 4
  store i32 %0, ptr %2, align 4
  %3 = load i32, ptr %2, align 4
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca ptr, align 8
  %3 = alloca ptr, align 8
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  %8 = alloca [4 x i8], align 1
  %9 = alloca i32, align 4
  %10 = alloca ptr, align 8
  store i32 0, ptr %1, align 4
  store ptr @"??_C@_0BB@NDKCCECJ@test_minimal?4wad?$AA@", ptr %2, align 8
  store i32 0, ptr %4, align 4
  call void @Z_Init()
  %11 = load ptr, ptr %2, align 8
  %12 = call i32 @build_test_wad(ptr noundef %11)
  %13 = icmp ne i32 %12, 0
  br i1 %13, label %15, label %14

14:                                               ; preds = %0
  store i32 0, ptr %1, align 4
  br label %76

15:                                               ; preds = %0
  %16 = load ptr, ptr %2, align 8
  %17 = call ptr @W_AddFile(ptr noundef %16)
  store ptr %17, ptr %3, align 8
  %18 = load ptr, ptr %3, align 8
  %19 = icmp ne ptr %18, null
  br i1 %19, label %20, label %23

20:                                               ; preds = %15
  %21 = load i32, ptr %4, align 4
  %22 = or i32 %21, 1
  store i32 %22, ptr %4, align 4
  br label %23

23:                                               ; preds = %20, %15
  %24 = load i32, ptr @numlumps, align 4
  %25 = icmp eq i32 %24, 2
  br i1 %25, label %26, label %29

26:                                               ; preds = %23
  %27 = load i32, ptr %4, align 4
  %28 = or i32 %27, 2
  store i32 %28, ptr %4, align 4
  br label %29

29:                                               ; preds = %26, %23
  %30 = call i32 @W_CheckNumForName(ptr noundef @"??_C@_07FLMOFAHC@PLAYPAL?$AA@")
  store i32 %30, ptr %5, align 4
  %31 = load i32, ptr %5, align 4
  %32 = icmp eq i32 %31, 0
  br i1 %32, label %33, label %36

33:                                               ; preds = %29
  %34 = load i32, ptr %4, align 4
  %35 = or i32 %34, 4
  store i32 %35, ptr %4, align 4
  br label %36

36:                                               ; preds = %33, %29
  %37 = call i32 @W_GetNumForName(ptr noundef @"??_C@_07FLMOFAHC@PLAYPAL?$AA@")
  store i32 %37, ptr %6, align 4
  %38 = load i32, ptr %6, align 4
  %39 = icmp eq i32 %38, 0
  br i1 %39, label %40, label %43

40:                                               ; preds = %36
  %41 = load i32, ptr %4, align 4
  %42 = or i32 %41, 8
  store i32 %42, ptr %4, align 4
  br label %43

43:                                               ; preds = %40, %36
  %44 = call i32 @W_LumpLength(i32 noundef 0)
  store i32 %44, ptr %7, align 4
  %45 = load i32, ptr %7, align 4
  %46 = icmp eq i32 %45, 4
  br i1 %46, label %47, label %50

47:                                               ; preds = %43
  %48 = load i32, ptr %4, align 4
  %49 = or i32 %48, 16
  store i32 %49, ptr %4, align 4
  br label %50

50:                                               ; preds = %47, %43
  %51 = getelementptr inbounds [4 x i8], ptr %8, i64 0, i64 0
  store i8 0, ptr %51, align 1
  %52 = getelementptr inbounds [4 x i8], ptr %8, i64 0, i64 0
  call void @W_ReadLump(i32 noundef 0, ptr noundef %52)
  %53 = getelementptr inbounds [4 x i8], ptr %8, i64 0, i64 0
  %54 = load i8, ptr %53, align 1
  %55 = zext i8 %54 to i32
  %56 = icmp eq i32 %55, 1
  br i1 %56, label %57, label %60

57:                                               ; preds = %50
  %58 = load i32, ptr %4, align 4
  %59 = or i32 %58, 32
  store i32 %59, ptr %4, align 4
  br label %60

60:                                               ; preds = %57, %50
  call void @W_GenerateHashTable()
  %61 = call i32 @W_CheckNumForName(ptr noundef @"??_C@_06BBOHFMBE@ENDOOM?$AA@")
  store i32 %61, ptr %9, align 4
  %62 = load i32, ptr %9, align 4
  %63 = icmp eq i32 %62, 1
  br i1 %63, label %64, label %67

64:                                               ; preds = %60
  %65 = load i32, ptr %4, align 4
  %66 = or i32 %65, 64
  store i32 %66, ptr %4, align 4
  br label %67

67:                                               ; preds = %64, %60
  %68 = call ptr @W_CacheLumpNum(i32 noundef 0, i32 noundef 1)
  store ptr %68, ptr %10, align 8
  %69 = load ptr, ptr %10, align 8
  %70 = icmp ne ptr %69, null
  br i1 %70, label %71, label %74

71:                                               ; preds = %67
  %72 = load i32, ptr %4, align 4
  %73 = or i32 %72, 128
  store i32 %73, ptr %4, align 4
  br label %74

74:                                               ; preds = %71, %67
  %75 = load i32, ptr %4, align 4
  store i32 %75, ptr %1, align 4
  br label %76

76:                                               ; preds = %74, %14
  %77 = load i32, ptr %1, align 4
  ret i32 %77
}

declare dso_local void @Z_Init() #4

; Function Attrs: noinline nounwind optnone uwtable
define internal i32 @build_test_wad(ptr noundef %0) #0 {
  %2 = alloca i32, align 4
  %3 = alloca ptr, align 8
  %4 = alloca [60 x i8], align 16
  %5 = alloca ptr, align 8
  store ptr %0, ptr %3, align 8
  %6 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 0
  call void @llvm.memset.p0.i64(ptr align 16 %6, i8 0, i64 60, i1 false)
  %7 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 0
  store i8 73, ptr %7, align 16
  %8 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 1
  store i8 87, ptr %8, align 1
  %9 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 2
  store i8 65, ptr %9, align 2
  %10 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 3
  store i8 68, ptr %10, align 1
  %11 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 0
  call void @write_le32(ptr noundef %11, i32 noundef 4, i32 noundef 2)
  %12 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 0
  call void @write_le32(ptr noundef %12, i32 noundef 8, i32 noundef 28)
  %13 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 12
  store i8 1, ptr %13, align 4
  %14 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 13
  store i8 2, ptr %14, align 1
  %15 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 14
  store i8 3, ptr %15, align 2
  %16 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 15
  store i8 4, ptr %16, align 1
  %17 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 16
  store i8 -86, ptr %17, align 16
  %18 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 17
  store i8 -69, ptr %18, align 1
  %19 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 0
  call void @write_le32(ptr noundef %19, i32 noundef 28, i32 noundef 12)
  %20 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 0
  call void @write_le32(ptr noundef %20, i32 noundef 32, i32 noundef 4)
  %21 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 36
  store i8 80, ptr %21, align 4
  %22 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 37
  store i8 76, ptr %22, align 1
  %23 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 38
  store i8 65, ptr %23, align 2
  %24 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 39
  store i8 89, ptr %24, align 1
  %25 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 40
  store i8 80, ptr %25, align 8
  %26 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 41
  store i8 65, ptr %26, align 1
  %27 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 42
  store i8 76, ptr %27, align 2
  %28 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 43
  store i8 0, ptr %28, align 1
  %29 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 0
  call void @write_le32(ptr noundef %29, i32 noundef 44, i32 noundef 16)
  %30 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 0
  call void @write_le32(ptr noundef %30, i32 noundef 48, i32 noundef 2)
  %31 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 52
  store i8 69, ptr %31, align 4
  %32 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 53
  store i8 78, ptr %32, align 1
  %33 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 54
  store i8 68, ptr %33, align 2
  %34 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 55
  store i8 79, ptr %34, align 1
  %35 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 56
  store i8 79, ptr %35, align 8
  %36 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 57
  store i8 77, ptr %36, align 1
  %37 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 58
  store i8 0, ptr %37, align 2
  %38 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 59
  store i8 0, ptr %38, align 1
  %39 = load ptr, ptr %3, align 8
  %40 = call ptr @fopen(ptr noundef %39, ptr noundef @"??_C@_02GMLFBBN@wb?$AA@")
  store ptr %40, ptr %5, align 8
  %41 = load ptr, ptr %5, align 8
  %42 = icmp ne ptr %41, null
  br i1 %42, label %44, label %43

43:                                               ; preds = %1
  store i32 0, ptr %2, align 4
  br label %50

44:                                               ; preds = %1
  %45 = load ptr, ptr %5, align 8
  %46 = getelementptr inbounds [60 x i8], ptr %4, i64 0, i64 0
  %47 = call i64 @fwrite(ptr noundef %46, i64 noundef 1, i64 noundef 60, ptr noundef %45)
  %48 = load ptr, ptr %5, align 8
  %49 = call i32 @fclose(ptr noundef %48)
  store i32 1, ptr %2, align 4
  br label %50

50:                                               ; preds = %44, %43
  %51 = load i32, ptr %2, align 4
  ret i32 %51
}

declare dso_local ptr @W_AddFile(ptr noundef) #4

declare dso_local i32 @W_CheckNumForName(ptr noundef) #4

declare dso_local i32 @W_GetNumForName(ptr noundef) #4

declare dso_local i32 @W_LumpLength(i32 noundef) #4

declare dso_local void @W_ReadLump(i32 noundef, ptr noundef) #4

declare dso_local void @W_GenerateHashTable() #4

declare dso_local ptr @W_CacheLumpNum(i32 noundef, i32 noundef) #4

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

declare dso_local i32 @__stdio_common_vsprintf(i64 noundef, ptr noundef, i64 noundef, ptr noundef, ptr noundef, ptr noundef) #4

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

declare dso_local ptr @__acrt_iob_func(i32 noundef) #4

declare dso_local i32 @__stdio_common_vfprintf(i64 noundef, ptr noundef, ptr noundef, ptr noundef, ptr noundef) #4

; Function Attrs: nocallback nofree nounwind willreturn memory(argmem: write)
declare void @llvm.memset.p0.i64(ptr writeonly captures(none), i8, i64, i1 immarg) #7

; Function Attrs: noinline nounwind optnone uwtable
define internal void @write_le32(ptr noundef %0, i32 noundef %1, i32 noundef %2) #0 {
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  %6 = alloca ptr, align 8
  %7 = alloca ptr, align 8
  store i32 %2, ptr %4, align 4
  store i32 %1, ptr %5, align 4
  store ptr %0, ptr %6, align 8
  %8 = load ptr, ptr %6, align 8
  %9 = load i32, ptr %5, align 4
  %10 = sext i32 %9 to i64
  %11 = getelementptr inbounds i8, ptr %8, i64 %10
  store ptr %11, ptr %7, align 8
  %12 = load i32, ptr %4, align 4
  %13 = and i32 %12, 255
  %14 = trunc i32 %13 to i8
  %15 = load ptr, ptr %7, align 8
  %16 = getelementptr inbounds i8, ptr %15, i64 0
  store i8 %14, ptr %16, align 1
  %17 = load i32, ptr %4, align 4
  %18 = ashr i32 %17, 8
  %19 = and i32 %18, 255
  %20 = trunc i32 %19 to i8
  %21 = load ptr, ptr %7, align 8
  %22 = getelementptr inbounds i8, ptr %21, i64 1
  store i8 %20, ptr %22, align 1
  %23 = load i32, ptr %4, align 4
  %24 = ashr i32 %23, 16
  %25 = and i32 %24, 255
  %26 = trunc i32 %25 to i8
  %27 = load ptr, ptr %7, align 8
  %28 = getelementptr inbounds i8, ptr %27, i64 2
  store i8 %26, ptr %28, align 1
  %29 = load i32, ptr %4, align 4
  %30 = ashr i32 %29, 24
  %31 = and i32 %30, 255
  %32 = trunc i32 %31 to i8
  %33 = load ptr, ptr %7, align 8
  %34 = getelementptr inbounds i8, ptr %33, i64 3
  store i8 %32, ptr %34, align 1
  ret void
}

declare dso_local ptr @fopen(ptr noundef, ptr noundef) #4

declare dso_local i64 @fwrite(ptr noundef, i64 noundef, i64 noundef, ptr noundef) #4

declare dso_local i32 @fclose(ptr noundef) #4

attributes #0 = { noinline nounwind optnone uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nocallback nofree nosync nounwind willreturn }
attributes #2 = { noreturn "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #3 = { allocsize(0) "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #4 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #5 = { nounwind "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #6 = { nounwind willreturn memory(read) "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #7 = { nocallback nofree nounwind willreturn memory(argmem: write) }
attributes #8 = { nounwind }
attributes #9 = { noreturn }
attributes #10 = { allocsize(0) }
attributes #11 = { nounwind willreturn memory(read) }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\Doom-Generic/vm-porting/tests/doom_wad\\src\\test_doom_wad.c", directory: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 1, !"wchar_size", i32 2}
!4 = !{i32 8, !"PIC Level", i32 2}
!5 = !{i32 7, !"uwtable", i32 2}
!6 = !{i32 1, !"MaxTLSAlign", i32 65536}
!7 = !{!"clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)"}
!8 = distinct !{!8, !9}
!9 = !{!"llvm.loop.mustprogress"}
!10 = distinct !{!10, !9}
!11 = distinct !{!11, !9}
