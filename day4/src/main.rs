use std::{collections::HashSet, fs::read_to_string};

fn main() {
    println!("Hello, world!");
    println!("SILVER: The example solution is : {}", day1("example.txt"));
    println!("SILVER: The solution is : {}", day1("input.txt"));
    println!("GOLD: The example solution is : {}", day2("example.txt"));
    println!("GOLD: The solution is : {}", day2("input.txt"));
}

type Round = (HashSet<u32>, HashSet<u32>);

fn read(loc: &str) -> Vec<Round> {
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
    read(loc)
        .iter()
        .map(|(win, have)| {
            let count = win.intersection(have).count() as u32;
            if 1 <= count {
                usize::pow(2, count - 1)
            } else {
                0
            }
        })
        .sum()
}

fn day2(loc: &str) -> usize {
    let rounds = read(loc);
    let mut cards = vec![1; rounds.len()];

    for (k, round) in rounds.into_iter().enumerate() {
        let (win, have) = round;
        let victories = win.intersection(&have).count();
        for i in 1..=victories {
            if cards.len() <= k + i {
                break;
            }
            cards[k + i] += cards[k];
        }
    }
    cards.into_iter().sum()
}
