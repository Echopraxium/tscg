; ModuleID = 'E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\projects\Doom-Generic/vm-porting/tests/doom_alloc\src/doom_alloc.c'
source_filename = "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\Doom-Generic/vm-porting/tests/doom_alloc\\src/doom_alloc.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-windows-msvc19.51.36246"

%struct.memzone_t = type { i32, %struct.memblock_s, ptr }
%struct.memblock_s = type { i32, ptr, i32, i32, ptr, ptr }

@mainzone = dso_local global ptr null, align 8

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @Z_ClearZone(ptr noundef %0) #0 {
  %2 = alloca ptr, align 8
  %3 = alloca ptr, align 8
  store ptr %0, ptr %2, align 8
  %4 = load ptr, ptr %2, align 8
  %5 = getelementptr inbounds nuw i8, ptr %4, i64 56
  store ptr %5, ptr %3, align 8
  %6 = load ptr, ptr %3, align 8
  %7 = load ptr, ptr %2, align 8
  %8 = getelementptr inbounds nuw %struct.memzone_t, ptr %7, i32 0, i32 1
  %9 = getelementptr inbounds nuw %struct.memblock_s, ptr %8, i32 0, i32 4
  store ptr %6, ptr %9, align 8
  %10 = load ptr, ptr %3, align 8
  %11 = load ptr, ptr %2, align 8
  %12 = getelementptr inbounds nuw %struct.memzone_t, ptr %11, i32 0, i32 1
  %13 = getelementptr inbounds nuw %struct.memblock_s, ptr %12, i32 0, i32 5
  store ptr %10, ptr %13, align 8
  %14 = load ptr, ptr %2, align 8
  %15 = load ptr, ptr %2, align 8
  %16 = getelementptr inbounds nuw %struct.memzone_t, ptr %15, i32 0, i32 1
  %17 = getelementptr inbounds nuw %struct.memblock_s, ptr %16, i32 0, i32 1
  store ptr %14, ptr %17, align 8
  %18 = load ptr, ptr %2, align 8
  %19 = getelementptr inbounds nuw %struct.memzone_t, ptr %18, i32 0, i32 1
  %20 = getelementptr inbounds nuw %struct.memblock_s, ptr %19, i32 0, i32 2
  store i32 1, ptr %20, align 8
  %21 = load ptr, ptr %3, align 8
  %22 = load ptr, ptr %2, align 8
  %23 = getelementptr inbounds nuw %struct.memzone_t, ptr %22, i32 0, i32 2
  store ptr %21, ptr %23, align 8
  %24 = load ptr, ptr %2, align 8
  %25 = getelementptr inbounds nuw %struct.memzone_t, ptr %24, i32 0, i32 1
  %26 = load ptr, ptr %3, align 8
  %27 = getelementptr inbounds nuw %struct.memblock_s, ptr %26, i32 0, i32 5
  store ptr %25, ptr %27, align 8
  %28 = load ptr, ptr %2, align 8
  %29 = getelementptr inbounds nuw %struct.memzone_t, ptr %28, i32 0, i32 1
  %30 = load ptr, ptr %3, align 8
  %31 = getelementptr inbounds nuw %struct.memblock_s, ptr %30, i32 0, i32 4
  store ptr %29, ptr %31, align 8
  %32 = load ptr, ptr %3, align 8
  %33 = getelementptr inbounds nuw %struct.memblock_s, ptr %32, i32 0, i32 2
  store i32 0, ptr %33, align 8
  %34 = load ptr, ptr %2, align 8
  %35 = getelementptr inbounds nuw %struct.memzone_t, ptr %34, i32 0, i32 0
  %36 = load i32, ptr %35, align 8
  %37 = sext i32 %36 to i64
  %38 = sub i64 %37, 56
  %39 = trunc i64 %38 to i32
  %40 = load ptr, ptr %3, align 8
  %41 = getelementptr inbounds nuw %struct.memblock_s, ptr %40, i32 0, i32 0
  store i32 %39, ptr %41, align 8
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @Z_Init(ptr noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca ptr, align 8
  store i32 %1, ptr %3, align 4
  store ptr %0, ptr %4, align 8
  %5 = load ptr, ptr %4, align 8
  store ptr %5, ptr @mainzone, align 8
  %6 = load i32, ptr %3, align 4
  %7 = load ptr, ptr @mainzone, align 8
  %8 = getelementptr inbounds nuw %struct.memzone_t, ptr %7, i32 0, i32 0
  store i32 %6, ptr %8, align 8
  %9 = load ptr, ptr @mainzone, align 8
  call void @Z_ClearZone(ptr noundef %9)
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @Z_Free(ptr noundef %0) #0 {
  %2 = alloca ptr, align 8
  %3 = alloca ptr, align 8
  %4 = alloca ptr, align 8
  store ptr %0, ptr %2, align 8
  %5 = load ptr, ptr %2, align 8
  %6 = getelementptr inbounds i8, ptr %5, i64 -40
  store ptr %6, ptr %3, align 8
  %7 = load ptr, ptr %3, align 8
  %8 = getelementptr inbounds nuw %struct.memblock_s, ptr %7, i32 0, i32 3
  %9 = load i32, ptr %8, align 4
  %10 = icmp ne i32 %9, 1919505
  br i1 %10, label %11, label %12

11:                                               ; preds = %1
  br label %105

12:                                               ; preds = %1
  %13 = load ptr, ptr %3, align 8
  %14 = getelementptr inbounds nuw %struct.memblock_s, ptr %13, i32 0, i32 2
  %15 = load i32, ptr %14, align 8
  %16 = icmp ne i32 %15, 0
  br i1 %16, label %17, label %26

17:                                               ; preds = %12
  %18 = load ptr, ptr %3, align 8
  %19 = getelementptr inbounds nuw %struct.memblock_s, ptr %18, i32 0, i32 1
  %20 = load ptr, ptr %19, align 8
  %21 = icmp ne ptr %20, null
  br i1 %21, label %22, label %26

22:                                               ; preds = %17
  %23 = load ptr, ptr %3, align 8
  %24 = getelementptr inbounds nuw %struct.memblock_s, ptr %23, i32 0, i32 1
  %25 = load ptr, ptr %24, align 8
  store ptr null, ptr %25, align 8
  br label %26

26:                                               ; preds = %22, %17, %12
  %27 = load ptr, ptr %3, align 8
  %28 = getelementptr inbounds nuw %struct.memblock_s, ptr %27, i32 0, i32 2
  store i32 0, ptr %28, align 8
  %29 = load ptr, ptr %3, align 8
  %30 = getelementptr inbounds nuw %struct.memblock_s, ptr %29, i32 0, i32 1
  store ptr null, ptr %30, align 8
  %31 = load ptr, ptr %3, align 8
  %32 = getelementptr inbounds nuw %struct.memblock_s, ptr %31, i32 0, i32 3
  store i32 0, ptr %32, align 4
  %33 = load ptr, ptr %3, align 8
  %34 = getelementptr inbounds nuw %struct.memblock_s, ptr %33, i32 0, i32 5
  %35 = load ptr, ptr %34, align 8
  store ptr %35, ptr %4, align 8
  %36 = load ptr, ptr %4, align 8
  %37 = getelementptr inbounds nuw %struct.memblock_s, ptr %36, i32 0, i32 2
  %38 = load i32, ptr %37, align 8
  %39 = icmp eq i32 %38, 0
  br i1 %39, label %40, label %69

40:                                               ; preds = %26
  %41 = load ptr, ptr %3, align 8
  %42 = getelementptr inbounds nuw %struct.memblock_s, ptr %41, i32 0, i32 0
  %43 = load i32, ptr %42, align 8
  %44 = load ptr, ptr %4, align 8
  %45 = getelementptr inbounds nuw %struct.memblock_s, ptr %44, i32 0, i32 0
  %46 = load i32, ptr %45, align 8
  %47 = add nsw i32 %46, %43
  store i32 %47, ptr %45, align 8
  %48 = load ptr, ptr %3, align 8
  %49 = getelementptr inbounds nuw %struct.memblock_s, ptr %48, i32 0, i32 4
  %50 = load ptr, ptr %49, align 8
  %51 = load ptr, ptr %4, align 8
  %52 = getelementptr inbounds nuw %struct.memblock_s, ptr %51, i32 0, i32 4
  store ptr %50, ptr %52, align 8
  %53 = load ptr, ptr %4, align 8
  %54 = load ptr, ptr %4, align 8
  %55 = getelementptr inbounds nuw %struct.memblock_s, ptr %54, i32 0, i32 4
  %56 = load ptr, ptr %55, align 8
  %57 = getelementptr inbounds nuw %struct.memblock_s, ptr %56, i32 0, i32 5
  store ptr %53, ptr %57, align 8
  %58 = load ptr, ptr %3, align 8
  %59 = load ptr, ptr @mainzone, align 8
  %60 = getelementptr inbounds nuw %struct.memzone_t, ptr %59, i32 0, i32 2
  %61 = load ptr, ptr %60, align 8
  %62 = icmp eq ptr %58, %61
  br i1 %62, label %63, label %67

63:                                               ; preds = %40
  %64 = load ptr, ptr %4, align 8
  %65 = load ptr, ptr @mainzone, align 8
  %66 = getelementptr inbounds nuw %struct.memzone_t, ptr %65, i32 0, i32 2
  store ptr %64, ptr %66, align 8
  br label %67

67:                                               ; preds = %63, %40
  %68 = load ptr, ptr %4, align 8
  store ptr %68, ptr %3, align 8
  br label %69

69:                                               ; preds = %67, %26
  %70 = load ptr, ptr %3, align 8
  %71 = getelementptr inbounds nuw %struct.memblock_s, ptr %70, i32 0, i32 4
  %72 = load ptr, ptr %71, align 8
  store ptr %72, ptr %4, align 8
  %73 = load ptr, ptr %4, align 8
  %74 = getelementptr inbounds nuw %struct.memblock_s, ptr %73, i32 0, i32 2
  %75 = load i32, ptr %74, align 8
  %76 = icmp eq i32 %75, 0
  br i1 %76, label %77, label %105

77:                                               ; preds = %69
  %78 = load ptr, ptr %4, align 8
  %79 = getelementptr inbounds nuw %struct.memblock_s, ptr %78, i32 0, i32 0
  %80 = load i32, ptr %79, align 8
  %81 = load ptr, ptr %3, align 8
  %82 = getelementptr inbounds nuw %struct.memblock_s, ptr %81, i32 0, i32 0
  %83 = load i32, ptr %82, align 8
  %84 = add nsw i32 %83, %80
  store i32 %84, ptr %82, align 8
  %85 = load ptr, ptr %4, align 8
  %86 = getelementptr inbounds nuw %struct.memblock_s, ptr %85, i32 0, i32 4
  %87 = load ptr, ptr %86, align 8
  %88 = load ptr, ptr %3, align 8
  %89 = getelementptr inbounds nuw %struct.memblock_s, ptr %88, i32 0, i32 4
  store ptr %87, ptr %89, align 8
  %90 = load ptr, ptr %3, align 8
  %91 = load ptr, ptr %3, align 8
  %92 = getelementptr inbounds nuw %struct.memblock_s, ptr %91, i32 0, i32 4
  %93 = load ptr, ptr %92, align 8
  %94 = getelementptr inbounds nuw %struct.memblock_s, ptr %93, i32 0, i32 5
  store ptr %90, ptr %94, align 8
  %95 = load ptr, ptr %4, align 8
  %96 = load ptr, ptr @mainzone, align 8
  %97 = getelementptr inbounds nuw %struct.memzone_t, ptr %96, i32 0, i32 2
  %98 = load ptr, ptr %97, align 8
  %99 = icmp eq ptr %95, %98
  br i1 %99, label %100, label %104

100:                                              ; preds = %77
  %101 = load ptr, ptr %3, align 8
  %102 = load ptr, ptr @mainzone, align 8
  %103 = getelementptr inbounds nuw %struct.memzone_t, ptr %102, i32 0, i32 2
  store ptr %101, ptr %103, align 8
  br label %104

104:                                              ; preds = %100, %77
  br label %105

105:                                              ; preds = %11, %104, %69
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local ptr @Z_Malloc(i32 noundef %0, i32 noundef %1, ptr noundef %2) #0 {
  %4 = alloca ptr, align 8
  %5 = alloca ptr, align 8
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  %9 = alloca ptr, align 8
  %10 = alloca ptr, align 8
  %11 = alloca ptr, align 8
  %12 = alloca ptr, align 8
  %13 = alloca ptr, align 8
  store ptr %2, ptr %5, align 8
  store i32 %1, ptr %6, align 4
  store i32 %0, ptr %7, align 4
  %14 = load i32, ptr %7, align 4
  %15 = add nsw i32 %14, 4
  %16 = sub nsw i32 %15, 1
  %17 = and i32 %16, -4
  store i32 %17, ptr %7, align 4
  %18 = load i32, ptr %7, align 4
  %19 = sext i32 %18 to i64
  %20 = add i64 %19, 40
  %21 = trunc i64 %20 to i32
  store i32 %21, ptr %7, align 4
  %22 = load ptr, ptr @mainzone, align 8
  %23 = getelementptr inbounds nuw %struct.memzone_t, ptr %22, i32 0, i32 2
  %24 = load ptr, ptr %23, align 8
  store ptr %24, ptr %12, align 8
  %25 = load ptr, ptr %12, align 8
  %26 = getelementptr inbounds nuw %struct.memblock_s, ptr %25, i32 0, i32 5
  %27 = load ptr, ptr %26, align 8
  %28 = getelementptr inbounds nuw %struct.memblock_s, ptr %27, i32 0, i32 2
  %29 = load i32, ptr %28, align 8
  %30 = icmp eq i32 %29, 0
  br i1 %30, label %31, label %35

31:                                               ; preds = %3
  %32 = load ptr, ptr %12, align 8
  %33 = getelementptr inbounds nuw %struct.memblock_s, ptr %32, i32 0, i32 5
  %34 = load ptr, ptr %33, align 8
  store ptr %34, ptr %12, align 8
  br label %35

35:                                               ; preds = %31, %3
  %36 = load ptr, ptr %12, align 8
  store ptr %36, ptr %10, align 8
  %37 = load ptr, ptr %12, align 8
  %38 = getelementptr inbounds nuw %struct.memblock_s, ptr %37, i32 0, i32 5
  %39 = load ptr, ptr %38, align 8
  store ptr %39, ptr %9, align 8
  br label %40

40:                                               ; preds = %88, %35
  %41 = load ptr, ptr %10, align 8
  %42 = load ptr, ptr %9, align 8
  %43 = icmp eq ptr %41, %42
  br i1 %43, label %44, label %45

44:                                               ; preds = %40
  store ptr null, ptr %4, align 8
  br label %163

45:                                               ; preds = %40
  %46 = load ptr, ptr %10, align 8
  %47 = getelementptr inbounds nuw %struct.memblock_s, ptr %46, i32 0, i32 2
  %48 = load i32, ptr %47, align 8
  %49 = icmp ne i32 %48, 0
  br i1 %49, label %50, label %72

50:                                               ; preds = %45
  %51 = load ptr, ptr %10, align 8
  %52 = getelementptr inbounds nuw %struct.memblock_s, ptr %51, i32 0, i32 2
  %53 = load i32, ptr %52, align 8
  %54 = icmp slt i32 %53, 100
  br i1 %54, label %55, label %59

55:                                               ; preds = %50
  %56 = load ptr, ptr %10, align 8
  %57 = getelementptr inbounds nuw %struct.memblock_s, ptr %56, i32 0, i32 4
  %58 = load ptr, ptr %57, align 8
  store ptr %58, ptr %10, align 8
  store ptr %58, ptr %12, align 8
  br label %71

59:                                               ; preds = %50
  %60 = load ptr, ptr %12, align 8
  %61 = getelementptr inbounds nuw %struct.memblock_s, ptr %60, i32 0, i32 5
  %62 = load ptr, ptr %61, align 8
  store ptr %62, ptr %12, align 8
  %63 = load ptr, ptr %10, align 8
  %64 = getelementptr inbounds nuw i8, ptr %63, i64 40
  call void @Z_Free(ptr noundef %64)
  %65 = load ptr, ptr %12, align 8
  %66 = getelementptr inbounds nuw %struct.memblock_s, ptr %65, i32 0, i32 4
  %67 = load ptr, ptr %66, align 8
  store ptr %67, ptr %12, align 8
  %68 = load ptr, ptr %12, align 8
  %69 = getelementptr inbounds nuw %struct.memblock_s, ptr %68, i32 0, i32 4
  %70 = load ptr, ptr %69, align 8
  store ptr %70, ptr %10, align 8
  br label %71

71:                                               ; preds = %59, %55
  br label %76

72:                                               ; preds = %45
  %73 = load ptr, ptr %10, align 8
  %74 = getelementptr inbounds nuw %struct.memblock_s, ptr %73, i32 0, i32 4
  %75 = load ptr, ptr %74, align 8
  store ptr %75, ptr %10, align 8
  br label %76

76:                                               ; preds = %72, %71
  br label %77

77:                                               ; preds = %76
  %78 = load ptr, ptr %12, align 8
  %79 = getelementptr inbounds nuw %struct.memblock_s, ptr %78, i32 0, i32 2
  %80 = load i32, ptr %79, align 8
  %81 = icmp ne i32 %80, 0
  br i1 %81, label %88, label %82

82:                                               ; preds = %77
  %83 = load ptr, ptr %12, align 8
  %84 = getelementptr inbounds nuw %struct.memblock_s, ptr %83, i32 0, i32 0
  %85 = load i32, ptr %84, align 8
  %86 = load i32, ptr %7, align 4
  %87 = icmp slt i32 %85, %86
  br label %88

88:                                               ; preds = %82, %77
  %89 = phi i1 [ true, %77 ], [ %87, %82 ]
  br i1 %89, label %40, label %90, !llvm.loop !8

90:                                               ; preds = %88
  %91 = load ptr, ptr %12, align 8
  %92 = getelementptr inbounds nuw %struct.memblock_s, ptr %91, i32 0, i32 0
  %93 = load i32, ptr %92, align 8
  %94 = load i32, ptr %7, align 4
  %95 = sub nsw i32 %93, %94
  store i32 %95, ptr %8, align 4
  %96 = load i32, ptr %8, align 4
  %97 = icmp sgt i32 %96, 64
  br i1 %97, label %98, label %129

98:                                               ; preds = %90
  %99 = load ptr, ptr %12, align 8
  %100 = load i32, ptr %7, align 4
  %101 = sext i32 %100 to i64
  %102 = getelementptr inbounds i8, ptr %99, i64 %101
  store ptr %102, ptr %11, align 8
  %103 = load i32, ptr %8, align 4
  %104 = load ptr, ptr %11, align 8
  %105 = getelementptr inbounds nuw %struct.memblock_s, ptr %104, i32 0, i32 0
  store i32 %103, ptr %105, align 8
  %106 = load ptr, ptr %11, align 8
  %107 = getelementptr inbounds nuw %struct.memblock_s, ptr %106, i32 0, i32 2
  store i32 0, ptr %107, align 8
  %108 = load ptr, ptr %11, align 8
  %109 = getelementptr inbounds nuw %struct.memblock_s, ptr %108, i32 0, i32 1
  store ptr null, ptr %109, align 8
  %110 = load ptr, ptr %12, align 8
  %111 = load ptr, ptr %11, align 8
  %112 = getelementptr inbounds nuw %struct.memblock_s, ptr %111, i32 0, i32 5
  store ptr %110, ptr %112, align 8
  %113 = load ptr, ptr %12, align 8
  %114 = getelementptr inbounds nuw %struct.memblock_s, ptr %113, i32 0, i32 4
  %115 = load ptr, ptr %114, align 8
  %116 = load ptr, ptr %11, align 8
  %117 = getelementptr inbounds nuw %struct.memblock_s, ptr %116, i32 0, i32 4
  store ptr %115, ptr %117, align 8
  %118 = load ptr, ptr %11, align 8
  %119 = load ptr, ptr %11, align 8
  %120 = getelementptr inbounds nuw %struct.memblock_s, ptr %119, i32 0, i32 4
  %121 = load ptr, ptr %120, align 8
  %122 = getelementptr inbounds nuw %struct.memblock_s, ptr %121, i32 0, i32 5
  store ptr %118, ptr %122, align 8
  %123 = load ptr, ptr %11, align 8
  %124 = load ptr, ptr %12, align 8
  %125 = getelementptr inbounds nuw %struct.memblock_s, ptr %124, i32 0, i32 4
  store ptr %123, ptr %125, align 8
  %126 = load i32, ptr %7, align 4
  %127 = load ptr, ptr %12, align 8
  %128 = getelementptr inbounds nuw %struct.memblock_s, ptr %127, i32 0, i32 0
  store i32 %126, ptr %128, align 8
  br label %129

129:                                              ; preds = %98, %90
  %130 = load ptr, ptr %5, align 8
  %131 = icmp eq ptr %130, null
  br i1 %131, label %132, label %136

132:                                              ; preds = %129
  %133 = load i32, ptr %6, align 4
  %134 = icmp sge i32 %133, 100
  br i1 %134, label %135, label %136

135:                                              ; preds = %132
  store ptr null, ptr %4, align 8
  br label %163

136:                                              ; preds = %132, %129
  %137 = load ptr, ptr %5, align 8
  %138 = load ptr, ptr %12, align 8
  %139 = getelementptr inbounds nuw %struct.memblock_s, ptr %138, i32 0, i32 1
  store ptr %137, ptr %139, align 8
  %140 = load i32, ptr %6, align 4
  %141 = load ptr, ptr %12, align 8
  %142 = getelementptr inbounds nuw %struct.memblock_s, ptr %141, i32 0, i32 2
  store i32 %140, ptr %142, align 8
  %143 = load ptr, ptr %12, align 8
  %144 = getelementptr inbounds nuw i8, ptr %143, i64 40
  store ptr %144, ptr %13, align 8
  %145 = load ptr, ptr %12, align 8
  %146 = getelementptr inbounds nuw %struct.memblock_s, ptr %145, i32 0, i32 1
  %147 = load ptr, ptr %146, align 8
  %148 = icmp ne ptr %147, null
  br i1 %148, label %149, label %154

149:                                              ; preds = %136
  %150 = load ptr, ptr %13, align 8
  %151 = load ptr, ptr %12, align 8
  %152 = getelementptr inbounds nuw %struct.memblock_s, ptr %151, i32 0, i32 1
  %153 = load ptr, ptr %152, align 8
  store ptr %150, ptr %153, align 8
  br label %154

154:                                              ; preds = %149, %136
  %155 = load ptr, ptr %12, align 8
  %156 = getelementptr inbounds nuw %struct.memblock_s, ptr %155, i32 0, i32 4
  %157 = load ptr, ptr %156, align 8
  %158 = load ptr, ptr @mainzone, align 8
  %159 = getelementptr inbounds nuw %struct.memzone_t, ptr %158, i32 0, i32 2
  store ptr %157, ptr %159, align 8
  %160 = load ptr, ptr %12, align 8
  %161 = getelementptr inbounds nuw %struct.memblock_s, ptr %160, i32 0, i32 3
  store i32 1919505, ptr %161, align 4
  %162 = load ptr, ptr %13, align 8
  store ptr %162, ptr %4, align 8
  br label %163

163:                                              ; preds = %154, %135, %44
  %164 = load ptr, ptr %4, align 8
  ret ptr %164
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @Z_FreeMemory() #0 {
  %1 = alloca ptr, align 8
  %2 = alloca i32, align 4
  store i32 0, ptr %2, align 4
  %3 = load ptr, ptr @mainzone, align 8
  %4 = getelementptr inbounds nuw %struct.memzone_t, ptr %3, i32 0, i32 1
  %5 = getelementptr inbounds nuw %struct.memblock_s, ptr %4, i32 0, i32 4
  %6 = load ptr, ptr %5, align 8
  store ptr %6, ptr %1, align 8
  br label %7

7:                                                ; preds = %28, %0
  %8 = load ptr, ptr %1, align 8
  %9 = load ptr, ptr @mainzone, align 8
  %10 = getelementptr inbounds nuw %struct.memzone_t, ptr %9, i32 0, i32 1
  %11 = icmp ne ptr %8, %10
  br i1 %11, label %12, label %32

12:                                               ; preds = %7
  %13 = load ptr, ptr %1, align 8
  %14 = getelementptr inbounds nuw %struct.memblock_s, ptr %13, i32 0, i32 2
  %15 = load i32, ptr %14, align 8
  %16 = icmp eq i32 %15, 0
  br i1 %16, label %22, label %17

17:                                               ; preds = %12
  %18 = load ptr, ptr %1, align 8
  %19 = getelementptr inbounds nuw %struct.memblock_s, ptr %18, i32 0, i32 2
  %20 = load i32, ptr %19, align 8
  %21 = icmp sge i32 %20, 100
  br i1 %21, label %22, label %28

22:                                               ; preds = %17, %12
  %23 = load ptr, ptr %1, align 8
  %24 = getelementptr inbounds nuw %struct.memblock_s, ptr %23, i32 0, i32 0
  %25 = load i32, ptr %24, align 8
  %26 = load i32, ptr %2, align 4
  %27 = add nsw i32 %26, %25
  store i32 %27, ptr %2, align 4
  br label %28

28:                                               ; preds = %22, %17
  %29 = load ptr, ptr %1, align 8
  %30 = getelementptr inbounds nuw %struct.memblock_s, ptr %29, i32 0, i32 4
  %31 = load ptr, ptr %30, align 8
  store ptr %31, ptr %1, align 8
  br label %7, !llvm.loop !10

32:                                               ; preds = %7
  %33 = load i32, ptr %2, align 4
  ret i32 %33
}

attributes #0 = { noinline nounwind optnone uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain\\projects\\Doom-Generic/vm-porting/tests/doom_alloc\\src\\doom_alloc.c", directory: "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg\\instances\\symbolic-system-grammars\\TriskeleToolchain")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 1, !"wchar_size", i32 2}
!4 = !{i32 8, !"PIC Level", i32 2}
!5 = !{i32 7, !"uwtable", i32 2}
!6 = !{i32 1, !"MaxTLSAlign", i32 65536}
!7 = !{!"clang version 22.1.7 (https://github.com/llvm/llvm-project a255c1ed36a1d06f79bd2633ba9f8d900153007c)"}
!8 = distinct !{!8, !9}
!9 = !{!"llvm.loop.mustprogress"}
!10 = distinct !{!10, !9}
