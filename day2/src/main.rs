fn main() {
    println!("Hello, world!");
    let given = Cubes {
        r: 12,
        g: 13,
        b: 14,
    };
    println!(
        "SILVER: The example result is : {}",
        silver("test1.txt", given)
    );
    println!("SILVER: The result is : {}", silver("input.txt", given));
    println!("GOLD: The example result is : {}", gold("test1.txt", given));
    println!("GOLD: The result is : {}", gold("input.txt", given));
}

#[derive(Clone, Copy)]
struct Cubes {
    r: u64,
    g: u64,
    b: u64,
}

impl Cubes {
    fn max(self, other: Cubes) -> Cubes {
        Cubes {
            r: self.r.max(other.r),
            g: self.g.max(other.g),
            b: self.b.max(other.b),
        }
    }
}

impl From<&str> for Cubes {
    fn from(s: &str) -> Self {
        let mut cube = Cubes { r: 0, b: 0, g: 0 };
        let cubes = s
            .split(',')
            .map(|cube| cube.trim().split_once(' ').unwrap())
            .map(|(count, color)| (count.parse().unwrap(), color));
        for (count, color) in cubes {
            match color {
                "red" => cube.r = count,
                "blue" => cube.b = count,
                "green" => cube.g = count,
                _ => {}
            }
        }
        cube
    }
}

struct Game {
    id: u64,
    rounds: Vec<Cubes>,
}

impl Game {
    fn get_cubes_needed_to_play(&self) -> Cubes {
        self.rounds
            .iter()
            .fold(Cubes { r: 0, b: 0, g: 0 }, |acc, &now| acc.max(now))
    }
}

fn read(loc: &str) -> Vec<Game> {
    std::fs::read_to_string(loc)
        .unwrap()
        .lines()
        .map(|line| {
            line.split_once("Game ")
                .unwrap()
                .1
                .split_once(": ")
                .unwrap()
        })
        .map(|(id, games)| Game {
            id: id.parse().unwrap(),
            rounds: games.split(';').map(|cubes| cubes.into()).collect(),
        })
        .collect()
}

fn silver(loc: &str, given: Cubes) -> u64 {
    let Cubes { r, b, g } = given;
    read(loc)
        .into_iter()
        .map(|game| (game.id, game.get_cubes_needed_to_play()))
        .filter(|(_, c)| c.r <= r && c.b <= b && c.g <= g)
        .map(|(id, _)| id)
        .sum()
}

fn gold(loc: &str, given: Cubes) -> u64 {
    let Cubes { r, b, g } = given;
    read(loc)
        .into_iter()
        .map(|game| game.get_cubes_needed_to_play())
        .map(|c| c.r * c.g * c.b)
        .sum()
}
