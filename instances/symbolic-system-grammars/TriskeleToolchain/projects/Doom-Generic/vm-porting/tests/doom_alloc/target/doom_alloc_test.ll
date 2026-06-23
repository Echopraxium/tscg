; ModuleID = 'E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\projects\Doom-Generic/vm-porting/tests/doom_alloc\src/doom_alloc_test.c'
source_filename = "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\Doom-Generic/vm-porting/tests/doom_alloc\\src/doom_alloc_test.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-windows-msvc19.51.36246"

@heap_buf = internal global [4096 x i8] zeroinitializer, align 16

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca ptr, align 8
  %4 = alloca ptr, align 8
  %5 = alloca ptr, align 8
  %6 = alloca ptr, align 8
  %7 = alloca ptr, align 8
  %8 = alloca i32, align 4
  %9 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  store i32 0, ptr %2, align 4
  call void @Z_Init(ptr noundef @heap_buf, i32 noundef 4096)
  %10 = call ptr @Z_Malloc(i32 noundef 64, i32 noundef 1, ptr noundef null)
  store ptr %10, ptr %3, align 8
  %11 = load ptr, ptr %3, align 8
  %12 = icmp ne ptr %11, null
  br i1 %12, label %13, label %16

13:                                               ; preds = %0
  %14 = load i32, ptr %2, align 4
  %15 = or i32 %14, 1
  store i32 %15, ptr %2, align 4
  br label %16

16:                                               ; preds = %13, %0
  store ptr inttoptr (i64 1 to ptr), ptr %6, align 8
  %17 = call ptr @Z_Malloc(i32 noundef 32, i32 noundef 1, ptr noundef %6)
  store ptr %17, ptr %4, align 8
  %18 = load ptr, ptr %4, align 8
  call void @Z_Free(ptr noundef %18)
  %19 = load ptr, ptr %6, align 8
  %20 = icmp eq ptr %19, null
  br i1 %20, label %21, label %24

21:                                               ; preds = %16
  %22 = load i32, ptr %2, align 4
  %23 = or i32 %22, 2
  store i32 %23, ptr %2, align 4
  br label %24

24:                                               ; preds = %21, %16
  store ptr null, ptr %7, align 8
  %25 = call ptr @Z_Malloc(i32 noundef 16, i32 noundef 1, ptr noundef %7)
  store ptr %25, ptr %5, align 8
  %26 = load ptr, ptr %7, align 8
  %27 = load ptr, ptr %5, align 8
  %28 = icmp eq ptr %26, %27
  br i1 %28, label %29, label %35

29:                                               ; preds = %24
  %30 = load ptr, ptr %5, align 8
  %31 = icmp ne ptr %30, null
  br i1 %31, label %32, label %35

32:                                               ; preds = %29
  %33 = load i32, ptr %2, align 4
  %34 = or i32 %33, 4
  store i32 %34, ptr %2, align 4
  br label %35

35:                                               ; preds = %32, %29, %24
  %36 = load ptr, ptr %5, align 8
  call void @Z_Free(ptr noundef %36)
  call void @Z_Init(ptr noundef @heap_buf, i32 noundef 4096)
  %37 = call ptr @Z_Malloc(i32 noundef 64, i32 noundef 1, ptr noundef null)
  store ptr %37, ptr %3, align 8
  %38 = call ptr @Z_Malloc(i32 noundef 128, i32 noundef 1, ptr noundef null)
  store ptr %38, ptr %4, align 8
  %39 = load ptr, ptr %3, align 8
  %40 = icmp ne ptr %39, null
  br i1 %40, label %41, label %51

41:                                               ; preds = %35
  %42 = load ptr, ptr %4, align 8
  %43 = icmp ne ptr %42, null
  br i1 %43, label %44, label %51

44:                                               ; preds = %41
  %45 = load ptr, ptr %4, align 8
  %46 = load ptr, ptr %3, align 8
  %47 = icmp ugt ptr %45, %46
  br i1 %47, label %48, label %51

48:                                               ; preds = %44
  %49 = load i32, ptr %2, align 4
  %50 = or i32 %49, 8
  store i32 %50, ptr %2, align 4
  br label %51

51:                                               ; preds = %48, %44, %41, %35
  call void @Z_Init(ptr noundef @heap_buf, i32 noundef 4096)
  %52 = call ptr @Z_Malloc(i32 noundef 64, i32 noundef 1, ptr noundef null)
  store ptr %52, ptr %3, align 8
  %53 = call ptr @Z_Malloc(i32 noundef 128, i32 noundef 1, ptr noundef null)
  store ptr %53, ptr %4, align 8
  %54 = load ptr, ptr %3, align 8
  call void @Z_Free(ptr noundef %54)
  %55 = call i32 @Z_FreeMemory()
  store i32 %55, ptr %8, align 4
  %56 = load ptr, ptr %4, align 8
  call void @Z_Free(ptr noundef %56)
  %57 = call i32 @Z_FreeMemory()
  store i32 %57, ptr %9, align 4
  %58 = load i32, ptr %9, align 4
  %59 = load i32, ptr %8, align 4
  %60 = icmp sgt i32 %58, %59
  br i1 %60, label %61, label %64

61:                                               ; preds = %51
  %62 = load i32, ptr %2, align 4
  %63 = or i32 %62, 16
  store i32 %63, ptr %2, align 4
  br label %64

64:                                               ; preds = %61, %51
  call void @Z_Init(ptr noundef @heap_buf, i32 noundef 4096)
  %65 = call ptr @Z_Malloc(i32 noundef 64, i32 noundef 1, ptr noundef null)
  store ptr %65, ptr %3, align 8
  %66 = call ptr @Z_Malloc(i32 noundef 64, i32 noundef 1, ptr noundef null)
  store ptr %66, ptr %4, align 8
  %67 = call ptr @Z_Malloc(i32 noundef 64, i32 noundef 1, ptr noundef null)
  store ptr %67, ptr %5, align 8
  %68 = load ptr, ptr %5, align 8
  call void @Z_Free(ptr noundef %68)
  %69 = call i32 @Z_FreeMemory()
  store i32 %69, ptr %8, align 4
  %70 = load ptr, ptr %4, align 8
  call void @Z_Free(ptr noundef %70)
  %71 = call i32 @Z_FreeMemory()
  store i32 %71, ptr %9, align 4
  %72 = load i32, ptr %9, align 4
  %73 = load i32, ptr %8, align 4
  %74 = icmp sgt i32 %72, %73
  br i1 %74, label %75, label %78

75:                                               ; preds = %64
  %76 = load i32, ptr %2, align 4
  %77 = or i32 %76, 32
  store i32 %77, ptr %2, align 4
  br label %78

78:                                               ; preds = %75, %64
  %79 = load ptr, ptr %3, align 8
  call void @Z_Free(ptr noundef %79)
  call void @Z_Init(ptr noundef @heap_buf, i32 noundef 4096)
  %80 = call ptr @Z_Malloc(i32 noundef 128, i32 noundef 1, ptr noundef null)
  store ptr %80, ptr %3, align 8
  %81 = call i32 @Z_FreeMemory()
  store i32 %81, ptr %9, align 4
  %82 = load i32, ptr %9, align 4
  %83 = icmp sgt i32 %82, 0
  br i1 %83, label %84, label %90

84:                                               ; preds = %78
  %85 = load i32, ptr %9, align 4
  %86 = icmp slt i32 %85, 4096
  br i1 %86, label %87, label %90

87:                                               ; preds = %84
  %88 = load i32, ptr %2, align 4
  %89 = or i32 %88, 64
  store i32 %89, ptr %2, align 4
  br label %90

90:                                               ; preds = %87, %84, %78
  %91 = load ptr, ptr %3, align 8
  call void @Z_Free(ptr noundef %91)
  call void @Z_Init(ptr noundef @heap_buf, i32 noundef 4096)
  %92 = call ptr @Z_Malloc(i32 noundef 64, i32 noundef 1, ptr noundef null)
  store ptr %92, ptr %3, align 8
  %93 = load ptr, ptr %3, align 8
  call void @Z_Free(ptr noundef %93)
  %94 = call ptr @Z_Malloc(i32 noundef 64, i32 noundef 1, ptr noundef null)
  store ptr %94, ptr %4, align 8
  %95 = load ptr, ptr %4, align 8
  %96 = load ptr, ptr %3, align 8
  %97 = icmp eq ptr %95, %96
  br i1 %97, label %98, label %101

98:                                               ; preds = %90
  %99 = load i32, ptr %2, align 4
  %100 = or i32 %99, 128
  store i32 %100, ptr %2, align 4
  br label %101

101:                                              ; preds = %98, %90
  %102 = load i32, ptr %2, align 4
  ret i32 %102
}

declare dso_local void @Z_Init(ptr noundef, i32 noundef) #1

declare dso_local ptr @Z_Malloc(i32 noundef, i32 noundef, ptr noundef) #1

declare dso_local void @Z_Free(ptr noundef) #1

declare dso_local i32 @Z_FreeMemory() #1

attributes #0 = { noinline nounwind optnone uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\Doom-Generic/vm-porting/tests/doom_alloc\\src\\doom_alloc_test.c", directory: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 1, !"wchar_size", i32 2}
!4 = !{i32 8, !"PIC Level", i32 2}
!5 = !{i32 7, !"uwtable", i32 2}
!6 = !{i32 1, !"MaxTLSAlign", i32 65536}
!7 = !{!"clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)"}
