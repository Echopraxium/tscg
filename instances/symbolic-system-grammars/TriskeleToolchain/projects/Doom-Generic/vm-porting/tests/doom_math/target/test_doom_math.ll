; ModuleID = 'E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\projects\Doom-Generic/vm-porting/tests/doom_math\src/test_doom_math.c'
source_filename = "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\Doom-Generic/vm-porting/tests/doom_math\\src/test_doom_math.c"
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
  store i32 0, ptr %1, align 4
  store i32 0, ptr %2, align 4
  store i32 65536, ptr %3, align 4
  store i32 131072, ptr %4, align 4
  %16 = load i32, ptr %4, align 4
  %17 = load i32, ptr %3, align 4
  %18 = call i32 @FixedMul(i32 noundef %17, i32 noundef %16)
  store i32 %18, ptr %5, align 4
  %19 = load i32, ptr %5, align 4
  %20 = icmp eq i32 %19, 131072
  br i1 %20, label %21, label %24

21:                                               ; preds = %0
  %22 = load i32, ptr %2, align 4
  %23 = or i32 %22, 1
  store i32 %23, ptr %2, align 4
  br label %24

24:                                               ; preds = %21, %0
  store i32 32768, ptr %6, align 4
  %25 = load i32, ptr %6, align 4
  %26 = load i32, ptr %6, align 4
  %27 = call i32 @FixedMul(i32 noundef %26, i32 noundef %25)
  store i32 %27, ptr %7, align 4
  %28 = load i32, ptr %7, align 4
  %29 = icmp eq i32 %28, 16384
  br i1 %29, label %30, label %33

30:                                               ; preds = %24
  %31 = load i32, ptr %2, align 4
  %32 = or i32 %31, 2
  store i32 %32, ptr %2, align 4
  br label %33

33:                                               ; preds = %30, %24
  %34 = call i32 @FixedDiv(i32 noundef 262144, i32 noundef 131072)
  store i32 %34, ptr %8, align 4
  %35 = load i32, ptr %8, align 4
  %36 = icmp eq i32 %35, 131072
  br i1 %36, label %37, label %40

37:                                               ; preds = %33
  %38 = load i32, ptr %2, align 4
  %39 = or i32 %38, 4
  store i32 %39, ptr %2, align 4
  br label %40

40:                                               ; preds = %37, %33
  %41 = call i32 @FixedDiv(i32 noundef 2147483647, i32 noundef 1)
  store i32 %41, ptr %9, align 4
  %42 = load i32, ptr %9, align 4
  %43 = icmp eq i32 %42, 2147483647
  br i1 %43, label %44, label %47

44:                                               ; preds = %40
  %45 = load i32, ptr %2, align 4
  %46 = or i32 %45, 8
  store i32 %46, ptr %2, align 4
  br label %47

47:                                               ; preds = %44, %40
  call void @M_ClearRandom()
  %48 = call i32 @M_Random()
  store i32 %48, ptr %10, align 4
  %49 = load i32, ptr %10, align 4
  %50 = icmp eq i32 %49, 8
  br i1 %50, label %51, label %54

51:                                               ; preds = %47
  %52 = load i32, ptr %2, align 4
  %53 = or i32 %52, 16
  store i32 %53, ptr %2, align 4
  br label %54

54:                                               ; preds = %51, %47
  %55 = call i32 @M_Random()
  %56 = call i32 @M_Random()
  call void @M_ClearRandom()
  %57 = call i32 @M_Random()
  store i32 %57, ptr %11, align 4
  %58 = load i32, ptr %11, align 4
  %59 = icmp eq i32 %58, 8
  br i1 %59, label %60, label %63

60:                                               ; preds = %54
  %61 = load i32, ptr %2, align 4
  %62 = or i32 %61, 32
  store i32 %62, ptr %2, align 4
  br label %63

63:                                               ; preds = %60, %54
  call void @M_ClearRandom()
  %64 = call i32 @M_Random()
  store i32 %64, ptr %12, align 4
  %65 = call i32 @P_Random()
  store i32 %65, ptr %13, align 4
  %66 = call i32 @M_Random()
  store i32 %66, ptr %14, align 4
  %67 = call i32 @P_Random()
  store i32 %67, ptr %15, align 4
  %68 = load i32, ptr %12, align 4
  %69 = icmp eq i32 %68, 8
  br i1 %69, label %70, label %82

70:                                               ; preds = %63
  %71 = load i32, ptr %13, align 4
  %72 = icmp eq i32 %71, 8
  br i1 %72, label %73, label %82

73:                                               ; preds = %70
  %74 = load i32, ptr %14, align 4
  %75 = icmp eq i32 %74, 109
  br i1 %75, label %76, label %82

76:                                               ; preds = %73
  %77 = load i32, ptr %15, align 4
  %78 = icmp eq i32 %77, 109
  br i1 %78, label %79, label %82

79:                                               ; preds = %76
  %80 = load i32, ptr %2, align 4
  %81 = or i32 %80, 64
  store i32 %81, ptr %2, align 4
  br label %82

82:                                               ; preds = %79, %76, %73, %70, %63
  %83 = load i32, ptr %2, align 4
  ret i32 %83
}

declare dso_local i32 @FixedMul(i32 noundef, i32 noundef) #1

declare dso_local i32 @FixedDiv(i32 noundef, i32 noundef) #1

declare dso_local void @M_ClearRandom() #1

declare dso_local i32 @M_Random() #1

declare dso_local i32 @P_Random() #1

attributes #0 = { noinline nounwind optnone uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\Doom-Generic/vm-porting/tests/doom_math\\src\\test_doom_math.c", directory: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 1, !"wchar_size", i32 2}
!4 = !{i32 8, !"PIC Level", i32 2}
!5 = !{i32 7, !"uwtable", i32 2}
!6 = !{i32 1, !"MaxTLSAlign", i32 65536}
!7 = !{!"clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)"}
