fn main() {
    println!("Hello, world!");
    println!("SILVER: The example result is : {}", silver("example.txt"));
    println!("SILVER: The result is : {}", silver("input.txt"));
    println!("GOLD: The example result is : {}", gold("example.txt"));
    println!("GOLD: The result is : {}", gold("input.txt"));
}

fn read(loc: &str) -> Vec<String> {
    std::fs::read_to_string(loc)
        .unwrap()
        .lines()
        .map(|line| line.to_owned())
        .collect()
}

fn get_number(s: &str) -> Option<u64> {
    if s.is_empty() {
        return None;
    }
    if let Some(digit) = s.chars().next().unwrap().to_digit(10) {
        return Some(digit as u64);
    }
    let numbers = [
        ("one", 1),
        ("two", 2),
        ("three", 3),
        ("four", 4),
        ("five", 5),
        ("six", 6),
        ("seven", 7),
        ("eight", 8),
        ("nine", 9),
    ];
    for (rep, val) in numbers {
        if s.starts_with(rep) {
            return Some(val);
        }
    }
    None
}

fn get_digit_value(line: String) -> u64 {
    let left = line.find(|s: char| s.is_digit(10)).unwrap();
    let right = line.rfind(|s: char| s.is_digit(10)).unwrap();
    let left: u64 = line[left..=left].parse().unwrap();
    let right: u64 = line[right..=right].parse().unwrap();
    left * 10 + right
}

fn get_number_value(line: String) -> u64 {
    let mut it = (0..line.len()).filter_map(|k| get_number(&line[k..]));
    let first = it.next().unwrap();

    10 * first + it.last().unwrap_or(first)
}

fn silver(loc: &str) -> u64 {
    read(loc)
        .into_iter()
        .map(|line| get_digit_value(line))
        .sum()
}

fn gold(loc: &str) -> u64 {
    read(loc)
        .into_iter()
        .map(|line| get_number_value(line))
        .sum()
}
