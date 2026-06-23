; ModuleID = 'E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\projects\Doom-Generic/vm-porting/tests/doom_wad\src/w_wad.c'
source_filename = "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\Doom-Generic/vm-porting/tests/doom_wad\\src/w_wad.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-windows-msvc19.51.36246"

%struct.wadinfo_t = type { [4 x i8], i32, i32 }
%struct.filelump_t = type { i32, i32, [8 x i8] }
%struct._wad_file_s = type { ptr, ptr, i32 }
%struct.lumpinfo_s = type { [8 x i8], ptr, i32, i32, ptr, ptr }
%struct.anon = type { i32, ptr }

$sprintf = comdat any

$vsprintf = comdat any

$_snprintf = comdat any

$_vsnprintf = comdat any

$printf = comdat any

$_vsprintf_l = comdat any

$_vsnprintf_l = comdat any

$__local_stdio_printf_options = comdat any

$_vfprintf_l = comdat any

$"??_C@_0BD@CLEJOJGJ@?5couldn?8t?5open?5?$CFs?6?$AA@" = comdat any

$"??_C@_03GANHLHHC@wad?$AA@" = comdat any

$"??_C@_04NPKJGIDH@IWAD?$AA@" = comdat any

$"??_C@_04LCFJJNME@PWAD?$AA@" = comdat any

$"??_C@_0CK@IMFJDFI@Wad?5file?5?$CFs?5doesn?8t?5have?5IWAD?5or@" = comdat any

$"??_C@_0BP@COOHDNEN@W_GetNumForName?3?5?$CFs?5not?5found?$CB?$AA@" = comdat any

$"??_C@_0BN@EDACHEJG@W_LumpLength?3?5?$CFi?5?$DO?$DN?5numlumps?$AA@" = comdat any

$"??_C@_0BL@HBOHBNCH@W_ReadLump?3?5?$CFi?5?$DO?$DN?5numlumps?$AA@" = comdat any

$"??_C@_0CK@HFJKDBJE@W_ReadLump?3?5only?5read?5?$CFi?5of?5?$CFi?5o@" = comdat any

$"??_C@_0BP@BJDOEDJF@W_CacheLumpNum?3?5?$CFi?5?$DO?$DN?5numlumps?$AA@" = comdat any

$"??_C@_0JH@IKPNEAF@E?3?2_00_Michel?2_00_Lab?2_00_GitHub@" = comdat any

$"??_C@_0CB@JGMILBJ@W_ReleaseLumpNum?3?5?$CFi?5?$DO?$DN?5numlumps@" = comdat any

$"??_C@_0M@EJPOMJDM@doomgeneric?$AA@" = comdat any

$"??_C@_0IA@JBOBILGP@?6You?5are?5trying?5to?5use?5a?5?$CFs?5IWAD@" = comdat any

$"??_C@_0BK@OGFJNHBD@Couldn?8t?5realloc?5lumpinfo?$AA@" = comdat any

$"??_C@_06KOEGIEJN@POSSA1?$AA@" = comdat any

$"??_C@_06IBGJABFK@IMPXA1?$AA@" = comdat any

$"??_C@_06OCOCJGPO@ETTNA1?$AA@" = comdat any

$"??_C@_06HDBCNHBM@AGRDA1?$AA@" = comdat any

@numlumps = dso_local global i32 0, align 4
@"??_C@_0BD@CLEJOJGJ@?5couldn?8t?5open?5?$CFs?6?$AA@" = linkonce_odr dso_local unnamed_addr constant [19 x i8] c" couldn't open %s\0A\00", comdat, align 1
@"??_C@_03GANHLHHC@wad?$AA@" = linkonce_odr dso_local unnamed_addr constant [4 x i8] c"wad\00", comdat, align 1
@"??_C@_04NPKJGIDH@IWAD?$AA@" = linkonce_odr dso_local unnamed_addr constant [5 x i8] c"IWAD\00", comdat, align 1
@"??_C@_04LCFJJNME@PWAD?$AA@" = linkonce_odr dso_local unnamed_addr constant [5 x i8] c"PWAD\00", comdat, align 1
@"??_C@_0CK@IMFJDFI@Wad?5file?5?$CFs?5doesn?8t?5have?5IWAD?5or@" = linkonce_odr dso_local unnamed_addr constant [42 x i8] c"Wad file %s doesn't have IWAD or PWAD id\0A\00", comdat, align 1
@lumpinfo = dso_local global ptr null, align 8
@lumphash = internal global ptr null, align 8
@"??_C@_0BP@COOHDNEN@W_GetNumForName?3?5?$CFs?5not?5found?$CB?$AA@" = linkonce_odr dso_local unnamed_addr constant [31 x i8] c"W_GetNumForName: %s not found!\00", comdat, align 1
@"??_C@_0BN@EDACHEJG@W_LumpLength?3?5?$CFi?5?$DO?$DN?5numlumps?$AA@" = linkonce_odr dso_local unnamed_addr constant [29 x i8] c"W_LumpLength: %i >= numlumps\00", comdat, align 1
@"??_C@_0BL@HBOHBNCH@W_ReadLump?3?5?$CFi?5?$DO?$DN?5numlumps?$AA@" = linkonce_odr dso_local unnamed_addr constant [27 x i8] c"W_ReadLump: %i >= numlumps\00", comdat, align 1
@"??_C@_0CK@HFJKDBJE@W_ReadLump?3?5only?5read?5?$CFi?5of?5?$CFi?5o@" = linkonce_odr dso_local unnamed_addr constant [42 x i8] c"W_ReadLump: only read %i of %i on lump %i\00", comdat, align 1
@"??_C@_0BP@BJDOEDJF@W_CacheLumpNum?3?5?$CFi?5?$DO?$DN?5numlumps?$AA@" = linkonce_odr dso_local unnamed_addr constant [31 x i8] c"W_CacheLumpNum: %i >= numlumps\00", comdat, align 1
@"??_C@_0JH@IKPNEAF@E?3?2_00_Michel?2_00_Lab?2_00_GitHub@" = linkonce_odr dso_local unnamed_addr constant [151 x i8] c"E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\Doom-Generic/vm-porting/tests/doom_wad\\src/w_wad.c\00", comdat, align 1
@"??_C@_0CB@JGMILBJ@W_ReleaseLumpNum?3?5?$CFi?5?$DO?$DN?5numlumps@" = linkonce_odr dso_local unnamed_addr constant [33 x i8] c"W_ReleaseLumpNum: %i >= numlumps\00", comdat, align 1
@"??_C@_0M@EJPOMJDM@doomgeneric?$AA@" = linkonce_odr dso_local unnamed_addr constant [12 x i8] c"doomgeneric\00", comdat, align 1
@"??_C@_0IA@JBOBILGP@?6You?5are?5trying?5to?5use?5a?5?$CFs?5IWAD@" = linkonce_odr dso_local unnamed_addr constant [128 x i8] c"\0AYou are trying to use a %s IWAD file with the %s%s binary.\0AThis isn't going to work.\0AYou probably want to use the %s%s binary.\00", comdat, align 1
@__local_stdio_printf_options._OptionsStorage = internal global i64 0, align 8
@"??_C@_0BK@OGFJNHBD@Couldn?8t?5realloc?5lumpinfo?$AA@" = linkonce_odr dso_local unnamed_addr constant [26 x i8] c"Couldn't realloc lumpinfo\00", comdat, align 1
@"??_C@_06KOEGIEJN@POSSA1?$AA@" = linkonce_odr dso_local unnamed_addr constant [7 x i8] c"POSSA1\00", comdat, align 1
@"??_C@_06IBGJABFK@IMPXA1?$AA@" = linkonce_odr dso_local unnamed_addr constant [7 x i8] c"IMPXA1\00", comdat, align 1
@"??_C@_06OCOCJGPO@ETTNA1?$AA@" = linkonce_odr dso_local unnamed_addr constant [7 x i8] c"ETTNA1\00", comdat, align 1
@"??_C@_06HDBCNHBM@AGRDA1?$AA@" = linkonce_odr dso_local unnamed_addr constant [7 x i8] c"AGRDA1\00", comdat, align 1
@unique_lumps = internal constant [4 x { i32, [4 x i8], ptr }] [{ i32, [4 x i8], ptr } { i32 0, [4 x i8] zeroinitializer, ptr @"??_C@_06KOEGIEJN@POSSA1?$AA@" }, { i32, [4 x i8], ptr } { i32 6, [4 x i8] zeroinitializer, ptr @"??_C@_06IBGJABFK@IMPXA1?$AA@" }, { i32, [4 x i8], ptr } { i32 7, [4 x i8] zeroinitializer, ptr @"??_C@_06OCOCJGPO@ETTNA1?$AA@" }, { i32, [4 x i8], ptr } { i32 8, [4 x i8] zeroinitializer, ptr @"??_C@_06HDBCNHBM@AGRDA1?$AA@" }], align 16

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
define dso_local i32 @W_LumpNameHash(ptr noundef %0) #0 {
  %2 = alloca ptr, align 8
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  store ptr %0, ptr %2, align 8
  store i32 5381, ptr %3, align 4
  store i32 0, ptr %4, align 4
  br label %5

5:                                                ; preds = %31, %1
  %6 = load i32, ptr %4, align 4
  %7 = icmp ult i32 %6, 8
  br i1 %7, label %8, label %16

8:                                                ; preds = %5
  %9 = load ptr, ptr %2, align 8
  %10 = load i32, ptr %4, align 4
  %11 = zext i32 %10 to i64
  %12 = getelementptr inbounds nuw i8, ptr %9, i64 %11
  %13 = load i8, ptr %12, align 1
  %14 = sext i8 %13 to i32
  %15 = icmp ne i32 %14, 0
  br label %16

16:                                               ; preds = %8, %5
  %17 = phi i1 [ false, %5 ], [ %15, %8 ]
  br i1 %17, label %18, label %34

18:                                               ; preds = %16
  %19 = load i32, ptr %3, align 4
  %20 = shl i32 %19, 5
  %21 = load i32, ptr %3, align 4
  %22 = xor i32 %20, %21
  %23 = load ptr, ptr %2, align 8
  %24 = load i32, ptr %4, align 4
  %25 = zext i32 %24 to i64
  %26 = getelementptr inbounds nuw i8, ptr %23, i64 %25
  %27 = load i8, ptr %26, align 1
  %28 = sext i8 %27 to i32
  %29 = call i32 @toupper(i32 noundef %28) #8
  %30 = xor i32 %22, %29
  store i32 %30, ptr %3, align 4
  br label %31

31:                                               ; preds = %18
  %32 = load i32, ptr %4, align 4
  %33 = add i32 %32, 1
  store i32 %33, ptr %4, align 4
  br label %5, !llvm.loop !8

34:                                               ; preds = %16
  %35 = load i32, ptr %3, align 4
  ret i32 %35
}

; Function Attrs: nounwind willreturn memory(read)
declare dso_local i32 @toupper(i32 noundef) #1

; Function Attrs: noinline nounwind optnone uwtable
define dso_local ptr @W_AddFile(ptr noundef %0) #0 {
  %2 = alloca ptr, align 8
  %3 = alloca ptr, align 8
  %4 = alloca %struct.wadinfo_t, align 4
  %5 = alloca ptr, align 8
  %6 = alloca i32, align 4
  %7 = alloca ptr, align 8
  %8 = alloca i32, align 4
  %9 = alloca i32, align 4
  %10 = alloca ptr, align 8
  %11 = alloca ptr, align 8
  %12 = alloca i32, align 4
  store ptr %0, ptr %3, align 8
  %13 = load ptr, ptr %3, align 8
  %14 = call ptr @W_OpenFile(ptr noundef %13)
  store ptr %14, ptr %7, align 8
  %15 = load ptr, ptr %7, align 8
  %16 = icmp eq ptr %15, null
  br i1 %16, label %17, label %20

17:                                               ; preds = %1
  %18 = load ptr, ptr %3, align 8
  %19 = call i32 (ptr, ...) @printf(ptr noundef @"??_C@_0BD@CLEJOJGJ@?5couldn?8t?5open?5?$CFs?6?$AA@", ptr noundef %18)
  store ptr null, ptr %2, align 8
  br label %135

20:                                               ; preds = %1
  %21 = load i32, ptr @numlumps, align 4
  store i32 %21, ptr %12, align 4
  %22 = load ptr, ptr %3, align 8
  %23 = load ptr, ptr %3, align 8
  %24 = call i64 @strlen(ptr noundef %23) #9
  %25 = getelementptr inbounds nuw i8, ptr %22, i64 %24
  %26 = getelementptr inbounds i8, ptr %25, i64 -3
  %27 = call i32 @_stricmp(ptr noundef %26, ptr noundef @"??_C@_03GANHLHHC@wad?$AA@")
  %28 = icmp ne i32 %27, 0
  br i1 %28, label %29, label %44

29:                                               ; preds = %20
  %30 = call ptr @Z_Malloc(i32 noundef 16, i32 noundef 1, ptr noundef null)
  store ptr %30, ptr %10, align 8
  %31 = load ptr, ptr %10, align 8
  %32 = getelementptr inbounds nuw %struct.filelump_t, ptr %31, i32 0, i32 0
  store i32 0, ptr %32, align 4
  %33 = load ptr, ptr %7, align 8
  %34 = getelementptr inbounds nuw %struct._wad_file_s, ptr %33, i32 0, i32 2
  %35 = load i32, ptr %34, align 8
  %36 = load ptr, ptr %10, align 8
  %37 = getelementptr inbounds nuw %struct.filelump_t, ptr %36, i32 0, i32 1
  store i32 %35, ptr %37, align 4
  %38 = load ptr, ptr %10, align 8
  %39 = getelementptr inbounds nuw %struct.filelump_t, ptr %38, i32 0, i32 2
  %40 = getelementptr inbounds [8 x i8], ptr %39, i64 0, i64 0
  %41 = load ptr, ptr %3, align 8
  call void @M_ExtractFileBase(ptr noundef %41, ptr noundef %40)
  %42 = load i32, ptr %12, align 4
  %43 = add nsw i32 %42, 1
  store i32 %43, ptr %12, align 4
  br label %84

44:                                               ; preds = %20
  %45 = load ptr, ptr %7, align 8
  %46 = call i64 @W_Read(ptr noundef %45, i32 noundef 0, ptr noundef %4, i64 noundef 12)
  %47 = getelementptr inbounds nuw %struct.wadinfo_t, ptr %4, i32 0, i32 0
  %48 = getelementptr inbounds [4 x i8], ptr %47, i64 0, i64 0
  %49 = call i32 @strncmp(ptr noundef %48, ptr noundef @"??_C@_04NPKJGIDH@IWAD?$AA@", i64 noundef 4) #9
  %50 = icmp ne i32 %49, 0
  br i1 %50, label %51, label %59

51:                                               ; preds = %44
  %52 = getelementptr inbounds nuw %struct.wadinfo_t, ptr %4, i32 0, i32 0
  %53 = getelementptr inbounds [4 x i8], ptr %52, i64 0, i64 0
  %54 = call i32 @strncmp(ptr noundef %53, ptr noundef @"??_C@_04LCFJJNME@PWAD?$AA@", i64 noundef 4) #9
  %55 = icmp ne i32 %54, 0
  br i1 %55, label %56, label %58

56:                                               ; preds = %51
  %57 = load ptr, ptr %3, align 8
  call void (ptr, ...) @I_Error(ptr noundef @"??_C@_0CK@IMFJDFI@Wad?5file?5?$CFs?5doesn?8t?5have?5IWAD?5or@", ptr noundef %57)
  br label %58

58:                                               ; preds = %56, %51
  br label %59

59:                                               ; preds = %58, %44
  %60 = getelementptr inbounds nuw %struct.wadinfo_t, ptr %4, i32 0, i32 1
  %61 = load i32, ptr %60, align 4
  %62 = getelementptr inbounds nuw %struct.wadinfo_t, ptr %4, i32 0, i32 1
  store i32 %61, ptr %62, align 4
  %63 = getelementptr inbounds nuw %struct.wadinfo_t, ptr %4, i32 0, i32 2
  %64 = load i32, ptr %63, align 4
  %65 = getelementptr inbounds nuw %struct.wadinfo_t, ptr %4, i32 0, i32 2
  store i32 %64, ptr %65, align 4
  %66 = getelementptr inbounds nuw %struct.wadinfo_t, ptr %4, i32 0, i32 1
  %67 = load i32, ptr %66, align 4
  %68 = sext i32 %67 to i64
  %69 = mul i64 %68, 16
  %70 = trunc i64 %69 to i32
  store i32 %70, ptr %8, align 4
  %71 = load i32, ptr %8, align 4
  %72 = call ptr @Z_Malloc(i32 noundef %71, i32 noundef 1, ptr noundef null)
  store ptr %72, ptr %10, align 8
  %73 = load i32, ptr %8, align 4
  %74 = sext i32 %73 to i64
  %75 = load ptr, ptr %10, align 8
  %76 = getelementptr inbounds nuw %struct.wadinfo_t, ptr %4, i32 0, i32 2
  %77 = load i32, ptr %76, align 4
  %78 = load ptr, ptr %7, align 8
  %79 = call i64 @W_Read(ptr noundef %78, i32 noundef %77, ptr noundef %75, i64 noundef %74)
  %80 = getelementptr inbounds nuw %struct.wadinfo_t, ptr %4, i32 0, i32 1
  %81 = load i32, ptr %80, align 4
  %82 = load i32, ptr %12, align 4
  %83 = add nsw i32 %82, %81
  store i32 %83, ptr %12, align 4
  br label %84

84:                                               ; preds = %59, %29
  %85 = load i32, ptr @numlumps, align 4
  store i32 %85, ptr %9, align 4
  %86 = load i32, ptr %12, align 4
  call void @ExtendLumpInfo(i32 noundef %86)
  %87 = load ptr, ptr @lumpinfo, align 8
  %88 = load i32, ptr %9, align 4
  %89 = sext i32 %88 to i64
  %90 = getelementptr inbounds %struct.lumpinfo_s, ptr %87, i64 %89
  store ptr %90, ptr %5, align 8
  %91 = load ptr, ptr %10, align 8
  store ptr %91, ptr %11, align 8
  %92 = load i32, ptr %9, align 4
  store i32 %92, ptr %6, align 4
  br label %93

93:                                               ; preds = %124, %84
  %94 = load i32, ptr %6, align 4
  %95 = load i32, ptr @numlumps, align 4
  %96 = icmp ult i32 %94, %95
  br i1 %96, label %97, label %127

97:                                               ; preds = %93
  %98 = load ptr, ptr %7, align 8
  %99 = load ptr, ptr %5, align 8
  %100 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %99, i32 0, i32 1
  store ptr %98, ptr %100, align 8
  %101 = load ptr, ptr %11, align 8
  %102 = getelementptr inbounds nuw %struct.filelump_t, ptr %101, i32 0, i32 0
  %103 = load i32, ptr %102, align 4
  %104 = load ptr, ptr %5, align 8
  %105 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %104, i32 0, i32 2
  store i32 %103, ptr %105, align 8
  %106 = load ptr, ptr %11, align 8
  %107 = getelementptr inbounds nuw %struct.filelump_t, ptr %106, i32 0, i32 1
  %108 = load i32, ptr %107, align 4
  %109 = load ptr, ptr %5, align 8
  %110 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %109, i32 0, i32 3
  store i32 %108, ptr %110, align 4
  %111 = load ptr, ptr %5, align 8
  %112 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %111, i32 0, i32 4
  store ptr null, ptr %112, align 8
  %113 = load ptr, ptr %11, align 8
  %114 = getelementptr inbounds nuw %struct.filelump_t, ptr %113, i32 0, i32 2
  %115 = getelementptr inbounds [8 x i8], ptr %114, i64 0, i64 0
  %116 = load ptr, ptr %5, align 8
  %117 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %116, i32 0, i32 0
  %118 = getelementptr inbounds [8 x i8], ptr %117, i64 0, i64 0
  %119 = call ptr @strncpy(ptr noundef %118, ptr noundef %115, i64 noundef 8) #9
  %120 = load ptr, ptr %5, align 8
  %121 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %120, i32 1
  store ptr %121, ptr %5, align 8
  %122 = load ptr, ptr %11, align 8
  %123 = getelementptr inbounds nuw %struct.filelump_t, ptr %122, i32 1
  store ptr %123, ptr %11, align 8
  br label %124

124:                                              ; preds = %97
  %125 = load i32, ptr %6, align 4
  %126 = add i32 %125, 1
  store i32 %126, ptr %6, align 4
  br label %93, !llvm.loop !10

127:                                              ; preds = %93
  %128 = load ptr, ptr %10, align 8
  call void @Z_Free(ptr noundef %128)
  %129 = load ptr, ptr @lumphash, align 8
  %130 = icmp ne ptr %129, null
  br i1 %130, label %131, label %133

131:                                              ; preds = %127
  %132 = load ptr, ptr @lumphash, align 8
  call void @Z_Free(ptr noundef %132)
  store ptr null, ptr @lumphash, align 8
  br label %133

133:                                              ; preds = %131, %127
  %134 = load ptr, ptr %7, align 8
  store ptr %134, ptr %2, align 8
  br label %135

135:                                              ; preds = %133, %17
  %136 = load ptr, ptr %2, align 8
  ret ptr %136
}

declare dso_local ptr @W_OpenFile(ptr noundef) #2

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

declare dso_local i32 @_stricmp(ptr noundef, ptr noundef) #2

; Function Attrs: nounwind
declare dso_local i64 @strlen(ptr noundef) #3

declare dso_local ptr @Z_Malloc(i32 noundef, i32 noundef, ptr noundef) #2

declare dso_local void @M_ExtractFileBase(ptr noundef, ptr noundef) #2

declare dso_local i64 @W_Read(ptr noundef, i32 noundef, ptr noundef, i64 noundef) #2

; Function Attrs: nounwind
declare dso_local i32 @strncmp(ptr noundef, ptr noundef, i64 noundef) #3

declare dso_local void @I_Error(ptr noundef, ...) #2

; Function Attrs: noinline nounwind optnone uwtable
define internal void @ExtendLumpInfo(i32 noundef %0) #0 {
  %2 = alloca i32, align 4
  %3 = alloca ptr, align 8
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  store i32 %0, ptr %2, align 4
  %6 = load i32, ptr %2, align 4
  %7 = sext i32 %6 to i64
  %8 = call noalias ptr @calloc(i64 noundef %7, i64 noundef 40) #10
  store ptr %8, ptr %3, align 8
  %9 = load ptr, ptr %3, align 8
  %10 = icmp eq ptr %9, null
  br i1 %10, label %11, label %12

11:                                               ; preds = %1
  call void (ptr, ...) @I_Error(ptr noundef @"??_C@_0BK@OGFJNHBD@Couldn?8t?5realloc?5lumpinfo?$AA@")
  br label %12

12:                                               ; preds = %11, %1
  store i32 0, ptr %4, align 4
  br label %13

13:                                               ; preds = %82, %12
  %14 = load i32, ptr %4, align 4
  %15 = load i32, ptr @numlumps, align 4
  %16 = icmp ult i32 %14, %15
  br i1 %16, label %17, label %21

17:                                               ; preds = %13
  %18 = load i32, ptr %4, align 4
  %19 = load i32, ptr %2, align 4
  %20 = icmp ult i32 %18, %19
  br label %21

21:                                               ; preds = %17, %13
  %22 = phi i1 [ false, %13 ], [ %20, %17 ]
  br i1 %22, label %23, label %85

23:                                               ; preds = %21
  %24 = load ptr, ptr %3, align 8
  %25 = load i32, ptr %4, align 4
  %26 = zext i32 %25 to i64
  %27 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %24, i64 %26
  %28 = load ptr, ptr @lumpinfo, align 8
  %29 = load i32, ptr %4, align 4
  %30 = zext i32 %29 to i64
  %31 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %28, i64 %30
  call void @llvm.memcpy.p0.p0.i64(ptr align 8 %27, ptr align 8 %31, i64 40, i1 false)
  %32 = load ptr, ptr %3, align 8
  %33 = load i32, ptr %4, align 4
  %34 = zext i32 %33 to i64
  %35 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %32, i64 %34
  %36 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %35, i32 0, i32 4
  %37 = load ptr, ptr %36, align 8
  %38 = icmp ne ptr %37, null
  br i1 %38, label %39, label %51

39:                                               ; preds = %23
  %40 = load ptr, ptr %3, align 8
  %41 = load i32, ptr %4, align 4
  %42 = zext i32 %41 to i64
  %43 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %40, i64 %42
  %44 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %43, i32 0, i32 4
  %45 = load ptr, ptr %3, align 8
  %46 = load i32, ptr %4, align 4
  %47 = zext i32 %46 to i64
  %48 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %45, i64 %47
  %49 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %48, i32 0, i32 4
  %50 = load ptr, ptr %49, align 8
  call void @Z_ChangeUser(ptr noundef %50, ptr noundef %44)
  br label %51

51:                                               ; preds = %39, %23
  %52 = load ptr, ptr @lumpinfo, align 8
  %53 = load i32, ptr %4, align 4
  %54 = zext i32 %53 to i64
  %55 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %52, i64 %54
  %56 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %55, i32 0, i32 5
  %57 = load ptr, ptr %56, align 8
  %58 = icmp ne ptr %57, null
  br i1 %58, label %59, label %81

59:                                               ; preds = %51
  %60 = load ptr, ptr @lumpinfo, align 8
  %61 = load i32, ptr %4, align 4
  %62 = zext i32 %61 to i64
  %63 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %60, i64 %62
  %64 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %63, i32 0, i32 5
  %65 = load ptr, ptr %64, align 8
  %66 = load ptr, ptr @lumpinfo, align 8
  %67 = ptrtoint ptr %65 to i64
  %68 = ptrtoint ptr %66 to i64
  %69 = sub i64 %67, %68
  %70 = sdiv exact i64 %69, 40
  %71 = trunc i64 %70 to i32
  store i32 %71, ptr %5, align 4
  %72 = load ptr, ptr %3, align 8
  %73 = load i32, ptr %5, align 4
  %74 = sext i32 %73 to i64
  %75 = getelementptr inbounds %struct.lumpinfo_s, ptr %72, i64 %74
  %76 = load ptr, ptr %3, align 8
  %77 = load i32, ptr %4, align 4
  %78 = zext i32 %77 to i64
  %79 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %76, i64 %78
  %80 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %79, i32 0, i32 5
  store ptr %75, ptr %80, align 8
  br label %81

81:                                               ; preds = %59, %51
  br label %82

82:                                               ; preds = %81
  %83 = load i32, ptr %4, align 4
  %84 = add i32 %83, 1
  store i32 %84, ptr %4, align 4
  br label %13, !llvm.loop !11

85:                                               ; preds = %21
  %86 = load ptr, ptr @lumpinfo, align 8
  call void @free(ptr noundef %86)
  %87 = load ptr, ptr %3, align 8
  store ptr %87, ptr @lumpinfo, align 8
  %88 = load i32, ptr %2, align 4
  store i32 %88, ptr @numlumps, align 4
  ret void
}

; Function Attrs: nounwind
declare dso_local ptr @strncpy(ptr noundef, ptr noundef, i64 noundef) #3

declare dso_local void @Z_Free(ptr noundef) #2

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @W_NumLumps() #0 {
  %1 = load i32, ptr @numlumps, align 4
  ret i32 %1
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @W_CheckNumForName(ptr noundef %0) #0 {
  %2 = alloca i32, align 4
  %3 = alloca ptr, align 8
  %4 = alloca ptr, align 8
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  store ptr %0, ptr %3, align 8
  %7 = load ptr, ptr @lumphash, align 8
  %8 = icmp ne ptr %7, null
  br i1 %8, label %9, label %43

9:                                                ; preds = %1
  %10 = load ptr, ptr %3, align 8
  %11 = call i32 @W_LumpNameHash(ptr noundef %10)
  %12 = load i32, ptr @numlumps, align 4
  %13 = urem i32 %11, %12
  store i32 %13, ptr %6, align 4
  %14 = load ptr, ptr @lumphash, align 8
  %15 = load i32, ptr %6, align 4
  %16 = sext i32 %15 to i64
  %17 = getelementptr inbounds ptr, ptr %14, i64 %16
  %18 = load ptr, ptr %17, align 8
  store ptr %18, ptr %4, align 8
  br label %19

19:                                               ; preds = %38, %9
  %20 = load ptr, ptr %4, align 8
  %21 = icmp ne ptr %20, null
  br i1 %21, label %22, label %42

22:                                               ; preds = %19
  %23 = load ptr, ptr %3, align 8
  %24 = load ptr, ptr %4, align 8
  %25 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %24, i32 0, i32 0
  %26 = getelementptr inbounds [8 x i8], ptr %25, i64 0, i64 0
  %27 = call i32 @_strnicmp(ptr noundef %26, ptr noundef %23, i64 noundef 8)
  %28 = icmp ne i32 %27, 0
  br i1 %28, label %37, label %29

29:                                               ; preds = %22
  %30 = load ptr, ptr %4, align 8
  %31 = load ptr, ptr @lumpinfo, align 8
  %32 = ptrtoint ptr %30 to i64
  %33 = ptrtoint ptr %31 to i64
  %34 = sub i64 %32, %33
  %35 = sdiv exact i64 %34, 40
  %36 = trunc i64 %35 to i32
  store i32 %36, ptr %2, align 4
  br label %67

37:                                               ; preds = %22
  br label %38

38:                                               ; preds = %37
  %39 = load ptr, ptr %4, align 8
  %40 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %39, i32 0, i32 5
  %41 = load ptr, ptr %40, align 8
  store ptr %41, ptr %4, align 8
  br label %19, !llvm.loop !12

42:                                               ; preds = %19
  br label %66

43:                                               ; preds = %1
  %44 = load i32, ptr @numlumps, align 4
  %45 = sub i32 %44, 1
  store i32 %45, ptr %5, align 4
  br label %46

46:                                               ; preds = %62, %43
  %47 = load i32, ptr %5, align 4
  %48 = icmp sge i32 %47, 0
  br i1 %48, label %49, label %65

49:                                               ; preds = %46
  %50 = load ptr, ptr %3, align 8
  %51 = load ptr, ptr @lumpinfo, align 8
  %52 = load i32, ptr %5, align 4
  %53 = sext i32 %52 to i64
  %54 = getelementptr inbounds %struct.lumpinfo_s, ptr %51, i64 %53
  %55 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %54, i32 0, i32 0
  %56 = getelementptr inbounds [8 x i8], ptr %55, i64 0, i64 0
  %57 = call i32 @_strnicmp(ptr noundef %56, ptr noundef %50, i64 noundef 8)
  %58 = icmp ne i32 %57, 0
  br i1 %58, label %61, label %59

59:                                               ; preds = %49
  %60 = load i32, ptr %5, align 4
  store i32 %60, ptr %2, align 4
  br label %67

61:                                               ; preds = %49
  br label %62

62:                                               ; preds = %61
  %63 = load i32, ptr %5, align 4
  %64 = add nsw i32 %63, -1
  store i32 %64, ptr %5, align 4
  br label %46, !llvm.loop !13

65:                                               ; preds = %46
  br label %66

66:                                               ; preds = %65, %42
  store i32 -1, ptr %2, align 4
  br label %67

67:                                               ; preds = %66, %59, %29
  %68 = load i32, ptr %2, align 4
  ret i32 %68
}

declare dso_local i32 @_strnicmp(ptr noundef, ptr noundef, i64 noundef) #2

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @W_GetNumForName(ptr noundef %0) #0 {
  %2 = alloca ptr, align 8
  %3 = alloca i32, align 4
  store ptr %0, ptr %2, align 8
  %4 = load ptr, ptr %2, align 8
  %5 = call i32 @W_CheckNumForName(ptr noundef %4)
  store i32 %5, ptr %3, align 4
  %6 = load i32, ptr %3, align 4
  %7 = icmp slt i32 %6, 0
  br i1 %7, label %8, label %10

8:                                                ; preds = %1
  %9 = load ptr, ptr %2, align 8
  call void (ptr, ...) @I_Error(ptr noundef @"??_C@_0BP@COOHDNEN@W_GetNumForName?3?5?$CFs?5not?5found?$CB?$AA@", ptr noundef %9)
  br label %10

10:                                               ; preds = %8, %1
  %11 = load i32, ptr %3, align 4
  ret i32 %11
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @W_LumpLength(i32 noundef %0) #0 {
  %2 = alloca i32, align 4
  store i32 %0, ptr %2, align 4
  %3 = load i32, ptr %2, align 4
  %4 = load i32, ptr @numlumps, align 4
  %5 = icmp uge i32 %3, %4
  br i1 %5, label %6, label %8

6:                                                ; preds = %1
  %7 = load i32, ptr %2, align 4
  call void (ptr, ...) @I_Error(ptr noundef @"??_C@_0BN@EDACHEJG@W_LumpLength?3?5?$CFi?5?$DO?$DN?5numlumps?$AA@", i32 noundef %7)
  br label %8

8:                                                ; preds = %6, %1
  %9 = load ptr, ptr @lumpinfo, align 8
  %10 = load i32, ptr %2, align 4
  %11 = zext i32 %10 to i64
  %12 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %9, i64 %11
  %13 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %12, i32 0, i32 3
  %14 = load i32, ptr %13, align 4
  ret i32 %14
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @W_ReadLump(i32 noundef %0, ptr noundef %1) #0 {
  %3 = alloca ptr, align 8
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  %6 = alloca ptr, align 8
  store ptr %1, ptr %3, align 8
  store i32 %0, ptr %4, align 4
  %7 = load i32, ptr %4, align 4
  %8 = load i32, ptr @numlumps, align 4
  %9 = icmp uge i32 %7, %8
  br i1 %9, label %10, label %12

10:                                               ; preds = %2
  %11 = load i32, ptr %4, align 4
  call void (ptr, ...) @I_Error(ptr noundef @"??_C@_0BL@HBOHBNCH@W_ReadLump?3?5?$CFi?5?$DO?$DN?5numlumps?$AA@", i32 noundef %11)
  br label %12

12:                                               ; preds = %10, %2
  %13 = load ptr, ptr @lumpinfo, align 8
  %14 = load i32, ptr %4, align 4
  %15 = zext i32 %14 to i64
  %16 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %13, i64 %15
  store ptr %16, ptr %6, align 8
  call void @I_BeginRead()
  %17 = load ptr, ptr %6, align 8
  %18 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %17, i32 0, i32 3
  %19 = load i32, ptr %18, align 4
  %20 = sext i32 %19 to i64
  %21 = load ptr, ptr %3, align 8
  %22 = load ptr, ptr %6, align 8
  %23 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %22, i32 0, i32 2
  %24 = load i32, ptr %23, align 8
  %25 = load ptr, ptr %6, align 8
  %26 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %25, i32 0, i32 1
  %27 = load ptr, ptr %26, align 8
  %28 = call i64 @W_Read(ptr noundef %27, i32 noundef %24, ptr noundef %21, i64 noundef %20)
  %29 = trunc i64 %28 to i32
  store i32 %29, ptr %5, align 4
  %30 = load i32, ptr %5, align 4
  %31 = load ptr, ptr %6, align 8
  %32 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %31, i32 0, i32 3
  %33 = load i32, ptr %32, align 4
  %34 = icmp slt i32 %30, %33
  br i1 %34, label %35, label %41

35:                                               ; preds = %12
  %36 = load i32, ptr %4, align 4
  %37 = load ptr, ptr %6, align 8
  %38 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %37, i32 0, i32 3
  %39 = load i32, ptr %38, align 4
  %40 = load i32, ptr %5, align 4
  call void (ptr, ...) @I_Error(ptr noundef @"??_C@_0CK@HFJKDBJE@W_ReadLump?3?5only?5read?5?$CFi?5of?5?$CFi?5o@", i32 noundef %40, i32 noundef %39, i32 noundef %36)
  br label %41

41:                                               ; preds = %35, %12
  call void @I_EndRead()
  ret void
}

declare dso_local void @I_BeginRead() #2

declare dso_local void @I_EndRead() #2

; Function Attrs: noinline nounwind optnone uwtable
define dso_local ptr @W_CacheLumpNum(i32 noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca ptr, align 8
  %6 = alloca ptr, align 8
  store i32 %1, ptr %3, align 4
  store i32 %0, ptr %4, align 4
  %7 = load i32, ptr %4, align 4
  %8 = load i32, ptr @numlumps, align 4
  %9 = icmp uge i32 %7, %8
  br i1 %9, label %10, label %12

10:                                               ; preds = %2
  %11 = load i32, ptr %4, align 4
  call void (ptr, ...) @I_Error(ptr noundef @"??_C@_0BP@BJDOEDJF@W_CacheLumpNum?3?5?$CFi?5?$DO?$DN?5numlumps?$AA@", i32 noundef %11)
  br label %12

12:                                               ; preds = %10, %2
  %13 = load ptr, ptr @lumpinfo, align 8
  %14 = load i32, ptr %4, align 4
  %15 = sext i32 %14 to i64
  %16 = getelementptr inbounds %struct.lumpinfo_s, ptr %13, i64 %15
  store ptr %16, ptr %6, align 8
  %17 = load ptr, ptr %6, align 8
  %18 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %17, i32 0, i32 1
  %19 = load ptr, ptr %18, align 8
  %20 = getelementptr inbounds nuw %struct._wad_file_s, ptr %19, i32 0, i32 1
  %21 = load ptr, ptr %20, align 8
  %22 = icmp ne ptr %21, null
  br i1 %22, label %23, label %34

23:                                               ; preds = %12
  %24 = load ptr, ptr %6, align 8
  %25 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %24, i32 0, i32 1
  %26 = load ptr, ptr %25, align 8
  %27 = getelementptr inbounds nuw %struct._wad_file_s, ptr %26, i32 0, i32 1
  %28 = load ptr, ptr %27, align 8
  %29 = load ptr, ptr %6, align 8
  %30 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %29, i32 0, i32 2
  %31 = load i32, ptr %30, align 8
  %32 = sext i32 %31 to i64
  %33 = getelementptr inbounds i8, ptr %28, i64 %32
  store ptr %33, ptr %5, align 8
  br label %64

34:                                               ; preds = %12
  %35 = load ptr, ptr %6, align 8
  %36 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %35, i32 0, i32 4
  %37 = load ptr, ptr %36, align 8
  %38 = icmp ne ptr %37, null
  br i1 %38, label %39, label %47

39:                                               ; preds = %34
  %40 = load ptr, ptr %6, align 8
  %41 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %40, i32 0, i32 4
  %42 = load ptr, ptr %41, align 8
  store ptr %42, ptr %5, align 8
  %43 = load i32, ptr %3, align 4
  %44 = load ptr, ptr %6, align 8
  %45 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %44, i32 0, i32 4
  %46 = load ptr, ptr %45, align 8
  call void @Z_ChangeTag2(ptr noundef %46, i32 noundef %43, ptr noundef @"??_C@_0JH@IKPNEAF@E?3?2_00_Michel?2_00_Lab?2_00_GitHub@", i32 noundef 410)
  br label %63

47:                                               ; preds = %34
  %48 = load ptr, ptr %6, align 8
  %49 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %48, i32 0, i32 4
  %50 = load i32, ptr %3, align 4
  %51 = load i32, ptr %4, align 4
  %52 = call i32 @W_LumpLength(i32 noundef %51)
  %53 = call ptr @Z_Malloc(i32 noundef %52, i32 noundef %50, ptr noundef %49)
  %54 = load ptr, ptr %6, align 8
  %55 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %54, i32 0, i32 4
  store ptr %53, ptr %55, align 8
  %56 = load ptr, ptr %6, align 8
  %57 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %56, i32 0, i32 4
  %58 = load ptr, ptr %57, align 8
  %59 = load i32, ptr %4, align 4
  call void @W_ReadLump(i32 noundef %59, ptr noundef %58)
  %60 = load ptr, ptr %6, align 8
  %61 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %60, i32 0, i32 4
  %62 = load ptr, ptr %61, align 8
  store ptr %62, ptr %5, align 8
  br label %63

63:                                               ; preds = %47, %39
  br label %64

64:                                               ; preds = %63, %23
  %65 = load ptr, ptr %5, align 8
  ret ptr %65
}

declare dso_local void @Z_ChangeTag2(ptr noundef, i32 noundef, ptr noundef, i32 noundef) #2

; Function Attrs: noinline nounwind optnone uwtable
define dso_local ptr @W_CacheLumpName(ptr noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca ptr, align 8
  store i32 %1, ptr %3, align 4
  store ptr %0, ptr %4, align 8
  %5 = load i32, ptr %3, align 4
  %6 = load ptr, ptr %4, align 8
  %7 = call i32 @W_GetNumForName(ptr noundef %6)
  %8 = call ptr @W_CacheLumpNum(i32 noundef %7, i32 noundef %5)
  ret ptr %8
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @W_ReleaseLumpNum(i32 noundef %0) #0 {
  %2 = alloca i32, align 4
  %3 = alloca ptr, align 8
  store i32 %0, ptr %2, align 4
  %4 = load i32, ptr %2, align 4
  %5 = load i32, ptr @numlumps, align 4
  %6 = icmp uge i32 %4, %5
  br i1 %6, label %7, label %9

7:                                                ; preds = %1
  %8 = load i32, ptr %2, align 4
  call void (ptr, ...) @I_Error(ptr noundef @"??_C@_0CB@JGMILBJ@W_ReleaseLumpNum?3?5?$CFi?5?$DO?$DN?5numlumps@", i32 noundef %8)
  br label %9

9:                                                ; preds = %7, %1
  %10 = load ptr, ptr @lumpinfo, align 8
  %11 = load i32, ptr %2, align 4
  %12 = sext i32 %11 to i64
  %13 = getelementptr inbounds %struct.lumpinfo_s, ptr %10, i64 %12
  store ptr %13, ptr %3, align 8
  %14 = load ptr, ptr %3, align 8
  %15 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %14, i32 0, i32 1
  %16 = load ptr, ptr %15, align 8
  %17 = getelementptr inbounds nuw %struct._wad_file_s, ptr %16, i32 0, i32 1
  %18 = load ptr, ptr %17, align 8
  %19 = icmp ne ptr %18, null
  br i1 %19, label %20, label %21

20:                                               ; preds = %9
  br label %25

21:                                               ; preds = %9
  %22 = load ptr, ptr %3, align 8
  %23 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %22, i32 0, i32 4
  %24 = load ptr, ptr %23, align 8
  call void @Z_ChangeTag2(ptr noundef %24, i32 noundef 8, ptr noundef @"??_C@_0JH@IKPNEAF@E?3?2_00_Michel?2_00_Lab?2_00_GitHub@", i32 noundef 461)
  br label %25

25:                                               ; preds = %21, %20
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @W_ReleaseLumpName(ptr noundef %0) #0 {
  %2 = alloca ptr, align 8
  store ptr %0, ptr %2, align 8
  %3 = load ptr, ptr %2, align 8
  %4 = call i32 @W_GetNumForName(ptr noundef %3)
  call void @W_ReleaseLumpNum(i32 noundef %4)
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @W_GenerateHashTable() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = load ptr, ptr @lumphash, align 8
  %4 = icmp ne ptr %3, null
  br i1 %4, label %5, label %7

5:                                                ; preds = %0
  %6 = load ptr, ptr @lumphash, align 8
  call void @Z_Free(ptr noundef %6)
  br label %7

7:                                                ; preds = %5, %0
  %8 = load i32, ptr @numlumps, align 4
  %9 = icmp ugt i32 %8, 0
  br i1 %9, label %10, label %56

10:                                               ; preds = %7
  %11 = load i32, ptr @numlumps, align 4
  %12 = zext i32 %11 to i64
  %13 = mul i64 8, %12
  %14 = trunc i64 %13 to i32
  %15 = call ptr @Z_Malloc(i32 noundef %14, i32 noundef 1, ptr noundef null)
  store ptr %15, ptr @lumphash, align 8
  %16 = load ptr, ptr @lumphash, align 8
  %17 = load i32, ptr @numlumps, align 4
  %18 = zext i32 %17 to i64
  %19 = mul i64 8, %18
  call void @llvm.memset.p0.i64(ptr align 8 %16, i8 0, i64 %19, i1 false)
  store i32 0, ptr %1, align 4
  br label %20

20:                                               ; preds = %52, %10
  %21 = load i32, ptr %1, align 4
  %22 = load i32, ptr @numlumps, align 4
  %23 = icmp ult i32 %21, %22
  br i1 %23, label %24, label %55

24:                                               ; preds = %20
  %25 = load ptr, ptr @lumpinfo, align 8
  %26 = load i32, ptr %1, align 4
  %27 = zext i32 %26 to i64
  %28 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %25, i64 %27
  %29 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %28, i32 0, i32 0
  %30 = getelementptr inbounds [8 x i8], ptr %29, i64 0, i64 0
  %31 = call i32 @W_LumpNameHash(ptr noundef %30)
  %32 = load i32, ptr @numlumps, align 4
  %33 = urem i32 %31, %32
  store i32 %33, ptr %2, align 4
  %34 = load ptr, ptr @lumphash, align 8
  %35 = load i32, ptr %2, align 4
  %36 = zext i32 %35 to i64
  %37 = getelementptr inbounds nuw ptr, ptr %34, i64 %36
  %38 = load ptr, ptr %37, align 8
  %39 = load ptr, ptr @lumpinfo, align 8
  %40 = load i32, ptr %1, align 4
  %41 = zext i32 %40 to i64
  %42 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %39, i64 %41
  %43 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %42, i32 0, i32 5
  store ptr %38, ptr %43, align 8
  %44 = load ptr, ptr @lumpinfo, align 8
  %45 = load i32, ptr %1, align 4
  %46 = zext i32 %45 to i64
  %47 = getelementptr inbounds nuw %struct.lumpinfo_s, ptr %44, i64 %46
  %48 = load ptr, ptr @lumphash, align 8
  %49 = load i32, ptr %2, align 4
  %50 = zext i32 %49 to i64
  %51 = getelementptr inbounds nuw ptr, ptr %48, i64 %50
  store ptr %47, ptr %51, align 8
  br label %52

52:                                               ; preds = %24
  %53 = load i32, ptr %1, align 4
  %54 = add i32 %53, 1
  store i32 %54, ptr %1, align 4
  br label %20, !llvm.loop !14

55:                                               ; preds = %20
  br label %56

56:                                               ; preds = %55, %7
  ret void
}

; Function Attrs: nocallback nofree nounwind willreturn memory(argmem: write)
declare void @llvm.memset.p0.i64(ptr writeonly captures(none), i8, i64, i1 immarg) #4

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @W_CheckCorrectIWAD(i32 noundef %0) #0 {
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  store i32 %0, ptr %2, align 4
  store i32 0, ptr %3, align 4
  br label %5

5:                                                ; preds = %43, %1
  %6 = load i32, ptr %3, align 4
  %7 = sext i32 %6 to i64
  %8 = icmp ult i64 %7, 4
  br i1 %8, label %9, label %46

9:                                                ; preds = %5
  %10 = load i32, ptr %2, align 4
  %11 = load i32, ptr %3, align 4
  %12 = sext i32 %11 to i64
  %13 = getelementptr inbounds [4 x %struct.anon], ptr @unique_lumps, i64 0, i64 %12
  %14 = getelementptr inbounds nuw %struct.anon, ptr %13, i32 0, i32 0
  %15 = load i32, ptr %14, align 16
  %16 = icmp ne i32 %10, %15
  br i1 %16, label %17, label %42

17:                                               ; preds = %9
  %18 = load i32, ptr %3, align 4
  %19 = sext i32 %18 to i64
  %20 = getelementptr inbounds [4 x %struct.anon], ptr @unique_lumps, i64 0, i64 %19
  %21 = getelementptr inbounds nuw %struct.anon, ptr %20, i32 0, i32 1
  %22 = load ptr, ptr %21, align 8
  %23 = call i32 @W_CheckNumForName(ptr noundef %22)
  store i32 %23, ptr %4, align 4
  %24 = load i32, ptr %4, align 4
  %25 = icmp sge i32 %24, 0
  br i1 %25, label %26, label %41

26:                                               ; preds = %17
  %27 = load i32, ptr %3, align 4
  %28 = sext i32 %27 to i64
  %29 = getelementptr inbounds [4 x %struct.anon], ptr @unique_lumps, i64 0, i64 %28
  %30 = getelementptr inbounds nuw %struct.anon, ptr %29, i32 0, i32 0
  %31 = load i32, ptr %30, align 16
  %32 = call ptr @D_GameMissionString(i32 noundef %31)
  %33 = load i32, ptr %2, align 4
  %34 = call ptr @D_GameMissionString(i32 noundef %33)
  %35 = load i32, ptr %3, align 4
  %36 = sext i32 %35 to i64
  %37 = getelementptr inbounds [4 x %struct.anon], ptr @unique_lumps, i64 0, i64 %36
  %38 = getelementptr inbounds nuw %struct.anon, ptr %37, i32 0, i32 0
  %39 = load i32, ptr %38, align 16
  %40 = call ptr @D_SuggestGameName(i32 noundef %39, i32 noundef 4)
  call void (ptr, ...) @I_Error(ptr noundef @"??_C@_0IA@JBOBILGP@?6You?5are?5trying?5to?5use?5a?5?$CFs?5IWAD@", ptr noundef %40, ptr noundef @"??_C@_0M@EJPOMJDM@doomgeneric?$AA@", ptr noundef %34, ptr noundef @"??_C@_0M@EJPOMJDM@doomgeneric?$AA@", ptr noundef %32)
  br label %41

41:                                               ; preds = %26, %17
  br label %42

42:                                               ; preds = %41, %9
  br label %43

43:                                               ; preds = %42
  %44 = load i32, ptr %3, align 4
  %45 = add nsw i32 %44, 1
  store i32 %45, ptr %3, align 4
  br label %5, !llvm.loop !15

46:                                               ; preds = %5
  ret void
}

declare dso_local ptr @D_GameMissionString(i32 noundef) #2

declare dso_local ptr @D_SuggestGameName(i32 noundef, i32 noundef) #2

; Function Attrs: nocallback nofree nosync nounwind willreturn
declare void @llvm.va_start.p0(ptr) #5

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
declare void @llvm.va_end.p0(ptr) #5

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

; Function Attrs: allocsize(0,1)
declare dso_local noalias ptr @calloc(i64 noundef, i64 noundef) #6

; Function Attrs: nocallback nofree nounwind willreturn memory(argmem: readwrite)
declare void @llvm.memcpy.p0.p0.i64(ptr noalias writeonly captures(none), ptr noalias readonly captures(none), i64, i1 immarg) #7

declare dso_local void @Z_ChangeUser(ptr noundef, ptr noundef) #2

declare dso_local void @free(ptr noundef) #2

attributes #0 = { noinline nounwind optnone uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nounwind willreturn memory(read) "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #3 = { nounwind "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #4 = { nocallback nofree nounwind willreturn memory(argmem: write) }
attributes #5 = { nocallback nofree nosync nounwind willreturn }
attributes #6 = { allocsize(0,1) "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #7 = { nocallback nofree nounwind willreturn memory(argmem: readwrite) }
attributes #8 = { nounwind willreturn memory(read) }
attributes #9 = { nounwind }
attributes #10 = { allocsize(0,1) }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\Doom-Generic/vm-porting/tests/doom_wad\\src\\w_wad.c", directory: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain")
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
!12 = distinct !{!12, !9}
!13 = distinct !{!13, !9}
!14 = distinct !{!14, !9}
!15 = distinct !{!15, !9}
