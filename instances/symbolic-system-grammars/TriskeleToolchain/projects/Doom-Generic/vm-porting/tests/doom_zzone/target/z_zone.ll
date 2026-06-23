; ModuleID = 'E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\projects\Doom-Generic/vm-porting/tests/doom_zzone\src/z_zone.c'
source_filename = "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\Doom-Generic/vm-porting/tests/doom_zzone\\src/z_zone.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-windows-msvc19.51.36246"

%struct.memzone_t = type { i32, %struct.memblock_s, ptr }
%struct.memblock_s = type { i32, ptr, i32, i32, ptr, ptr }

$sprintf = comdat any

$vsprintf = comdat any

$_snprintf = comdat any

$_vsnprintf = comdat any

$printf = comdat any

$fprintf = comdat any

$_vsprintf_l = comdat any

$_vsnprintf_l = comdat any

$__local_stdio_printf_options = comdat any

$_vfprintf_l = comdat any

$"??_C@_0CH@OJFIIOIA@Z_Free?3?5freed?5a?5pointer?5without?5@" = comdat any

$"??_C@_0CL@FLAFPDCH@Z_Malloc?3?5failed?5on?5allocation?5o@" = comdat any

$"??_C@_0DD@MJJDHHFN@Z_Malloc?3?5an?5owner?5is?5required?5f@" = comdat any

$"??_C@_0BN@DBGKJAGK@zone?5size?3?5?$CFi?5?5location?3?5?$CFp?6?$AA@" = comdat any

$"??_C@_0BF@BCHJJIJD@tag?5range?3?5?$CFi?5to?5?$CFi?6?$AA@" = comdat any

$"??_C@_0CM@IHDHPOFO@block?3?$CFp?5?5?5?5size?3?$CF7i?5?5?5?5user?3?$CFp?5@" = comdat any

$"??_C@_0DB@EJEJBDEF@ERROR?3?5block?5size?5does?5not?5touch@" = comdat any

$"??_C@_0DB@INBMMEOG@ERROR?3?5next?5block?5doesn?8t?5have?5p@" = comdat any

$"??_C@_0CE@BLFCFJMN@ERROR?3?5two?5consecutive?5free?5bloc@" = comdat any

$"??_C@_0DH@PDLFHKNN@Z_CheckHeap?3?5block?5size?5does?5not@" = comdat any

$"??_C@_0DH@DHOAKNHO@Z_CheckHeap?3?5next?5block?5doesn?8t?5@" = comdat any

$"??_C@_0CK@MHBJLLKL@Z_CheckHeap?3?5two?5consecutive?5fre@" = comdat any

$"??_C@_0CM@CJBLFFHI@?$CFs?3?$CFi?3?5Z_ChangeTag?3?5block?5withou@" = comdat any

$"??_C@_0DN@MAENEHJP@?$CFs?3?$CFi?3?5Z_ChangeTag?3?5an?5owner?5is?5@" = comdat any

$"??_C@_0DG@EOELOILK@Z_ChangeUser?3?5Tried?5to?5change?5us@" = comdat any

$"??_C@_09OJHNFIGK@I_Error?3?5?$AA@" = comdat any

$"??_C@_03OFAPEBGM@?$CFs?6?$AA@" = comdat any

@mainzone = dso_local global ptr null, align 8
@"??_C@_0CH@OJFIIOIA@Z_Free?3?5freed?5a?5pointer?5without?5@" = linkonce_odr dso_local unnamed_addr constant [39 x i8] c"Z_Free: freed a pointer without ZONEID\00", comdat, align 1
@"??_C@_0CL@FLAFPDCH@Z_Malloc?3?5failed?5on?5allocation?5o@" = linkonce_odr dso_local unnamed_addr constant [43 x i8] c"Z_Malloc: failed on allocation of %i bytes\00", comdat, align 1
@"??_C@_0DD@MJJDHHFN@Z_Malloc?3?5an?5owner?5is?5required?5f@" = linkonce_odr dso_local unnamed_addr constant [51 x i8] c"Z_Malloc: an owner is required for purgable blocks\00", comdat, align 1
@"??_C@_0BN@DBGKJAGK@zone?5size?3?5?$CFi?5?5location?3?5?$CFp?6?$AA@" = linkonce_odr dso_local unnamed_addr constant [29 x i8] c"zone size: %i  location: %p\0A\00", comdat, align 1
@"??_C@_0BF@BCHJJIJD@tag?5range?3?5?$CFi?5to?5?$CFi?6?$AA@" = linkonce_odr dso_local unnamed_addr constant [21 x i8] c"tag range: %i to %i\0A\00", comdat, align 1
@"??_C@_0CM@IHDHPOFO@block?3?$CFp?5?5?5?5size?3?$CF7i?5?5?5?5user?3?$CFp?5@" = linkonce_odr dso_local unnamed_addr constant [44 x i8] c"block:%p    size:%7i    user:%p    tag:%3i\0A\00", comdat, align 1
@"??_C@_0DB@EJEJBDEF@ERROR?3?5block?5size?5does?5not?5touch@" = linkonce_odr dso_local unnamed_addr constant [49 x i8] c"ERROR: block size does not touch the next block\0A\00", comdat, align 1
@"??_C@_0DB@INBMMEOG@ERROR?3?5next?5block?5doesn?8t?5have?5p@" = linkonce_odr dso_local unnamed_addr constant [49 x i8] c"ERROR: next block doesn't have proper back link\0A\00", comdat, align 1
@"??_C@_0CE@BLFCFJMN@ERROR?3?5two?5consecutive?5free?5bloc@" = linkonce_odr dso_local unnamed_addr constant [36 x i8] c"ERROR: two consecutive free blocks\0A\00", comdat, align 1
@"??_C@_0DH@PDLFHKNN@Z_CheckHeap?3?5block?5size?5does?5not@" = linkonce_odr dso_local unnamed_addr constant [55 x i8] c"Z_CheckHeap: block size does not touch the next block\0A\00", comdat, align 1
@"??_C@_0DH@DHOAKNHO@Z_CheckHeap?3?5next?5block?5doesn?8t?5@" = linkonce_odr dso_local unnamed_addr constant [55 x i8] c"Z_CheckHeap: next block doesn't have proper back link\0A\00", comdat, align 1
@"??_C@_0CK@MHBJLLKL@Z_CheckHeap?3?5two?5consecutive?5fre@" = linkonce_odr dso_local unnamed_addr constant [42 x i8] c"Z_CheckHeap: two consecutive free blocks\0A\00", comdat, align 1
@"??_C@_0CM@CJBLFFHI@?$CFs?3?$CFi?3?5Z_ChangeTag?3?5block?5withou@" = linkonce_odr dso_local unnamed_addr constant [44 x i8] c"%s:%i: Z_ChangeTag: block without a ZONEID!\00", comdat, align 1
@"??_C@_0DN@MAENEHJP@?$CFs?3?$CFi?3?5Z_ChangeTag?3?5an?5owner?5is?5@" = linkonce_odr dso_local unnamed_addr constant [61 x i8] c"%s:%i: Z_ChangeTag: an owner is required for purgable blocks\00", comdat, align 1
@"??_C@_0DG@EOELOILK@Z_ChangeUser?3?5Tried?5to?5change?5us@" = linkonce_odr dso_local unnamed_addr constant [54 x i8] c"Z_ChangeUser: Tried to change user for invalid block!\00", comdat, align 1
@__local_stdio_printf_options._OptionsStorage = internal global i64 0, align 8
@doom_zone_heap = internal global [2097152 x i8] zeroinitializer, align 16
@"??_C@_09OJHNFIGK@I_Error?3?5?$AA@" = linkonce_odr dso_local unnamed_addr constant [10 x i8] c"I_Error: \00", comdat, align 1
@"??_C@_03OFAPEBGM@?$CFs?6?$AA@" = linkonce_odr dso_local unnamed_addr constant [4 x i8] c"%s\0A\00", comdat, align 1

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
define dso_local void @Z_ClearZone(ptr noundef %0) #0 {
  %2 = alloca ptr, align 8
  %3 = alloca ptr, align 8
  store ptr %0, ptr %2, align 8
  %4 = load ptr, ptr %2, align 8
  %5 = getelementptr inbounds nuw i8, ptr %4, i64 56
  store ptr %5, ptr %3, align 8
  %6 = load ptr, ptr %2, align 8
  %7 = getelementptr inbounds nuw %struct.memzone_t, ptr %6, i32 0, i32 1
  %8 = getelementptr inbounds nuw %struct.memblock_s, ptr %7, i32 0, i32 5
  store ptr %5, ptr %8, align 8
  %9 = load ptr, ptr %2, align 8
  %10 = getelementptr inbounds nuw %struct.memzone_t, ptr %9, i32 0, i32 1
  %11 = getelementptr inbounds nuw %struct.memblock_s, ptr %10, i32 0, i32 4
  store ptr %5, ptr %11, align 8
  %12 = load ptr, ptr %2, align 8
  %13 = load ptr, ptr %2, align 8
  %14 = getelementptr inbounds nuw %struct.memzone_t, ptr %13, i32 0, i32 1
  %15 = getelementptr inbounds nuw %struct.memblock_s, ptr %14, i32 0, i32 1
  store ptr %12, ptr %15, align 8
  %16 = load ptr, ptr %2, align 8
  %17 = getelementptr inbounds nuw %struct.memzone_t, ptr %16, i32 0, i32 1
  %18 = getelementptr inbounds nuw %struct.memblock_s, ptr %17, i32 0, i32 2
  store i32 1, ptr %18, align 8
  %19 = load ptr, ptr %3, align 8
  %20 = load ptr, ptr %2, align 8
  %21 = getelementptr inbounds nuw %struct.memzone_t, ptr %20, i32 0, i32 2
  store ptr %19, ptr %21, align 8
  %22 = load ptr, ptr %2, align 8
  %23 = getelementptr inbounds nuw %struct.memzone_t, ptr %22, i32 0, i32 1
  %24 = load ptr, ptr %3, align 8
  %25 = getelementptr inbounds nuw %struct.memblock_s, ptr %24, i32 0, i32 4
  store ptr %23, ptr %25, align 8
  %26 = load ptr, ptr %3, align 8
  %27 = getelementptr inbounds nuw %struct.memblock_s, ptr %26, i32 0, i32 5
  store ptr %23, ptr %27, align 8
  %28 = load ptr, ptr %3, align 8
  %29 = getelementptr inbounds nuw %struct.memblock_s, ptr %28, i32 0, i32 2
  store i32 4, ptr %29, align 8
  %30 = load ptr, ptr %2, align 8
  %31 = getelementptr inbounds nuw %struct.memzone_t, ptr %30, i32 0, i32 0
  %32 = load i32, ptr %31, align 8
  %33 = sext i32 %32 to i64
  %34 = sub i64 %33, 56
  %35 = trunc i64 %34 to i32
  %36 = load ptr, ptr %3, align 8
  %37 = getelementptr inbounds nuw %struct.memblock_s, ptr %36, i32 0, i32 0
  store i32 %35, ptr %37, align 8
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @Z_Init() #0 {
  %1 = alloca ptr, align 8
  %2 = alloca i32, align 4
  %3 = call ptr @I_ZoneBase(ptr noundef %2)
  store ptr %3, ptr @mainzone, align 8
  %4 = load i32, ptr %2, align 4
  %5 = load ptr, ptr @mainzone, align 8
  %6 = getelementptr inbounds nuw %struct.memzone_t, ptr %5, i32 0, i32 0
  store i32 %4, ptr %6, align 8
  %7 = load ptr, ptr @mainzone, align 8
  %8 = getelementptr inbounds nuw i8, ptr %7, i64 56
  store ptr %8, ptr %1, align 8
  %9 = load ptr, ptr @mainzone, align 8
  %10 = getelementptr inbounds nuw %struct.memzone_t, ptr %9, i32 0, i32 1
  %11 = getelementptr inbounds nuw %struct.memblock_s, ptr %10, i32 0, i32 5
  store ptr %8, ptr %11, align 8
  %12 = load ptr, ptr @mainzone, align 8
  %13 = getelementptr inbounds nuw %struct.memzone_t, ptr %12, i32 0, i32 1
  %14 = getelementptr inbounds nuw %struct.memblock_s, ptr %13, i32 0, i32 4
  store ptr %8, ptr %14, align 8
  %15 = load ptr, ptr @mainzone, align 8
  %16 = load ptr, ptr @mainzone, align 8
  %17 = getelementptr inbounds nuw %struct.memzone_t, ptr %16, i32 0, i32 1
  %18 = getelementptr inbounds nuw %struct.memblock_s, ptr %17, i32 0, i32 1
  store ptr %15, ptr %18, align 8
  %19 = load ptr, ptr @mainzone, align 8
  %20 = getelementptr inbounds nuw %struct.memzone_t, ptr %19, i32 0, i32 1
  %21 = getelementptr inbounds nuw %struct.memblock_s, ptr %20, i32 0, i32 2
  store i32 1, ptr %21, align 8
  %22 = load ptr, ptr %1, align 8
  %23 = load ptr, ptr @mainzone, align 8
  %24 = getelementptr inbounds nuw %struct.memzone_t, ptr %23, i32 0, i32 2
  store ptr %22, ptr %24, align 8
  %25 = load ptr, ptr @mainzone, align 8
  %26 = getelementptr inbounds nuw %struct.memzone_t, ptr %25, i32 0, i32 1
  %27 = load ptr, ptr %1, align 8
  %28 = getelementptr inbounds nuw %struct.memblock_s, ptr %27, i32 0, i32 4
  store ptr %26, ptr %28, align 8
  %29 = load ptr, ptr %1, align 8
  %30 = getelementptr inbounds nuw %struct.memblock_s, ptr %29, i32 0, i32 5
  store ptr %26, ptr %30, align 8
  %31 = load ptr, ptr %1, align 8
  %32 = getelementptr inbounds nuw %struct.memblock_s, ptr %31, i32 0, i32 2
  store i32 4, ptr %32, align 8
  %33 = load ptr, ptr @mainzone, align 8
  %34 = getelementptr inbounds nuw %struct.memzone_t, ptr %33, i32 0, i32 0
  %35 = load i32, ptr %34, align 8
  %36 = sext i32 %35 to i64
  %37 = sub i64 %36, 56
  %38 = trunc i64 %37 to i32
  %39 = load ptr, ptr %1, align 8
  %40 = getelementptr inbounds nuw %struct.memblock_s, ptr %39, i32 0, i32 0
  store i32 %38, ptr %40, align 8
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define internal ptr @I_ZoneBase(ptr noundef %0) #0 {
  %2 = alloca ptr, align 8
  store ptr %0, ptr %2, align 8
  %3 = load ptr, ptr %2, align 8
  store i32 2097152, ptr %3, align 4
  ret ptr @doom_zone_heap
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @Z_Free(ptr noundef %0) #0 {
  %2 = alloca ptr, align 8
  %3 = alloca ptr, align 8
  %4 = alloca ptr, align 8
  store ptr %0, ptr %2, align 8
  %5 = load ptr, ptr %2, align 8
  %6 = getelementptr inbounds i8, ptr %5, i64 -40
  store ptr %6, ptr %3, align 8
  %7 = load ptr, ptr %3, align 8
  %8 = getelementptr inbounds nuw %struct.memblock_s, ptr %7, i32 0, i32 3
  %9 = load i32, ptr %8, align 4
  %10 = icmp ne i32 %9, 1919505
  br i1 %10, label %11, label %12

11:                                               ; preds = %1
  call void (ptr, ...) @I_Error(ptr noundef @"??_C@_0CH@OJFIIOIA@Z_Free?3?5freed?5a?5pointer?5without?5@")
  br label %12

12:                                               ; preds = %11, %1
  %13 = load ptr, ptr %3, align 8
  %14 = getelementptr inbounds nuw %struct.memblock_s, ptr %13, i32 0, i32 2
  %15 = load i32, ptr %14, align 8
  %16 = icmp ne i32 %15, 4
  br i1 %16, label %17, label %26

17:                                               ; preds = %12
  %18 = load ptr, ptr %3, align 8
  %19 = getelementptr inbounds nuw %struct.memblock_s, ptr %18, i32 0, i32 1
  %20 = load ptr, ptr %19, align 8
  %21 = icmp ne ptr %20, null
  br i1 %21, label %22, label %26

22:                                               ; preds = %17
  %23 = load ptr, ptr %3, align 8
  %24 = getelementptr inbounds nuw %struct.memblock_s, ptr %23, i32 0, i32 1
  %25 = load ptr, ptr %24, align 8
  store ptr null, ptr %25, align 8
  br label %26

26:                                               ; preds = %22, %17, %12
  %27 = load ptr, ptr %3, align 8
  %28 = getelementptr inbounds nuw %struct.memblock_s, ptr %27, i32 0, i32 2
  store i32 4, ptr %28, align 8
  %29 = load ptr, ptr %3, align 8
  %30 = getelementptr inbounds nuw %struct.memblock_s, ptr %29, i32 0, i32 1
  store ptr null, ptr %30, align 8
  %31 = load ptr, ptr %3, align 8
  %32 = getelementptr inbounds nuw %struct.memblock_s, ptr %31, i32 0, i32 3
  store i32 0, ptr %32, align 4
  %33 = load ptr, ptr %3, align 8
  %34 = getelementptr inbounds nuw %struct.memblock_s, ptr %33, i32 0, i32 5
  %35 = load ptr, ptr %34, align 8
  store ptr %35, ptr %4, align 8
  %36 = load ptr, ptr %4, align 8
  %37 = getelementptr inbounds nuw %struct.memblock_s, ptr %36, i32 0, i32 2
  %38 = load i32, ptr %37, align 8
  %39 = icmp eq i32 %38, 4
  br i1 %39, label %40, label %69

40:                                               ; preds = %26
  %41 = load ptr, ptr %3, align 8
  %42 = getelementptr inbounds nuw %struct.memblock_s, ptr %41, i32 0, i32 0
  %43 = load i32, ptr %42, align 8
  %44 = load ptr, ptr %4, align 8
  %45 = getelementptr inbounds nuw %struct.memblock_s, ptr %44, i32 0, i32 0
  %46 = load i32, ptr %45, align 8
  %47 = add nsw i32 %46, %43
  store i32 %47, ptr %45, align 8
  %48 = load ptr, ptr %3, align 8
  %49 = getelementptr inbounds nuw %struct.memblock_s, ptr %48, i32 0, i32 4
  %50 = load ptr, ptr %49, align 8
  %51 = load ptr, ptr %4, align 8
  %52 = getelementptr inbounds nuw %struct.memblock_s, ptr %51, i32 0, i32 4
  store ptr %50, ptr %52, align 8
  %53 = load ptr, ptr %4, align 8
  %54 = load ptr, ptr %4, align 8
  %55 = getelementptr inbounds nuw %struct.memblock_s, ptr %54, i32 0, i32 4
  %56 = load ptr, ptr %55, align 8
  %57 = getelementptr inbounds nuw %struct.memblock_s, ptr %56, i32 0, i32 5
  store ptr %53, ptr %57, align 8
  %58 = load ptr, ptr %3, align 8
  %59 = load ptr, ptr @mainzone, align 8
  %60 = getelementptr inbounds nuw %struct.memzone_t, ptr %59, i32 0, i32 2
  %61 = load ptr, ptr %60, align 8
  %62 = icmp eq ptr %58, %61
  br i1 %62, label %63, label %67

63:                                               ; preds = %40
  %64 = load ptr, ptr %4, align 8
  %65 = load ptr, ptr @mainzone, align 8
  %66 = getelementptr inbounds nuw %struct.memzone_t, ptr %65, i32 0, i32 2
  store ptr %64, ptr %66, align 8
  br label %67

67:                                               ; preds = %63, %40
  %68 = load ptr, ptr %4, align 8
  store ptr %68, ptr %3, align 8
  br label %69

69:                                               ; preds = %67, %26
  %70 = load ptr, ptr %3, align 8
  %71 = getelementptr inbounds nuw %struct.memblock_s, ptr %70, i32 0, i32 4
  %72 = load ptr, ptr %71, align 8
  store ptr %72, ptr %4, align 8
  %73 = load ptr, ptr %4, align 8
  %74 = getelementptr inbounds nuw %struct.memblock_s, ptr %73, i32 0, i32 2
  %75 = load i32, ptr %74, align 8
  %76 = icmp eq i32 %75, 4
  br i1 %76, label %77, label %105

77:                                               ; preds = %69
  %78 = load ptr, ptr %4, align 8
  %79 = getelementptr inbounds nuw %struct.memblock_s, ptr %78, i32 0, i32 0
  %80 = load i32, ptr %79, align 8
  %81 = load ptr, ptr %3, align 8
  %82 = getelementptr inbounds nuw %struct.memblock_s, ptr %81, i32 0, i32 0
  %83 = load i32, ptr %82, align 8
  %84 = add nsw i32 %83, %80
  store i32 %84, ptr %82, align 8
  %85 = load ptr, ptr %4, align 8
  %86 = getelementptr inbounds nuw %struct.memblock_s, ptr %85, i32 0, i32 4
  %87 = load ptr, ptr %86, align 8
  %88 = load ptr, ptr %3, align 8
  %89 = getelementptr inbounds nuw %struct.memblock_s, ptr %88, i32 0, i32 4
  store ptr %87, ptr %89, align 8
  %90 = load ptr, ptr %3, align 8
  %91 = load ptr, ptr %3, align 8
  %92 = getelementptr inbounds nuw %struct.memblock_s, ptr %91, i32 0, i32 4
  %93 = load ptr, ptr %92, align 8
  %94 = getelementptr inbounds nuw %struct.memblock_s, ptr %93, i32 0, i32 5
  store ptr %90, ptr %94, align 8
  %95 = load ptr, ptr %4, align 8
  %96 = load ptr, ptr @mainzone, align 8
  %97 = getelementptr inbounds nuw %struct.memzone_t, ptr %96, i32 0, i32 2
  %98 = load ptr, ptr %97, align 8
  %99 = icmp eq ptr %95, %98
  br i1 %99, label %100, label %104

100:                                              ; preds = %77
  %101 = load ptr, ptr %3, align 8
  %102 = load ptr, ptr @mainzone, align 8
  %103 = getelementptr inbounds nuw %struct.memzone_t, ptr %102, i32 0, i32 2
  store ptr %101, ptr %103, align 8
  br label %104

104:                                              ; preds = %100, %77
  br label %105

105:                                              ; preds = %104, %69
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define internal void @I_Error(ptr noundef %0, ...) #0 {
  %2 = alloca ptr, align 8
  store ptr %0, ptr %2, align 8
  %3 = call ptr @__acrt_iob_func(i32 noundef 2)
  %4 = call i32 (ptr, ptr, ...) @fprintf(ptr noundef %3, ptr noundef @"??_C@_09OJHNFIGK@I_Error?3?5?$AA@") #3
  %5 = load ptr, ptr %2, align 8
  %6 = call ptr @__acrt_iob_func(i32 noundef 2)
  %7 = call i32 (ptr, ptr, ...) @fprintf(ptr noundef %6, ptr noundef @"??_C@_03OFAPEBGM@?$CFs?6?$AA@", ptr noundef %5) #3
  %8 = call ptr @__acrt_iob_func(i32 noundef 2)
  %9 = call i32 @fflush(ptr noundef %8)
  br label %10

10:                                               ; preds = %1, %10
  br label %10
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local ptr @Z_Malloc(i32 noundef %0, i32 noundef %1, ptr noundef %2) #0 {
  %4 = alloca ptr, align 8
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  %8 = alloca ptr, align 8
  %9 = alloca ptr, align 8
  %10 = alloca ptr, align 8
  %11 = alloca ptr, align 8
  %12 = alloca ptr, align 8
  store ptr %2, ptr %4, align 8
  store i32 %1, ptr %5, align 4
  store i32 %0, ptr %6, align 4
  %13 = load i32, ptr %6, align 4
  %14 = sext i32 %13 to i64
  %15 = add i64 %14, 8
  %16 = sub i64 %15, 1
  %17 = and i64 %16, -8
  %18 = trunc i64 %17 to i32
  store i32 %18, ptr %6, align 4
  %19 = load i32, ptr %6, align 4
  %20 = sext i32 %19 to i64
  %21 = add i64 %20, 40
  %22 = trunc i64 %21 to i32
  store i32 %22, ptr %6, align 4
  %23 = load ptr, ptr @mainzone, align 8
  %24 = getelementptr inbounds nuw %struct.memzone_t, ptr %23, i32 0, i32 2
  %25 = load ptr, ptr %24, align 8
  store ptr %25, ptr %11, align 8
  %26 = load ptr, ptr %11, align 8
  %27 = getelementptr inbounds nuw %struct.memblock_s, ptr %26, i32 0, i32 5
  %28 = load ptr, ptr %27, align 8
  %29 = getelementptr inbounds nuw %struct.memblock_s, ptr %28, i32 0, i32 2
  %30 = load i32, ptr %29, align 8
  %31 = icmp eq i32 %30, 4
  br i1 %31, label %32, label %36

32:                                               ; preds = %3
  %33 = load ptr, ptr %11, align 8
  %34 = getelementptr inbounds nuw %struct.memblock_s, ptr %33, i32 0, i32 5
  %35 = load ptr, ptr %34, align 8
  store ptr %35, ptr %11, align 8
  br label %36

36:                                               ; preds = %32, %3
  %37 = load ptr, ptr %11, align 8
  store ptr %37, ptr %9, align 8
  %38 = load ptr, ptr %11, align 8
  %39 = getelementptr inbounds nuw %struct.memblock_s, ptr %38, i32 0, i32 5
  %40 = load ptr, ptr %39, align 8
  store ptr %40, ptr %8, align 8
  br label %41

41:                                               ; preds = %90, %36
  %42 = load ptr, ptr %9, align 8
  %43 = load ptr, ptr %8, align 8
  %44 = icmp eq ptr %42, %43
  br i1 %44, label %45, label %47

45:                                               ; preds = %41
  %46 = load i32, ptr %6, align 4
  call void (ptr, ...) @I_Error(ptr noundef @"??_C@_0CL@FLAFPDCH@Z_Malloc?3?5failed?5on?5allocation?5o@", i32 noundef %46)
  br label %47

47:                                               ; preds = %45, %41
  %48 = load ptr, ptr %9, align 8
  %49 = getelementptr inbounds nuw %struct.memblock_s, ptr %48, i32 0, i32 2
  %50 = load i32, ptr %49, align 8
  %51 = icmp ne i32 %50, 4
  br i1 %51, label %52, label %74

52:                                               ; preds = %47
  %53 = load ptr, ptr %9, align 8
  %54 = getelementptr inbounds nuw %struct.memblock_s, ptr %53, i32 0, i32 2
  %55 = load i32, ptr %54, align 8
  %56 = icmp slt i32 %55, 7
  br i1 %56, label %57, label %61

57:                                               ; preds = %52
  %58 = load ptr, ptr %9, align 8
  %59 = getelementptr inbounds nuw %struct.memblock_s, ptr %58, i32 0, i32 4
  %60 = load ptr, ptr %59, align 8
  store ptr %60, ptr %9, align 8
  store ptr %60, ptr %11, align 8
  br label %73

61:                                               ; preds = %52
  %62 = load ptr, ptr %11, align 8
  %63 = getelementptr inbounds nuw %struct.memblock_s, ptr %62, i32 0, i32 5
  %64 = load ptr, ptr %63, align 8
  store ptr %64, ptr %11, align 8
  %65 = load ptr, ptr %9, align 8
  %66 = getelementptr inbounds nuw i8, ptr %65, i64 40
  call void @Z_Free(ptr noundef %66)
  %67 = load ptr, ptr %11, align 8
  %68 = getelementptr inbounds nuw %struct.memblock_s, ptr %67, i32 0, i32 4
  %69 = load ptr, ptr %68, align 8
  store ptr %69, ptr %11, align 8
  %70 = load ptr, ptr %11, align 8
  %71 = getelementptr inbounds nuw %struct.memblock_s, ptr %70, i32 0, i32 4
  %72 = load ptr, ptr %71, align 8
  store ptr %72, ptr %9, align 8
  br label %73

73:                                               ; preds = %61, %57
  br label %78

74:                                               ; preds = %47
  %75 = load ptr, ptr %9, align 8
  %76 = getelementptr inbounds nuw %struct.memblock_s, ptr %75, i32 0, i32 4
  %77 = load ptr, ptr %76, align 8
  store ptr %77, ptr %9, align 8
  br label %78

78:                                               ; preds = %74, %73
  br label %79

79:                                               ; preds = %78
  %80 = load ptr, ptr %11, align 8
  %81 = getelementptr inbounds nuw %struct.memblock_s, ptr %80, i32 0, i32 2
  %82 = load i32, ptr %81, align 8
  %83 = icmp ne i32 %82, 4
  br i1 %83, label %90, label %84

84:                                               ; preds = %79
  %85 = load ptr, ptr %11, align 8
  %86 = getelementptr inbounds nuw %struct.memblock_s, ptr %85, i32 0, i32 0
  %87 = load i32, ptr %86, align 8
  %88 = load i32, ptr %6, align 4
  %89 = icmp slt i32 %87, %88
  br label %90

90:                                               ; preds = %84, %79
  %91 = phi i1 [ true, %79 ], [ %89, %84 ]
  br i1 %91, label %41, label %92, !llvm.loop !8

92:                                               ; preds = %90
  %93 = load ptr, ptr %11, align 8
  %94 = getelementptr inbounds nuw %struct.memblock_s, ptr %93, i32 0, i32 0
  %95 = load i32, ptr %94, align 8
  %96 = load i32, ptr %6, align 4
  %97 = sub nsw i32 %95, %96
  store i32 %97, ptr %7, align 4
  %98 = load i32, ptr %7, align 4
  %99 = icmp sgt i32 %98, 64
  br i1 %99, label %100, label %131

100:                                              ; preds = %92
  %101 = load ptr, ptr %11, align 8
  %102 = load i32, ptr %6, align 4
  %103 = sext i32 %102 to i64
  %104 = getelementptr inbounds i8, ptr %101, i64 %103
  store ptr %104, ptr %10, align 8
  %105 = load i32, ptr %7, align 4
  %106 = load ptr, ptr %10, align 8
  %107 = getelementptr inbounds nuw %struct.memblock_s, ptr %106, i32 0, i32 0
  store i32 %105, ptr %107, align 8
  %108 = load ptr, ptr %10, align 8
  %109 = getelementptr inbounds nuw %struct.memblock_s, ptr %108, i32 0, i32 2
  store i32 4, ptr %109, align 8
  %110 = load ptr, ptr %10, align 8
  %111 = getelementptr inbounds nuw %struct.memblock_s, ptr %110, i32 0, i32 1
  store ptr null, ptr %111, align 8
  %112 = load ptr, ptr %11, align 8
  %113 = load ptr, ptr %10, align 8
  %114 = getelementptr inbounds nuw %struct.memblock_s, ptr %113, i32 0, i32 5
  store ptr %112, ptr %114, align 8
  %115 = load ptr, ptr %11, align 8
  %116 = getelementptr inbounds nuw %struct.memblock_s, ptr %115, i32 0, i32 4
  %117 = load ptr, ptr %116, align 8
  %118 = load ptr, ptr %10, align 8
  %119 = getelementptr inbounds nuw %struct.memblock_s, ptr %118, i32 0, i32 4
  store ptr %117, ptr %119, align 8
  %120 = load ptr, ptr %10, align 8
  %121 = load ptr, ptr %10, align 8
  %122 = getelementptr inbounds nuw %struct.memblock_s, ptr %121, i32 0, i32 4
  %123 = load ptr, ptr %122, align 8
  %124 = getelementptr inbounds nuw %struct.memblock_s, ptr %123, i32 0, i32 5
  store ptr %120, ptr %124, align 8
  %125 = load ptr, ptr %10, align 8
  %126 = load ptr, ptr %11, align 8
  %127 = getelementptr inbounds nuw %struct.memblock_s, ptr %126, i32 0, i32 4
  store ptr %125, ptr %127, align 8
  %128 = load i32, ptr %6, align 4
  %129 = load ptr, ptr %11, align 8
  %130 = getelementptr inbounds nuw %struct.memblock_s, ptr %129, i32 0, i32 0
  store i32 %128, ptr %130, align 8
  br label %131

131:                                              ; preds = %100, %92
  %132 = load ptr, ptr %4, align 8
  %133 = icmp eq ptr %132, null
  br i1 %133, label %134, label %138

134:                                              ; preds = %131
  %135 = load i32, ptr %5, align 4
  %136 = icmp sge i32 %135, 7
  br i1 %136, label %137, label %138

137:                                              ; preds = %134
  call void (ptr, ...) @I_Error(ptr noundef @"??_C@_0DD@MJJDHHFN@Z_Malloc?3?5an?5owner?5is?5required?5f@")
  br label %138

138:                                              ; preds = %137, %134, %131
  %139 = load ptr, ptr %4, align 8
  %140 = load ptr, ptr %11, align 8
  %141 = getelementptr inbounds nuw %struct.memblock_s, ptr %140, i32 0, i32 1
  store ptr %139, ptr %141, align 8
  %142 = load i32, ptr %5, align 4
  %143 = load ptr, ptr %11, align 8
  %144 = getelementptr inbounds nuw %struct.memblock_s, ptr %143, i32 0, i32 2
  store i32 %142, ptr %144, align 8
  %145 = load ptr, ptr %11, align 8
  %146 = getelementptr inbounds nuw i8, ptr %145, i64 40
  store ptr %146, ptr %12, align 8
  %147 = load ptr, ptr %11, align 8
  %148 = getelementptr inbounds nuw %struct.memblock_s, ptr %147, i32 0, i32 1
  %149 = load ptr, ptr %148, align 8
  %150 = icmp ne ptr %149, null
  br i1 %150, label %151, label %156

151:                                              ; preds = %138
  %152 = load ptr, ptr %12, align 8
  %153 = load ptr, ptr %11, align 8
  %154 = getelementptr inbounds nuw %struct.memblock_s, ptr %153, i32 0, i32 1
  %155 = load ptr, ptr %154, align 8
  store ptr %152, ptr %155, align 8
  br label %156

156:                                              ; preds = %151, %138
  %157 = load ptr, ptr %11, align 8
  %158 = getelementptr inbounds nuw %struct.memblock_s, ptr %157, i32 0, i32 4
  %159 = load ptr, ptr %158, align 8
  %160 = load ptr, ptr @mainzone, align 8
  %161 = getelementptr inbounds nuw %struct.memzone_t, ptr %160, i32 0, i32 2
  store ptr %159, ptr %161, align 8
  %162 = load ptr, ptr %11, align 8
  %163 = getelementptr inbounds nuw %struct.memblock_s, ptr %162, i32 0, i32 3
  store i32 1919505, ptr %163, align 4
  %164 = load ptr, ptr %12, align 8
  ret ptr %164
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @Z_FreeTags(i32 noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca ptr, align 8
  %6 = alloca ptr, align 8
  store i32 %1, ptr %3, align 4
  store i32 %0, ptr %4, align 4
  %7 = load ptr, ptr @mainzone, align 8
  %8 = getelementptr inbounds nuw %struct.memzone_t, ptr %7, i32 0, i32 1
  %9 = getelementptr inbounds nuw %struct.memblock_s, ptr %8, i32 0, i32 4
  %10 = load ptr, ptr %9, align 8
  store ptr %10, ptr %5, align 8
  br label %11

11:                                               ; preds = %41, %2
  %12 = load ptr, ptr %5, align 8
  %13 = load ptr, ptr @mainzone, align 8
  %14 = getelementptr inbounds nuw %struct.memzone_t, ptr %13, i32 0, i32 1
  %15 = icmp ne ptr %12, %14
  br i1 %15, label %16, label %43

16:                                               ; preds = %11
  %17 = load ptr, ptr %5, align 8
  %18 = getelementptr inbounds nuw %struct.memblock_s, ptr %17, i32 0, i32 4
  %19 = load ptr, ptr %18, align 8
  store ptr %19, ptr %6, align 8
  %20 = load ptr, ptr %5, align 8
  %21 = getelementptr inbounds nuw %struct.memblock_s, ptr %20, i32 0, i32 2
  %22 = load i32, ptr %21, align 8
  %23 = icmp eq i32 %22, 4
  br i1 %23, label %24, label %25

24:                                               ; preds = %16
  br label %41

25:                                               ; preds = %16
  %26 = load ptr, ptr %5, align 8
  %27 = getelementptr inbounds nuw %struct.memblock_s, ptr %26, i32 0, i32 2
  %28 = load i32, ptr %27, align 8
  %29 = load i32, ptr %4, align 4
  %30 = icmp sge i32 %28, %29
  br i1 %30, label %31, label %40

31:                                               ; preds = %25
  %32 = load ptr, ptr %5, align 8
  %33 = getelementptr inbounds nuw %struct.memblock_s, ptr %32, i32 0, i32 2
  %34 = load i32, ptr %33, align 8
  %35 = load i32, ptr %3, align 4
  %36 = icmp sle i32 %34, %35
  br i1 %36, label %37, label %40

37:                                               ; preds = %31
  %38 = load ptr, ptr %5, align 8
  %39 = getelementptr inbounds nuw i8, ptr %38, i64 40
  call void @Z_Free(ptr noundef %39)
  br label %40

40:                                               ; preds = %37, %31, %25
  br label %41

41:                                               ; preds = %40, %24
  %42 = load ptr, ptr %6, align 8
  store ptr %42, ptr %5, align 8
  br label %11, !llvm.loop !10

43:                                               ; preds = %11
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @Z_DumpHeap(i32 noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca ptr, align 8
  store i32 %1, ptr %3, align 4
  store i32 %0, ptr %4, align 4
  %6 = load ptr, ptr @mainzone, align 8
  %7 = load ptr, ptr @mainzone, align 8
  %8 = getelementptr inbounds nuw %struct.memzone_t, ptr %7, i32 0, i32 0
  %9 = load i32, ptr %8, align 8
  %10 = call i32 (ptr, ...) @printf(ptr noundef @"??_C@_0BN@DBGKJAGK@zone?5size?3?5?$CFi?5?5location?3?5?$CFp?6?$AA@", i32 noundef %9, ptr noundef %6)
  %11 = load i32, ptr %3, align 4
  %12 = load i32, ptr %4, align 4
  %13 = call i32 (ptr, ...) @printf(ptr noundef @"??_C@_0BF@BCHJJIJD@tag?5range?3?5?$CFi?5to?5?$CFi?6?$AA@", i32 noundef %12, i32 noundef %11)
  %14 = load ptr, ptr @mainzone, align 8
  %15 = getelementptr inbounds nuw %struct.memzone_t, ptr %14, i32 0, i32 1
  %16 = getelementptr inbounds nuw %struct.memblock_s, ptr %15, i32 0, i32 4
  %17 = load ptr, ptr %16, align 8
  store ptr %17, ptr %5, align 8
  br label %18

18:                                               ; preds = %88, %2
  %19 = load ptr, ptr %5, align 8
  %20 = getelementptr inbounds nuw %struct.memblock_s, ptr %19, i32 0, i32 2
  %21 = load i32, ptr %20, align 8
  %22 = load i32, ptr %4, align 4
  %23 = icmp sge i32 %21, %22
  br i1 %23, label %24, label %42

24:                                               ; preds = %18
  %25 = load ptr, ptr %5, align 8
  %26 = getelementptr inbounds nuw %struct.memblock_s, ptr %25, i32 0, i32 2
  %27 = load i32, ptr %26, align 8
  %28 = load i32, ptr %3, align 4
  %29 = icmp sle i32 %27, %28
  br i1 %29, label %30, label %42

30:                                               ; preds = %24
  %31 = load ptr, ptr %5, align 8
  %32 = getelementptr inbounds nuw %struct.memblock_s, ptr %31, i32 0, i32 2
  %33 = load i32, ptr %32, align 8
  %34 = load ptr, ptr %5, align 8
  %35 = getelementptr inbounds nuw %struct.memblock_s, ptr %34, i32 0, i32 1
  %36 = load ptr, ptr %35, align 8
  %37 = load ptr, ptr %5, align 8
  %38 = getelementptr inbounds nuw %struct.memblock_s, ptr %37, i32 0, i32 0
  %39 = load i32, ptr %38, align 8
  %40 = load ptr, ptr %5, align 8
  %41 = call i32 (ptr, ...) @printf(ptr noundef @"??_C@_0CM@IHDHPOFO@block?3?$CFp?5?5?5?5size?3?$CF7i?5?5?5?5user?3?$CFp?5@", ptr noundef %40, i32 noundef %39, ptr noundef %36, i32 noundef %33)
  br label %42

42:                                               ; preds = %30, %24, %18
  %43 = load ptr, ptr %5, align 8
  %44 = getelementptr inbounds nuw %struct.memblock_s, ptr %43, i32 0, i32 4
  %45 = load ptr, ptr %44, align 8
  %46 = load ptr, ptr @mainzone, align 8
  %47 = getelementptr inbounds nuw %struct.memzone_t, ptr %46, i32 0, i32 1
  %48 = icmp eq ptr %45, %47
  br i1 %48, label %49, label %50

49:                                               ; preds = %42
  br label %92

50:                                               ; preds = %42
  %51 = load ptr, ptr %5, align 8
  %52 = load ptr, ptr %5, align 8
  %53 = getelementptr inbounds nuw %struct.memblock_s, ptr %52, i32 0, i32 0
  %54 = load i32, ptr %53, align 8
  %55 = sext i32 %54 to i64
  %56 = getelementptr inbounds i8, ptr %51, i64 %55
  %57 = load ptr, ptr %5, align 8
  %58 = getelementptr inbounds nuw %struct.memblock_s, ptr %57, i32 0, i32 4
  %59 = load ptr, ptr %58, align 8
  %60 = icmp ne ptr %56, %59
  br i1 %60, label %61, label %63

61:                                               ; preds = %50
  %62 = call i32 (ptr, ...) @printf(ptr noundef @"??_C@_0DB@EJEJBDEF@ERROR?3?5block?5size?5does?5not?5touch@")
  br label %63

63:                                               ; preds = %61, %50
  %64 = load ptr, ptr %5, align 8
  %65 = getelementptr inbounds nuw %struct.memblock_s, ptr %64, i32 0, i32 4
  %66 = load ptr, ptr %65, align 8
  %67 = getelementptr inbounds nuw %struct.memblock_s, ptr %66, i32 0, i32 5
  %68 = load ptr, ptr %67, align 8
  %69 = load ptr, ptr %5, align 8
  %70 = icmp ne ptr %68, %69
  br i1 %70, label %71, label %73

71:                                               ; preds = %63
  %72 = call i32 (ptr, ...) @printf(ptr noundef @"??_C@_0DB@INBMMEOG@ERROR?3?5next?5block?5doesn?8t?5have?5p@")
  br label %73

73:                                               ; preds = %71, %63
  %74 = load ptr, ptr %5, align 8
  %75 = getelementptr inbounds nuw %struct.memblock_s, ptr %74, i32 0, i32 2
  %76 = load i32, ptr %75, align 8
  %77 = icmp eq i32 %76, 4
  br i1 %77, label %78, label %87

78:                                               ; preds = %73
  %79 = load ptr, ptr %5, align 8
  %80 = getelementptr inbounds nuw %struct.memblock_s, ptr %79, i32 0, i32 4
  %81 = load ptr, ptr %80, align 8
  %82 = getelementptr inbounds nuw %struct.memblock_s, ptr %81, i32 0, i32 2
  %83 = load i32, ptr %82, align 8
  %84 = icmp eq i32 %83, 4
  br i1 %84, label %85, label %87

85:                                               ; preds = %78
  %86 = call i32 (ptr, ...) @printf(ptr noundef @"??_C@_0CE@BLFCFJMN@ERROR?3?5two?5consecutive?5free?5bloc@")
  br label %87

87:                                               ; preds = %85, %78, %73
  br label %88

88:                                               ; preds = %87
  %89 = load ptr, ptr %5, align 8
  %90 = getelementptr inbounds nuw %struct.memblock_s, ptr %89, i32 0, i32 4
  %91 = load ptr, ptr %90, align 8
  store ptr %91, ptr %5, align 8
  br label %18

92:                                               ; preds = %49
  ret void
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
define dso_local void @Z_FileDumpHeap(ptr noundef %0) #0 {
  %2 = alloca ptr, align 8
  %3 = alloca ptr, align 8
  store ptr %0, ptr %2, align 8
  %4 = load ptr, ptr @mainzone, align 8
  %5 = load ptr, ptr @mainzone, align 8
  %6 = getelementptr inbounds nuw %struct.memzone_t, ptr %5, i32 0, i32 0
  %7 = load i32, ptr %6, align 8
  %8 = load ptr, ptr %2, align 8
  %9 = call i32 (ptr, ptr, ...) @fprintf(ptr noundef %8, ptr noundef @"??_C@_0BN@DBGKJAGK@zone?5size?3?5?$CFi?5?5location?3?5?$CFp?6?$AA@", i32 noundef %7, ptr noundef %4) #3
  %10 = load ptr, ptr @mainzone, align 8
  %11 = getelementptr inbounds nuw %struct.memzone_t, ptr %10, i32 0, i32 1
  %12 = getelementptr inbounds nuw %struct.memblock_s, ptr %11, i32 0, i32 4
  %13 = load ptr, ptr %12, align 8
  store ptr %13, ptr %3, align 8
  br label %14

14:                                               ; preds = %75, %1
  %15 = load ptr, ptr %3, align 8
  %16 = getelementptr inbounds nuw %struct.memblock_s, ptr %15, i32 0, i32 2
  %17 = load i32, ptr %16, align 8
  %18 = load ptr, ptr %3, align 8
  %19 = getelementptr inbounds nuw %struct.memblock_s, ptr %18, i32 0, i32 1
  %20 = load ptr, ptr %19, align 8
  %21 = load ptr, ptr %3, align 8
  %22 = getelementptr inbounds nuw %struct.memblock_s, ptr %21, i32 0, i32 0
  %23 = load i32, ptr %22, align 8
  %24 = load ptr, ptr %3, align 8
  %25 = load ptr, ptr %2, align 8
  %26 = call i32 (ptr, ptr, ...) @fprintf(ptr noundef %25, ptr noundef @"??_C@_0CM@IHDHPOFO@block?3?$CFp?5?5?5?5size?3?$CF7i?5?5?5?5user?3?$CFp?5@", ptr noundef %24, i32 noundef %23, ptr noundef %20, i32 noundef %17) #3
  %27 = load ptr, ptr %3, align 8
  %28 = getelementptr inbounds nuw %struct.memblock_s, ptr %27, i32 0, i32 4
  %29 = load ptr, ptr %28, align 8
  %30 = load ptr, ptr @mainzone, align 8
  %31 = getelementptr inbounds nuw %struct.memzone_t, ptr %30, i32 0, i32 1
  %32 = icmp eq ptr %29, %31
  br i1 %32, label %33, label %34

33:                                               ; preds = %14
  br label %79

34:                                               ; preds = %14
  %35 = load ptr, ptr %3, align 8
  %36 = load ptr, ptr %3, align 8
  %37 = getelementptr inbounds nuw %struct.memblock_s, ptr %36, i32 0, i32 0
  %38 = load i32, ptr %37, align 8
  %39 = sext i32 %38 to i64
  %40 = getelementptr inbounds i8, ptr %35, i64 %39
  %41 = load ptr, ptr %3, align 8
  %42 = getelementptr inbounds nuw %struct.memblock_s, ptr %41, i32 0, i32 4
  %43 = load ptr, ptr %42, align 8
  %44 = icmp ne ptr %40, %43
  br i1 %44, label %45, label %48

45:                                               ; preds = %34
  %46 = load ptr, ptr %2, align 8
  %47 = call i32 (ptr, ptr, ...) @fprintf(ptr noundef %46, ptr noundef @"??_C@_0DB@EJEJBDEF@ERROR?3?5block?5size?5does?5not?5touch@") #3
  br label %48

48:                                               ; preds = %45, %34
  %49 = load ptr, ptr %3, align 8
  %50 = getelementptr inbounds nuw %struct.memblock_s, ptr %49, i32 0, i32 4
  %51 = load ptr, ptr %50, align 8
  %52 = getelementptr inbounds nuw %struct.memblock_s, ptr %51, i32 0, i32 5
  %53 = load ptr, ptr %52, align 8
  %54 = load ptr, ptr %3, align 8
  %55 = icmp ne ptr %53, %54
  br i1 %55, label %56, label %59

56:                                               ; preds = %48
  %57 = load ptr, ptr %2, align 8
  %58 = call i32 (ptr, ptr, ...) @fprintf(ptr noundef %57, ptr noundef @"??_C@_0DB@INBMMEOG@ERROR?3?5next?5block?5doesn?8t?5have?5p@") #3
  br label %59

59:                                               ; preds = %56, %48
  %60 = load ptr, ptr %3, align 8
  %61 = getelementptr inbounds nuw %struct.memblock_s, ptr %60, i32 0, i32 2
  %62 = load i32, ptr %61, align 8
  %63 = icmp eq i32 %62, 4
  br i1 %63, label %64, label %74

64:                                               ; preds = %59
  %65 = load ptr, ptr %3, align 8
  %66 = getelementptr inbounds nuw %struct.memblock_s, ptr %65, i32 0, i32 4
  %67 = load ptr, ptr %66, align 8
  %68 = getelementptr inbounds nuw %struct.memblock_s, ptr %67, i32 0, i32 2
  %69 = load i32, ptr %68, align 8
  %70 = icmp eq i32 %69, 4
  br i1 %70, label %71, label %74

71:                                               ; preds = %64
  %72 = load ptr, ptr %2, align 8
  %73 = call i32 (ptr, ptr, ...) @fprintf(ptr noundef %72, ptr noundef @"??_C@_0CE@BLFCFJMN@ERROR?3?5two?5consecutive?5free?5bloc@") #3
  br label %74

74:                                               ; preds = %71, %64, %59
  br label %75

75:                                               ; preds = %74
  %76 = load ptr, ptr %3, align 8
  %77 = getelementptr inbounds nuw %struct.memblock_s, ptr %76, i32 0, i32 4
  %78 = load ptr, ptr %77, align 8
  store ptr %78, ptr %3, align 8
  br label %14

79:                                               ; preds = %33
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local i32 @fprintf(ptr noundef %0, ptr noundef %1, ...) #0 comdat {
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
  %10 = call i32 @_vfprintf_l(ptr noundef %9, ptr noundef %8, ptr noundef null, ptr noundef %7)
  store i32 %10, ptr %5, align 4
  call void @llvm.va_end.p0(ptr %6)
  %11 = load i32, ptr %5, align 4
  ret i32 %11
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @Z_CheckHeap() #0 {
  %1 = alloca ptr, align 8
  %2 = load ptr, ptr @mainzone, align 8
  %3 = getelementptr inbounds nuw %struct.memzone_t, ptr %2, i32 0, i32 1
  %4 = getelementptr inbounds nuw %struct.memblock_s, ptr %3, i32 0, i32 4
  %5 = load ptr, ptr %4, align 8
  store ptr %5, ptr %1, align 8
  br label %6

6:                                                ; preds = %49, %0
  %7 = load ptr, ptr %1, align 8
  %8 = getelementptr inbounds nuw %struct.memblock_s, ptr %7, i32 0, i32 4
  %9 = load ptr, ptr %8, align 8
  %10 = load ptr, ptr @mainzone, align 8
  %11 = getelementptr inbounds nuw %struct.memzone_t, ptr %10, i32 0, i32 1
  %12 = icmp eq ptr %9, %11
  br i1 %12, label %13, label %14

13:                                               ; preds = %6
  br label %53

14:                                               ; preds = %6
  %15 = load ptr, ptr %1, align 8
  %16 = load ptr, ptr %1, align 8
  %17 = getelementptr inbounds nuw %struct.memblock_s, ptr %16, i32 0, i32 0
  %18 = load i32, ptr %17, align 8
  %19 = sext i32 %18 to i64
  %20 = getelementptr inbounds i8, ptr %15, i64 %19
  %21 = load ptr, ptr %1, align 8
  %22 = getelementptr inbounds nuw %struct.memblock_s, ptr %21, i32 0, i32 4
  %23 = load ptr, ptr %22, align 8
  %24 = icmp ne ptr %20, %23
  br i1 %24, label %25, label %26

25:                                               ; preds = %14
  call void (ptr, ...) @I_Error(ptr noundef @"??_C@_0DH@PDLFHKNN@Z_CheckHeap?3?5block?5size?5does?5not@")
  br label %26

26:                                               ; preds = %25, %14
  %27 = load ptr, ptr %1, align 8
  %28 = getelementptr inbounds nuw %struct.memblock_s, ptr %27, i32 0, i32 4
  %29 = load ptr, ptr %28, align 8
  %30 = getelementptr inbounds nuw %struct.memblock_s, ptr %29, i32 0, i32 5
  %31 = load ptr, ptr %30, align 8
  %32 = load ptr, ptr %1, align 8
  %33 = icmp ne ptr %31, %32
  br i1 %33, label %34, label %35

34:                                               ; preds = %26
  call void (ptr, ...) @I_Error(ptr noundef @"??_C@_0DH@DHOAKNHO@Z_CheckHeap?3?5next?5block?5doesn?8t?5@")
  br label %35

35:                                               ; preds = %34, %26
  %36 = load ptr, ptr %1, align 8
  %37 = getelementptr inbounds nuw %struct.memblock_s, ptr %36, i32 0, i32 2
  %38 = load i32, ptr %37, align 8
  %39 = icmp eq i32 %38, 4
  br i1 %39, label %40, label %48

40:                                               ; preds = %35
  %41 = load ptr, ptr %1, align 8
  %42 = getelementptr inbounds nuw %struct.memblock_s, ptr %41, i32 0, i32 4
  %43 = load ptr, ptr %42, align 8
  %44 = getelementptr inbounds nuw %struct.memblock_s, ptr %43, i32 0, i32 2
  %45 = load i32, ptr %44, align 8
  %46 = icmp eq i32 %45, 4
  br i1 %46, label %47, label %48

47:                                               ; preds = %40
  call void (ptr, ...) @I_Error(ptr noundef @"??_C@_0CK@MHBJLLKL@Z_CheckHeap?3?5two?5consecutive?5fre@")
  br label %48

48:                                               ; preds = %47, %40, %35
  br label %49

49:                                               ; preds = %48
  %50 = load ptr, ptr %1, align 8
  %51 = getelementptr inbounds nuw %struct.memblock_s, ptr %50, i32 0, i32 4
  %52 = load ptr, ptr %51, align 8
  store ptr %52, ptr %1, align 8
  br label %6

53:                                               ; preds = %13
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @Z_ChangeTag2(ptr noundef %0, i32 noundef %1, ptr noundef %2, i32 noundef %3) #0 {
  %5 = alloca i32, align 4
  %6 = alloca ptr, align 8
  %7 = alloca i32, align 4
  %8 = alloca ptr, align 8
  %9 = alloca ptr, align 8
  store i32 %3, ptr %5, align 4
  store ptr %2, ptr %6, align 8
  store i32 %1, ptr %7, align 4
  store ptr %0, ptr %8, align 8
  %10 = load ptr, ptr %8, align 8
  %11 = getelementptr inbounds i8, ptr %10, i64 -40
  store ptr %11, ptr %9, align 8
  %12 = load ptr, ptr %9, align 8
  %13 = getelementptr inbounds nuw %struct.memblock_s, ptr %12, i32 0, i32 3
  %14 = load i32, ptr %13, align 4
  %15 = icmp ne i32 %14, 1919505
  br i1 %15, label %16, label %19

16:                                               ; preds = %4
  %17 = load i32, ptr %5, align 4
  %18 = load ptr, ptr %6, align 8
  call void (ptr, ...) @I_Error(ptr noundef @"??_C@_0CM@CJBLFFHI@?$CFs?3?$CFi?3?5Z_ChangeTag?3?5block?5withou@", ptr noundef %18, i32 noundef %17)
  br label %19

19:                                               ; preds = %16, %4
  %20 = load i32, ptr %7, align 4
  %21 = icmp sge i32 %20, 7
  br i1 %21, label %22, label %30

22:                                               ; preds = %19
  %23 = load ptr, ptr %9, align 8
  %24 = getelementptr inbounds nuw %struct.memblock_s, ptr %23, i32 0, i32 1
  %25 = load ptr, ptr %24, align 8
  %26 = icmp eq ptr %25, null
  br i1 %26, label %27, label %30

27:                                               ; preds = %22
  %28 = load i32, ptr %5, align 4
  %29 = load ptr, ptr %6, align 8
  call void (ptr, ...) @I_Error(ptr noundef @"??_C@_0DN@MAENEHJP@?$CFs?3?$CFi?3?5Z_ChangeTag?3?5an?5owner?5is?5@", ptr noundef %29, i32 noundef %28)
  br label %30

30:                                               ; preds = %27, %22, %19
  %31 = load i32, ptr %7, align 4
  %32 = load ptr, ptr %9, align 8
  %33 = getelementptr inbounds nuw %struct.memblock_s, ptr %32, i32 0, i32 2
  store i32 %31, ptr %33, align 8
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @Z_ChangeUser(ptr noundef %0, ptr noundef %1) #0 {
  %3 = alloca ptr, align 8
  %4 = alloca ptr, align 8
  %5 = alloca ptr, align 8
  store ptr %1, ptr %3, align 8
  store ptr %0, ptr %4, align 8
  %6 = load ptr, ptr %4, align 8
  %7 = getelementptr inbounds i8, ptr %6, i64 -40
  store ptr %7, ptr %5, align 8
  %8 = load ptr, ptr %5, align 8
  %9 = getelementptr inbounds nuw %struct.memblock_s, ptr %8, i32 0, i32 3
  %10 = load i32, ptr %9, align 4
  %11 = icmp ne i32 %10, 1919505
  br i1 %11, label %12, label %13

12:                                               ; preds = %2
  call void (ptr, ...) @I_Error(ptr noundef @"??_C@_0DG@EOELOILK@Z_ChangeUser?3?5Tried?5to?5change?5us@")
  br label %13

13:                                               ; preds = %12, %2
  %14 = load ptr, ptr %3, align 8
  %15 = load ptr, ptr %5, align 8
  %16 = getelementptr inbounds nuw %struct.memblock_s, ptr %15, i32 0, i32 1
  store ptr %14, ptr %16, align 8
  %17 = load ptr, ptr %4, align 8
  %18 = load ptr, ptr %3, align 8
  store ptr %17, ptr %18, align 8
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @Z_FreeMemory() #0 {
  %1 = alloca ptr, align 8
  %2 = alloca i32, align 4
  store i32 0, ptr %2, align 4
  %3 = load ptr, ptr @mainzone, align 8
  %4 = getelementptr inbounds nuw %struct.memzone_t, ptr %3, i32 0, i32 1
  %5 = getelementptr inbounds nuw %struct.memblock_s, ptr %4, i32 0, i32 4
  %6 = load ptr, ptr %5, align 8
  store ptr %6, ptr %1, align 8
  br label %7

7:                                                ; preds = %29, %0
  %8 = load ptr, ptr %1, align 8
  %9 = load ptr, ptr @mainzone, align 8
  %10 = getelementptr inbounds nuw %struct.memzone_t, ptr %9, i32 0, i32 1
  %11 = icmp ne ptr %8, %10
  br i1 %11, label %12, label %33

12:                                               ; preds = %7
  %13 = load ptr, ptr %1, align 8
  %14 = getelementptr inbounds nuw %struct.memblock_s, ptr %13, i32 0, i32 2
  %15 = load i32, ptr %14, align 8
  %16 = icmp eq i32 %15, 4
  br i1 %16, label %22, label %17

17:                                               ; preds = %12
  %18 = load ptr, ptr %1, align 8
  %19 = getelementptr inbounds nuw %struct.memblock_s, ptr %18, i32 0, i32 2
  %20 = load i32, ptr %19, align 8
  %21 = icmp sge i32 %20, 7
  br i1 %21, label %22, label %28

22:                                               ; preds = %17, %12
  %23 = load ptr, ptr %1, align 8
  %24 = getelementptr inbounds nuw %struct.memblock_s, ptr %23, i32 0, i32 0
  %25 = load i32, ptr %24, align 8
  %26 = load i32, ptr %2, align 4
  %27 = add nsw i32 %26, %25
  store i32 %27, ptr %2, align 4
  br label %28

28:                                               ; preds = %22, %17
  br label %29

29:                                               ; preds = %28
  %30 = load ptr, ptr %1, align 8
  %31 = getelementptr inbounds nuw %struct.memblock_s, ptr %30, i32 0, i32 4
  %32 = load ptr, ptr %31, align 8
  store ptr %32, ptr %1, align 8
  br label %7, !llvm.loop !11

33:                                               ; preds = %7
  %34 = load i32, ptr %2, align 4
  ret i32 %34
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @Z_ZoneSize() #0 {
  %1 = load ptr, ptr @mainzone, align 8
  %2 = getelementptr inbounds nuw %struct.memzone_t, ptr %1, i32 0, i32 0
  %3 = load i32, ptr %2, align 8
  ret i32 %3
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

declare dso_local ptr @__acrt_iob_func(i32 noundef) #2

declare dso_local i32 @fflush(ptr noundef) #2

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

declare dso_local i32 @__stdio_common_vfprintf(i64 noundef, ptr noundef, ptr noundef, ptr noundef, ptr noundef) #2

attributes #0 = { noinline nounwind optnone uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nocallback nofree nosync nounwind willreturn }
attributes #2 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #3 = { nounwind }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\Doom-Generic/vm-porting/tests/doom_zzone\\src\\z_zone.c", directory: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain")
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
