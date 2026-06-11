// triskele-vm/build.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.2.0

use std::path::PathBuf;

fn main() {
    let manifest_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    let workspace_root = manifest_dir
        .parent().unwrap()
        .parent().unwrap();

    let lib_dir = workspace_root.join("lib");

    if lib_dir.exists() {
        println!("cargo:rustc-link-search=native={}", lib_dir.display());
        println!("cargo:rustc-link-lib=SDL2");

        let dll_src = lib_dir.join("SDL2.dll");
        if dll_src.exists() {
            let out_dir = PathBuf::from(std::env::var("OUT_DIR").unwrap());
            // OUT_DIR = target\debug\build\triskele-vm-{hash}\out
            // tskvm.exe is at target\debug\
            // 3 levels up: out → triskele-vm-{hash} → build → debug
            let exe_dir = out_dir
                .parent().unwrap()  // triskele-vm-{hash}
                .parent().unwrap()  // build
                .parent().unwrap(); // debug  ← tskvm.exe lives here

            println!("cargo:warning=exe_dir={}", exe_dir.display());

            let dll_dst = exe_dir.join("SDL2.dll");
            match std::fs::copy(&dll_src, &dll_dst) {
                Ok(_)  => println!("cargo:warning=SDL2.dll OK -> {}", dll_dst.display()),
                Err(e) => println!("cargo:warning=SDL2.dll FAILED: {}", e),
            }
        }
    }

    println!("cargo:rerun-if-changed=build.rs");
}
