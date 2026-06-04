; ModuleID = '/tmp/wolf3d_sample.c'
source_filename = "/tmp/wolf3d_sample.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

%struct.actor_t = type { i64, i64, i32 }

@tilemap = dso_local local_unnamed_addr global [4096 x i8] zeroinitializer, align 16

; Function Attrs: mustprogress nofree norecurse nosync nounwind willreturn memory(none) uwtable
define dso_local noundef i32 @ScaleDiv(i32 noundef %0, i32 noundef %1) local_unnamed_addr #0 {
  %3 = icmp eq i32 %1, 0
  br i1 %3, label %6, label %4

4:                                                ; preds = %2
  %5 = sdiv i32 %0, %1
  br label %6

6:                                                ; preds = %2, %4
  %7 = phi i32 [ %5, %4 ], [ 0, %2 ]
  ret i32 %7
}

; Function Attrs: mustprogress nofree norecurse nosync nounwind willreturn memory(read, argmem: none, inaccessiblemem: none) uwtable
define dso_local i32 @IsSolid(i32 noundef %0, i32 noundef %1) local_unnamed_addr #1 {
  %3 = or i32 %1, %0
  %4 = icmp ult i32 %3, 64
  br i1 %4, label %5, label %13

5:                                                ; preds = %2
  %6 = shl nuw nsw i32 %1, 6
  %7 = add nuw nsw i32 %6, %0
  %8 = zext nneg i32 %7 to i64
  %9 = getelementptr inbounds [4096 x i8], ptr @tilemap, i64 0, i64 %8
  %10 = load i8, ptr %9, align 1, !tbaa !5
  %11 = icmp ne i8 %10, 0
  %12 = zext i1 %11 to i32
  br label %13

13:                                               ; preds = %2, %5
  %14 = phi i32 [ %12, %5 ], [ 1, %2 ]
  ret i32 %14
}

; Function Attrs: mustprogress nofree norecurse nosync nounwind willreturn memory(read, argmem: readwrite, inaccessiblemem: none) uwtable
define dso_local void @MoveActor(ptr nocapture noundef %0, i32 noundef %1, i32 noundef %2) local_unnamed_addr #2 {
  %4 = load i64, ptr %0, align 8, !tbaa !8
  %5 = lshr i64 %4, 16
  %6 = trunc i64 %5 to i32
  %7 = add nsw i32 %6, %1
  %8 = getelementptr inbounds %struct.actor_t, ptr %0, i64 0, i32 1
  %9 = load i64, ptr %8, align 8, !tbaa !12
  %10 = lshr i64 %9, 16
  %11 = trunc i64 %10 to i32
  %12 = add nsw i32 %11, %2
  %13 = or i32 %7, %11
  %14 = icmp ult i32 %13, 64
  br i1 %14, label %15, label %26

15:                                               ; preds = %3
  %16 = shl nuw nsw i32 %11, 6
  %17 = add nuw nsw i32 %16, %7
  %18 = zext nneg i32 %17 to i64
  %19 = getelementptr inbounds [4096 x i8], ptr @tilemap, i64 0, i64 %18
  %20 = load i8, ptr %19, align 1, !tbaa !5
  %21 = icmp eq i8 %20, 0
  br i1 %21, label %22, label %26

22:                                               ; preds = %15
  %23 = sext i32 %1 to i64
  %24 = shl nsw i64 %23, 16
  %25 = add nsw i64 %4, %24
  store i64 %25, ptr %0, align 8, !tbaa !8
  br label %26

26:                                               ; preds = %3, %22, %15
  %27 = load i64, ptr %0, align 8, !tbaa !8
  %28 = lshr i64 %27, 16
  %29 = trunc i64 %28 to i32
  %30 = or i32 %12, %29
  %31 = icmp ult i32 %30, 64
  br i1 %31, label %32, label %43

32:                                               ; preds = %26
  %33 = shl nuw nsw i32 %12, 6
  %34 = add nuw nsw i32 %33, %29
  %35 = zext nneg i32 %34 to i64
  %36 = getelementptr inbounds [4096 x i8], ptr @tilemap, i64 0, i64 %35
  %37 = load i8, ptr %36, align 1, !tbaa !5
  %38 = icmp eq i8 %37, 0
  br i1 %38, label %39, label %43

39:                                               ; preds = %32
  %40 = sext i32 %2 to i64
  %41 = shl nsw i64 %40, 16
  %42 = add nsw i64 %9, %41
  store i64 %42, ptr %8, align 8, !tbaa !12
  br label %43

43:                                               ; preds = %26, %39, %32
  ret void
}

; Function Attrs: nofree norecurse nosync nounwind memory(read, argmem: none, inaccessiblemem: none) uwtable
define dso_local i32 @SumTiles(i32 noundef %0, i32 noundef %1, i32 noundef %2, i32 noundef %3) local_unnamed_addr #3 {
  %5 = icmp sgt i32 %3, 0
  br i1 %5, label %6, label %35

6:                                                ; preds = %4
  %7 = add nsw i32 %3, %1
  %8 = add nsw i32 %2, %0
  %9 = icmp sgt i32 %2, 0
  %10 = sext i32 %0 to i64
  %11 = sext i32 %8 to i64
  %12 = sext i32 %1 to i64
  %13 = sext i32 %7 to i64
  br label %14

14:                                               ; preds = %6, %31
  %15 = phi i64 [ %12, %6 ], [ %33, %31 ]
  %16 = phi i32 [ 0, %6 ], [ %32, %31 ]
  br i1 %9, label %17, label %31

17:                                               ; preds = %14
  %18 = trunc i64 %15 to i32
  %19 = shl nsw i32 %18, 6
  %20 = sext i32 %19 to i64
  br label %21

21:                                               ; preds = %17, %21
  %22 = phi i64 [ %10, %17 ], [ %29, %21 ]
  %23 = phi i32 [ %16, %17 ], [ %28, %21 ]
  %24 = add nsw i64 %22, %20
  %25 = getelementptr inbounds [4096 x i8], ptr @tilemap, i64 0, i64 %24
  %26 = load i8, ptr %25, align 1, !tbaa !5
  %27 = zext i8 %26 to i32
  %28 = add nsw i32 %23, %27
  %29 = add nsw i64 %22, 1
  %30 = icmp slt i64 %29, %11
  br i1 %30, label %21, label %31, !llvm.loop !13

31:                                               ; preds = %21, %14
  %32 = phi i32 [ %16, %14 ], [ %28, %21 ]
  %33 = add nsw i64 %15, 1
  %34 = icmp slt i64 %33, %13
  br i1 %34, label %14, label %35, !llvm.loop !16

35:                                               ; preds = %31, %4
  %36 = phi i32 [ 0, %4 ], [ %32, %31 ]
  ret i32 %36
}

attributes #0 = { mustprogress nofree norecurse nosync nounwind willreturn memory(none) uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { mustprogress nofree norecurse nosync nounwind willreturn memory(read, argmem: none, inaccessiblemem: none) uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { mustprogress nofree norecurse nosync nounwind willreturn memory(read, argmem: readwrite, inaccessiblemem: none) uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #3 = { nofree norecurse nosync nounwind memory(read, argmem: none, inaccessiblemem: none) uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.module.flags = !{!0, !1, !2, !3}
!llvm.ident = !{!4}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 8, !"PIC Level", i32 2}
!2 = !{i32 7, !"PIE Level", i32 2}
!3 = !{i32 7, !"uwtable", i32 2}
!4 = !{!"Ubuntu clang version 18.1.3 (1ubuntu1)"}
!5 = !{!6, !6, i64 0}
!6 = !{!"omnipotent char", !7, i64 0}
!7 = !{!"Simple C/C++ TBAA"}
!8 = !{!9, !10, i64 0}
!9 = !{!"", !10, i64 0, !10, i64 8, !11, i64 16}
!10 = !{!"long", !6, i64 0}
!11 = !{!"int", !6, i64 0}
!12 = !{!9, !10, i64 8}
!13 = distinct !{!13, !14, !15}
!14 = !{!"llvm.loop.mustprogress"}
!15 = !{!"llvm.loop.unroll.disable"}
!16 = distinct !{!16, !14, !15}
