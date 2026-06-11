; ModuleID = 'E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\projects\test-lib-dos\test_dos.c'
source_filename = "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\test-lib-dos\\test_dos.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-windows-msvc19.51.36246"

$"??_C@_0BF@EAOLKOJ@Touche?5press?C?$KJe?3?5?$CFd?6?$AA@" = comdat any

@"??_C@_0BF@EAOLKOJ@Touche?5press?C?$KJe?3?5?$CFd?6?$AA@" = linkonce_odr dso_local unnamed_addr constant [21 x i8] c"Touche press\C3\A9e: %d\0A\00", comdat, align 1

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  call void @sound(i32 noundef 440)
  call void @delay(i32 noundef 500)
  call void @nosound()
  %3 = call i32 @getch()
  store i32 %3, ptr %2, align 4
  %4 = load i32, ptr %2, align 4
  %5 = call i32 (ptr, ...) @printf(ptr noundef @"??_C@_0BF@EAOLKOJ@Touche?5press?C?$KJe?3?5?$CFd?6?$AA@", i32 noundef %4)
  ret i32 0
}

declare dso_local void @sound(i32 noundef) #1

declare dso_local void @delay(i32 noundef) #1

declare dso_local void @nosound() #1

declare dso_local i32 @getch() #1

declare dso_local i32 @printf(ptr noundef, ...) #1

attributes #0 = { noinline nounwind optnone uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\test-lib-dos\\test_dos.c", directory: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 1, !"wchar_size", i32 2}
!4 = !{i32 8, !"PIC Level", i32 2}
!5 = !{i32 7, !"uwtable", i32 2}
!6 = !{i32 1, !"MaxTLSAlign", i32 65536}
!7 = !{!"clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)"}
