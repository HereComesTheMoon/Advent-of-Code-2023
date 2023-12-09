fn main() {
    println!("Hello, world!");
    println!("SILVER: The example result is : {}", silver("test.txt"));
    println!("SILVER: The result is : {}", silver("input.txt"));
    // println!("GOLD: The example result is : {}", gold("test.txt"));
    // println!("GOLD: The example result is : {}", gold("input.txt"));
}

// 10:20

fn read(loc: &str) -> Vec<Vec<i64>> {
    std::fs::read_to_string(loc)
        .unwrap()
        .lines()
        .map(|line| line
            .split_whitespace()
            .map(|num| num.parse().unwrap())
            .collect()
        ).collect()
}

fn generate_diffs(seq: Vec<i64>) -> Vec<Vec<i64>> {
    let mut res = vec![seq.clone()];
    while res.last().unwrap().iter().any(|&x| x != 0) {
        let last = res.last().unwrap();
        let mut diff = vec![];
        for k in 1..last.len() {
            diff.push(last[k] - last[k-1]);
        }
        res.push(diff);
    }
    res
}

fn extrapolate(diffs: &mut Vec<Vec<i64>>) -> i64 {
    diffs.last_mut().unwrap().push(0);
    for k in (0..diffs.len()-1).rev() {
        let val = diffs[k].last().unwrap() + diffs[k+1].last().unwrap();
        diffs[k].push(val);
    }

    *diffs.first().unwrap().last().unwrap()
}

fn silver(loc: &str) -> i64 {
    read(loc)
        .into_iter()
        .map(|seq| generate_diffs(seq))
        .map(|mut diffs| extrapolate(&mut diffs))
        .sum()
}
