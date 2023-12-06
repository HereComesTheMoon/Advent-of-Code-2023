use std::{collections::HashSet, fs::read_to_string, str::from_utf8};

fn main() {
    println!("Hello, world!");
    println!("SILVER: The example result is : {}", silver("test.txt"));
    println!("SILVER: The result is : {}", silver("input.txt"));
    println!("GOLD: The example result is : {}", gold("test.txt"));
    println!("GOLD: The result is : {}", gold("input.txt"));
}

const ADJ: [(isize, isize); 8] = [
    (1, 1),
    (1, 0),
    (1, -1),
    (-1, 1),
    (-1, 0),
    (-1, -1),
    (0, 1),
    (0, -1),
];

fn read(loc: &str) -> Vec<Vec<u8>> {
    read_to_string(loc)
        .unwrap()
        .lines()
        .map(|line| line.as_bytes().to_owned())
        .collect()
}

fn grab_number(s: &Vec<Vec<u8>>, y: isize, i: isize) -> Option<(usize, usize, usize)> {
    let Some(s) = s.get(y as usize) else {
        return None;
    };
    let mut i = i as usize;
    if s.get(i).is_none() || !s[i].is_ascii_digit() {
        return None;
    }
    let mut j = i;
    while 0 < i && s[i - 1].is_ascii_digit() {
        i -= 1;
    }
    while j < s.len() && s[j].is_ascii_digit() {
        j += 1;
    }
    Some((y as usize, i, j))
}

fn silver(loc: &str) -> usize {
    let data = read(loc);
    let mut res = 0;
    for y in 0..data.len() {
        for x in 0..data[y].len() {
            if data[y][x] == b'.' || data[y][x].is_ascii_digit() {
                continue;
            }
            res += ADJ
                .iter()
                .filter_map(|(yy, xx)| grab_number(&data, y as isize + yy, x as isize + xx))
                .collect::<HashSet<_>>()
                .drain()
                .map(|(y, i, j)| from_utf8(&data[y][i..j]).unwrap().parse::<usize>().unwrap())
                .sum::<usize>()
        }
    }
    res
}

fn gold(loc: &str) -> usize {
    let data = read(loc);
    let mut res = 0;
    for y in 0..data.len() {
        for x in 0..data[y].len() {
            if data[y][x] != b'*' {
                continue;
            }
            let mut nums = ADJ
                .iter()
                .filter_map(|(yy, xx)| grab_number(&data, y as isize + yy, x as isize + xx))
                .collect::<HashSet<_>>();
            if nums.len() != 2 {
                continue;
            }
            res += nums
                .drain()
                .map(|(y, i, j)| from_utf8(&data[y][i..j]).unwrap().parse::<usize>().unwrap())
                .product::<usize>()
        }
    }
    res
}
