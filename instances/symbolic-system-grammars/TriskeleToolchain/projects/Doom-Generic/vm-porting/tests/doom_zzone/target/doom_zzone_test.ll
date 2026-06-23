; ModuleID = 'E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\projects\Doom-Generic/vm-porting/tests/doom_zzone\src/doom_zzone_test.c'
source_filename = "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\Doom-Generic/vm-porting/tests/doom_zzone\\src/doom_zzone_test.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-windows-msvc19.51.36246"

$sprintf = comdat any

$vsprintf = comdat any

$_snprintf = comdat any

$_vsnprintf = comdat any

$_vsprintf_l = comdat any

$_vsnprintf_l = comdat any

$__local_stdio_printf_options = comdat any

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
  %2 = alloca ptr, align 8
  %3 = alloca ptr, align 8
  %4 = alloca ptr, align 8
  %5 = alloca ptr, align 8
  %6 = alloca ptr, align 8
  %7 = alloca ptr, align 8
  %8 = alloca i32, align 4
  %9 = alloca i32, align 4
  %10 = alloca i32, align 4
  %11 = alloca i32, align 4
  %12 = alloca [8 x ptr], align 16
  %13 = alloca ptr, align 8
  %14 = alloca ptr, align 8
  %15 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  store ptr %6, ptr %7, align 8
  store i32 0, ptr %10, align 4
  call void @Z_Init()
  %16 = call ptr @Z_Malloc(i32 noundef 256, i32 noundef 1, ptr noundef null)
  store ptr %16, ptr %2, align 8
  %17 = load ptr, ptr %2, align 8
  %18 = icmp ne ptr %17, null
  br i1 %18, label %19, label %22

19:                                               ; preds = %0
  %20 = load i32, ptr %10, align 4
  %21 = or i32 %20, 1
  store i32 %21, ptr %10, align 4
  br label %22

22:                                               ; preds = %19, %0
  %23 = call ptr @Z_Malloc(i32 noundef 256, i32 noundef 1, ptr noundef null)
  store ptr %23, ptr %3, align 8
  %24 = load ptr, ptr %2, align 8
  call void @Z_Free(ptr noundef %24)
  call void @Z_CheckHeap()
  %25 = load i32, ptr %10, align 4
  %26 = or i32 %25, 2
  store i32 %26, ptr %10, align 4
  store ptr null, ptr %6, align 8
  %27 = load ptr, ptr %7, align 8
  %28 = call ptr @Z_Malloc(i32 noundef 128, i32 noundef 1, ptr noundef %27)
  store ptr %28, ptr %4, align 8
  %29 = load ptr, ptr %6, align 8
  %30 = load ptr, ptr %4, align 8
  %31 = icmp eq ptr %29, %30
  br i1 %31, label %32, label %35

32:                                               ; preds = %22
  %33 = load i32, ptr %10, align 4
  %34 = or i32 %33, 4
  store i32 %34, ptr %10, align 4
  br label %35

35:                                               ; preds = %32, %22
  %36 = call ptr @Z_Malloc(i32 noundef 128, i32 noundef 5, ptr noundef null)
  store ptr %36, ptr %5, align 8
  %37 = load ptr, ptr %5, align 8
  %38 = load ptr, ptr %4, align 8
  %39 = icmp ne ptr %37, %38
  br i1 %39, label %40, label %46

40:                                               ; preds = %35
  %41 = load ptr, ptr %5, align 8
  %42 = icmp ne ptr %41, null
  br i1 %42, label %43, label %46

43:                                               ; preds = %40
  %44 = load i32, ptr %10, align 4
  %45 = or i32 %44, 8
  store i32 %45, ptr %10, align 4
  br label %46

46:                                               ; preds = %43, %40, %35
  %47 = call i32 @Z_FreeMemory()
  store i32 %47, ptr %8, align 4
  call void @Z_FreeTags(i32 noundef 5, i32 noundef 8)
  %48 = call i32 @Z_FreeMemory()
  store i32 %48, ptr %9, align 4
  %49 = load i32, ptr %9, align 4
  %50 = load i32, ptr %8, align 4
  %51 = icmp sgt i32 %49, %50
  br i1 %51, label %52, label %55

52:                                               ; preds = %46
  %53 = load i32, ptr %10, align 4
  %54 = or i32 %53, 16
  store i32 %54, ptr %10, align 4
  br label %55

55:                                               ; preds = %52, %46
  %56 = call i32 @Z_FreeMemory()
  store i32 %56, ptr %8, align 4
  %57 = load ptr, ptr %4, align 8
  call void @Z_Free(ptr noundef %57)
  %58 = call i32 @Z_FreeMemory()
  store i32 %58, ptr %9, align 4
  %59 = load i32, ptr %9, align 4
  %60 = load i32, ptr %8, align 4
  %61 = icmp sgt i32 %59, %60
  br i1 %61, label %62, label %65

62:                                               ; preds = %55
  %63 = load i32, ptr %10, align 4
  %64 = or i32 %63, 32
  store i32 %64, ptr %10, align 4
  br label %65

65:                                               ; preds = %62, %55
  store i32 0, ptr %11, align 4
  br label %66

66:                                               ; preds = %74, %65
  %67 = load i32, ptr %11, align 4
  %68 = icmp slt i32 %67, 8
  br i1 %68, label %69, label %77

69:                                               ; preds = %66
  %70 = call ptr @Z_Malloc(i32 noundef 64, i32 noundef 1, ptr noundef null)
  %71 = load i32, ptr %11, align 4
  %72 = sext i32 %71 to i64
  %73 = getelementptr inbounds [8 x ptr], ptr %12, i64 0, i64 %72
  store ptr %70, ptr %73, align 8
  br label %74

74:                                               ; preds = %69
  %75 = load i32, ptr %11, align 4
  %76 = add nsw i32 %75, 1
  store i32 %76, ptr %11, align 4
  br label %66, !llvm.loop !8

77:                                               ; preds = %66
  store i32 0, ptr %11, align 4
  br label %78

78:                                               ; preds = %86, %77
  %79 = load i32, ptr %11, align 4
  %80 = icmp slt i32 %79, 4
  br i1 %80, label %81, label %89

81:                                               ; preds = %78
  %82 = load i32, ptr %11, align 4
  %83 = sext i32 %82 to i64
  %84 = getelementptr inbounds [8 x ptr], ptr %12, i64 0, i64 %83
  %85 = load ptr, ptr %84, align 8
  call void @Z_Free(ptr noundef %85)
  br label %86

86:                                               ; preds = %81
  %87 = load i32, ptr %11, align 4
  %88 = add nsw i32 %87, 1
  store i32 %88, ptr %11, align 4
  br label %78, !llvm.loop !10

89:                                               ; preds = %78
  call void @Z_CheckHeap()
  %90 = load i32, ptr %10, align 4
  %91 = or i32 %90, 64
  store i32 %91, ptr %10, align 4
  store i32 4, ptr %11, align 4
  br label %92

92:                                               ; preds = %100, %89
  %93 = load i32, ptr %11, align 4
  %94 = icmp slt i32 %93, 8
  br i1 %94, label %95, label %103

95:                                               ; preds = %92
  %96 = load i32, ptr %11, align 4
  %97 = sext i32 %96 to i64
  %98 = getelementptr inbounds [8 x ptr], ptr %12, i64 0, i64 %97
  %99 = load ptr, ptr %98, align 8
  call void @Z_Free(ptr noundef %99)
  br label %100

100:                                              ; preds = %95
  %101 = load i32, ptr %11, align 4
  %102 = add nsw i32 %101, 1
  store i32 %102, ptr %11, align 4
  br label %92, !llvm.loop !11

103:                                              ; preds = %92
  %104 = call ptr @Z_Malloc(i32 noundef 512, i32 noundef 1, ptr noundef null)
  store ptr %104, ptr %13, align 8
  %105 = load ptr, ptr %13, align 8
  call void @Z_Free(ptr noundef %105)
  %106 = call ptr @Z_Malloc(i32 noundef 512, i32 noundef 1, ptr noundef null)
  store ptr %106, ptr %14, align 8
  %107 = load ptr, ptr %14, align 8
  %108 = icmp ne ptr %107, null
  br i1 %108, label %109, label %128

109:                                              ; preds = %103
  %110 = load ptr, ptr %14, align 8
  %111 = load ptr, ptr %13, align 8
  %112 = ptrtoint ptr %110 to i64
  %113 = ptrtoint ptr %111 to i64
  %114 = sub i64 %112, %113
  %115 = trunc i64 %114 to i32
  store i32 %115, ptr %15, align 4
  %116 = load i32, ptr %15, align 4
  %117 = icmp slt i32 %116, 0
  br i1 %117, label %118, label %121

118:                                              ; preds = %109
  %119 = load i32, ptr %15, align 4
  %120 = sub nsw i32 0, %119
  store i32 %120, ptr %15, align 4
  br label %121

121:                                              ; preds = %118, %109
  %122 = load i32, ptr %15, align 4
  %123 = icmp slt i32 %122, 1024
  br i1 %123, label %124, label %127

124:                                              ; preds = %121
  %125 = load i32, ptr %10, align 4
  %126 = or i32 %125, 128
  store i32 %126, ptr %10, align 4
  br label %127

127:                                              ; preds = %124, %121
  br label %128

128:                                              ; preds = %127, %103
  %129 = load ptr, ptr %14, align 8
  %130 = icmp ne ptr %129, null
  br i1 %130, label %131, label %133

131:                                              ; preds = %128
  %132 = load ptr, ptr %14, align 8
  call void @Z_Free(ptr noundef %132)
  br label %133

133:                                              ; preds = %131, %128
  call void @Z_CheckHeap()
  %134 = load i32, ptr %10, align 4
  ret i32 %134
}

declare dso_local void @Z_Init() #1

declare dso_local ptr @Z_Malloc(i32 noundef, i32 noundef, ptr noundef) #1

declare dso_local void @Z_Free(ptr noundef) #1

declare dso_local void @Z_CheckHeap() #1

declare dso_local i32 @Z_FreeMemory() #1

declare dso_local void @Z_FreeTags(i32 noundef, i32 noundef) #1

; Function Attrs: nocallback nofree nosync nounwind willreturn
declare void @llvm.va_start.p0(ptr) #2

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
declare void @llvm.va_end.p0(ptr) #2

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

attributes #0 = { noinline nounwind optnone uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { nocallback nofree nosync nounwind willreturn }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\Doom-Generic/vm-porting/tests/doom_zzone\\src\\doom_zzone_test.c", directory: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain")
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
