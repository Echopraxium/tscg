; ModuleID = 'E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\projects\wolfenstein3D/wolf3d\src/wolf3d_test.c'
source_filename = "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\wolfenstein3D/wolf3d\\src/wolf3d_test.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-windows-msvc19.51.36246"

%struct.actor_t = type { i32, i32, i32 }

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca %struct.actor_t, align 4
  store i32 0, ptr %1, align 4
  store i32 0, ptr %2, align 4
  %4 = call i32 @ScaleDiv(i32 noundef 10, i32 noundef 2)
  %5 = icmp eq i32 %4, 5
  br i1 %5, label %6, label %9

6:                                                ; preds = %0
  %7 = load i32, ptr %2, align 4
  %8 = or i32 %7, 1
  store i32 %8, ptr %2, align 4
  br label %9

9:                                                ; preds = %6, %0
  %10 = call i32 @IsSolid(i32 noundef 0, i32 noundef 0)
  %11 = icmp eq i32 %10, 0
  br i1 %11, label %12, label %15

12:                                               ; preds = %9
  %13 = load i32, ptr %2, align 4
  %14 = or i32 %13, 2
  store i32 %14, ptr %2, align 4
  br label %15

15:                                               ; preds = %12, %9
  %16 = getelementptr inbounds nuw %struct.actor_t, ptr %3, i32 0, i32 0
  store i32 655360, ptr %16, align 4
  %17 = getelementptr inbounds nuw %struct.actor_t, ptr %3, i32 0, i32 1
  store i32 1310720, ptr %17, align 4
  %18 = getelementptr inbounds nuw %struct.actor_t, ptr %3, i32 0, i32 2
  store i32 0, ptr %18, align 4
  call void @MoveActor(ptr noundef %3, i32 noundef 5, i32 noundef 3)
  %19 = getelementptr inbounds nuw %struct.actor_t, ptr %3, i32 0, i32 0
  %20 = load i32, ptr %19, align 4
  %21 = ashr i32 %20, 16
  %22 = icmp eq i32 %21, 15
  br i1 %22, label %23, label %31

23:                                               ; preds = %15
  %24 = getelementptr inbounds nuw %struct.actor_t, ptr %3, i32 0, i32 1
  %25 = load i32, ptr %24, align 4
  %26 = ashr i32 %25, 16
  %27 = icmp eq i32 %26, 23
  br i1 %27, label %28, label %31

28:                                               ; preds = %23
  %29 = load i32, ptr %2, align 4
  %30 = or i32 %29, 4
  store i32 %30, ptr %2, align 4
  br label %31

31:                                               ; preds = %28, %23, %15
  %32 = call i32 @SumTiles(i32 noundef 0, i32 noundef 0, i32 noundef 8, i32 noundef 8)
  %33 = icmp eq i32 %32, 0
  br i1 %33, label %34, label %37

34:                                               ; preds = %31
  %35 = load i32, ptr %2, align 4
  %36 = or i32 %35, 8
  store i32 %36, ptr %2, align 4
  br label %37

37:                                               ; preds = %34, %31
  %38 = load i32, ptr %2, align 4
  ret i32 %38
}

declare dso_local i32 @ScaleDiv(i32 noundef, i32 noundef) #1

declare dso_local i32 @IsSolid(i32 noundef, i32 noundef) #1

declare dso_local void @MoveActor(ptr noundef, i32 noundef, i32 noundef) #1

declare dso_local i32 @SumTiles(i32 noundef, i32 noundef, i32 noundef, i32 noundef) #1

attributes #0 = { noinline nounwind optnone uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\wolfenstein3D/wolf3d\\src\\wolf3d_test.c", directory: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 1, !"wchar_size", i32 2}
!4 = !{i32 8, !"PIC Level", i32 2}
!5 = !{i32 7, !"uwtable", i32 2}
!6 = !{i32 1, !"MaxTLSAlign", i32 65536}
!7 = !{!"clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)"}
