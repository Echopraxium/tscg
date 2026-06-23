; ModuleID = 'E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\projects\Doom-Generic/vm-porting/tests/doom_math\src/m_random.c'
source_filename = "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\Doom-Generic/vm-porting/tests/doom_math\\src/m_random.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-windows-msvc19.51.36246"

@rndindex = dso_local global i32 0, align 4
@prndindex = dso_local global i32 0, align 4
@rndtable = internal constant [256 x i8] c"\00\08m\DC\DE\F1\95kK\F8\FE\8C\10BJ\15\D3/P\F2\9A\1B\CD\80\A1YM$_nU0\D4\8C\D3\F9\16O\C82\1C\BC4\8C\CAxD\91>F\B8\BE[\C5\98\E0\95h\19\B2\FC\B6\CA\B6\8D\C5\04Q\B5\F2\91*'\E3\9C\C6\E1\C1\DB]z\AF\F9\00\AF\8FF\EF.\F6\A35\A3m\A8\87\02\EB\19\\\14\91\8AME\A6N\B0\AD\D4\A6q^\A1)2\EF1o\A4F<\02%\ABK\88\9C\0B8*\92\8A\E5I\92M=b\C4\87j?\C5\C3V`\CBqe\AA\F7\B5qP\FAl\07\FF\ED\81\E2Okp\A6g\F1\18\DF\EFx\C6:<R\80\03\B8B\8F\E0\91\E0Q\CE\A3-?Z\A8r;!\9F_\1C\8B{b}\C4\0FF\C2\FD6\0Em\E2G\11\A1]\BAW\F4\8A\144{\FB\1A$\11.4\E7\E8L\1F\DDT%\D8\A5\D4j\C5\F2b+'\AF\FE\91\BETv\DE\BB\88x\A3\EC\F9", align 16

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @P_Random() #0 {
  %1 = load i32, ptr @prndindex, align 4
  %2 = add nsw i32 %1, 1
  %3 = and i32 %2, 255
  store i32 %3, ptr @prndindex, align 4
  %4 = load i32, ptr @prndindex, align 4
  %5 = sext i32 %4 to i64
  %6 = getelementptr inbounds [256 x i8], ptr @rndtable, i64 0, i64 %5
  %7 = load i8, ptr %6, align 1
  %8 = zext i8 %7 to i32
  ret i32 %8
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @M_Random() #0 {
  %1 = load i32, ptr @rndindex, align 4
  %2 = add nsw i32 %1, 1
  %3 = and i32 %2, 255
  store i32 %3, ptr @rndindex, align 4
  %4 = load i32, ptr @rndindex, align 4
  %5 = sext i32 %4 to i64
  %6 = getelementptr inbounds [256 x i8], ptr @rndtable, i64 0, i64 %5
  %7 = load i8, ptr %6, align 1
  %8 = zext i8 %7 to i32
  ret i32 %8
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @M_ClearRandom() #0 {
  store i32 0, ptr @prndindex, align 4
  store i32 0, ptr @rndindex, align 4
  ret void
}

attributes #0 = { noinline nounwind optnone uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\Doom-Generic/vm-porting/tests/doom_math\\src\\m_random.c", directory: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 1, !"wchar_size", i32 2}
!4 = !{i32 8, !"PIC Level", i32 2}
!5 = !{i32 7, !"uwtable", i32 2}
!6 = !{i32 1, !"MaxTLSAlign", i32 65536}
!7 = !{!"clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)"}
