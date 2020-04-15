// Guest OS

use std::env;

#[allow(dead_code)]
fn args() {
    let argv: Vec<String> = env::args().collect();
    let argc: usize = env::args().count();
    assert!(argc > 1);
    let mut n = 0;
    for i in argv {
        println!("argv[{}] = {}", n, i);
        n += 1;
    }
}

fn main() {
    // args()
}
