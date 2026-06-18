; ModuleID = 'E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\projects\toolchain-tests/c89/test_main\test_main.c'
source_filename = "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\toolchain-tests/c89/test_main\\test_main.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-windows-msvc19.51.36246"

@tilemap = dso_local global [4096 x i8] zeroinitializer, align 16

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @ScaleDiv(i32 noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  store i32 %1, ptr %4, align 4
  store i32 %0, ptr %5, align 4
  %6 = load i32, ptr %4, align 4
  %7 = icmp eq i32 %6, 0
  br i1 %7, label %8, label %9

8:                                                ; preds = %2
  store i32 0, ptr %3, align 4
  br label %13

9:                                                ; preds = %2
  %10 = load i32, ptr %5, align 4
  %11 = load i32, ptr %4, align 4
  %12 = sdiv i32 %10, %11
  store i32 %12, ptr %3, align 4
  br label %13

13:                                               ; preds = %9, %8
  %14 = load i32, ptr %3, align 4
  ret i32 %14
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @IsSolid(i32 noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  store i32 %1, ptr %4, align 4
  store i32 %0, ptr %5, align 4
  %6 = load i32, ptr %5, align 4
  %7 = icmp slt i32 %6, 0
  br i1 %7, label %17, label %8

8:                                                ; preds = %2
  %9 = load i32, ptr %5, align 4
  %10 = icmp sge i32 %9, 64
  br i1 %10, label %17, label %11

11:                                               ; preds = %8
  %12 = load i32, ptr %4, align 4
  %13 = icmp slt i32 %12, 0
  br i1 %13, label %17, label %14

14:                                               ; preds = %11
  %15 = load i32, ptr %4, align 4
  %16 = icmp sge i32 %15, 64
  br i1 %16, label %17, label %18

17:                                               ; preds = %14, %11, %8, %2
  store i32 1, ptr %3, align 4
  br label %29

18:                                               ; preds = %14
  %19 = load i32, ptr %4, align 4
  %20 = mul nsw i32 %19, 64
  %21 = load i32, ptr %5, align 4
  %22 = add nsw i32 %20, %21
  %23 = sext i32 %22 to i64
  %24 = getelementptr inbounds [4096 x i8], ptr @tilemap, i64 0, i64 %23
  %25 = load i8, ptr %24, align 1
  %26 = zext i8 %25 to i32
  %27 = icmp ne i32 %26, 0
  %28 = zext i1 %27 to i32
  store i32 %28, ptr %3, align 4
  br label %29

29:                                               ; preds = %18, %17
  %30 = load i32, ptr %3, align 4
  ret i32 %30
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @SumTiles(i32 noundef %0, i32 noundef %1, i32 noundef %2, i32 noundef %3) #0 {
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  %9 = alloca i32, align 4
  %10 = alloca i32, align 4
  %11 = alloca i32, align 4
  store i32 %3, ptr %5, align 4
  store i32 %2, ptr %6, align 4
  store i32 %1, ptr %7, align 4
  store i32 %0, ptr %8, align 4
  store i32 0, ptr %9, align 4
  %12 = load i32, ptr %7, align 4
  store i32 %12, ptr %11, align 4
  br label %13

13:                                               ; preds = %42, %4
  %14 = load i32, ptr %11, align 4
  %15 = load i32, ptr %7, align 4
  %16 = load i32, ptr %5, align 4
  %17 = add nsw i32 %15, %16
  %18 = icmp slt i32 %14, %17
  br i1 %18, label %19, label %45

19:                                               ; preds = %13
  %20 = load i32, ptr %8, align 4
  store i32 %20, ptr %10, align 4
  br label %21

21:                                               ; preds = %38, %19
  %22 = load i32, ptr %10, align 4
  %23 = load i32, ptr %8, align 4
  %24 = load i32, ptr %6, align 4
  %25 = add nsw i32 %23, %24
  %26 = icmp slt i32 %22, %25
  br i1 %26, label %27, label %41

27:                                               ; preds = %21
  %28 = load i32, ptr %11, align 4
  %29 = mul nsw i32 %28, 64
  %30 = load i32, ptr %10, align 4
  %31 = add nsw i32 %29, %30
  %32 = sext i32 %31 to i64
  %33 = getelementptr inbounds [4096 x i8], ptr @tilemap, i64 0, i64 %32
  %34 = load i8, ptr %33, align 1
  %35 = zext i8 %34 to i32
  %36 = load i32, ptr %9, align 4
  %37 = add nsw i32 %36, %35
  store i32 %37, ptr %9, align 4
  br label %38

38:                                               ; preds = %27
  %39 = load i32, ptr %10, align 4
  %40 = add nsw i32 %39, 1
  store i32 %40, ptr %10, align 4
  br label %21, !llvm.loop !8

41:                                               ; preds = %21
  br label %42

42:                                               ; preds = %41
  %43 = load i32, ptr %11, align 4
  %44 = add nsw i32 %43, 1
  store i32 %44, ptr %11, align 4
  br label %13, !llvm.loop !10

45:                                               ; preds = %13
  %46 = load i32, ptr %9, align 4
  ret i32 %46
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  store i32 0, ptr %2, align 4
  %3 = call i32 @ScaleDiv(i32 noundef 10, i32 noundef 2)
  %4 = icmp eq i32 %3, 5
  br i1 %4, label %5, label %8

5:                                                ; preds = %0
  %6 = load i32, ptr %2, align 4
  %7 = or i32 %6, 1
  store i32 %7, ptr %2, align 4
  br label %8

8:                                                ; preds = %5, %0
  %9 = call i32 @ScaleDiv(i32 noundef 7, i32 noundef 0)
  %10 = icmp eq i32 %9, 0
  br i1 %10, label %11, label %14

11:                                               ; preds = %8
  %12 = load i32, ptr %2, align 4
  %13 = or i32 %12, 2
  store i32 %13, ptr %2, align 4
  br label %14

14:                                               ; preds = %11, %8
  store i8 9, ptr getelementptr inbounds ([4096 x i8], ptr @tilemap, i64 0, i64 323), align 1
  %15 = call i32 @IsSolid(i32 noundef 3, i32 noundef 5)
  %16 = icmp eq i32 %15, 1
  br i1 %16, label %17, label %20

17:                                               ; preds = %14
  %18 = load i32, ptr %2, align 4
  %19 = or i32 %18, 4
  store i32 %19, ptr %2, align 4
  br label %20

20:                                               ; preds = %17, %14
  %21 = call i32 @IsSolid(i32 noundef 0, i32 noundef 0)
  %22 = icmp eq i32 %21, 0
  br i1 %22, label %23, label %26

23:                                               ; preds = %20
  %24 = load i32, ptr %2, align 4
  %25 = or i32 %24, 8
  store i32 %25, ptr %2, align 4
  br label %26

26:                                               ; preds = %23, %20
  %27 = call i32 @SumTiles(i32 noundef 0, i32 noundef 0, i32 noundef 8, i32 noundef 8)
  %28 = icmp eq i32 %27, 9
  br i1 %28, label %29, label %32

29:                                               ; preds = %26
  %30 = load i32, ptr %2, align 4
  %31 = or i32 %30, 16
  store i32 %31, ptr %2, align 4
  br label %32

32:                                               ; preds = %29, %26
  %33 = load i32, ptr %2, align 4
  ret i32 %33
}

attributes #0 = { noinline nounwind optnone uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\toolchain-tests/c89/test_main\\test_main.c", directory: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 1, !"wchar_size", i32 2}
!4 = !{i32 8, !"PIC Level", i32 2}
!5 = !{i32 7, !"uwtable", i32 2}
!6 = !{i32 1, !"MaxTLSAlign", i32 65536}
!7 = !{!"clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)"}
!8 = distinct !{!8, !9}
!9 = !{!"llvm.loop.mustprogress"}
!10 = distinct !{!10, !9}
