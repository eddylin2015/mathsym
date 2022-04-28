fn main() {
    println!("Hello, world!");
    let x = 5;
    let x = x + 1;
    let x = x * 2;
    let x= 3_14159;
    println!("The value of x is: {}", x);
    let guess:u32 = "42".parse().expect("Not a number!");
}
fn plus_one(x: i32) -> i32 {
    x + 1
   }

/*
Ownership Rules
First, let’s take a look at the ownership rules. Keep these rules in mind as we
work through the examples that illustrate them:
•	 Each value in Rust has a variable that’s called its owner.
•	 There can be only one owner at a time.
•	 When the owner goes out of scope, the value will be dropped.
*/