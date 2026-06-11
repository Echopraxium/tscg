; ModuleID = 'E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\projects\toolchain-tests/c89/test_patterns\src/test_patterns.c'
source_filename = "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\toolchain-tests/c89/test_patterns\\src/test_patterns.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-windows-msvc19.51.36246"

@grid = internal global [4 x [4 x i32]] zeroinitializer, align 16

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @classify(i32 noundef %0) #0 {
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  store i32 %0, ptr %3, align 4
  %4 = load i32, ptr %3, align 4
  switch i32 %4, label %8 [
    i32 0, label %5
    i32 1, label %6
    i32 2, label %7
  ]

5:                                                ; preds = %1
  store i32 10, ptr %2, align 4
  br label %9

6:                                                ; preds = %1
  store i32 20, ptr %2, align 4
  br label %9

7:                                                ; preds = %1
  store i32 30, ptr %2, align 4
  br label %9

8:                                                ; preds = %1
  store i32 99, ptr %2, align 4
  br label %9

9:                                                ; preds = %8, %7, %6, %5
  %10 = load i32, ptr %2, align 4
  ret i32 %10
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @add(i32 noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  store i32 %1, ptr %3, align 4
  store i32 %0, ptr %4, align 4
  %5 = load i32, ptr %4, align 4
  %6 = load i32, ptr %3, align 4
  %7 = add nsw i32 %5, %6
  ret i32 %7
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @mul(i32 noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  store i32 %1, ptr %3, align 4
  store i32 %0, ptr %4, align 4
  %5 = load i32, ptr %4, align 4
  %6 = load i32, ptr %3, align 4
  %7 = mul nsw i32 %5, %6
  ret i32 %7
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @apply(ptr noundef %0, i32 noundef %1, i32 noundef %2) #0 {
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  %6 = alloca ptr, align 8
  store i32 %2, ptr %4, align 4
  store i32 %1, ptr %5, align 4
  store ptr %0, ptr %6, align 8
  %7 = load ptr, ptr %6, align 8
  %8 = load i32, ptr %4, align 4
  %9 = load i32, ptr %5, align 4
  %10 = call i32 %7(i32 noundef %9, i32 noundef %8)
  ret i32 %10
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @fill_grid() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  br label %3

3:                                                ; preds = %25, %0
  %4 = load i32, ptr %1, align 4
  %5 = icmp slt i32 %4, 4
  br i1 %5, label %6, label %28

6:                                                ; preds = %3
  store i32 0, ptr %2, align 4
  br label %7

7:                                                ; preds = %21, %6
  %8 = load i32, ptr %2, align 4
  %9 = icmp slt i32 %8, 4
  br i1 %9, label %10, label %24

10:                                               ; preds = %7
  %11 = load i32, ptr %1, align 4
  %12 = mul nsw i32 %11, 4
  %13 = load i32, ptr %2, align 4
  %14 = add nsw i32 %12, %13
  %15 = load i32, ptr %1, align 4
  %16 = sext i32 %15 to i64
  %17 = getelementptr inbounds [4 x [4 x i32]], ptr @grid, i64 0, i64 %16
  %18 = load i32, ptr %2, align 4
  %19 = sext i32 %18 to i64
  %20 = getelementptr inbounds [4 x i32], ptr %17, i64 0, i64 %19
  store i32 %14, ptr %20, align 4
  br label %21

21:                                               ; preds = %10
  %22 = load i32, ptr %2, align 4
  %23 = add nsw i32 %22, 1
  store i32 %23, ptr %2, align 4
  br label %7, !llvm.loop !8

24:                                               ; preds = %7
  br label %25

25:                                               ; preds = %24
  %26 = load i32, ptr %1, align 4
  %27 = add nsw i32 %26, 1
  store i32 %27, ptr %1, align 4
  br label %3, !llvm.loop !10

28:                                               ; preds = %3
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @sum_grid() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  store i32 0, ptr %3, align 4
  store i32 0, ptr %1, align 4
  br label %4

4:                                                ; preds = %25, %0
  %5 = load i32, ptr %1, align 4
  %6 = icmp slt i32 %5, 4
  br i1 %6, label %7, label %28

7:                                                ; preds = %4
  store i32 0, ptr %2, align 4
  br label %8

8:                                                ; preds = %21, %7
  %9 = load i32, ptr %2, align 4
  %10 = icmp slt i32 %9, 4
  br i1 %10, label %11, label %24

11:                                               ; preds = %8
  %12 = load i32, ptr %1, align 4
  %13 = sext i32 %12 to i64
  %14 = getelementptr inbounds [4 x [4 x i32]], ptr @grid, i64 0, i64 %13
  %15 = load i32, ptr %2, align 4
  %16 = sext i32 %15 to i64
  %17 = getelementptr inbounds [4 x i32], ptr %14, i64 0, i64 %16
  %18 = load i32, ptr %17, align 4
  %19 = load i32, ptr %3, align 4
  %20 = add nsw i32 %19, %18
  store i32 %20, ptr %3, align 4
  br label %21

21:                                               ; preds = %11
  %22 = load i32, ptr %2, align 4
  %23 = add nsw i32 %22, 1
  store i32 %23, ptr %2, align 4
  br label %8, !llvm.loop !11

24:                                               ; preds = %8
  br label %25

25:                                               ; preds = %24
  %26 = load i32, ptr %1, align 4
  %27 = add nsw i32 %26, 1
  store i32 %27, ptr %1, align 4
  br label %4, !llvm.loop !12

28:                                               ; preds = %4
  %29 = load i32, ptr %3, align 4
  ret i32 %29
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @sum_array(ptr noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca ptr, align 8
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  store i32 %1, ptr %3, align 4
  store ptr %0, ptr %4, align 8
  store i32 0, ptr %6, align 4
  store i32 0, ptr %5, align 4
  br label %7

7:                                                ; preds = %19, %2
  %8 = load i32, ptr %5, align 4
  %9 = load i32, ptr %3, align 4
  %10 = icmp slt i32 %8, %9
  br i1 %10, label %11, label %22

11:                                               ; preds = %7
  %12 = load ptr, ptr %4, align 8
  %13 = load i32, ptr %5, align 4
  %14 = sext i32 %13 to i64
  %15 = getelementptr inbounds i32, ptr %12, i64 %14
  %16 = load i32, ptr %15, align 4
  %17 = load i32, ptr %6, align 4
  %18 = add nsw i32 %17, %16
  store i32 %18, ptr %6, align 4
  br label %19

19:                                               ; preds = %11
  %20 = load i32, ptr %5, align 4
  %21 = add nsw i32 %20, 1
  store i32 %21, ptr %5, align 4
  br label %7, !llvm.loop !13

22:                                               ; preds = %7
  %23 = load i32, ptr %6, align 4
  ret i32 %23
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca [5 x i32], align 16
  %4 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  store i32 0, ptr %2, align 4
  %5 = call i32 @classify(i32 noundef 0)
  %6 = icmp eq i32 %5, 10
  br i1 %6, label %7, label %19

7:                                                ; preds = %0
  %8 = call i32 @classify(i32 noundef 1)
  %9 = icmp eq i32 %8, 20
  br i1 %9, label %10, label %19

10:                                               ; preds = %7
  %11 = call i32 @classify(i32 noundef 2)
  %12 = icmp eq i32 %11, 30
  br i1 %12, label %13, label %19

13:                                               ; preds = %10
  %14 = call i32 @classify(i32 noundef 99)
  %15 = icmp eq i32 %14, 99
  br i1 %15, label %16, label %19

16:                                               ; preds = %13
  %17 = load i32, ptr %2, align 4
  %18 = or i32 %17, 1
  store i32 %18, ptr %2, align 4
  br label %19

19:                                               ; preds = %16, %13, %10, %7, %0
  %20 = call i32 @apply(ptr noundef @add, i32 noundef 3, i32 noundef 4)
  %21 = icmp eq i32 %20, 7
  br i1 %21, label %22, label %28

22:                                               ; preds = %19
  %23 = call i32 @apply(ptr noundef @mul, i32 noundef 3, i32 noundef 4)
  %24 = icmp eq i32 %23, 12
  br i1 %24, label %25, label %28

25:                                               ; preds = %22
  %26 = load i32, ptr %2, align 4
  %27 = or i32 %26, 2
  store i32 %27, ptr %2, align 4
  br label %28

28:                                               ; preds = %25, %22, %19
  call void @fill_grid()
  %29 = call i32 @sum_grid()
  %30 = icmp eq i32 %29, 120
  br i1 %30, label %31, label %34

31:                                               ; preds = %28
  %32 = load i32, ptr %2, align 4
  %33 = or i32 %32, 4
  store i32 %33, ptr %2, align 4
  br label %34

34:                                               ; preds = %31, %28
  store i32 0, ptr %4, align 4
  br label %35

35:                                               ; preds = %44, %34
  %36 = load i32, ptr %4, align 4
  %37 = icmp slt i32 %36, 5
  br i1 %37, label %38, label %47

38:                                               ; preds = %35
  %39 = load i32, ptr %4, align 4
  %40 = add nsw i32 %39, 1
  %41 = load i32, ptr %4, align 4
  %42 = sext i32 %41 to i64
  %43 = getelementptr inbounds [5 x i32], ptr %3, i64 0, i64 %42
  store i32 %40, ptr %43, align 4
  br label %44

44:                                               ; preds = %38
  %45 = load i32, ptr %4, align 4
  %46 = add nsw i32 %45, 1
  store i32 %46, ptr %4, align 4
  br label %35, !llvm.loop !14

47:                                               ; preds = %35
  %48 = getelementptr inbounds [5 x i32], ptr %3, i64 0, i64 0
  %49 = call i32 @sum_array(ptr noundef %48, i32 noundef 5)
  %50 = icmp eq i32 %49, 15
  br i1 %50, label %51, label %54

51:                                               ; preds = %47
  %52 = load i32, ptr %2, align 4
  %53 = or i32 %52, 8
  store i32 %53, ptr %2, align 4
  br label %54

54:                                               ; preds = %51, %47
  %55 = load i32, ptr %2, align 4
  ret i32 %55
}

attributes #0 = { noinline nounwind optnone uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\toolchain-tests/c89/test_patterns\\src\\test_patterns.c", directory: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain")
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
