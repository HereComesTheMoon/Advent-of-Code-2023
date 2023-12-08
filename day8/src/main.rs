use std::collections::HashMap;

fn main() {
    println!("Hello, world!");
    println!("SILVER: The example result is : {}", silver("test1.txt"));
    println!("SILVER: The example result is : {}", silver("test2.txt"));
    println!("SILVER: The result is : {}", silver("input.txt"));
    println!("GOLD: The example result is : {}", gold("test3.txt"));
    println!("GOLD: The example result is : {}", gold("test4.txt"));
    println!("GOLD: The result is : {}", gold("input.txt"));
}

struct Map {
    g: HashMap<String, (String, String)>,
    path: Vec<bool>,
}

impl Map {
    fn walk(&self) -> usize {
        let mut pos = "AAA";

        for steps in 0.. {
            if pos == "ZZZ" {
                return steps;
            }
            pos = if self.path[steps % self.path.len()] {
                &self.g.get(pos).unwrap().0
            } else {
                &self.g.get(pos).unwrap().1
            }
        }

        unreachable!()
    }

    fn ghost<'a>(&'a self, mut pos: &'a str) -> usize {
        for steps in 0.. {
            if pos.ends_with("Z") {
                return steps;
            }
            pos = if self.path[steps % self.path.len()] {
                &self.g.get(pos).unwrap().0
            } else {
                &self.g.get(pos).unwrap().1
            }
        }

        unreachable!()
    }
    
}

fn read(loc: &str) -> Map {
    let data = std::fs::read_to_string(loc).unwrap();
    let mut it = data.lines();
    let path = it.next().unwrap().chars().map(|c| match c {
        'L' => true,
        'R' => false,
        _ => panic!("Oh no!"),
    }).collect();

    it.next();

    let g = HashMap::from_iter(it.map(|line| (line[..3].into(), (line[7..10].into(), line[12..15].into()))));

    Map {
        g,
        path,
    }
}

fn gcd(a: usize, b: usize) -> usize {
    if a == 0 { return b; }
    if b == 0 { return a; }
    match (a % 2, b % 2) {
        (0, 0) => 2 * gcd(a / 2, b / 2),
        (1, 0) => gcd(a, b / 2),
        (0, 1) => gcd(a / 2, b),
        (1, 1) => gcd(if a < b { b - a } else { a - b }, usize::min(a, b)),
        _ => unreachable!(),
    }
}

fn silver(loc: &str) -> usize {
    let map = read(loc);
    map.walk()
}

fn gold(loc: &str) -> usize {
    let map = read(loc);
    let positions = map.g.keys().filter(|s| s.ends_with("A")).collect::<Vec<_>>();
    let divisors = positions.iter().map(|pos| map.ghost(pos)).collect::<Vec<_>>();

    let lcd = divisors.iter().fold(divisors[0], |acc, x| (acc * x) / gcd(acc, *x));
    // let gcd = divisors.iter().fold(divisors[0], |acc, x| gcd(acc, *x));
    // println!("{divisors:?}");
    // println!("{gcd:?}");
    // println!("{lcd:?}");
    lcd
}
