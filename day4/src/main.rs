use std::{fs::read_to_string, collections::HashSet};

fn main() {
    println!("Hello, world!");
    println!("SILVER: The example solution is : {}", day1("example.txt"));
    println!("SILVER: The solution is : {}", day1("input.txt"));
    // println!("GOLD: The example solution is : {}", day2("test.txt"));
    // println!("GOLD: The solution is : {}", day2("input.txt"));
}

fn read(loc: &str) -> Vec<(HashSet<u32>, HashSet<u32>)> {
    read_to_string(loc)
        .unwrap()
        .lines()
        .map(|line| line.split_once(':').unwrap().1)
        .map(|line| line.split_once('|').unwrap())
        .map(|(l, r)| {
            (
                l.split_whitespace()
                    .map(|num| num.parse().unwrap())
                    .collect(),
                r.split_whitespace()
                    .map(|num| num.parse().unwrap())
                    .collect(),
            )
        })
        .collect()
}

fn day1(loc: &str) -> usize {
    let data = read(loc);
    let mut res = 0;
    for (win, have) in data.iter() {
        let count = win.intersection(have).count() as u32;
        if 1 <= count {
            res += usize::pow(2_usize, count - 1);
        }
    }
    res
}
