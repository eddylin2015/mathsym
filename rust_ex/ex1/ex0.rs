//"" 
fn fact_recursive(n: u64) -> u64 
{ 
    match n { 
        0 => 1, 
        _ => n * fact_recursive(n-1) 
    } 
}

fn fact_iterative(n: u64) -> u64 {
    let mut i = 1u64;
    let mut result = 1u64;
    while i<=n {
        result *= i;
        i += 1;
    }
    return result;
}

fn fact_iterator_lamda(n: u64) -> u64 {
    (1..n+1).fold(1, |p, m| p*m)
}

/*
Ownership fn foo(v: T) { ...}
Shared Borrow fn foo(v: &T) { ...}
Mutable Borrow fn foo(v: &mut T) { ...}
*/

fn main () 
{ 
    for i in 1..10 
    { 
        println!("{}\t{}", i, fact_recursive(i)); 
    }
    for i in 1..10 {
        println!("{}\t{}",i, fact_iterative(i));
    }
    for i in 1..10 {
        println!("{}\t{}",i, fact_iterator_lamda(i));
    }  
}