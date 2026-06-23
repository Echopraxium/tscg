; ModuleID = 'E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\projects\Doom-Generic/vm-porting/tests/doom_math\src/m_fixed.c'
source_filename = "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\Doom-Generic/vm-porting/tests/doom_math\\src/m_fixed.c"
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
  %8 = call i32 @llvm.abs.i32(i32 %7, i1 true)
  %9 = ashr i32 %8, 14
  %10 = load i32, ptr %4, align 4
  %11 = call i32 @llvm.abs.i32(i32 %10, i1 true)
  %12 = icmp sge i32 %9, %11
  br i1 %12, label %13, label %20

13:                                               ; preds = %2
  %14 = load i32, ptr %5, align 4
  %15 = load i32, ptr %4, align 4
  %16 = xor i32 %14, %15
  %17 = icmp slt i32 %16, 0
  %18 = zext i1 %17 to i64
  %19 = select i1 %17, i32 -2147483648, i32 2147483647
  store i32 %19, ptr %3, align 4
  br label %29

20:                                               ; preds = %2
  %21 = load i32, ptr %5, align 4
  %22 = sext i32 %21 to i64
  %23 = shl i64 %22, 16
  %24 = load i32, ptr %4, align 4
  %25 = sext i32 %24 to i64
  %26 = sdiv i64 %23, %25
  store i64 %26, ptr %6, align 8
  %27 = load i64, ptr %6, align 8
  %28 = trunc i64 %27 to i32
  store i32 %28, ptr %3, align 4
  br label %29

29:                                               ; preds = %20, %13
  %30 = load i32, ptr %3, align 4
  ret i32 %30
}

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare i32 @llvm.abs.i32(i32, i1 immarg) #1

attributes #0 = { noinline nounwind optnone uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nocallback nofree nosync nounwind speculatable willreturn memory(none) }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\Doom-Generic/vm-porting/tests/doom_math\\src\\m_fixed.c", directory: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 1, !"wchar_size", i32 2}
!4 = !{i32 8, !"PIC Level", i32 2}
!5 = !{i32 7, !"uwtable", i32 2}
!6 = !{i32 1, !"MaxTLSAlign", i32 65536}
!7 = !{!"clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)"}
