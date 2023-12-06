fn main() {
    println!("Hello, world!");
    println!("SILVER: The example result is : {}", silver("example.txt"));
    println!("SILVER: The result is : {}", silver("input.txt"));
    println!("GOLD: The example result is : {}", gold("example.txt"));
    println!("GOLD: The result is : {}", gold("input.txt"));
}

fn read_silver(loc: &str) -> Vec<(u64, u64)> {
    let input = std::fs::read_to_string(loc).unwrap();
    let mut iter = input.lines().map(|line| {
        line.split_whitespace()
            .skip(1)
            .map(|num| num.parse::<u64>().unwrap())
    });
    let time = iter.next().unwrap();
    let dist = iter.next().unwrap();

    time.zip(dist).collect()
}

fn read_gold(loc: &str) -> (u64, u64) {
    let input = std::fs::read_to_string(loc).unwrap();
    let mut iter = input.lines().map(|line| {
        line.split_whitespace()
            .skip(1)
            .collect::<String>()
            .parse()
            .unwrap()
    });
    let time = iter.next().unwrap();
    let dist = iter.next().unwrap();

    (time, dist)
}

// dist(t) = 0 if t <= 0
// dist(t) = 0 if length <= t
// dist(t) == (length - t) * t
// dist(t) == max(length - t, 0) * max(t, 0)

// goal <= (length - t) * t
// 0 == t*length - t*t - goal
// t*t - t*length + goal == 0

// solutions = (length +- sqrt(length**2 - 4*goal)) / 2

fn solve_eq(length_of_race: u64, goal_dist: u64) -> (f64, f64) {
    let dist = ((length_of_race.pow(2) - 4 * goal_dist) as f64).sqrt();
    let x0 = (length_of_race as f64 - dist) / 2.;
    let mut x1 = (length_of_race as f64 + dist) / 2.;

    if x1.fract() == 0. {
        x1 -= 1.;
    }

    (x0, x1)
}

fn silver(loc: &str) -> u64 {
    read_silver(loc)
        .into_iter()
        .map(|(t, d)| solve_eq(t, d))
        .map(|(x0, x1)| (x1.ceil() - x0.ceil()) as u64)
        .product()
}

fn gold(loc: &str) -> u64 {
    let (time, dist) = read_gold(loc);
    let (x0, x1) = solve_eq(time, dist);
    (x1.ceil() - x0.ceil()) as u64
}
