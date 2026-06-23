; ModuleID = 'E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\projects\Doom-Generic/vm-porting/tests/doom_fixed\src/doom_fixed_test.c'
source_filename = "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\Doom-Generic/vm-porting/tests/doom_fixed\\src/doom_fixed_test.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-windows-msvc19.51.36246"

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  %9 = alloca i32, align 4
  %10 = alloca i32, align 4
  %11 = alloca i32, align 4
  %12 = alloca i32, align 4
  %13 = alloca i32, align 4
  %14 = alloca i32, align 4
  %15 = alloca i32, align 4
  %16 = alloca i32, align 4
  %17 = alloca i32, align 4
  %18 = alloca i32, align 4
  %19 = alloca i32, align 4
  %20 = alloca i32, align 4
  %21 = alloca i32, align 4
  %22 = alloca i32, align 4
  %23 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  store i32 0, ptr %2, align 4
  store i32 65536, ptr %3, align 4
  store i32 131072, ptr %4, align 4
  %24 = load i32, ptr %4, align 4
  %25 = load i32, ptr %3, align 4
  %26 = call i32 @FixedMul(i32 noundef %25, i32 noundef %24)
  store i32 %26, ptr %5, align 4
  %27 = load i32, ptr %5, align 4
  %28 = icmp eq i32 %27, 131072
  br i1 %28, label %29, label %32

29:                                               ; preds = %0
  %30 = load i32, ptr %2, align 4
  %31 = or i32 %30, 1
  store i32 %31, ptr %2, align 4
  br label %32

32:                                               ; preds = %29, %0
  store i32 -65536, ptr %6, align 4
  store i32 196608, ptr %7, align 4
  %33 = load i32, ptr %7, align 4
  %34 = load i32, ptr %6, align 4
  %35 = call i32 @FixedMul(i32 noundef %34, i32 noundef %33)
  store i32 %35, ptr %8, align 4
  %36 = load i32, ptr %8, align 4
  %37 = icmp eq i32 %36, -196608
  br i1 %37, label %38, label %41

38:                                               ; preds = %32
  %39 = load i32, ptr %2, align 4
  %40 = or i32 %39, 2
  store i32 %40, ptr %2, align 4
  br label %41

41:                                               ; preds = %38, %32
  store i32 0, ptr %9, align 4
  store i32 65536, ptr %10, align 4
  %42 = load i32, ptr %10, align 4
  %43 = load i32, ptr %9, align 4
  %44 = call i32 @FixedMul(i32 noundef %43, i32 noundef %42)
  store i32 %44, ptr %11, align 4
  %45 = load i32, ptr %11, align 4
  %46 = icmp eq i32 %45, 0
  br i1 %46, label %47, label %50

47:                                               ; preds = %41
  %48 = load i32, ptr %2, align 4
  %49 = or i32 %48, 4
  store i32 %49, ptr %2, align 4
  br label %50

50:                                               ; preds = %47, %41
  store i32 131072, ptr %12, align 4
  store i32 65536, ptr %13, align 4
  %51 = load i32, ptr %13, align 4
  %52 = load i32, ptr %12, align 4
  %53 = call i32 @FixedDiv(i32 noundef %52, i32 noundef %51)
  store i32 %53, ptr %14, align 4
  %54 = load i32, ptr %14, align 4
  %55 = icmp eq i32 %54, 131072
  br i1 %55, label %56, label %59

56:                                               ; preds = %50
  %57 = load i32, ptr %2, align 4
  %58 = or i32 %57, 8
  store i32 %58, ptr %2, align 4
  br label %59

59:                                               ; preds = %56, %50
  store i32 -131072, ptr %15, align 4
  store i32 65536, ptr %16, align 4
  %60 = load i32, ptr %16, align 4
  %61 = load i32, ptr %15, align 4
  %62 = call i32 @FixedDiv(i32 noundef %61, i32 noundef %60)
  store i32 %62, ptr %17, align 4
  %63 = load i32, ptr %17, align 4
  %64 = icmp eq i32 %63, -131072
  br i1 %64, label %65, label %68

65:                                               ; preds = %59
  %66 = load i32, ptr %2, align 4
  %67 = or i32 %66, 16
  store i32 %67, ptr %2, align 4
  br label %68

68:                                               ; preds = %65, %59
  store i32 196608, ptr %18, align 4
  store i32 1, ptr %19, align 4
  %69 = load i32, ptr %19, align 4
  %70 = load i32, ptr %18, align 4
  %71 = call i32 @FixedDiv(i32 noundef %70, i32 noundef %69)
  store i32 %71, ptr %20, align 4
  %72 = load i32, ptr %20, align 4
  %73 = icmp sgt i32 %72, 0
  br i1 %73, label %74, label %77

74:                                               ; preds = %68
  %75 = load i32, ptr %2, align 4
  %76 = or i32 %75, 32
  store i32 %76, ptr %2, align 4
  br label %77

77:                                               ; preds = %74, %68
  store i32 196608, ptr %21, align 4
  store i32 -1, ptr %22, align 4
  %78 = load i32, ptr %22, align 4
  %79 = load i32, ptr %21, align 4
  %80 = call i32 @FixedDiv(i32 noundef %79, i32 noundef %78)
  store i32 %80, ptr %23, align 4
  %81 = load i32, ptr %23, align 4
  %82 = icmp slt i32 %81, 0
  br i1 %82, label %83, label %86

83:                                               ; preds = %77
  %84 = load i32, ptr %2, align 4
  %85 = or i32 %84, 64
  store i32 %85, ptr %2, align 4
  br label %86

86:                                               ; preds = %83, %77
  %87 = load i32, ptr %2, align 4
  ret i32 %87
}

declare dso_local i32 @FixedMul(i32 noundef, i32 noundef) #1

declare dso_local i32 @FixedDiv(i32 noundef, i32 noundef) #1

attributes #0 = { noinline nounwind optnone uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\Doom-Generic/vm-porting/tests/doom_fixed\\src\\doom_fixed_test.c", directory: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 1, !"wchar_size", i32 2}
!4 = !{i32 8, !"PIC Level", i32 2}
!5 = !{i32 7, !"uwtable", i32 2}
!6 = !{i32 1, !"MaxTLSAlign", i32 65536}
!7 = !{!"clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)"}
