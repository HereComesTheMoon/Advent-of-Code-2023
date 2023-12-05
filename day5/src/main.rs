fn main() {
    println!("Hello, world!");
    println!("SILVER: The example result is : {}", silver("example.txt"));
    println!("SILVER: The result is : {}", silver("input.txt"));
    println!("GOLD: The example result is : {}", gold("example.txt"));
    println!("GOLD: The result is : {}", gold("input.txt"));
}

#[derive(Debug)]
struct Map(Vec<(u64, u64)>);

fn read_seeds(loc: &str) -> Vec<u64> {
    std::fs::read_to_string(loc)
        .unwrap()
        .lines()
        .next()
        .unwrap()[7..]
        .split_whitespace()
        .map(|seed| seed.parse().unwrap())
        .collect()
}

fn read_maps(loc: &str) -> Vec<Map> {
    std::fs::read_to_string(loc)
        .unwrap()
        .split("\n\n")
        .skip(1)
        .map(|chunk| parse_map(chunk))
        .collect()
}

fn parse_map(chunk: &str) -> Map {
    let mut map = vec![(0, 0)];

    let mut ranges: Vec<_> = chunk
        .lines()
        .skip(1)
        .map(|line| {
            line.split_whitespace()
                .map(|num| num.parse::<u64>().unwrap())
                .collect::<Vec<_>>()
        })
        .map(|v| TryInto::<[_; 3]>::try_into(v).unwrap())
        .map(|[dest, source, len]| (source, dest, len))
        .collect();

    ranges.sort_unstable();

    for (k, &(source, dest, len)) in ranges.iter().enumerate() {
        let next_source = ranges.get(k + 1).map(|x| x.0).unwrap_or(u64::MAX);
        map.push((source, dest));
        assert!(source + len <= next_source);
        if source + len < next_source {
            map.push((source + len, source + len));
        }
    }

    assert_eq!(map.last().unwrap().0, map.last().unwrap().1);
    Map(map)
}

impl Map {
    fn map(&self, inp: u64) -> u64 {
        let index = match self.0.binary_search(&(inp, u64::MAX)) {
            Ok(index) => index,
            Err(index) => index - 1,
        };
        let diff = inp - self.0[index].0;
        self.0[index].1 + diff
    }
}

fn silver(loc: &str) -> u64 {
    let seeds = read_seeds(loc);
    let maps = read_maps(loc);

    let mut min = u64::MAX;

    for &(mut seed) in seeds.iter() {
        for map in maps.iter() {
            seed = map.map(seed);
        }
        min = min.min(seed);
    }

    min
}

fn gold(loc: &str) -> u64 {
    let seeds = read_seeds(loc);
    let maps = read_maps(loc);

    let mut min = u64::MAX;

    for chunk in seeds.chunks_exact(2) {
        let start = chunk[0];
        let len = chunk[1];
        for mut seed in start..start + len {
            for map in maps.iter() {
                seed = map.map(seed);
            }
            min = min.min(seed);
        }
    }

    min
}
