; ModuleID = 'E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\projects\Doom-Generic/vm-porting/tests/doom_fixed\src/m_fixed.c'
source_filename = "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\Doom-Generic/vm-porting/tests/doom_fixed\\src/m_fixed.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-windows-msvc19.51.36246"

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @FixedMul(i32 noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  store i32 %1, ptr %3, align 4
  store i32 %0, ptr %4, align 4
  %5 = load i32, ptr %4, align 4
  %6 = sext i32 %5 to i64
  %7 = load i32, ptr %3, align 4
  %8 = sext i32 %7 to i64
  %9 = mul nsw i64 %6, %8
  %10 = ashr i64 %9, 16
  %11 = trunc i64 %10 to i32
  ret i32 %11
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @FixedDiv(i32 noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  %6 = alloca i64, align 8
  store i32 %1, ptr %4, align 4
  store i32 %0, ptr %5, align 4
  %7 = load i32, ptr %5, align 4
  %8 = icmp slt i32 %7, 0
  br i1 %8, label %9, label %12

9:                                                ; preds = %2
  %10 = load i32, ptr %5, align 4
  %11 = sub nsw i32 0, %10
  br label %14

12:                                               ; preds = %2
  %13 = load i32, ptr %5, align 4
  br label %14

14:                                               ; preds = %12, %9
  %15 = phi i32 [ %11, %9 ], [ %13, %12 ]
  %16 = ashr i32 %15, 14
  %17 = load i32, ptr %4, align 4
  %18 = icmp slt i32 %17, 0
  br i1 %18, label %19, label %22

19:                                               ; preds = %14
  %20 = load i32, ptr %4, align 4
  %21 = sub nsw i32 0, %20
  br label %24

22:                                               ; preds = %14
  %23 = load i32, ptr %4, align 4
  br label %24

24:                                               ; preds = %22, %19
  %25 = phi i32 [ %21, %19 ], [ %23, %22 ]
  %26 = icmp sge i32 %16, %25
  br i1 %26, label %27, label %34

27:                                               ; preds = %24
  %28 = load i32, ptr %5, align 4
  %29 = load i32, ptr %4, align 4
  %30 = xor i32 %28, %29
  %31 = icmp slt i32 %30, 0
  %32 = zext i1 %31 to i64
  %33 = select i1 %31, i32 -2147483648, i32 2147483647
  store i32 %33, ptr %3, align 4
  br label %43

34:                                               ; preds = %24
  %35 = load i32, ptr %5, align 4
  %36 = sext i32 %35 to i64
  %37 = shl i64 %36, 16
  %38 = load i32, ptr %4, align 4
  %39 = sext i32 %38 to i64
  %40 = sdiv i64 %37, %39
  store i64 %40, ptr %6, align 8
  %41 = load i64, ptr %6, align 8
  %42 = trunc i64 %41 to i32
  store i32 %42, ptr %3, align 4
  br label %43

43:                                               ; preds = %34, %27
  %44 = load i32, ptr %3, align 4
  ret i32 %44
}

attributes #0 = { noinline nounwind optnone uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\Doom-Generic/vm-porting/tests/doom_fixed\\src\\m_fixed.c", directory: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 1, !"wchar_size", i32 2}
!4 = !{i32 8, !"PIC Level", i32 2}
!5 = !{i32 7, !"uwtable", i32 2}
!6 = !{i32 1, !"MaxTLSAlign", i32 65536}
!7 = !{!"clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)"}
